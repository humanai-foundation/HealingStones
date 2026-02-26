import numpy as np
import open3d as o3d
from scipy.spatial.transform import Rotation
from scipy.optimize import minimize
import copy

class FragmentAligner:
    """
    Align and register fragments based on matched break surfaces
    """
    
    def __init__(self, icp_threshold=0.02):
        self.aligned_fragments = {}
        self.transformation_history = {}
        self.icp_threshold = icp_threshold
    
    def compute_surface_alignment(self, surface1_points, surface2_points, 
                                surface1_normal, surface2_normal):
        """
        Compute transformation to align two surfaces
        
        Args:
            surface1_points, surface2_points: Point arrays for the surfaces
            surface1_normal, surface2_normal: Normal vectors of the surfaces
        
        Returns:
            4x4 transformation matrix
        """
        # Step 1: Align centroids
        centroid1 = np.mean(surface1_points, axis=0)
        centroid2 = np.mean(surface2_points, axis=0)
        translation = centroid1 - centroid2
        
        # Step 2: Align normals (surface2 normal should be opposite to surface1)
        normal1 = np.array(surface1_normal) / np.linalg.norm(surface1_normal)
        normal2 = np.array(surface2_normal) / np.linalg.norm(surface2_normal)
        
        # We want normal2 to point in the opposite direction of normal1
        target_normal = -normal1
        
        # Compute rotation to align normal2 with target_normal
        if np.allclose(normal2, target_normal):
            rotation_matrix = np.eye(3)
        elif np.allclose(normal2, -target_normal):
            # 180-degree rotation around any perpendicular axis
            perpendicular = np.array([1, 0, 0])
            if np.abs(np.dot(normal2, perpendicular)) > 0.9:
                perpendicular = np.array([0, 1, 0])
            rotation_matrix = Rotation.from_rotvec(np.pi * perpendicular).as_matrix()
        else:
            # General case: rotation from normal2 to target_normal
            cross_product = np.cross(normal2, target_normal)
            dot_product = np.dot(normal2, target_normal)
            
            # Rodrigues' rotation formula
            skew_matrix = np.array([
                [0, -cross_product[2], cross_product[1]],
                [cross_product[2], 0, -cross_product[0]],
                [-cross_product[1], cross_product[0], 0]
            ])
            
            rotation_matrix = (np.eye(3) + skew_matrix + 
                             skew_matrix @ skew_matrix * (1 / (1 + dot_product)))
        
        # Create 4x4 transformation matrix
        transform = np.eye(4)
        transform[:3, :3] = rotation_matrix
        transform[:3, 3] = translation
        
        return transform
    
    def refine_alignment_icp(self, mesh1, mesh2, initial_transform, 
                           max_iterations=100, tolerance=1e-6):
        """
        Refine alignment using Iterative Closest Point (ICP)
        
        Args:
            mesh1, mesh2: Open3D meshes
            initial_transform: Initial 4x4 transformation matrix
            max_iterations: Maximum ICP iterations
            tolerance: Convergence tolerance
        
        Returns:
            Refined transformation matrix
        """
        # Convert meshes to point clouds
        pcd1 = mesh1.sample_points_uniformly(number_of_points=5000)
        pcd2 = mesh2.sample_points_uniformly(number_of_points=5000)
        
        # Apply initial transformation to pcd2
        pcd2_transformed = copy.deepcopy(pcd2)
        pcd2_transformed.transform(initial_transform)
        
        # Estimate normals
        pcd1.estimate_normals()
        pcd2_transformed.estimate_normals()
        
        # Run ICP
        threshold = self.icp_threshold  # Distance threshold (configurable)
        reg_p2p = o3d.pipelines.registration.registration_icp(
            pcd2_transformed, pcd1, threshold, np.eye(4),
            o3d.pipelines.registration.TransformationEstimationPointToPoint(),
            o3d.pipelines.registration.ICPConvergenceCriteria(
                max_iteration=max_iterations, relative_fitness=tolerance
            )
        )
        
        # Combine transformations
        final_transform = reg_p2p.transformation @ initial_transform
        return final_transform, reg_p2p.fitness
    
    def align_fragments_by_match(self, fragment1, fragment2, match_info):
        """
        Align fragment2 to fragment1 based on a surface match
        
        Args:
            fragment1, fragment2: Fragment data
            match_info: Match information from SurfaceMatcher
        
        Returns:
            Transformation matrix and alignment quality metrics
        """
        color = match_info['color']
        idx1 = match_info['fragment1_idx']
        idx2 = match_info['fragment2_idx']
        
        # Get surface data
        surface1 = fragment1['break_surfaces'][color][idx1]
        surface2 = fragment2['break_surfaces'][color][idx2]
        
        points1 = surface1['points']
        points2 = surface2['points']
        normal1 = match_info['surface1_features']['normal']
        normal2 = match_info['surface2_features']['normal']
        
        # Compute initial alignment
        initial_transform = self.compute_surface_alignment(
            points1, points2, normal1, normal2
        )
        
        # Refine with ICP if meshes are available
        if 'mesh' in fragment1 and 'mesh' in fragment2:
            final_transform, fitness = self.refine_alignment_icp(
                fragment1['mesh'], fragment2['mesh'], initial_transform
            )
        else:
            final_transform = initial_transform
            fitness = match_info['similarity']
        
        # Compute alignment metrics
        # Transform surface2 points and compute distance to surface1
        surface2_transformed = self.transform_points(points2, final_transform)
        distances = self.compute_point_to_surface_distances(
            surface2_transformed, points1
        )
        
        alignment_metrics = {
            'mean_distance': np.mean(distances),
            'std_distance': np.std(distances),
            'max_distance': np.max(distances),
            'icp_fitness': fitness,
            'original_similarity': match_info['similarity']
        }
        
        return final_transform, alignment_metrics
    
    def transform_points(self, points, transform_matrix):
        """Apply 4x4 transformation matrix to points"""
        homogeneous_points = np.hstack([points, np.ones((len(points), 1))])
        transformed_homogeneous = homogeneous_points @ transform_matrix.T
        return transformed_homogeneous[:, :3]
    
    def compute_point_to_surface_distances(self, points, surface_points):
        """Compute minimum distances from points to surface"""
        distances = []
        for point in points:
            dists_to_surface = np.linalg.norm(surface_points - point, axis=1)
            distances.append(np.min(dists_to_surface))
        return np.array(distances)
    
    def evaluate_alignment_quality(self, fragment1, fragment2, transform, matches):
        """
        Evaluate the quality of fragment alignment across all matched surfaces
        
        Args:
            fragment1, fragment2: Fragment data
            transform: Transformation matrix
            matches: List of surface matches
        
        Returns:
            Overall alignment quality metrics
        """
        total_distance_errors = []
        total_overlap_scores = []
        
        for match in matches:
            color = match['color']
            idx1 = match['fragment1_idx']
            idx2 = match['fragment2_idx']
            
            # Get surface points
            points1 = fragment1['break_surfaces'][color][idx1]['points']
            points2 = fragment2['break_surfaces'][color][idx2]['points']
            
            # Transform fragment2 surface
            points2_transformed = self.transform_points(points2, transform)
            
            # Compute distance errors
            distances = self.compute_point_to_surface_distances(
                points2_transformed, points1
            )
            total_distance_errors.extend(distances)
            
            # Compute overlap score (percentage of points within threshold)
            overlap_threshold = 0.01  # 1cm
            overlap_score = np.sum(distances < overlap_threshold) / len(distances)
            total_overlap_scores.append(overlap_score)
        
        quality_metrics = {
            'mean_distance_error': np.mean(total_distance_errors),
            'std_distance_error': np.std(total_distance_errors),
            'max_distance_error': np.max(total_distance_errors),
            'mean_overlap_score': np.mean(total_overlap_scores),
            'total_matched_surfaces': len(matches)
        }
        
        return quality_metrics
    
    def optimize_multi_surface_alignment(self, fragment1, fragment2, matches, 
                                       initial_transform=None):
        """
        Optimize alignment considering multiple surface matches simultaneously
        
        Args:
            fragment1, fragment2: Fragment data
            matches: List of surface matches
            initial_transform: Initial transformation guess
        
        Returns:
            Optimized transformation matrix and quality metrics
        """
        if not matches:
            return np.eye(4), {}
        
        # Use best match for initial alignment if not provided
        if initial_transform is None:
            best_match = max(matches, key=lambda x: x['similarity'])
            initial_transform, _ = self.align_fragments_by_match(
                fragment1, fragment2, best_match
            )
        
        # Define optimization objective
        def alignment_objective(transform_params):
            """Objective function for optimization"""
            # Convert parameters to transformation matrix
            translation = transform_params[:3]
            rotation_angles = transform_params[3:6]
            
            rotation_matrix = Rotation.from_euler('xyz', rotation_angles).as_matrix()
            transform = np.eye(4)
            transform[:3, :3] = rotation_matrix
            transform[:3, 3] = translation
            
            # Compute total alignment error across all matches
            total_error = 0
            for match in matches:
                color = match['color']
                idx1 = match['fragment1_idx']
                idx2 = match['fragment2_idx']
                
                points1 = fragment1['break_surfaces'][color][idx1]['points']
                points2 = fragment2['break_surfaces'][color][idx2]['points']
                
                points2_transformed = self.transform_points(points2, transform)
                distances = self.compute_point_to_surface_distances(
                    points2_transformed, points1
                )
                
                # Weighted by match similarity
                weight = match['similarity']
                total_error += weight * np.mean(distances**2)
            
            return total_error
        
        # Extract initial parameters
        initial_translation = initial_transform[:3, 3]
        initial_rotation = Rotation.from_matrix(initial_transform[:3, :3]).as_euler('xyz')
        initial_params = np.concatenate([initial_translation, initial_rotation])
        
        # Optimize
        result = minimize(
            alignment_objective, 
            initial_params, 
            method='BFGS',
            options={'maxiter': 100, 'disp': False}
        )
        
        # Convert optimized parameters back to transformation matrix
        opt_translation = result.x[:3]
        opt_rotation_angles = result.x[3:6]
        opt_rotation_matrix = Rotation.from_euler('xyz', opt_rotation_angles).as_matrix()
        
        optimized_transform = np.eye(4)
        optimized_transform[:3, :3] = opt_rotation_matrix
        optimized_transform[:3, 3] = opt_translation
        
        # Evaluate final quality
        quality_metrics = self.evaluate_alignment_quality(
            fragment1, fragment2, optimized_transform, matches
        )
        quality_metrics['optimization_success'] = result.success
        quality_metrics['optimization_error'] = result.fun
        
        return optimized_transform, quality_metrics
    
    def create_aligned_visualization(self, fragments, transformations):
        """
        Create visualization of aligned fragments
        
        Args:
            fragments: List of fragment data
            transformations: Dict of transformation matrices for each fragment
        
        Returns:
            Open3D visualization
        """
        vis = o3d.visualization.Visualizer()
        vis.create_window(window_name="Aligned Fragments")
        
        colors = [[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 0], [1, 0, 1], [0, 1, 1]]
        
        for i, fragment in enumerate(fragments):
            if 'mesh' in fragment:
                mesh = copy.deepcopy(fragment['mesh'])
                
                # Apply transformation if available
                if i in transformations:
                    mesh.transform(transformations[i])
                
                # Color the fragment
                color = colors[i % len(colors)]
                mesh.paint_uniform_color(color)
                
                vis.add_geometry(mesh)
        
        vis.run()
        vis.destroy_window()

# Example usage
if __name__ == "__main__":
    # Assuming you have fragments and matches from previous scripts
    aligner = FragmentAligner()
    
    # Example: Align two fragments based on their best match
    if all_matches:
        # Get first fragment pair with matches
        pair_key = list(all_matches.keys())[0]
        color_matches = all_matches[pair_key]
        
        if color_matches:
            # Get first color with matches
            color = list(color_matches.keys())[0]
            matches = color_matches[color]
            
            if matches:
                # Align fragments
                fragment_indices = [int(x) for x in pair_key.split('_')[1::2]]
                fragment1 = enhanced_fragments[fragment_indices[0]]
                fragment2 = enhanced_fragments[fragment_indices[1]]
                
                transform, metrics = aligner.optimize_multi_surface_alignment(
                    fragment1, fragment2, matches
                )
                
                print(f"Alignment completed:")
                print(f"Mean distance error: {metrics['mean_distance_error']:.4f}")
                print(f"Mean overlap score: {metrics['mean_overlap_score']:.4f}")
                
                # Visualize alignment
                transformations = {0: np.eye(4), 1: transform}
                aligner.create_aligned_visualization(
                    [fragment1, fragment2], transformations
                )
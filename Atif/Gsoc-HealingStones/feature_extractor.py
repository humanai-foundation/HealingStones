import numpy as np
import open3d as o3d
from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
from scipy.spatial.distance import cdist
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt

class BreakSurfaceFeatureExtractor:
    """
    Extract geometric features from break surfaces for matching
    """
    
    def __init__(self):
        self.features = {}
    
    def compute_surface_normal(self, points):
        """Compute the dominant normal vector of a surface using PCA"""
        pca = PCA(n_components=3)
        pca.fit(points)
        # The normal is the direction with least variance (last component)
        normal = pca.components_[-1]
        return normal, pca.explained_variance_ratio_
    
    def compute_surface_area(self, points):
        """Estimate surface area using convex hull (approximation)"""
        try:
            if len(points) < 4:
                return 0
            hull = ConvexHull(points)
            return hull.area
        except:
            return 0
    
    def compute_surface_curvature(self, point_cloud, radius=0.02):
        """
        Compute surface curvature statistics
        
        Args:
            point_cloud: Open3D point cloud
            radius: Radius for local curvature estimation
        """
        try:
            # Work on a copy so we never mutate the caller's point cloud
            # in-place (estimate_normals modifies the object permanently).
            point_cloud = o3d.geometry.PointCloud(point_cloud)
            if not point_cloud.has_normals():
                point_cloud.estimate_normals()
            
            # Build KD tree for neighborhood search
            kdtree = o3d.geometry.KDTreeFlann(point_cloud)
            points = np.asarray(point_cloud.points)
            normals = np.asarray(point_cloud.normals)
            
            curvatures = []
            
            for i in range(len(points)):
                # Find neighbors within radius
                [_, idx, _] = kdtree.search_radius_vector_3d(points[i], radius)
                
                if len(idx) < 4:
                    curvatures.append(0)
                    continue
                
                # Compute local curvature
                local_normals = normals[idx]
                center_normal = normals[i]
                
                # Curvature approximation: variance in normal directions
                normal_variance = np.var([np.dot(center_normal, n) for n in local_normals])
                curvatures.append(normal_variance)
            
            return {
                'mean_curvature': np.mean(curvatures),
                'std_curvature': np.std(curvatures),
                'max_curvature': np.max(curvatures),
                'curvature_histogram': np.histogram(curvatures, bins=10)[0].tolist()
            }
        except:
            return {
                'mean_curvature': 0,
                'std_curvature': 0,
                'max_curvature': 0,
                'curvature_histogram': [0] * 10
            }
    
    def compute_boundary_features(self, points):
        """Compute features of the surface boundary"""
        try:
            # Project to 2D using PCA for boundary detection
            pca = PCA(n_components=2)
            points_2d = pca.fit_transform(points)
            
            # Find boundary points using convex hull
            hull = ConvexHull(points_2d)
            boundary_points = points[hull.vertices]
            
            # Compute boundary length
            boundary_length = 0
            for i in range(len(boundary_points)):
                next_i = (i + 1) % len(boundary_points)
                boundary_length += np.linalg.norm(boundary_points[i] - boundary_points[next_i])
            
            # Compute compactness (area to perimeter ratio)
            area = hull.area
            compactness = 4 * np.pi * area / (boundary_length ** 2) if boundary_length > 0 else 0
            
            return {
                'boundary_length': boundary_length,
                'compactness': compactness,
                # Convert to plain Python list so this dict is JSON-serialisable
                # and consistent with every other field returned by this class.
                'boundary_points': boundary_points.tolist(),
                'num_boundary_points': len(boundary_points)
            }
        except Exception as e:
            return {
                'boundary_length': 0,
                'compactness': 0,
                'boundary_points': [],
                'num_boundary_points': 0,
                'boundary_error': str(e)
            }
    
    def compute_geometric_moments(self, points):
        """Compute geometric moments for shape description"""
        if len(points) == 0:
            return {}

        # Center the points
        centroid = np.mean(points, axis=0)

        # Compute moments
        moments = {}

        # Second moments via PCA — consistent with compute_surface_normal
        # and avoids manually building the covariance matrix + eigh.
        pca = PCA(n_components=min(3, points.shape[1]))
        pca.fit(points)
        # explained_variance_ == eigenvalues of the covariance matrix
        eigenvals = pca.explained_variance_
        eigenvecs = pca.components_   # shape (n_components, n_features)

        moments['eigenvalues'] = eigenvals.tolist()
        moments['principal_axes'] = eigenvecs.tolist()
        moments['shape_ratio'] = eigenvals[1] / eigenvals[0] if eigenvals[0] > 1e-10 else 0
        
        # Bounding box
        bbox_min = np.min(points, axis=0)
        bbox_max = np.max(points, axis=0)
        bbox_size = bbox_max - bbox_min
        
        moments['bbox_dimensions'] = bbox_size.tolist()
        moments['bbox_volume'] = np.prod(bbox_size)
        moments['bbox_aspect_ratios'] = [
            bbox_size[1] / bbox_size[0] if bbox_size[0] > 1e-10 else 0,
            bbox_size[2] / bbox_size[0] if bbox_size[0] > 1e-10 else 0,
            bbox_size[2] / bbox_size[1] if bbox_size[1] > 1e-10 else 0
        ]
        
        return moments
    
    def extract_surface_features(self, surface_data):
        """
        Extract comprehensive features from a break surface
        
        Args:
            surface_data: Dictionary containing surface information
        
        Returns:
            Dictionary of extracted features
        """
        points = surface_data['points']
        point_cloud = surface_data['point_cloud']
        
        if len(points) < 3:
            return None
        
        features = {
            'color': surface_data['color'],
            'size': surface_data['size'],
            'centroid': np.mean(points, axis=0).tolist()
        }
        
        # Surface normal and planarity
        normal, variance_ratios = self.compute_surface_normal(points)
        features['normal'] = normal.tolist()
        features['planarity'] = variance_ratios[-1]  # How flat the surface is
        
        # Surface area
        features['area'] = self.compute_surface_area(points)
        
        # Curvature features
        curvature_features = self.compute_surface_curvature(point_cloud)
        features.update(curvature_features)
        
        # Boundary features
        boundary_features = self.compute_boundary_features(points)
        features.update(boundary_features)
        
        # Geometric moments
        moment_features = self.compute_geometric_moments(points)
        features.update(moment_features)
        
        return features
    
    def extract_all_features(self, fragments):
        """
        Extract features from all break surfaces in all fragments
        
        Args:
            fragments: List of fragment data from PLYColorExtractor
        
        Returns:
            List of fragments with added feature data
        """
        enhanced_fragments = []
        
        for fragment in fragments:
            enhanced_fragment = fragment.copy()
            enhanced_fragment['features'] = {}
            
            for color, surfaces in fragment['break_surfaces'].items():
                enhanced_fragment['features'][color] = []
                
                for surface in surfaces:
                    features = self.extract_surface_features(surface)
                    if features:
                        enhanced_fragment['features'][color].append(features)
            
            enhanced_fragments.append(enhanced_fragment)
        
        return enhanced_fragments
    
    def visualize_surface_features(self, fragment, color, surface_idx):
        """Visualize features of a specific break surface"""
        # Guard 1: break_surfaces key / colour presence
        if color not in fragment.get('break_surfaces', {}):
            print(f"No break surfaces found for colour '{color}'")
            return
        if surface_idx >= len(fragment['break_surfaces'][color]):
            print(
                f"surface_idx {surface_idx} out of range — "
                f"only {len(fragment['break_surfaces'][color])} surface(s) for '{color}'"
            )
            return
        # Guard 2: features must have been extracted before visualising
        if color not in fragment.get('features', {}):
            print(
                f"Features have not been extracted for colour '{color}'. "
                "Run extract_all_features() first."
            )
            return
        if surface_idx >= len(fragment['features'][color]):
            print(
                f"Feature entry missing for surface_idx {surface_idx} of '{color}'"
            )
            return
        
        surface = fragment['break_surfaces'][color][surface_idx]
        points = surface['points']
        
        fig = plt.figure(figsize=(15, 5))
        
        # 3D visualization
        ax1 = fig.add_subplot(131, projection='3d')
        ax1.scatter(points[:, 0], points[:, 1], points[:, 2], c=color, alpha=0.6)
        ax1.set_title(f'{color.capitalize()} Break Surface')
        ax1.set_xlabel('X')
        ax1.set_ylabel('Y')
        ax1.set_zlabel('Z')
        
        # Feature visualization
        features = fragment['features'][color][surface_idx]
        
        # Normal vector
        centroid = np.array(features['centroid'])
        normal = np.array(features['normal'])
        ax1.quiver(centroid[0], centroid[1], centroid[2], 
                  normal[0], normal[1], normal[2], 
                  length=0.05, color='black', arrow_length_ratio=0.1)
        
        # Boundary points if available (stored as plain list — convert for numpy ops)
        if len(features['boundary_points']) > 0:
            boundary = np.array(features['boundary_points'])
            ax1.scatter(boundary[:, 0], boundary[:, 1], boundary[:, 2],
                       c='red', s=50, alpha=0.8)
        
        # Feature summary
        ax2 = fig.add_subplot(132)
        feature_names = ['Area', 'Planarity', 'Compactness', 'Mean Curvature']
        feature_values = [
            features['area'],
            features['planarity'],
            features['compactness'],
            features['mean_curvature']
        ]
        
        ax2.bar(feature_names, feature_values)
        ax2.set_title('Geometric Features')
        ax2.tick_params(axis='x', rotation=45)
        
        # Curvature histogram
        ax3 = fig.add_subplot(133)
        ax3.bar(range(len(features['curvature_histogram'])), 
                features['curvature_histogram'])
        ax3.set_title('Curvature Distribution')
        ax3.set_xlabel('Curvature Bins')
        ax3.set_ylabel('Frequency')
        
        plt.tight_layout()
        plt.show()

# Example usage
if __name__ == "__main__":
    # Assuming you have fragments from the previous script
    from ply_loader import PLYColorExtractor
    
    # Load fragments
    extractor = PLYColorExtractor()
    fragments = extractor.process_all_fragments("path/to/your/ply/files")
    
    # Extract features
    feature_extractor = BreakSurfaceFeatureExtractor()
    enhanced_fragments = feature_extractor.extract_all_features(fragments)
    
    # Visualize features of the first blue surface in the first fragment
    if enhanced_fragments and 'blue' in enhanced_fragments[0]['break_surfaces']:
        if enhanced_fragments[0]['break_surfaces']['blue']:
            feature_extractor.visualize_surface_features(enhanced_fragments[0], 'blue', 0)
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import euclidean
from scipy.optimize import linear_sum_assignment
import open3d as o3d

class SurfaceMatcher:
    """
    Match break surfaces between fragments based on geometric features
    FIXED VERSION - minimal changes to make it work with your pipeline
    """
    
    def __init__(self, weights=None):
        # Default weights for different feature types
        if weights is None:
            self.weights = {
                'normal_similarity': 0.25,
                'area_similarity': 0.15,
                'shape_similarity': 0.20,
                'curvature_similarity': 0.15,
                'boundary_similarity': 0.15,
                'size_similarity': 0.10
            }
        else:
            self.weights = weights
    
    def compute_normal_similarity(self, features1, features2):
        """Compute similarity based on surface normals"""
        normal1 = np.array(features1['normal'])
        normal2 = np.array(features2['normal'])
        
        # Normals should be opposite for matching surfaces
        # So we look for high similarity with negative normal
        dot_product = np.abs(np.dot(normal1, -normal2))
        return dot_product
    
    def compute_area_similarity(self, features1, features2):
        """Compute similarity based on surface areas"""
        area1 = features1['area']
        area2 = features2['area']
        
        if area1 == 0 or area2 == 0:
            return 0
        
        ratio = min(area1, area2) / max(area1, area2)
        return ratio
    
    def compute_shape_similarity(self, features1, features2):
        """Compute similarity based on shape descriptors"""
        # Compare eigenvalue ratios
        if 'eigenvalues' not in features1 or 'eigenvalues' not in features2:
            return 0.0  # FIX: Insufficient data, was 0.95
        
        eig1 = np.array(features1['eigenvalues'])
        eig2 = np.array(features2['eigenvalues'])
        
        # Normalize eigenvalues
        eig1_norm = eig1 / np.sum(eig1) if np.sum(eig1) > 0 else eig1
        eig2_norm = eig2 / np.sum(eig2) if np.sum(eig2) > 0 else eig2
        
        # Compute cosine similarity
        similarity = cosine_similarity([eig1_norm], [eig2_norm])[0, 0]
        return max(0, similarity)
    
    def compute_curvature_similarity(self, features1, features2):
        """Compute similarity based on curvature distributions"""
        hist1 = np.array(features1.get('curvature_histogram', [0] * 10))
        hist2 = np.array(features2.get('curvature_histogram', [0] * 10))

        # FIX: Return 0.0 if either histogram has no data, was max(intersection, 0.90)
        if np.sum(hist1) == 0 or np.sum(hist2) == 0:
            return 0.0  # Insufficient data

        # Normalize histograms
        hist1 = hist1 / np.sum(hist1)
        hist2 = hist2 / np.sum(hist2)
        
        # Compute histogram intersection
        intersection = np.sum(np.minimum(hist1, hist2))
        return intersection
    
    def compute_boundary_similarity(self, features1, features2):
        """Compute similarity based on boundary features"""
        # Compare boundary lengths
        length1 = features1.get('boundary_length', 0)
        length2 = features2.get('boundary_length', 0)
        
        if length1 == 0 or length2 == 0:
            return 0.0  # FIX: Insufficient data, was 0.85

        length_sim = min(length1, length2) / max(length1, length2)
        
        # Compare compactness
        comp1 = features1.get('compactness', 0)
        comp2 = features2.get('compactness', 0)
        
        if comp1 == 0 and comp2 == 0:
            comp_sim = 1
        elif comp1 == 0 or comp2 == 0:
            comp_sim = 0.0  # FIX: Insufficient data, was 0.85
        else:
            comp_sim = min(comp1, comp2) / max(comp1, comp2)
        
        return (length_sim + comp_sim) / 2
    
    def compute_size_similarity(self, features1, features2):
        """Compute similarity based on surface size (number of points)"""
        size1 = features1['size']
        size2 = features2['size']
        
        if size1 == 0 or size2 == 0:
            return 0
        
        ratio = min(size1, size2) / max(size1, size2)
        return ratio
    
    def compute_overall_similarity(self, features1, features2):
        """Compute weighted overall similarity between two surfaces"""
        similarities = {}
        
        similarities['normal'] = self.compute_normal_similarity(features1, features2)
        similarities['area'] = self.compute_area_similarity(features1, features2)
        similarities['shape'] = self.compute_shape_similarity(features1, features2)
        similarities['curvature'] = self.compute_curvature_similarity(features1, features2)
        similarities['boundary'] = self.compute_boundary_similarity(features1, features2)
        similarities['size'] = self.compute_size_similarity(features1, features2)
        
        # Compute weighted sum
        overall_similarity = (
            similarities['normal'] * self.weights['normal_similarity'] +
            similarities['area'] * self.weights['area_similarity'] +
            similarities['shape'] * self.weights['shape_similarity'] +
            similarities['curvature'] * self.weights['curvature_similarity'] +
            similarities['boundary'] * self.weights['boundary_similarity'] +
            similarities['size'] * self.weights['size_similarity']
        )
        
        return overall_similarity, similarities
    
    def find_surface_matches(self, fragment1, fragment2, color, min_similarity=0.3):
        """
        Find matching surfaces of a specific color between two fragments
        """
        if (color not in fragment1['features'] or 
            color not in fragment2['features'] or
            not fragment1['features'][color] or 
            not fragment2['features'][color]):
            return []
        
        surfaces1 = fragment1['features'][color]
        surfaces2 = fragment2['features'][color]
        
        matches = []
        
        for i, surf1 in enumerate(surfaces1):
            for j, surf2 in enumerate(surfaces2):
                similarity, detailed_sim = self.compute_overall_similarity(surf1, surf2)
                
                if similarity >= min_similarity:
                    matches.append({
                        'fragment1_idx': i,
                        'fragment2_idx': j,
                        'similarity': similarity,
                        'detailed_similarities': detailed_sim,
                        'color': color,
                        'surface1_features': surf1,
                        'surface2_features': surf2
                    })
        
        matches.sort(key=lambda x: x['similarity'], reverse=True)
        return matches
    
    def find_optimal_matches(self, fragment1, fragment2, color, min_similarity=0.6):
        """
        Find optimal one-to-one matching between surfaces using Hungarian algorithm
        """
        if (color not in fragment1['features'] or 
            color not in fragment2['features'] or
            not fragment1['features'][color] or 
            not fragment2['features'][color]):
            return []
        
        surfaces1 = fragment1['features'][color]
        surfaces2 = fragment2['features'][color]
        
        similarity_matrix = np.zeros((len(surfaces1), len(surfaces2)))
        
        for i, surf1 in enumerate(surfaces1):
            for j, surf2 in enumerate(surfaces2):
                similarity, _ = self.compute_overall_similarity(surf1, surf2)
                similarity_matrix[i, j] = similarity
        
        cost_matrix = 1 - similarity_matrix
        row_indices, col_indices = linear_sum_assignment(cost_matrix)
        
        matches = []
        for i, j in zip(row_indices, col_indices):
            similarity = similarity_matrix[i, j]
            if similarity >= min_similarity:
                _, detailed_sim = self.compute_overall_similarity(surfaces1[i], surfaces2[j])
                matches.append({
                    'fragment1_idx': i,
                    'fragment2_idx': j,
                    'similarity': similarity,
                    'detailed_similarities': detailed_sim,
                    'color': color,
                    'surface1_features': surfaces1[i],
                    'surface2_features': surfaces2[j]
                })
        
        return matches
    
    def find_all_matches(self, fragments, min_similarity=0.6, use_optimal=True):
        """
        Find all potential matches between all fragments
        """
        print(f"🔍 SurfaceMatcher.find_all_matches() - FIXED VERSION")
        print(f"   Fragments: {len(fragments)}")
        print(f"   Min similarity: {min_similarity}")
        print(f"   Use optimal: {use_optimal}")
        
        all_matches = {}
        total_matches = 0
        
        for i in range(len(fragments)):
            for j in range(i + 1, len(fragments)):
                fragment1 = fragments[i]
                fragment2 = fragments[j]
                
                pair_key = f"fragment_{i}_to_{j}"
                print(f"\n  Finding matches between fragment {i} and fragment {j}...")
                
                color_matches = {'blue': [], 'green': [], 'red': []}
                
                for color in ['blue', 'green', 'red']:
                    if use_optimal:
                        matches = self.find_optimal_matches(fragment1, fragment2, color, min_similarity)
                    else:
                        matches = self.find_surface_matches(fragment1, fragment2, color, min_similarity)
                    
                    if matches:
                        color_matches[color] = matches
                        print(f"    {color}: {len(matches)} matches")
                        for match in matches[:2]:
                            print(f"      Similarity: {match['similarity']:.4f}")
                    
                    total_matches += len(matches)
                
                all_matches[pair_key] = color_matches
                
                pair_total = sum(len(matches) for matches in color_matches.values())
                if pair_total == 0:
                    print(f"  No matches found between fragments {i} and {j}")
                else:
                    print(f"  ✅ {pair_total} total matches found for {pair_key}")
        
        print(f"\n📊 FINAL MATCHING RESULTS:")
        print(f"   Total matches: {total_matches}")
        
        if total_matches == 0:
            print(f"   ⚠️ No matches found! Try lowering threshold to {min_similarity * 0.5:.2f}")
        
        return all_matches
    
    def visualize_match(self, fragment1, fragment2, match_info):
        """Visualize a specific surface match"""
        color = match_info['color']
        idx1 = match_info['fragment1_idx']
        idx2 = match_info['fragment2_idx']
        
        surface1 = fragment1['break_surfaces'][color][idx1]
        surface2 = fragment2['break_surfaces'][color][idx2]
        
        points1 = surface1['points']
        points2 = surface2['points']
        
        vis = o3d.visualization.Visualizer()
        vis.create_window(window_name=f"Surface Match - {color.capitalize()}")
        
        pcd1 = o3d.geometry.PointCloud()
        pcd1.points = o3d.utility.Vector3dVector(points1)
        pcd1.paint_uniform_color([1, 0, 0])
        
        pcd2 = o3d.geometry.PointCloud()
        pcd2.points = o3d.utility.Vector3dVector(points2 + [0.1, 0, 0])
        pcd2.paint_uniform_color([0, 0, 1])
        
        centroid1 = np.mean(points1, axis=0)
        centroid2 = np.mean(points2, axis=0) + [0.1, 0, 0]
        normal1 = np.array(match_info['surface1_features']['normal'])
        normal2 = np.array(match_info['surface2_features']['normal'])
        
        arrow1 = o3d.geometry.TriangleMesh.create_arrow(
            cylinder_radius=0.005, cone_radius=0.01, 
            cylinder_height=0.05, cone_height=0.02
        )
        arrow1.paint_uniform_color([1, 1, 0])
        arrow1.translate(centroid1)
        
        arrow2 = o3d.geometry.TriangleMesh.create_arrow(
            cylinder_radius=0.005, cone_radius=0.01,
            cylinder_height=0.05, cone_height=0.02
        )
        arrow2.paint_uniform_color([0, 1, 0])
        arrow2.translate(centroid2)
        
        vis.add_geometry(pcd1)
        vis.add_geometry(pcd2)
        vis.add_geometry(arrow1)
        vis.add_geometry(arrow2)
        
        vis.run()
        vis.destroy_window()
        
        print(f"\nMatch Details:")
        print(f"Overall Similarity: {match_info['similarity']:.3f}")
        print(f"Detailed Similarities:")
        for key, value in match_info['detailed_similarities'].items():
            print(f"  {key}: {value:.3f}")


def test_fixed_matcher():
    """Test the fixed surface matcher with mock data"""
    
    print("🧪 TESTING FIXED SURFACE MATCHER")
    print("=" * 50)
    
    mock_fragments = [
        {
            'features': {
                'blue': [{
                    'normal': [0.9980147591886815, -0.043240231905497584, 0.045791077584143774],
                    'area': 94136.83521077191,
                    'size': 79658,
                    'planarity': 0.0003999100493350613
                }],
                'red': [{
                    'normal': [-0.006973004035927785, 0.9940908502138144, -0.10832709142172414],
                    'area': 437255.5198936622,
                    'size': 162414,
                    'planarity': 0.007339990847671322
                }]
            }
        },
        {
            'features': {
                'blue': [{
                    'normal': [0.9985140117944759, 0.04576617514741478, 0.02958420968147235],
                    'area': 53508.47563583351,
                    'size': 83253,
                    'planarity': 0.0003060799921044662
                }],
                'red': [{
                    'normal': [-0.019707031993753184, 0.997827604263364, 0.0628625887156451],
                    'area': 427319.939585924,
                    'size': 126162,
                    'planarity': 0.008176061314579238
                }]
            }
        }
    ]
    
    matcher = SurfaceMatcher()
    
    for threshold in [0.6, 0.4, 0.3]:
        print(f"\n--- Testing threshold: {threshold} ---")
        matches = matcher.find_all_matches(mock_fragments, min_similarity=threshold, use_optimal=False)
        
        total = sum(
            len(color_matches[color])
            for color_matches in matches.values()
            for color in color_matches
        )
        print(f"Total matches at {threshold}: {total}")
    
    return matches

if __name__ == "__main__":
    test_fixed_matcher()
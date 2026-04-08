import numpy as np
import open3d as o3d
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
from pathlib import Path
import json

class PLYColorExtractor:
    """
    Class for loading PLY files and extracting colored break surfaces
    """
    
    def __init__(self, min_cluster_size=50):
        self.color_ranges = {
            'blue': {'min': [0, 0, 100], 'max': [100, 100, 255]},
            'green': {'min': [0, 100, 0], 'max': [100, 255, 100]},
            'red': {'min': [100, 0, 0], 'max': [255, 100, 100]}
        }
        # [CHANGE 3] Configurable at class level instead of hardcoded per call
        self.min_cluster_size = min_cluster_size
    
    def load_ply(self, filepath):
        """Load PLY file and return mesh or point cloud with colors"""
        try:
            mesh = o3d.io.read_triangle_mesh(str(filepath))

            # [CHANGE 1] read_triangle_mesh returns an empty mesh (silently) when the
            # PLY has no faces (i.e. it is a point cloud). Fall back to read_point_cloud
            # so these files are not silently dropped.
            if mesh.is_empty():
                pcd = o3d.io.read_point_cloud(str(filepath))
                if pcd.is_empty():
                    print(f"Warning: {filepath} could not be loaded as a mesh or point cloud")
                    return None
                if not pcd.has_colors():
                    print(f"Warning: {filepath} (point cloud) has no vertex colors")
                    return None
                print(f"Note: {Path(filepath).name} loaded as point cloud (no triangle faces found)")
                return pcd

            if not mesh.has_vertex_colors():
                print(f"Warning: {filepath} has no vertex colors")
                return None
            return mesh
        except Exception as e:
            print(f"Error loading {filepath}: {e}")
            return None
    
    def extract_colored_vertices(self, mesh, color_name, tolerance=0.3):
        """
        Extract vertices of a specific color using direct mesh approach
        
        Args:
            mesh: Open3D triangle mesh or point cloud
            color_name: 'blue', 'green', or 'red'
            tolerance: Color matching tolerance (not used with direct method)
        
        Returns:
            numpy array of colored vertex indices
        """
        if not mesh.has_vertex_colors():
            return np.array([])
        
        colors = np.asarray(mesh.vertex_colors)  # Already in 0-1 range
        
        print(f"    Using direct mesh detection for {color_name}...")
        
        # Use direct color thresholds (same as direct_mesh_detector)
        if color_name == 'green':
            mask = (
                (colors[:, 1] > 0.6) &  # Green channel is high  
                (colors[:, 0] < 0.4) &  # Red channel is low
                (colors[:, 2] < 0.4)    # Blue channel is low
            )
        elif color_name == 'blue':
            mask = (
                (colors[:, 2] > 0.6) &  # Blue channel is high
                (colors[:, 0] < 0.4) &  # Red channel is low
                (colors[:, 1] < 0.4)    # Green channel is low
            )
        elif color_name == 'red':
            mask = (
                (colors[:, 0] > 0.6) &  # Red channel is high
                (colors[:, 1] < 0.4) &  # Green channel is low
                (colors[:, 2] < 0.4)    # Blue channel is low
            )
        else:
            return np.array([])
        
        colored_indices = np.where(mask)[0]
        print(f"    Found {len(colored_indices)} {color_name} vertices using direct detection")
        
        return colored_indices
    
    def extract_break_surface_points(self, mesh, color_name, fragment_name="unknown"):
        """
        Extract break surface point clouds for a specific color - direct approach
        
        Args:
            mesh: Open3D triangle mesh or point cloud
            color_name: 'blue', 'green', or 'red'
            fragment_name: Name of the source file, used in skip warnings
        
        Returns:
            List of point clouds representing break surfaces
        """
        colored_indices = self.extract_colored_vertices(mesh, color_name)
        
        if len(colored_indices) == 0:
            return []
        
        vertices = np.asarray(mesh.vertices)
        colored_points = vertices[colored_indices]
        
        # Since we know each fragment has exactly 1 surface of each color,
        # skip clustering and create a single surface directly
        if len(colored_points) >= self.min_cluster_size:
            # Create point cloud directly from all colored points
            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(colored_points)
            
            # Estimate normals
            pcd.estimate_normals()
            
            break_surface = {
                'points': colored_points,
                'point_cloud': pcd,
                'color': color_name,
                'size': len(colored_points)
            }
            
            print(f"    Created {color_name} break surface with {len(colored_points)} points")
            return [break_surface]
        else:
            # [CHANGE 3] Include fragment name so large batch runs are debuggable
            print(
                f"    Warning: {color_name} surface in '{fragment_name}' skipped — "
                f"{len(colored_points)} points is below min_cluster_size={self.min_cluster_size}"
            )
            return []
    
    def process_fragment(self, filepath):
        """
        Process a single fragment file and extract all break surfaces
        
        Returns:
            Dictionary containing fragment data and break surfaces
        """
        mesh = self.load_ply(filepath)
        if mesh is None:
            return None
        
        fragment_data = {
            'filepath': str(filepath),
            'mesh': mesh,
            'break_surfaces': {}
        }
        
        # Extract break surfaces for each color
        for color in ['blue', 'green', 'red']:
            # [CHANGE 3] Pass fragment name so skip warnings are traceable
            break_surfaces = self.extract_break_surface_points(mesh, color, fragment_name=filepath.name)
            fragment_data['break_surfaces'][color] = break_surfaces
            print(f"Found {len(break_surfaces)} {color} break surfaces in {filepath.name}")
        
        return fragment_data
    
    def process_all_fragments(self, directory_path):
        """
        Process all PLY files in a directory
        
        Returns:
            List of fragment data dictionaries
        """
        directory = Path(directory_path)
        ply_files = list(directory.glob("*.ply"))
        
        if not ply_files:
            print(f"No PLY files found in {directory_path}")
            return []
        
        fragments = []
        for ply_file in ply_files:
            print(f"Processing {ply_file.name}...")
            fragment_data = self.process_fragment(ply_file)
            if fragment_data:
                fragments.append(fragment_data)
        
        # [CHANGE 2] Summary log so the caller knows the success/failure ratio at a glance
        total = len(ply_files)
        loaded = len(fragments)
        skipped = total - loaded
        print(f"\nLoaded {loaded}/{total} fragments successfully"
              + (f" ({skipped} skipped — see warnings above)." if skipped else "."))

        return fragments
    
    def save_fragment_data(self, fragments, output_path):
        """Save fragment data to JSON (excluding mesh objects)"""
        serializable_data = []
        
        for fragment in fragments:
            frag_data = {
                'filepath': fragment['filepath'],
                'break_surfaces': {}
            }
            
            for color, surfaces in fragment['break_surfaces'].items():
                frag_data['break_surfaces'][color] = []
                for surface in surfaces:
                    frag_data['break_surfaces'][color].append({
                        'points': surface['points'].tolist(),
                        'color': surface['color'],
                        'size': surface['size']
                    })
            
            serializable_data.append(frag_data)
        
        with open(output_path, 'w') as f:
            json.dump(serializable_data, f, indent=2)
        
        print(f"Fragment data saved to {output_path}")

# Example usage
if __name__ == "__main__":
    extractor = PLYColorExtractor()
    
    # Process all fragments in a directory
    fragments = extractor.process_all_fragments("path/to/your/ply/files")
    
    # Save data for later use
    extractor.save_fragment_data(fragments, "fragment_data.json")
    
    # Print summary
    for i, fragment in enumerate(fragments):
        print(f"\nFragment {i+1}: {Path(fragment['filepath']).name}")
        for color, surfaces in fragment['break_surfaces'].items():
            if surfaces:
                print(f"  {color}: {len(surfaces)} surfaces")

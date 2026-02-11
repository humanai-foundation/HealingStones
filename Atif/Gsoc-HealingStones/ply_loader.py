
import logging
import json
from pathlib import Path
from typing import Dict, List, Optional, Union, Tuple, Any

import numpy as np
import open3d as o3d

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PLYColorExtractor:
    """
    Class for loading PLY files and extracting colored break surfaces
    """
    
    # Default color configuration: channel indices and thresholds
    DEFAULT_COLOR_CONFIG = {
        'red':   {'channel': 0, 'min_val': 0.6, 'max_other': 0.4},
        'green': {'channel': 1, 'min_val': 0.6, 'max_other': 0.4},
        'blue':  {'channel': 2, 'min_val': 0.6, 'max_other': 0.4}
    }

    def __init__(self, color_config: Optional[Dict[str, Dict[str, float]]] = None):
        """
        Initialize the extractor with optional custom color configuration.
        
        Args:
            color_config: Dictionary defining color thresholds. 
                          Format: {'color_name': {'channel': int, 'min_val': float, 'max_other': float}}
        """
        self.color_config = color_config if color_config else self.DEFAULT_COLOR_CONFIG
    
    def load_ply(self, filepath: Union[str, Path]) -> Optional[o3d.geometry.TriangleMesh]:
        """
        Load PLY file and return mesh with colors.
        
        Args:
            filepath: Path to the PLY file.
            
        Returns:
            Open3D TriangleMesh or None if loading fails.
        """
        try:
            filepath_str = str(filepath)
            mesh = o3d.io.read_triangle_mesh(filepath_str)
            if not mesh.has_vertex_colors():
                logger.warning(f"{filepath} has no vertex colors")
                return None
            return mesh
        except Exception as e:
            logger.error(f"Error loading {filepath}: {e}")
            return None
    
    def extract_colored_vertices(self, mesh: o3d.geometry.TriangleMesh, color_name: str) -> np.ndarray:
        """
        Extract vertices of a specific color using direct mesh approach.
        
        Args:
            mesh: Open3D triangle mesh
            color_name: Name of the color to extract (must exist in config)
        
        Returns:
            numpy array of colored vertex indices
        """
        if not mesh.has_vertex_colors():
            return np.array([])
        
        if color_name not in self.color_config:
            logger.warning(f"Color '{color_name}' not found in configuration")
            return np.array([])

        colors = np.asarray(mesh.vertex_colors)  # Already in 0-1 range
        config = self.color_config[color_name]
        
        target_channel = int(config['channel'])
        min_val = config['min_val']
        max_other = config['max_other']
        
        logger.debug(f"Using direct mesh detection for {color_name}...")
        
        # Create mask based on configuration
        # The target channel must be > min_val
        # All other channels must be < max_other
        mask = (colors[:, target_channel] > min_val)
        
        for i in range(3):
            if i != target_channel:
                mask &= (colors[:, i] < max_other)
        
        colored_indices = np.where(mask)[0]
        logger.debug(f"Found {len(colored_indices)} {color_name} vertices using direct detection")
        
        return colored_indices
    
    def extract_break_surface_points(self, mesh: o3d.geometry.TriangleMesh, color_name: str, min_cluster_size: int = 50) -> List[Dict[str, Any]]:
        """
        Extract break surface point clouds for a specific color - direct approach.
        
        Args:
            mesh: Open3D triangle mesh
            color_name: Name of the color to extract
            min_cluster_size: Minimum points in a cluster
        
        Returns:
            List of dictionaries representing break surfaces
        """
        colored_indices = self.extract_colored_vertices(mesh, color_name)
        
        if len(colored_indices) == 0:
            return []
        
        vertices = np.asarray(mesh.vertices)
        colored_points = vertices[colored_indices]
        
        # Since we know each fragment has exactly 1 surface of each color,
        # skip clustering and create a single surface directly
        if len(colored_points) >= min_cluster_size:
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
            
            logger.info(f"Created {color_name} break surface with {len(colored_points)} points")
            return [break_surface]
        else:
            logger.debug(f"{color_name} surface too small: {len(colored_points)} < {min_cluster_size}")
            return []
    
    def process_fragment(self, filepath: Union[str, Path]) -> Optional[Dict[str, Any]]:
        """
        Process a single fragment file and extract all break surfaces.
        
        Args:
            filepath: Path to the fragment file
            
        Returns:
            Dictionary containing fragment data and break surfaces, or None
        """
        path_obj = Path(filepath)
        mesh = self.load_ply(path_obj)
        if mesh is None:
            return None
        
        fragment_data = {
            'filepath': str(path_obj),
            'mesh': mesh,
            'break_surfaces': {}
        }
        
        # Extract break surfaces for each configured color
        for color in self.color_config:
            break_surfaces = self.extract_break_surface_points(mesh, color)
            fragment_data['break_surfaces'][color] = break_surfaces # type: ignore
            if break_surfaces:
                logger.info(f"Found {len(break_surfaces)} {color} break surfaces in {path_obj.name}")
        
        return fragment_data
    
    def process_all_fragments(self, directory_path: Union[str, Path]) -> List[Dict[str, Any]]:
        """
        Process all PLY files in a directory.
        
        Args:
            directory_path: Directory containing PLY files
            
        Returns:
            List of fragment data dictionaries
        """
        directory = Path(directory_path)
        ply_files = list(directory.glob("*.ply"))
        
        if not ply_files:
            logger.warning(f"No PLY files found in {directory_path}")
            return []
        
        fragments = []
        for ply_file in ply_files:
            logger.info(f"Processing {ply_file.name}...")
            fragment_data = self.process_fragment(ply_file)
            if fragment_data:
                fragments.append(fragment_data)
        
        return fragments
    
    def save_fragment_data(self, fragments: List[Dict[str, Any]], output_path: Union[str, Path]) -> None:
        """
        Save fragment data to JSON (excluding mesh objects).
        
        Args:
            fragments: List of fragment data dictionaries
            output_path: Path to save the JSON file
        """
        serializable_data = []
        
        for fragment in fragments:
            frag_data = {
                'filepath': fragment['filepath'],
                'break_surfaces': {}
            }
            
            for color, surfaces in fragment['break_surfaces'].items(): # type: ignore
                frag_data['break_surfaces'][color] = [] # type: ignore
                for surface in surfaces:
                    frag_data['break_surfaces'][color].append({ # type: ignore
                        'points': surface['points'].tolist(),
                        'color': surface['color'],
                        'size': surface['size']
                    })
            
            serializable_data.append(frag_data)
        
        try:
            with open(output_path, 'w') as f:
                json.dump(serializable_data, f, indent=2)
            logger.info(f"Fragment data saved to {output_path}")
        except IOError as e:
            logger.error(f"Failed to save fragment data to {output_path}: {e}")

# Example usage
if __name__ == "__main__":
    extractor = PLYColorExtractor()
    
    # Process all fragments in a directory
    # Note: Replace with actual path or use argparse
    # fragments = extractor.process_all_fragments("path/to/your/ply/files")
    
    # Save data for later use
    # extractor.save_fragment_data(fragments, "fragment_data.json")
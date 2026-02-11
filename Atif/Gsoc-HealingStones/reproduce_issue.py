
import numpy as np
import open3d as o3d
import os
from ply_loader import PLYColorExtractor

def create_dummy_ply(filename):
    """Creates a dummy PLY file with specific colored vertices."""
    print(f"Creating dummy PLY: {filename}")
    
    # Create vertices
    # 100 points
    points = np.random.rand(100, 3).astype(np.float64)
    
    # Create colors
    colors = np.zeros((100, 3), dtype(np.float64))
    
    # indices 0-29: RED (0.8, 0.1, 0.1) -> Should be detected as RED
    colors[0:30] = [0.8, 0.1, 0.1]
    
    # indices 30-59: GREEN (0.1, 0.8, 0.1) -> Should be detected as GREEN
    colors[30:60] = [0.1, 0.8, 0.1]
    
    # indices 60-89: BLUE (0.1, 0.1, 0.8) -> Should be detected as BLUE
    colors[60:90] = [0.1, 0.1, 0.8]
    
    # indices 90-99: WHITE/NOISE (0.9, 0.9, 0.9) -> Should be ignored
    colors[90:100] = [0.9, 0.9, 0.9]
    
    # Create mesh
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.colors = o3d.utility.Vector3dVector(colors)
    
    # Estimate normals so it looks like a mesh if we were to reconstruct, 
    # but for PLYColorExtractor it loads as a mesh using read_triangle_mesh.
    # To truly simulate a mesh, we need triangles.
    
    mesh = o3d.geometry.TriangleMesh()
    mesh.vertices = o3d.utility.Vector3dVector(points)
    mesh.vertex_colors = o3d.utility.Vector3dVector(colors)
    
    # Create some dummy triangles
    triangles = []
    for i in range(0, 90, 3):
        triangles.append([i, i+1, i+2])
    mesh.triangles = o3d.utility.Vector3iVector(np.array(triangles))
    
    o3d.io.write_triangle_mesh(filename, mesh)
    return filename

def test_ply_loader():
    filename = "test_fragment.ply"
    try:
        create_dummy_ply(filename)
        
        extractor = PLYColorExtractor()
        print("\n--- Testing Load PLY ---")
        mesh = extractor.load_ply(filename)
        if mesh is None:
            print("FAILED: Could not load mesh")
            return
            
        print("Mesh loaded successfully")
        
        print("\n--- Testing Color Extraction ---")
        # Test Red
        red_indices = extractor.extract_colored_vertices(mesh, 'red')
        print(f"Red indices found: {len(red_indices)} (Expected 30)")
        
        # Test Green
        green_indices = extractor.extract_colored_vertices(mesh, 'green')
        print(f"Green indices found: {len(green_indices)} (Expected 30)")
        
        # Test Blue
        blue_indices = extractor.extract_colored_vertices(mesh, 'blue')
        print(f"Blue indices found: {len(blue_indices)} (Expected 30)")
        
        print("\n--- Testing Fragment Processing ---")
        # We need to set min_cluster_size low because we only have 30 points
        # The default in extract_break_surface_points is 50, so we expect 0 surfaces unless we modify call
        # But process_fragment calls it with default.
        
        # Let's inspect the extractor's method signature in the file being refactored to see if we can easily mock it 
        # or if we should just monkeypatch the default for this test.
        # process_fragment calls extract_break_surface_points(mesh, color) -> uses default min_cluster_size=50.
        
        # So we expect 0 surfaces with current code for 30 points.
        fragment_data = extractor.process_fragment(Path(filename))
        
        for color in ['red', 'green', 'blue']:
            surfaces = fragment_data['break_surfaces'][color]
            print(f"Surfaces for {color}: {len(surfaces)}")
            
    finally:
        if os.path.exists(filename):
            os.remove(filename)
            print(f"\nCleaned up {filename}")

if __name__ == "__main__":
    test_ply_loader()

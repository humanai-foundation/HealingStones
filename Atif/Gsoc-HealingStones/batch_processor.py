import os
import numpy as np
import open3d as o3d
from pathlib import Path
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
import json
import argparse
from typing import List, Dict, Tuple, Optional
import cv2

class PLYValidator:
    """
    Validate PLY files for reconstruction pipeline
    """
    
    def __init__(self):
        self.validation_results = {}
        self.color_ranges = {
            'blue': {'min': [0, 0, 100], 'max': [100, 100, 255]},
            'green': {'min': [0, 100, 0], 'max': [100, 255, 100]},
            'red': {'min': [100, 0, 0], 'max': [255, 100, 100]}
        }
    
    # ------------------------------------------------------------------ #
    # HIGH PRIORITY DEFENSIVE CHECKS                                      #
    # ------------------------------------------------------------------ #

    MAX_FILE_SIZE_MB = 500
    MIN_FILE_SIZE_BYTES = 80  # A valid PLY header is at least ~80 bytes

    def _validate_path(self, filepath: Path) -> Tuple[List[str], List[str]]:
        """
        Check that the path exists, is a regular file, has a .ply extension,
        and is readable.

        Returns:
            (errors, warnings) — errors are fatal; warnings are informational.
        """
        errors: List[str] = []
        warnings: List[str] = []

        if not filepath.exists():
            errors.append(f"File does not exist: {filepath}")
            return errors, warnings  # Nothing more to check

        if not filepath.is_file():
            errors.append(f"Path is not a regular file: {filepath}")
            return errors, warnings

        if filepath.suffix.lower() != '.ply':
            errors.append(
                f"Unexpected file extension '{filepath.suffix}' — expected '.ply'"
            )

        if not os.access(filepath, os.R_OK):
            errors.append(f"File is not readable (permission denied): {filepath}")

        return errors, warnings

    def _check_file_size(self, filepath: Path) -> Tuple[List[str], List[str]]:
        """
        Reject files that are suspiciously small (likely corrupt/empty) and
        warn on files so large they may exhaust memory.

        Returns:
            (errors, warnings)
        """
        errors: List[str] = []
        warnings: List[str] = []

        try:
            size_bytes = filepath.stat().st_size
        except OSError as exc:
            errors.append(f"Could not stat file: {exc}")
            return errors, warnings

        size_mb = size_bytes / (1024 ** 2)

        if size_bytes < self.MIN_FILE_SIZE_BYTES:
            errors.append(
                f"File is suspiciously small ({size_bytes} bytes) — "
                "likely corrupt or empty"
            )

        if size_mb > self.MAX_FILE_SIZE_MB:
            warnings.append(
                f"File is very large ({size_mb:.1f} MB) — "
                "processing may be slow or exhaust memory"
            )

        return errors, warnings

    # ------------------------------------------------------------------ #

    def validate_ply_file(self, filepath: str) -> Dict:
        """
        Comprehensive validation of a single PLY file
        
        Returns:
            Dictionary with validation results
        """
        filepath = Path(filepath)
        results = {
            'filepath': str(filepath),
            'valid': True,
            'warnings': [],
            'errors': [],
            'statistics': {}
        }

        # --- HIGH 1: path / extension / permission checks ---
        path_errors, path_warnings = self._validate_path(filepath)
        results['errors'].extend(path_errors)
        results['warnings'].extend(path_warnings)
        if path_errors:
            results['valid'] = False
            return results

        # --- HIGH 2: file size checks ---
        size_errors, size_warnings = self._check_file_size(filepath)
        results['errors'].extend(size_errors)
        results['warnings'].extend(size_warnings)
        if size_errors:
            results['valid'] = False
            return results

        try:
            # Load mesh
            mesh = o3d.io.read_triangle_mesh(str(filepath))
            
            if len(mesh.vertices) == 0:
                results['errors'].append("Mesh has no vertices")
                results['valid'] = False
                return results
            
            # Basic statistics
            results['statistics']['num_vertices'] = len(mesh.vertices)
            results['statistics']['num_triangles'] = len(mesh.triangles)
            results['statistics']['has_vertex_colors'] = mesh.has_vertex_colors()
            results['statistics']['has_vertex_normals'] = mesh.has_vertex_normals()
            results['statistics']['has_triangle_normals'] = mesh.has_triangle_normals()
            
            # Check for vertex colors (required for break surface detection)
            if not mesh.has_vertex_colors():
                results['errors'].append("Mesh has no vertex colors (required for break surface detection)")
                results['valid'] = False
                return results
            
            # Analyze colors
            colors = np.asarray(mesh.vertex_colors) * 255  # Convert to 0-255
            results['statistics']['color_analysis'] = self._analyze_colors(colors)
            
            # Check for colored break surfaces
            break_surface_analysis = self._analyze_break_surfaces(mesh)
            results['statistics']['break_surfaces'] = break_surface_analysis
            
            # Validate break surface presence
            total_colored_surfaces = sum(len(surfaces) for surfaces in break_surface_analysis.values())
            if total_colored_surfaces == 0:
                results['warnings'].append("No colored break surfaces detected")
            
            # Check mesh quality
            mesh_quality = self._check_mesh_quality(mesh)
            results['statistics']['mesh_quality'] = mesh_quality
            
            # Add warnings based on analysis
            if mesh_quality['is_watertight'] == False:
                results['warnings'].append("Mesh is not watertight")
            
            if mesh_quality['has_degenerate_triangles']:
                results['warnings'].append("Mesh contains degenerate triangles")
            
            if results['statistics']['num_vertices'] < 1000:
                results['warnings'].append("Mesh has very few vertices (< 1000)")
            
            if results['statistics']['num_vertices'] > 1000000:
                results['warnings'].append("Mesh has very many vertices (> 1M), processing may be slow")
            
        except Exception as e:
            results['errors'].append(f"Failed to load or analyze file: {str(e)}")
            results['valid'] = False
        
        return results
    
    def _analyze_colors(self, colors: np.ndarray) -> Dict:
        """Analyze color distribution in the mesh"""
        analysis = {
            'unique_colors': len(np.unique(colors.view(np.void), axis=0)),
            'color_stats': {},
            'dominant_colors': []
        }
        
        # Statistics for each channel
        for i, channel in enumerate(['red', 'green', 'blue']):
            channel_data = colors[:, i]
            analysis['color_stats'][channel] = {
                'mean': float(np.mean(channel_data)),
                'std': float(np.std(channel_data)),
                'min': float(np.min(channel_data)),
                'max': float(np.max(channel_data))
            }
        
        # Find dominant colors using k-means clustering
        try:
            from sklearn.cluster import KMeans
            kmeans = KMeans(n_clusters=min(8, len(colors)), random_state=42, n_init=10)
            labels = kmeans.fit_predict(colors)
            
            # Get cluster centers and sizes
            for i, center in enumerate(kmeans.cluster_centers_):
                cluster_size = np.sum(labels == i)
                analysis['dominant_colors'].append({
                    'color': center.astype(int).tolist(),
                    'percentage': float(cluster_size / len(colors) * 100)
                })
        except Exception as e:
                analysis['dominant_colors'] = []
                analysis['kmeans_error'] = str(e)
        
        return analysis
    
    def _analyze_break_surfaces(self, mesh) -> Dict:
        """Analyze colored break surfaces in the mesh"""
        surfaces = {'blue': [], 'green': [], 'red': []}
        
        vertices = np.asarray(mesh.vertices)
        colors = np.asarray(mesh.vertex_colors) * 255
        
        for color_name, color_range in self.color_ranges.items():
            # Find vertices with this color
            mask = np.all([
                colors[:, 0] >= color_range['min'][0] - 50,
                colors[:, 0] <= color_range['max'][0] + 50,
                colors[:, 1] >= color_range['min'][1] - 50,
                colors[:, 1] <= color_range['max'][1] + 50,
                colors[:, 2] >= color_range['min'][2] - 50,
                colors[:, 2] <= color_range['max'][2] + 50
            ], axis=0)
            
            colored_indices = np.where(mask)[0]
            
            if len(colored_indices) > 0:
                colored_points = vertices[colored_indices]
                
                # Cluster colored regions
                if len(colored_points) >= 10:
                    clustering = DBSCAN(eps=0.02, min_samples=5).fit(colored_points)
                    labels = clustering.labels_
                    
                    for label in np.unique(labels):
                        if label == -1:  # Skip noise
                            continue
                        
                        cluster_points = colored_points[labels == label]
                        if len(cluster_points) >= 20:  # Minimum surface size
                            surfaces[color_name].append({
                                'num_points': len(cluster_points),
                                'centroid': np.mean(cluster_points, axis=0).tolist(),
                                'bounding_box_size': (np.max(cluster_points, axis=0) - 
                                                    np.min(cluster_points, axis=0)).tolist()
                            })
        
        return surfaces
    
    def _check_mesh_quality(self, mesh) -> Dict:
        """Check mesh quality metrics"""
        quality = {}
        
        # Check if watertight
        quality['is_watertight'] = mesh.is_watertight()
        
        # Check for degenerate triangles
        triangles = np.asarray(mesh.triangles)
        vertices = np.asarray(mesh.vertices)
        
        degenerate_count = 0
        if len(triangles) > 0:
            for triangle in triangles[:min(1000, len(triangles))]:  # Sample for speed
                v0, v1, v2 = vertices[triangle]
                # Check if triangle area is very small
                edge1 = v1 - v0
                edge2 = v2 - v0
                cross = np.cross(edge1, edge2)
                area = 0.5 * np.linalg.norm(cross)
                if area < 1e-10:
                    degenerate_count += 1
        
        quality['has_degenerate_triangles'] = degenerate_count > 0
        quality['degenerate_triangle_count'] = degenerate_count
        
        # Check vertex connectivity
        if len(mesh.vertices) > 0:
            mesh.remove_duplicated_vertices()
            mesh.remove_unreferenced_vertices()
            quality['removed_duplicates'] = True
        
        # Bounding box
        if len(mesh.vertices) > 0:
            bbox = mesh.get_axis_aligned_bounding_box()
            extent = bbox.get_extent()
            quality['bounding_box_extent'] = extent.tolist()
            quality['largest_dimension'] = float(np.max(extent))
        
        return quality
    
    def validate_directory(self, directory: str) -> Dict:
        """Validate all PLY files in a directory"""
        directory = Path(directory)
        
        if not directory.exists():
            raise FileNotFoundError(f"Directory not found: {directory}")
        
        ply_files = list(directory.glob("*.ply"))
        
        if not ply_files:
            raise ValueError(f"No PLY files found in {directory}")
        
        results = {
            'directory': str(directory),
            'total_files': len(ply_files),
            'valid_files': 0,
            'files_with_warnings': 0,
            'files_with_errors': 0,
            'file_results': []
        }
        
        for ply_file in ply_files:
            print(f"Validating {ply_file.name}...")
            file_result = self.validate_ply_file(ply_file)
            results['file_results'].append(file_result)
            
            if file_result['valid']:
                results['valid_files'] += 1
            else:
                results['files_with_errors'] += 1
            
            if file_result['warnings']:
                results['files_with_warnings'] += 1
        
        return results
    
    def generate_validation_report(self, validation_results: Dict, output_path: str = None):
        """Generate a comprehensive validation report"""
        report = []
        report.append("=" * 60)
        report.append("PLY FILE VALIDATION REPORT")
        report.append("=" * 60)
        report.append("")
        
        # Summary
        report.append(f"Directory: {validation_results['directory']}")
        report.append(f"Total files: {validation_results['total_files']}")
        report.append(f"Valid files: {validation_results['valid_files']}")
        report.append(f"Files with warnings: {validation_results['files_with_warnings']}")
        report.append(f"Files with errors: {validation_results['files_with_errors']}")
        report.append("")
        
        # Detailed results
        for file_result in validation_results['file_results']:
            report.append(f"File: {Path(file_result['filepath']).name}")
            report.append(f"  Status: {'VALID' if file_result['valid'] else 'INVALID'}")
            
            # Statistics
            stats = file_result['statistics']
            if stats:
                report.append(f"  Vertices: {stats.get('num_vertices', 'N/A')}")
                report.append(f"  Triangles: {stats.get('num_triangles', 'N/A')}")
                report.append(f"  Has colors: {stats.get('has_vertex_colors', 'N/A')}")
                
                # Break surfaces
                if 'break_surfaces' in stats:
                    bs = stats['break_surfaces']
                    total_surfaces = sum(len(surfaces) for surfaces in bs.values())
                    report.append(f"  Break surfaces: {total_surfaces}")
                    for color, surfaces in bs.items():
                        if surfaces:
                            report.append(f"    {color}: {len(surfaces)}")
            
            # Warnings
            if file_result['warnings']:
                report.append("  Warnings:")
                for warning in file_result['warnings']:
                    report.append(f"    - {warning}")
            
            # Errors
            if file_result['errors']:
                report.append("  Errors:")
                for error in file_result['errors']:
                    report.append(f"    - {error}")
            
            report.append("")
        
        report_text = "\n".join(report)
        
        if output_path:
            with open(output_path, 'w') as f:
                f.write(report_text)
            print(f"Validation report saved to: {output_path}")
        else:
            print(report_text)

class PLYPreprocessor:
    """
    Preprocessing utilities for PLY files
    """
    
    def __init__(self):
        pass
    
    def clean_mesh(self, mesh: o3d.geometry.TriangleMesh) -> o3d.geometry.TriangleMesh:
        """Clean and repair mesh"""
        print("Cleaning mesh...")
        
        # Remove duplicated vertices
        mesh.remove_duplicated_vertices()
        print(f"  Removed duplicated vertices")
        
        # Remove unreferenced vertices
        mesh.remove_unreferenced_vertices()
        print(f"  Removed unreferenced vertices")
        
        # Remove degenerate triangles
        mesh.remove_degenerate_triangles()
        print(f"  Removed degenerate triangles")
        
        # Remove duplicated triangles
        mesh.remove_duplicated_triangles()
        print(f"  Removed duplicated triangles")
        
        # Filter smooth mesh (optional)
        # mesh = mesh.filter_smooth_simple(number_of_iterations=5)
        
        return mesh
    
    def normalize_mesh_scale(self, mesh: o3d.geometry.TriangleMesh, target_size: float = 1.0) -> o3d.geometry.TriangleMesh:
        """Normalize mesh to a standard scale"""
        # --- MEDIUM 2: guard against zero extent and invalid target_size ---
        if target_size <= 0:
            raise ValueError(
                f"target_size must be a positive number, got {target_size}"
            )

        bbox = mesh.get_axis_aligned_bounding_box()
        extent = bbox.get_extent()
        max_extent = float(np.max(extent))

        if max_extent == 0.0:
            print("Warning: Mesh has zero bounding-box extent — skipping normalization")
            return mesh

        scale_factor = target_size / max_extent
        mesh.scale(scale_factor, center=mesh.get_center())

        print(f"Scaled mesh by factor {scale_factor:.3f}")
        return mesh
    
    def center_mesh(self, mesh: o3d.geometry.TriangleMesh) -> o3d.geometry.TriangleMesh:
        """Center mesh at origin"""
        center = mesh.get_center()
        mesh.translate(-center)
        print(f"Centered mesh (was at {center})")
        return mesh
    
    def enhance_break_surface_colors(self, mesh: o3d.geometry.TriangleMesh, 
                                   color_enhancement: float = 1.5) -> o3d.geometry.TriangleMesh:
        """Enhance the visibility of break surface colors"""
        if not mesh.has_vertex_colors():
            print("Mesh has no vertex colors to enhance")
            return mesh
        
        colors = np.asarray(mesh.vertex_colors)
        
        # Define break surface color ranges (normalized 0-1)
        break_colors = {
            'blue': [0, 0, 1],
            'green': [0, 1, 0], 
            'red': [1, 0, 0]
        }
        
        enhanced_colors = colors.copy()
        
        for color_name, target_color in break_colors.items():
            target_color = np.array(target_color)
            
            # Find vertices close to this color
            color_distances = np.linalg.norm(colors - target_color, axis=1)
            close_to_color = color_distances < 0.3  # Threshold for "close"
            
            if np.any(close_to_color):
                # Enhance these colors
                enhanced_colors[close_to_color] = (
                    enhanced_colors[close_to_color] * (1 - color_enhancement) + 
                    target_color * color_enhancement
                )
                # Clamp to valid range
                enhanced_colors[close_to_color] = np.clip(enhanced_colors[close_to_color], 0, 1)
                
                print(f"Enhanced {np.sum(close_to_color)} {color_name} vertices")
        
        mesh.vertex_colors = o3d.utility.Vector3dVector(enhanced_colors)
        return mesh
    
    def preprocess_file(self, input_path: str, output_path: str, 
                       clean: bool = True, 
                       normalize_scale: bool = True, 
                       center: bool = True,
                       enhance_colors: bool = True) -> bool:
        """Preprocess a single PLY file"""
        try:
            input_path_obj = Path(input_path)
            output_path_obj = Path(output_path)

            # --- MEDIUM 1a: prevent overwriting the source file ---
            if input_path_obj.resolve() == output_path_obj.resolve():
                print(
                    f"Error: Output path is the same as input path ({input_path}). "
                    "Aborting to avoid data loss."
                )
                return False

            # --- MEDIUM 1b: ensure output directory exists and is writable ---
            output_dir = output_path_obj.parent
            output_dir.mkdir(parents=True, exist_ok=True)
            if not os.access(output_dir, os.W_OK):
                print(
                    f"Error: No write permission to output directory: {output_dir}"
                )
                return False

            print(f"Preprocessing {input_path}...")
            
            # Load mesh
            mesh = o3d.io.read_triangle_mesh(input_path)
            
            if len(mesh.vertices) == 0:
                print(f"Error: Empty mesh in {input_path}")
                return False
            
            # Apply preprocessing steps
            if clean:
                mesh = self.clean_mesh(mesh)
            
            if center:
                mesh = self.center_mesh(mesh)
            
            if normalize_scale:
                mesh = self.normalize_mesh_scale(mesh)
            
            if enhance_colors and mesh.has_vertex_colors():
                mesh = self.enhance_break_surface_colors(mesh)
            
            # Ensure normals are computed
            if not mesh.has_vertex_normals():
                mesh.compute_vertex_normals()
                print("Computed vertex normals")
            
            # Save processed mesh
            success = o3d.io.write_triangle_mesh(output_path, mesh)
            
            if success:
                print(f"Preprocessed mesh saved to {output_path}")
                return True
            else:
                print(f"Error: Failed to save mesh to {output_path}")
                return False
                
        except Exception as e:
            print(f"Error preprocessing {input_path}: {e}")
            return False
    
    def preprocess_directory(self, input_dir: str, output_dir: str, **kwargs) -> Dict:
        """Preprocess all PLY files in a directory"""
        input_dir = Path(input_dir)
        output_dir = Path(output_dir)
        
        if not input_dir.exists():
            raise FileNotFoundError(f"Input directory not found: {input_dir}")
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        ply_files = list(input_dir.glob("*.ply"))
        
        if not ply_files:
            raise ValueError(f"No PLY files found in {input_dir}")
        
        results = {
            'input_directory': str(input_dir),
            'output_directory': str(output_dir),
            'total_files': len(ply_files),
            'successful': 0,
            'failed': 0,
            'file_results': []
        }
        
        for ply_file in ply_files:
            output_path = output_dir / ply_file.name
            
            success = self.preprocess_file(str(ply_file), str(output_path), **kwargs)
            
            results['file_results'].append({
                'input_file': str(ply_file),
                'output_file': str(output_path),
                'success': success
            })
            
            if success:
                results['successful'] += 1
            else:
                results['failed'] += 1
        
        print(f"\nPreprocessing complete:")
        print(f"  Successful: {results['successful']}")
        print(f"  Failed: {results['failed']}")
        
        return results

# CLI Interface
def main():
    parser = argparse.ArgumentParser(description="PLY Preprocessing and Validation Tools")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Validation command
    validate_parser = subparsers.add_parser('validate', help='Validate PLY files')
    validate_parser.add_argument('input', help='PLY file or directory to validate')
    validate_parser.add_argument('--output', '-o', help='Output validation report file')
    validate_parser.add_argument('--json', action='store_true', help='Output results as JSON')
    
    # Preprocessing command
    preprocess_parser = subparsers.add_parser('preprocess', help='Preprocess PLY files')
    preprocess_parser.add_argument('input', help='Input PLY file or directory')
    preprocess_parser.add_argument('output', help='Output PLY file or directory')
    preprocess_parser.add_argument('--no-clean', action='store_true', help='Skip mesh cleaning')
    preprocess_parser.add_argument('--no-normalize', action='store_true', help='Skip scale normalization')
    preprocess_parser.add_argument('--no-center', action='store_true', help='Skip centering')
    preprocess_parser.add_argument('--no-enhance-colors', action='store_true', help='Skip color enhancement')
    
    args = parser.parse_args()
    
    if args.command == 'validate':
        validator = PLYValidator()
        
        input_path = Path(args.input)
        
        if input_path.is_file():
            # Validate single file
            result = validator.validate_ply_file(args.input)
            
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print(f"File: {result['filepath']}")
                print(f"Valid: {result['valid']}")
                if result['warnings']:
                    print("Warnings:")
                    for warning in result['warnings']:
                        print(f"  - {warning}")
                if result['errors']:
                    print("Errors:")
                    for error in result['errors']:
                        print(f"  - {error}")
        
        elif input_path.is_dir():
            # Validate directory
            results = validator.validate_directory(args.input)
            
            if args.json:
                if args.output:
                    with open(args.output, 'w') as f:
                        json.dump(results, f, indent=2)
                else:
                    print(json.dumps(results, indent=2))
            else:
                validator.generate_validation_report(results, args.output)
        
        else:
            print(f"Error: {args.input} is not a valid file or directory")
    
    elif args.command == 'preprocess':
        preprocessor = PLYPreprocessor()
        
        input_path = Path(args.input)
        output_path = Path(args.output)
        
        # Set preprocessing options
        options = {
            'clean': not args.no_clean,
            'normalize_scale': not args.no_normalize,
            'center': not args.no_center,
            'enhance_colors': not args.no_enhance_colors
        }
        
        if input_path.is_file():
            # Preprocess single file
            success = preprocessor.preprocess_file(str(input_path), str(output_path), **options)
            if not success:
                exit(1)
        
        elif input_path.is_dir():
            # Preprocess directory
            results = preprocessor.preprocess_directory(str(input_path), str(output_path), **options)
            if results['failed'] > 0:
                exit(1)
        
        else:
            print(f"Error: {args.input} is not a valid file or directory")
            exit(1)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
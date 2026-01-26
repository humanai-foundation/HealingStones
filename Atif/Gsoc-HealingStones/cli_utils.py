import os
import glob
from pathlib import Path

def validate_dataset(input_path, output_path=None):
    """
    Validate dataset structure and inputs without side effects.
    
    Args:
        input_path: Path to the directory containing .ply files
        output_path: Optional path to an output directory
        
    Returns:
        tuple: (results_dict, success_bool)
    """
    ip = Path(input_path).resolve()
    results = {
        'input_path': str(input_path),
        'exists': False,
        'is_dir': False,
        'ply_count': 0,
        'output_writable': True if output_path is None else False,
        'issues': []
    }
    
    # Check input path (strictly read-only)
    if not ip.exists():
        results['issues'].append(f"Input path does not exist: {input_path}")
    else:
        results['exists'] = True
        if not ip.is_dir():
            results['issues'].append(f"Input path is not a directory: {input_path}")
        else:
            results['is_dir'] = True
            try:
                ply_files = glob.glob(str(ip / "*.ply"))
                results['ply_count'] = len(ply_files)
                if results['ply_count'] == 0:
                    results['issues'].append(f"No .ply files found in: {input_path}")
            except Exception as e:
                results['issues'].append(f"Error accessing input directory: {e}")
    
    # Check output path writability (strictly read-only)
    if output_path:
        op = Path(output_path).resolve()
        # Find first existing parent
        curr = op
        while not curr.exists() and curr != curr.parent:
            curr = curr.parent
            
        if not os.access(curr, os.W_OK):
            results['issues'].append(f"Output location is not writable: {curr}")
        else:
            results['output_writable'] = True
            
    success = len(results['issues']) == 0
    return results, success

def print_validation_report(results, command_name="DATASET CHECK"):
    """
    Print a standardized validation report summary.
    """
    print(f"\n🔍 {command_name}")
    print("=" * 60)
    print(f"Input Path:  {results['input_path']}")
    print(f"PLY Files:   {results['ply_count']}")
    
    if results['issues']:
        print("\n❌ ISSUES DETECTED:")
        for issue in results['issues']:
            print(f"   - {issue}")
        print("\nRESULT: FAIL ❌")
    else:
        print("\nRESULT: PASS ✅")
        print("Dataset is ready for processing.")
        
    print("=" * 60)

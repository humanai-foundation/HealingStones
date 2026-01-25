import os
import sys
import glob
from pathlib import Path

def validate_paths(input_path, output_path=None, config_path=None):
    """
    Validate input/output paths and config without side effects.
    Returns a dict with validation results and a success boolean.
    """
    results = {
        'input': {'exists': False, 'is_dir': False, 'ply_count': 0},
        'output': {'exists': False, 'writable': False},
        'config': {'exists': False}
    }
    success = True

    # Validate input
    ip = Path(input_path)
    if ip.exists():
        results['input']['exists'] = True
        if ip.is_dir():
            results['input']['is_dir'] = True
            results['input']['ply_count'] = len(glob.glob(str(ip / "*.ply")))
        else:
            if str(ip).lower().endswith('.ply'):
                results['input']['ply_count'] = 1
    else:
        success = False

    # Validate output (without creating it)
    if output_path:
        op = Path(output_path)
        if op.exists():
            results['output']['exists'] = True
            # Check writability of existing directory/file parent
            if os.access(op if op.is_dir() else op.parent, os.W_OK):
                results['output']['writable'] = True
            else:
                success = False
        else:
            # If it doesn't exist, check if we CAN create it (parent must be writable)
            parent = op.parent
            if parent.exists() and os.access(parent, os.W_OK):
                results['output']['writable'] = True
            else:
                # Trace back to find first existing parent
                curr = parent
                while not curr.exists() and curr != curr.parent:
                    curr = curr.parent
                if curr.exists() and os.access(curr, os.W_OK):
                    results['output']['writable'] = True
                else:
                    success = False

    # Validate config
    if config_path:
        cp = Path(config_path)
        if cp.exists() and cp.is_file():
            results['config']['exists'] = True
        else:
            success = False

    return results, success

def print_dry_run_summary(command_name, validation_results, planned_actions):
    """
    Print a consistent, structured dry run summary.
    """
    print(f"\n🔍 DRY RUN: {command_name.upper()}")
    print("=" * 60)
    
    # Input info
    v = validation_results
    input_status = "✔" if v['input']['exists'] else "❌"
    msg = f"{input_status} Input: {v['input']['ply_count']} .ply file(s) found"
    print(msg)
    
    # Output info
    if 'writable' in v.get('output', {}):
        output_status = "✔" if v['output']['writable'] else "❌"
        exists_msg = " (exists)" if v['output']['exists'] else " (will be created)"
        print(f"{output_status} Output: {output_status == '✔' and 'Writable' or 'Not writable'}{exists_msg}")

    # Config info
    if v.get('config', {}).get('exists'):
        print("✔ Config: Loaded")
    elif 'config' in v:
        if v['config'].get('exists') is False:
             # Only print if config was actually requested (i.e. path was provided)
             pass 

    print("\n📋 PLANNED ACTIONS:")
    for action in planned_actions:
        print(f"   - {action}")

    print("\nℹ Dry run complete — no files were modified.")
    print("=" * 60)

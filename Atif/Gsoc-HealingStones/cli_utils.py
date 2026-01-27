import json
from datetime import datetime
import sys

def format_json_output(command, status, metadata=None, errors=None, warnings=None):
    """
    Format and print a deterministic JSON object for CLI output.
    
    Args:
        command (str): The CLI command executed (e.g., check-data, validate, dry-run).
        status (str): Outcome status (e.g., PASS, FAIL).
        metadata (dict, optional): Input metadata like paths, counts, etc.
        errors (list, optional): List of error messages.
        warnings (list, optional): List of warning messages.
    """
    output = {
        "command": command,
        "status": status,
        "input_metadata": metadata or {},
        "errors": errors or [],
        "warnings": warnings or [],
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    
    # Use sys.__stdout__ directly to ensure output even if sys.stdout is redirected
    json.dump(output, sys.__stdout__, indent=2, sort_keys=True)
    sys.__stdout__.write('\n')
    sys.__stdout__.flush()

def is_json_mode(args):
    """Check if JSON mode is enabled based on argparse arguments."""
    return getattr(args, 'json', False) or getattr(args, 'report', False)

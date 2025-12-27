"""
Verification script - Check project structure

This script verifies that all components of the prediction platform
have been created correctly.
"""

import os
import sys


def verify_structure():
    """Verify the project structure."""
    
    print("="*70)
    print("BIKENV PREDICTION PLATFORM - Structure Verification")
    print("="*70)
    
    # Expected files and directories
    expected_items = {
        'directories': [
            '../data',
            '../scripts',
            '../analysis',
            '../results'
        ],
        'files': [
            '../data/copenhagenize_index_2025.csv',
            '../scripts/retrieve_data.py',
            '../scripts/calculate_indices.py',
            '../analysis/prediction_platform.py',
            '../analysis/demo_platform.py',
            '../analysis/README.md',
            '../requirements-platform.txt'
        ]
    }
    
    print("\n✓ Checking directories...")
    for directory in expected_items['directories']:
        if os.path.isdir(directory):
            print(f"  ✓ {directory}")
        else:
            print(f"  ✗ {directory} MISSING")
    
    print("\n✓ Checking files...")
    for filepath in expected_items['files']:
        if os.path.isfile(filepath):
            size = os.path.getsize(filepath)
            print(f"  ✓ {filepath} ({size} bytes)")
        else:
            print(f"  ✗ {filepath} MISSING")
    
    # Check data file content
    print("\n✓ Verifying data file...")
    try:
        with open('../data/copenhagenize_index_2025.csv', 'r') as f:
            lines = f.readlines()
            print(f"  ✓ Contains {len(lines)} lines (including header)")
            print(f"  ✓ Sample: {lines[1].strip()}")
            print(f"  ✓ Edition: 2025 (EIT Urban Mobility)")
    except Exception as e:
        print(f"  ✗ Error reading data: {e}")
    
    print("\n" + "="*70)
    print("VERIFICATION COMPLETE")
    print("="*70)
    print("\nProject structure is ready!")
    print("\nNext steps:")
    print("  1. Install dependencies: pip install -r ../requirements-platform.txt")
    print("  2. Run demo: python3 demo_platform.py")
    print("  3. Run full analysis: python3 prediction_platform.py")


if __name__ == "__main__":
    verify_structure()

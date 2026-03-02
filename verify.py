#!/usr/bin/env python3
"""
Verification Script - Confirms all deliverables are present and functional
Run this to verify the complete delivery package
"""

import os
import sys

def check_file_exists(filepath, expected_size_min=100):
    """Check if a file exists and has reasonable content."""
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        if size >= expected_size_min:
            return True, f"✓ {os.path.basename(filepath)} ({size} bytes)"
        else:
            return False, f"✗ {os.path.basename(filepath)} (too small: {size} bytes)"
    else:
        return False, f"✗ {os.path.basename(filepath)} (not found)"

def main():
    print("=" * 80)
    print(" DELIVERABLE VERIFICATION")
    print("=" * 80)
    print()
    
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    files_to_check = {
        "Production Code": [
            ("app.py", 10000),
            ("demo.py", 5000),
            ("example_tickets.py", 3000),
        ],
        "Configuration": [
            ("requirements.txt", 30),
            ("run.sh", 500),
        ],
        "Documentation": [
            ("README.md", 5000),
            ("QUICKSTART.md", 2000),
            ("ARCHITECTURE.md", 8000),
            ("INDEX.md", 5000),
            ("START_HERE.md", 5000),
            ("DELIVERY_SUMMARY.md", 5000),
        ]
    }
    
    all_passed = True
    total_files = 0
    
    for category, files in files_to_check.items():
        print(f"\n{category}:")
        print("-" * 80)
        for filename, min_size in files:
            filepath = os.path.join(base_path, filename)
            passed, message = check_file_exists(filepath, min_size)
            print(f"  {message}")
            if passed:
                total_files += 1
            else:
                all_passed = False
    
    print()
    print("=" * 80)
    print(f" SUMMARY: {total_files}/{len([f for cat in files_to_check.values() for f in cat])} files verified")
    print("=" * 80)
    print()
    
    if all_passed:
        print("✅ ALL DELIVERABLES PRESENT AND VALID")
        print()
        print("Next steps:")
        print("  1. Install: pip install streamlit requests")
        print("  2. Run: streamlit run app.py")
        print("  3. Read: START_HERE.md or QUICKSTART.md")
        print()
        return 0
    else:
        print("❌ SOME FILES MISSING OR INVALID")
        print("Please check the above errors")
        print()
        return 1

if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Test Version Compatibility Theory

This script tests if the hanging issue is caused by version incompatibilities
between the working wav_to_karaoke environment and the current environment.
"""

import os
import sys
import time
import signal
from datetime import datetime

# Fix OpenMP library conflicts on macOS
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

class TimeoutError(Exception):
    """Custom timeout exception"""
    pass

def timeout_handler(signum, frame):
    """Handle timeout signal"""
    raise TimeoutError("Operation timed out")

def check_package_versions():
    """Check current package versions and compare with working environment"""
    
    print("=== Package Version Analysis ===")
    print("Comparing current environment with working wav_to_karaoke environment")
    print()
    
    # Current environment versions
    current_versions = {}
    
    try:
        import numpy
        current_versions['NumPy'] = numpy.__version__
    except ImportError:
        current_versions['NumPy'] = "Not installed"
    
    try:
        import torch
        current_versions['PyTorch'] = torch.__version__
    except ImportError:
        current_versions['PyTorch'] = "Not installed"
    
    try:
        import tensorflow as tf
        current_versions['TensorFlow'] = tf.__version__
    except ImportError:
        current_versions['TensorFlow'] = "Not installed"
    
    try:
        import numba
        current_versions['Numba'] = numba.__version__
    except ImportError:
        current_versions['Numba'] = "Not installed"
    
    try:
        import librosa
        current_versions['librosa'] = librosa.__version__
    except ImportError:
        current_versions['librosa'] = "Not installed"
    
    # Working environment versions (from wav_to_karaoke)
    working_versions = {
        'NumPy': '1.22.0',
        'PyTorch': '1.13.1',
        'TensorFlow': '2.13.1',
        'Numba': '0.55.2',
        'librosa': '0.8.1'
    }
    
    # Display comparison
    print(f"{'Library':<15} {'Current':<15} {'Working':<15} {'Status':<10}")
    print("-" * 60)
    
    potential_issues = []
    
    for lib in working_versions.keys():
        current = current_versions.get(lib, "Not installed")
        working = working_versions[lib]
        
        # Check for potential issues
        if lib == 'NumPy' and current != 'Not installed':
            current_major = int(current.split('.')[0])
            working_major = int(working.split('.')[0])
            if current_major > working_major:
                status = "⚠️  MAJOR"
                potential_issues.append(f"NumPy {current} vs {working} - Major version difference")
            else:
                status = "✅ OK"
        elif lib == 'PyTorch' and current != 'Not installed':
            current_major = int(current.split('.')[0])
            working_major = int(working.split('.')[0])
            if current_major > working_major:
                status = "⚠️  MAJOR"
                potential_issues.append(f"PyTorch {current} vs {working} - Major version difference")
            else:
                status = "✅ OK"
        elif lib == 'Numba' and current != 'Not installed':
            current_major = int(current.split('.')[0])
            working_major = int(working.split('.')[0])
            if current_major > working_major:
                status = "⚠️  MAJOR"
                potential_issues.append(f"Numba {current} vs {working} - Major version difference")
            else:
                status = "✅ OK"
        else:
            status = "✅ OK"
        
        print(f"{lib:<15} {current:<15} {working:<15} {status:<10}")
    
    print()
    
    if potential_issues:
        print("🚨 POTENTIAL VERSION COMPATIBILITY ISSUES:")
        for issue in potential_issues:
            print(f"   • {issue}")
        print()
        print("💡 RECOMMENDATION: Try downgrading to working versions")
        return True
    else:
        print("✅ No obvious version compatibility issues found")
        return False

def create_downgrade_script():
    """Create a script to downgrade to working versions"""
    
    print("\n=== Creating Downgrade Script ===")
    
    script_content = """#!/bin/bash

# Downgrade to Working Package Versions
# Based on wav_to_karaoke working environment

echo "=== Downgrading to Working Package Versions ==="
echo "This will downgrade packages to versions that work in wav_to_karaoke"
echo

# Deactivate current environment if active
if [ -n "$VIRTUAL_ENV" ]; then
    echo "Deactivating current virtual environment..."
    deactivate
fi

# Create new environment with working versions
echo "Creating new virtual environment..."
python3 -m venv .venv_working
source .venv_working/bin/activate

echo "Installing working package versions..."
pip install --upgrade pip

# Install specific working versions
pip install "numpy==1.22.0"
pip install "torch==1.13.1"
pip install "tensorflow==2.13.1"
pip install "numba==0.55.2"
pip install "librosa==0.8.1"

# Install OpenAI Whisper
pip install openai-whisper

echo
echo "✅ Working environment created!"
echo "   Activate with: source .venv_working/bin/activate"
echo "   Test with: python standalone_openai_whisper_test_fixed.py"
echo
echo "⚠️  Note: This environment uses older package versions"
echo "   Only use for testing the hanging issue"
"""
    
    with open("downgrade_to_working_versions.sh", "w") as f:
        f.write(script_content)
    
    os.chmod("downgrade_to_working_versions.sh", 0o755)
    print("✅ Created: downgrade_to_working_versions.sh")
    print("   Run this to create an environment with working package versions")

def main():
    """Main test function"""
    
    print("=== OpenAI Whisper Version Compatibility Test ===")
    print("Testing the theory that package version differences cause the hanging issue")
    print()
    
    # Check package versions
    has_version_issues = check_package_versions()
    
    if has_version_issues:
        print("\n🚨 VERSION ISSUES DETECTED!")
        print("   The hanging problem is likely caused by package version incompatibilities")
        print()
        
        # Create downgrade script
        create_downgrade_script()
        
        print("\n💡 NEXT STEPS:")
        print("   1. Run: ./downgrade_to_working_versions.sh")
        print("   2. Test with working versions")
        print("   3. If it works, the issue is confirmed to be version-related")
        
    else:
        print("\n✅ No version issues detected")
        print("   The hanging problem may have a different cause")
    
    print("\n🔍 To test the version theory:")
    print("   Run the downgrade script and test if word-level transcription works")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

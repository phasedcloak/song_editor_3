#!/bin/bash

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

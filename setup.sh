#!/bin/bash

# Setup script for OpenAI Whisper Debug Project

echo "=== Setting up OpenAI Whisper Debug Environment ==="

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install requirements
pip install -r requirements.txt

echo "✅ Environment setup complete!"
echo "Run: source .venv/bin/activate"
echo "Then test with: python standalone_openai_whisper_test_fixed.py"

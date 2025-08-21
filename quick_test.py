#!/usr/bin/env python3
"""
Quick test to verify OpenAI Whisper installation
"""

import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

try:
    import whisper
    print("✅ OpenAI Whisper imported successfully")
    print(f"   Version: {whisper.__version__}")
    
    # Test model loading
    print("\n🔧 Testing model loading...")
    model = whisper.load_model("tiny")
    print("✅ Model loaded successfully")
    
    print("\n🎯 OpenAI Whisper is working! Ready for debugging.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

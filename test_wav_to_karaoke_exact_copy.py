#!/usr/bin/env python3
"""
Exact Copy of Working wav_to_karaoke OpenAI Whisper Implementation

This test uses the exact same code and parameters that work in wav_to_karaoke
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

def test_wav_to_karaoke_exact_copy():
    """Test using the exact working implementation from wav_to_karaoke"""
    
    print("=== Testing Exact wav_to_karaoke OpenAI Whisper Implementation ===")
    print("This uses the exact same code that works in wav_to_karaoke")
    print()
    
    try:
        # Step 1: Import whisper (exactly like wav_to_karaoke)
        print("1. Importing OpenAI Whisper...")
        import whisper
        print("✅ OpenAI Whisper imported successfully")
        
        # Step 2: Load model with exact same parameters
        print("\n2. Loading model (exactly like wav_to_karaoke)...")
        start_time = time.time()
        model = whisper.load_model("large-v2")  # EXACTLY like wav_to_karaoke
        load_time = time.time() - start_time
        print(f"✅ Model loaded successfully in {load_time:.2f}s")
        print(f"   Model: large-v2 (exactly like wav_to_karaoke)")
        
        # Step 3: Load audio file
        print("\n3. Loading audio file...")
        audio_file = "25-03-12 we see your love - 02.wav"
        
        if not os.path.exists(audio_file):
            print(f"❌ Audio file not found: {audio_file}")
            return False
        
        print(f"✅ Audio file: {audio_file}")
        
        # Step 4: Transcribe with EXACT same parameters as wav_to_karaoke
        print("\n4. Testing transcription with EXACT wav_to_karaoke parameters...")
        print("   Parameters:")
        print("   - language='en'")
        print("   - word_timestamps=True")
        print("   - beam_size=5")
        print("   - best_of=5")
        print("   - temperature=0.0")
        print()
        
        # Set timeout for word-level transcription
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(300)  # 5 minutes timeout (longer for large-v2 model)
        
        try:
            transcribe_start = datetime.now()
            
            # EXACT same transcription call as wav_to_karaoke
            result = model.transcribe(
                audio_file,
                language="en",
                word_timestamps=True,
                beam_size=5,  # Use beam search
                best_of=5,  # Generate multiple candidates
                temperature=0.0  # Deterministic for consistent alternatives
            )
            
            signal.alarm(0)  # Cancel timeout
            
            transcribe_time = (datetime.now() - transcribe_start).total_seconds()
            print(f"✅ Transcription completed in {transcribe_time:.2f}s")
            
            # Debug: Log the result structure (exactly like wav_to_karaoke)
            print(f"\n5. Result analysis (exactly like wav_to_karaoke)...")
            print(f"   Result keys: {list(result.keys())}")
            
            if 'segments' in result:
                print(f"   Number of segments: {len(result['segments'])}")
                if result['segments']:
                    first_segment = result['segments'][0]
                    print(f"   First segment keys: {list(first_segment.keys())}")
                    if 'words' in first_segment and first_segment['words']:
                        first_word = first_segment['words'][0]
                        print(f"   First word keys: {list(first_word.keys())}")
                        print(f"   First word attributes: {dir(first_word)}")
            
            # Extract words with their timestamps (exactly like wav_to_karaoke)
            print(f"\n6. Extracting word timestamps...")
            lyrics = []
            for segment in result['segments']:
                if 'words' in segment:
                    for word in segment['words']:
                        lyrics.append({
                            'word': word['word'],
                            'start': word['start'],
                            'end': word['end'],
                            'confidence': word.get('probability', 1.0)
                        })
            
            print(f"✅ Extracted {len(lyrics)} words with timestamps")
            
            if lyrics:
                print("   Sample words:")
                for i, lyric in enumerate(lyrics[:5]):
                    print(f"     {i+1}. '{lyric['word']}' at {lyric['start']:.2f}s - {lyric['end']:.2f}s")
                if len(lyrics) > 5:
                    print(f"     ... and {len(lyrics) - 5} more words")
            
            total_time = (datetime.now() - start_time).total_seconds()
            print(f"\n🎯 Total processing time: {total_time:.2f}s")
            print("✅ SUCCESS: Word-level transcription worked exactly like wav_to_karaoke!")
            
            return True
            
        except TimeoutError:
            signal.alarm(0)
            print("❌ Transcription timed out after 5 minutes")
            print("   This suggests the issue is not with the parameters")
            return False
        except Exception as e:
            signal.alarm(0)
            print(f"❌ Transcription failed: {e}")
            import traceback
            traceback.print_exc()
            return False
            
    except Exception as e:
        print(f"\n❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    try:
        success = test_wav_to_karaoke_exact_copy()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

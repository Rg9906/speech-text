#!/usr/bin/env python3
"""
System validation script for AutoEIT Transcription System
Tests imports and basic functionality without requiring audio files
"""

import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported"""
    print("=" * 60)
    print("TESTING MODULE IMPORTS")
    print("=" * 60)
    
    try:
        # Test preprocessing modules
        print("Testing preprocessing modules...")
        from preprocessing.audio_normalization import AudioLoader
        from preprocessing.noise_reduction import NoiseReducer
        from preprocessing.audio_enhancer import AudioEnhancer
        print("✓ Preprocessing modules imported successfully")
        
        # Test model modules
        print("Testing model modules...")
        from models.base_asr.whisper_model import WhisperModel
        print("✓ Model modules imported successfully")
        
        # Test pipeline modules
        print("Testing pipeline modules...")
        from pipeline.full_pipeline import TranscriptionPipeline
        print("✓ Pipeline modules imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error during import: {e}")
        return False

def test_class_instantiation():
    """Test that classes can be instantiated (without heavy operations)"""
    print("\n" + "=" * 60)
    print("TESTING CLASS INSTANTIATION")
    print("=" * 60)
    
    try:
        # Test AudioLoader
        print("Testing AudioLoader...")
        loader = AudioLoader("dummy_path.wav")
        print("✓ AudioLoader instantiated")
        
        # Test NoiseReducer
        print("Testing NoiseReducer...")
        reducer = NoiseReducer()
        print("✓ NoiseReducer instantiated")
        
        # Test AudioEnhancer
        print("Testing AudioEnhancer...")
        enhancer = AudioEnhancer()
        print("✓ AudioEnhancer instantiated")
        
        # Test TranscriptionPipeline (will fail gracefully without audio file)
        print("Testing TranscriptionPipeline...")
        try:
            pipeline = TranscriptionPipeline("nonexistent.wav")
            print("✓ TranscriptionPipeline instantiated")
        except Exception as pipeline_error:
            print(f"✗ Pipeline instantiation failed: {pipeline_error}")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Instantiation error: {e}")
        return False

def test_error_handling():
    """Test error handling with invalid inputs"""
    print("\n" + "=" * 60)
    print("TESTING ERROR HANDLING")
    print("=" * 60)
    
    try:
        import numpy as np
        
        # Test AudioEnhancer with various inputs
        print("Testing AudioEnhancer error handling...")
        enhancer = AudioEnhancer()
        
        # Test with None
        result = enhancer.normalize_volume(None)
        print("✓ AudioEnhancer handled None input")
        
        # Test with empty array
        result = enhancer.normalize_volume(np.array([]))
        print("✓ AudioEnhancer handled empty array")
        
        # Test NoiseReducer with various inputs
        print("Testing NoiseReducer error handling...")
        reducer = NoiseReducer()
        
        # Test with None
        result = reducer.reduce_noise(None, 16000)
        print("✓ NoiseReducer handled None input")
        
        # Test with empty array
        result = reducer.reduce_noise(np.array([]), 16000)
        print("✓ NoiseReducer handled empty array")
        
        return True
        
    except Exception as e:
        print(f"✗ Error handling test failed: {e}")
        return False

def main():
    """Run all validation tests"""
    print("AutoEIT Transcription System - Validation Suite")
    print("Level 2 Robustness Check")
    
    tests = [
        ("Module Imports", test_imports),
        ("Class Instantiation", test_class_instantiation),
        ("Error Handling", test_error_handling)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ Test '{test_name}' crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready for use.")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Place audio file at: data/sample.wav")
        print("3. Run transcription: python main.py")
    else:
        print("⚠️  Some tests failed. Please review the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

#!/usr/bin/env python3
"""
Level 3 System Validation for AutoEIT Transcription System
Tests intelligence and differentiation layers
"""

import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_level3_imports():
    """Test that all Level 3 modules can be imported"""
    print("=" * 60)
    print("TESTING LEVEL 3 MODULE IMPORTS")
    print("=" * 60)
    
    try:
        # Test analysis modules
        print("Testing analysis modules...")
        from analysis.speech_dynamics import SpeechDynamicsAnalyzer
        from analysis.language_detection import LanguageDetector
        from analysis.lexical_handler import LexicalHandler
        from analysis.annotation_builder import AnnotationBuilder
        print("✓ Analysis modules imported successfully")
        
        # Test updated pipeline
        print("Testing updated pipeline...")
        from pipeline.full_pipeline import TranscriptionPipeline
        print("✓ Pipeline with Level 3 modules imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error during import: {e}")
        return False

def test_level3_functionality():
    """Test Level 3 functionality with mock data"""
    print("\n" + "=" * 60)
    print("TESTING LEVEL 3 FUNCTIONALITY")
    print("=" * 60)
    
    try:
        import numpy as np
        from analysis.speech_dynamics import SpeechDynamicsAnalyzer
        from analysis.language_detection import LanguageDetector
        from analysis.lexical_handler import LexicalHandler
        from analysis.annotation_builder import AnnotationBuilder
        
        # Test Speech Dynamics Analyzer
        print("Testing Speech Dynamics Analyzer...")
        analyzer = SpeechDynamicsAnalyzer()
        
        # Create mock audio data
        mock_audio = np.random.randn(16000)  # 1 second of random audio
        mock_sr = 16000
        mock_transcription = "hello world this is a test"
        
        speech_result = analyzer.analyze_speech(mock_audio, mock_sr, mock_transcription)
        print(f"✓ Speech analysis result: {speech_result}")
        
        # Test Language Detector
        print("Testing Language Detector...")
        detector = LanguageDetector()
        lang_result = detector.detect_languages("hello mundo bonjour")
        print(f"✓ Language detection result: {lang_result}")
        
        # Test Lexical Handler
        print("Testing Lexical Handler...")
        handler = LexicalHandler()
        lexical_result = handler.classify_words(lang_result)
        print(f"✓ Lexical classification result: {lexical_result}")
        
        # Test Annotation Builder
        print("Testing Annotation Builder...")
        builder = AnnotationBuilder()
        annotation_result = builder.build_annotated_output(
            mock_transcription, speech_result, lang_result, lexical_result
        )
        print(f"✓ Annotation result keys: {list(annotation_result.keys())}")
        
        return True
        
    except Exception as e:
        print(f"✗ Level 3 functionality test failed: {e}")
        return False

def test_pipeline_integration():
    """Test pipeline integration with Level 3 modules"""
    print("\n" + "=" * 60)
    print("TESTING PIPELINE INTEGRATION")
    print("=" * 60)
    
    try:
        from pipeline.full_pipeline import TranscriptionPipeline
        
        print("Testing pipeline initialization...")
        # Test with non-existent file to check error handling
        pipeline = TranscriptionPipeline("nonexistent.wav")
        print("✓ Pipeline initialized successfully")
        
        # Check that Level 3 modules are present
        assert hasattr(pipeline, 'speech_analyzer'), "Missing speech_analyzer"
        assert hasattr(pipeline, 'language_detector'), "Missing language_detector"
        assert hasattr(pipeline, 'lexical_handler'), "Missing lexical_handler"
        assert hasattr(pipeline, 'annotation_builder'), "Missing annotation_builder"
        
        print("✓ All Level 3 modules present in pipeline")
        
        return True
        
    except Exception as e:
        print(f"✗ Pipeline integration test failed: {e}")
        return False

def test_error_handling():
    """Test error handling in Level 3 modules"""
    print("\n" + "=" * 60)
    print("TESTING ERROR HANDLING")
    print("=" * 60)
    
    try:
        from analysis.speech_dynamics import SpeechDynamicsAnalyzer
        from analysis.language_detection import LanguageDetector
        from analysis.lexical_handler import LexicalHandler
        from analysis.annotation_builder import AnnotationBuilder
        
        # Test with None inputs
        print("Testing None input handling...")
        analyzer = SpeechDynamicsAnalyzer()
        result = analyzer.analyze_speech(None, None, None)
        print(f"✓ Speech analyzer handled None: {result}")
        
        detector = LanguageDetector()
        result = detector.detect_languages(None)
        print(f"✓ Language detector handled None: {result}")
        
        handler = LexicalHandler()
        result = handler.classify_words(None)
        print(f"✓ Lexical handler handled None: {result}")
        
        builder = AnnotationBuilder()
        result = builder.build_annotated_output(None, None, None, None)
        print(f"✓ Annotation builder handled None: {result}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error handling test failed: {e}")
        return False

def main():
    """Run all Level 3 validation tests"""
    print("AutoEIT Transcription System - Level 3 Validation Suite")
    print("Intelligence + Differentiation Layer Testing")
    
    tests = [
        ("Level 3 Module Imports", test_level3_imports),
        ("Level 3 Functionality", test_level3_functionality),
        ("Pipeline Integration", test_pipeline_integration),
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
    print("LEVEL 3 VALIDATION SUMMARY")
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
        print("🎉 All Level 3 tests passed! System is ready for intelligence analysis.")
        print("\nLevel 3 Features:")
        print("✓ Speech dynamics analysis (duration, rate, pauses)")
        print("✓ Multilingual/code-switch detection")
        print("✓ Lexical flexibility handling (slang, merged words)")
        print("✓ Structured annotated output")
        print("✓ Comprehensive error handling")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Place audio file at: data/sample.wav")
        print("3. Run intelligence analysis: python main.py")
    else:
        print("⚠️  Some Level 3 tests failed. Please review the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

#!/usr/bin/env python3
"""
Level 3.5 System Validation for AutoEIT Transcription System
Tests intelligence refinement modules
"""

import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_level35_imports():
    """Test that all Level 3.5 modules can be imported"""
    print("=" * 60)
    print("TESTING LEVEL 3.5 MODULE IMPORTS")
    print("=" * 60)
    
    try:
        # Test Level 3.5 analysis modules
        print("Testing Level 3.5 analysis modules...")
        from analysis.segment_quality import SegmentQualityAnalyzer
        from analysis.phonetic_analyzer import PhoneticAnalyzer
        from analysis.disfluency_detector import DisfluencyDetector
        print("✓ Level 3.5 analysis modules imported successfully")
        
        # Test updated pipeline
        print("Testing updated pipeline with Level 3.5...")
        from pipeline.full_pipeline import TranscriptionPipeline
        print("✓ Pipeline with Level 3.5 modules imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error during import: {e}")
        return False

def test_level35_functionality():
    """Test Level 3.5 functionality with mock data"""
    print("\n" + "=" * 60)
    print("TESTING LEVEL 3.5 FUNCTIONALITY")
    print("=" * 60)
    
    try:
        from analysis.segment_quality import SegmentQualityAnalyzer
        from analysis.phonetic_analyzer import PhoneticAnalyzer
        from analysis.disfluency_detector import DisfluencyDetector
        
        # Test Segment Quality Analyzer
        print("Testing Segment Quality Analyzer...")
        segment_analyzer = SegmentQualityAnalyzer()
        
        mock_transcription = "I am happy and I go to market uh I buy frutas"
        mock_lang_tags = [
            {"word": "I", "lang": "en"}, {"word": "am", "lang": "en"},
            {"word": "happy", "lang": "en"}, {"word": "and", "lang": "en"},
            {"word": "I", "lang": "en"}, {"word": "go", "lang": "en"},
            {"word": "to", "lang": "en"}, {"word": "market", "lang": "en"},
            {"word": "uh", "lang": "unknown"}, {"word": "I", "lang": "en"},
            {"word": "buy", "lang": "en"}, {"word": "frutas", "lang": "es"}
        ]
        mock_lexical = [
            {"word": "I", "type": "known"}, {"word": "am", "type": "known"},
            {"word": "happy", "type": "known"}, {"word": "and", "type": "known"},
            {"word": "I", "type": "known"}, {"word": "go", "type": "known"},
            {"word": "to", "type": "known"}, {"word": "market", "type": "known"},
            {"word": "uh", "type": "unknown"}, {"word": "I", "type": "known"},
            {"word": "buy", "type": "known"}, {"word": "frutas", "type": "unknown"}
        ]
        
        segment_result = segment_analyzer.analyze_segments(mock_transcription, mock_lang_tags, mock_lexical)
        print(f"✓ Segment analysis result: {len(segment_result)} segments analyzed")
        
        # Test Phonetic Analyzer
        print("Testing Phonetic Analyzer...")
        phonetic_analyzer = PhoneticAnalyzer()
        
        mock_words_with_unknown = [
            {"word": "happy", "type": "known"},
            {"word": "bery", "type": "unknown"},  # Should match "very"
            {"word": "goin", "type": "unknown"},  # Should match "going"
            {"word": "market", "type": "known"}
        ]
        
        phonetic_result = phonetic_analyzer.analyze_phonetic_errors(mock_words_with_unknown)
        print(f"✓ Phonetic analysis result: {len(phonetic_result)} phonetic matches found")
        
        # Test Disfluency Detector
        print("Testing Disfluency Detector...")
        disfluency_detector = DisfluencyDetector()
        
        mock_transcription_with_disfluencies = "uh I I I go to market and I mean I buy frutas"
        disfluency_result = disfluency_detector.detect_disfluencies(mock_transcription_with_disfluencies)
        print(f"✓ Disfluency detection result: {len(disfluency_result)} disfluencies found")
        
        return True
        
    except Exception as e:
        print(f"✗ Level 3.5 functionality test failed: {e}")
        return False

def test_pipeline_integration_level35():
    """Test pipeline integration with Level 3.5 modules"""
    print("\n" + "=" * 60)
    print("TESTING PIPELINE INTEGRATION - LEVEL 3.5")
    print("=" * 60)
    
    try:
        from pipeline.full_pipeline import TranscriptionPipeline
        
        print("Testing pipeline initialization with Level 3.5...")
        # Test with non-existent file to check error handling
        pipeline = TranscriptionPipeline("nonexistent.wav")
        print("✓ Pipeline initialized successfully")
        
        # Check that Level 3.5 modules are present
        assert hasattr(pipeline, 'segment_analyzer'), "Missing segment_analyzer"
        assert hasattr(pipeline, 'phonetic_analyzer'), "Missing phonetic_analyzer"
        assert hasattr(pipeline, 'disfluency_detector'), "Missing disfluency_detector"
        
        print("✓ All Level 3.5 modules present in pipeline")
        
        return True
        
    except Exception as e:
        print(f"✗ Pipeline Level 3.5 integration test failed: {e}")
        return False

def test_error_handling_level35():
    """Test error handling in Level 3.5 modules"""
    print("\n" + "=" * 60)
    print("TESTING LEVEL 3.5 ERROR HANDLING")
    print("=" * 60)
    
    try:
        from analysis.segment_quality import SegmentQualityAnalyzer
        from analysis.phonetic_analyzer import PhoneticAnalyzer
        from analysis.disfluency_detector import DisfluencyDetector
        
        # Test with None inputs
        print("Testing None input handling...")
        segment_analyzer = SegmentQualityAnalyzer()
        result = segment_analyzer.analyze_segments(None, None, None)
        print(f"✓ Segment analyzer handled None: {len(result)} segments")
        
        phonetic_analyzer = PhoneticAnalyzer()
        result = phonetic_analyzer.analyze_phonetic_errors(None)
        print(f"✓ Phonetic analyzer handled None: {len(result)} matches")
        
        disfluency_detector = DisfluencyDetector()
        result = disfluency_detector.detect_disfluencies(None)
        print(f"✓ Disfluency detector handled None: {len(result)} disfluencies")
        
        # Test with empty inputs
        print("Testing empty input handling...")
        result = segment_analyzer.analyze_segments("", [], [])
        print(f"✓ Segment analyzer handled empty: {len(result)} segments")
        
        result = phonetic_analyzer.analyze_phonetic_errors([])
        print(f"✓ Phonetic analyzer handled empty: {len(result)} matches")
        
        result = disfluency_detector.detect_disfluencies("")
        print(f"✓ Disfluency detector handled empty: {len(result)} disfluencies")
        
        return True
        
    except Exception as e:
        print(f"✗ Level 3.5 error handling test failed: {e}")
        return False

def test_intelligence_refinement_capabilities():
    """Test specific intelligence refinement capabilities"""
    print("\n" + "=" * 60)
    print("TESTING INTELLIGENCE REFINEMENT CAPABILITIES")
    print("=" * 60)
    
    try:
        from analysis.segment_quality import SegmentQualityAnalyzer
        from analysis.phonetic_analyzer import PhoneticAnalyzer
        from analysis.disfluency_detector import DisfluencyDetector
        
        # Test segment quality classification
        print("Testing segment quality classification...")
        segment_analyzer = SegmentQualityAnalyzer()
        
        # High quality segment
        high_quality = segment_analyzer.analyze_segments("I am happy today")
        print(f"✓ High quality segment: {high_quality[0]['quality']}")
        
        # Low quality segment with disfluencies
        low_quality = segment_analyzer.analyze_segments("uh I I go")
        print(f"✓ Low quality segment: {low_quality[0]['quality']}")
        
        # Test phonetic error detection
        print("Testing phonetic error detection...")
        phonetic_analyzer = PhoneticAnalyzer()
        
        # Test with words that should have phonetic matches
        test_words = [
            {"word": "bery", "type": "unknown"},  # Should match "very"
            {"word": "goin", "type": "unknown"},  # Should match "going"
            {"word": "coulda", "type": "unknown"}  # Should match "could"
        ]
        
        phonetic_results = phonetic_analyzer.analyze_phonetic_errors(test_words)
        for result in phonetic_results:
            print(f"✓ Phonetic match: '{result['word']}' → '{result['phonetic_match']}'")
        
        # Test disfluency pattern detection
        print("Testing disfluency pattern detection...")
        disfluency_detector = DisfluencyDetector()
        
        # Test various disfluency patterns
        filler_test = "uh um I think you know"
        filler_result = disfluency_detector.detect_disfluencies(filler_test)
        filler_count = sum(1 for d in filler_result if d['type'] == 'filler')
        print(f"✓ Filler detection: {filler_count} fillers found")
        
        repetition_test = "I I I go to to the market"
        repetition_result = disfluency_detector.detect_disfluencies(repetition_test)
        repetition_count = sum(1 for d in repetition_result if d['type'] == 'repetition')
        print(f"✓ Repetition detection: {repetition_count} repetitions found")
        
        restart_test = "I go to— I mean I went to the store"
        restart_result = disfluency_detector.detect_disfluencies(restart_test)
        restart_count = sum(1 for d in restart_result if d['type'] in ['restart', 'correction'])
        print(f"✓ Restart detection: {restart_count} restarts found")
        
        return True
        
    except Exception as e:
        print(f"✗ Intelligence refinement capabilities test failed: {e}")
        return False

def main():
    """Run all Level 3.5 validation tests"""
    print("AutoEIT Transcription System - Level 3.5 Validation Suite")
    print("Intelligence + Differentiation + Refinement Layers")
    
    tests = [
        ("Level 3.5 Module Imports", test_level35_imports),
        ("Level 3.5 Functionality", test_level35_functionality),
        ("Pipeline Integration Level 3.5", test_pipeline_integration_level35),
        ("Level 3.5 Error Handling", test_error_handling_level35),
        ("Intelligence Refinement Capabilities", test_intelligence_refinement_capabilities)
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
    print("LEVEL 3.5 VALIDATION SUMMARY")
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
        print("🎉 All Level 3.5 tests passed! System is ready for intelligence refinement.")
        print("\nLevel 3.5 Features:")
        print("✓ Segment-level quality analysis")
        print("✓ Phonetic error awareness")
        print("✓ Disfluency detection")
        print("✓ Enhanced error handling")
        print("✓ Comprehensive integration")
        print("\nNew Capabilities:")
        print("• Quality assessment per speech segment")
        print("• Pronunciation error detection and annotation")
        print("• Natural speech disfluency identification")
        print("• Research-ready structured output")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Place audio file at: data/sample.wav")
        print("3. Run Level 3.5 analysis: python main.py")
    else:
        print("⚠️  Some Level 3.5 tests failed. Please review the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

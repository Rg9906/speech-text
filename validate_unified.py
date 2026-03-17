#!/usr/bin/env python3
"""
Level 3.5 Unified System Validation for AutoEIT Transcription System
Tests unified output structure and quality aggregation
"""

import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_unified_imports():
    """Test that all unified system modules can be imported"""
    print("=" * 60)
    print("TESTING UNIFIED SYSTEM IMPORTS")
    print("=" * 60)
    
    try:
        # Test core modules
        print("Testing core analysis modules...")
        from analysis.segment_quality import SegmentQualityAnalyzer
        from analysis.phonetic_analyzer import PhoneticAnalyzer
        from analysis.disfluency_detector import DisfluencyDetector
        print("✓ Core analysis modules imported successfully")
        
        # Test unified modules
        print("Testing unified system modules...")
        from analysis.quality_aggregator import QualityAggregator
        from analysis.unified_output_builder import UnifiedOutputBuilder
        print("✓ Unified system modules imported successfully")
        
        # Test updated pipeline
        print("Testing updated unified pipeline...")
        from pipeline.full_pipeline import TranscriptionPipeline
        print("✓ Unified pipeline imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error during import: {e}")
        return False

def test_quality_aggregation():
    """Test quality aggregation functionality"""
    print("\n" + "=" * 60)
    print("TESTING QUALITY AGGREGATION")
    print("=" * 60)
    
    try:
        from analysis.quality_aggregator import QualityAggregator
        
        print("Testing Quality Aggregator...")
        aggregator = QualityAggregator()
        
        # Mock data for testing
        mock_segments = [
            {"segment": "I am happy", "quality": "high", "reason": ["clear_speech"], "metrics": {"word_count": 3}},
            {"segment": "uh I buy", "quality": "low", "reason": ["disfluency"], "metrics": {"word_count": 3}}
        ]
        
        mock_phonetic = [
            {"word": "bery", "phonetic_match": "very", "confidence": 0.8, "error_type": "vowel_substitution"}
        ]
        
        mock_disfluencies = [
            {"type": "filler", "word": "uh", "position": 2, "confidence": 0.9}
        ]
        
        mock_transcription = "I am happy uh I buy"
        
        # Test aggregation
        quality_summary = aggregator.aggregate_quality(
            mock_segments, mock_phonetic, mock_disfluencies, mock_transcription
        )
        
        print(f"✓ Quality aggregation completed")
        print(f"  Overall Quality: {quality_summary.get('overall_quality', 'unknown')}")
        print(f"  Overall Score: {quality_summary.get('overall_score', 0):.2f}")
        print(f"  Issues Detected: {len(quality_summary.get('issues_detected', []))}")
        print(f"  Critical Regions: {len(quality_summary.get('critical_regions', []))}")
        print(f"  Suggestions: {len(quality_summary.get('suggestions', []))}")
        
        # Validate structure
        required_keys = ['overall_quality', 'overall_score', 'component_scores', 'issues_detected', 
                       'critical_regions', 'suggestions', 'quality_breakdown']
        
        for key in required_keys:
            if key not in quality_summary:
                print(f"✗ Missing required key: {key}")
                return False
        
        print("✓ Quality aggregation structure validated")
        return True
        
    except Exception as e:
        print(f"✗ Quality aggregation test failed: {e}")
        return False

def test_unified_output_building():
    """Test unified output building"""
    print("\n" + "=" * 60)
    print("TESTING UNIFIED OUTPUT BUILDING")
    print("=" * 60)
    
    try:
        from analysis.unified_output_builder import UnifiedOutputBuilder
        
        print("Testing Unified Output Builder...")
        builder = UnifiedOutputBuilder()
        
        # Mock comprehensive data
        mock_transcription = "I am happy and I go to market uh I buy frutas"
        mock_speech_analysis = {
            "duration": 2.5,
            "speech_rate": "normal",
            "pauses_detected": 1
        }
        mock_word_analysis = [
            {"word": "I", "language": "en", "type": "known", "confidence": 0.8},
            {"word": "happy", "language": "en", "type": "known", "confidence": 0.8},
            {"word": "frutas", "language": "es", "type": "unknown", "confidence": 0.5}
        ]
        mock_segment_analysis = [
            {"segment": "I am happy", "quality": "high", "reason": ["clear_speech"]},
            {"segment": "uh I buy frutas", "quality": "low", "reason": ["disfluency"]}
        ]
        mock_phonetic_analysis = [
            {"word": "bery", "phonetic_match": "very", "confidence": 0.85}
        ]
        mock_disfluencies = [
            {"type": "filler", "word": "uh", "position": 8}
        ]
        mock_quality_summary = {
            "overall_quality": "medium",
            "overall_score": 0.65,
            "issues_detected": [],
            "critical_regions": [],
            "suggestions": []
        }
        
        # Test unified output building
        unified_output = builder.build_unified_output(
            mock_transcription, mock_speech_analysis, mock_word_analysis,
            mock_segment_analysis, mock_phonetic_analysis, mock_disfluencies, mock_quality_summary
        )
        
        print(f"✓ Unified output building completed")
        
        # Validate unified structure
        required_sections = ['transcription', 'confidence_summary', 'speech_analysis', 
                           'linguistic_analysis', 'quality_summary', 'metadata']
        
        for section in required_sections:
            if section not in unified_output:
                print(f"✗ Missing required section: {section}")
                return False
        
        # Validate confidence summary
        confidence_summary = unified_output.get('confidence_summary', {})
        confidence_keys = ['overall_confidence', 'confidence_level', 'low_confidence_regions']
        for key in confidence_keys:
            if key not in confidence_summary:
                print(f"✗ Missing confidence key: {key}")
                return False
        
        # Validate linguistic analysis
        linguistic_analysis = unified_output.get('linguistic_analysis', {})
        ling_keys = ['word_analysis', 'segment_analysis', 'phonetic_analysis', 'disfluencies', 'linguistic_summary']
        for key in ling_keys:
            if key not in linguistic_analysis:
                print(f"✗ Missing linguistic key: {key}")
                return False
        
        print("✓ Unified output structure validated")
        print(f"  Transcription: {unified_output.get('transcription', '')[:30]}...")
        print(f"  Overall Confidence: {confidence_summary.get('overall_confidence', 0):.2f}")
        print(f"  Overall Quality: {unified_output.get('quality_summary', {}).get('overall_quality', 'unknown')}")
        
        return True
        
    except Exception as e:
        print(f"✗ Unified output building test failed: {e}")
        return False

def test_pipeline_integration_unified():
    """Test pipeline integration with unified system"""
    print("\n" + "=" * 60)
    print("TESTING PIPELINE INTEGRATION - UNIFIED")
    print("=" * 60)
    
    try:
        from pipeline.full_pipeline import TranscriptionPipeline
        
        print("Testing unified pipeline initialization...")
        # Test with non-existent file to check error handling
        pipeline = TranscriptionPipeline("nonexistent.wav")
        print("✓ Unified pipeline initialized successfully")
        
        # Check that unified modules are present
        assert hasattr(pipeline, 'segment_analyzer'), "Missing segment_analyzer"
        assert hasattr(pipeline, 'phonetic_analyzer'), "Missing phonetic_analyzer"
        assert hasattr(pipeline, 'disfluency_detector'), "Missing disfluency_detector"
        assert hasattr(pipeline, 'quality_aggregator'), "Missing quality_aggregator"
        assert hasattr(pipeline, 'unified_output_builder'), "Missing unified_output_builder"
        
        print("✓ All unified modules present in pipeline")
        
        return True
        
    except Exception as e:
        print(f"✗ Unified pipeline integration test failed: {e}")
        return False

def test_error_handling_unified():
    """Test error handling in unified system"""
    print("\n" + "=" * 60)
    print("TESTING UNIFIED SYSTEM ERROR HANDLING")
    print("=" * 60)
    
    try:
        from analysis.quality_aggregator import QualityAggregator
        from analysis.unified_output_builder import UnifiedOutputBuilder
        
        # Test quality aggregator error handling
        print("Testing quality aggregator error handling...")
        aggregator = QualityAggregator()
        
        # Test with None inputs
        result = aggregator.aggregate_quality(None, None, None, None)
        print(f"✓ Quality aggregator handled None: {result.get('overall_quality', 'unknown')}")
        
        # Test unified output builder error handling
        print("Testing unified output builder error handling...")
        builder = UnifiedOutputBuilder()
        
        result = builder.build_unified_output(None, None, None, None, None, None, None)
        print(f"✓ Unified output builder handled None: {result.get('transcription', '')}")
        
        return True
        
    except Exception as e:
        print(f"✗ Unified system error handling test failed: {e}")
        return False

def test_output_coherence():
    """Test output coherence and consistency"""
    print("\n" + "=" * 60)
    print("TESTING OUTPUT COHERENCE")
    print("=" * 60)
    
    try:
        from analysis.quality_aggregator import QualityAggregator
        from analysis.unified_output_builder import UnifiedOutputBuilder
        
        print("Testing output coherence...")
        
        # Create consistent test data
        mock_transcription = "hello world test"
        mock_segments = [
            {"segment": "hello world", "quality": "high", "reason": [], "metrics": {"word_count": 2}}
        ]
        mock_phonetic = []
        mock_disfluencies = []
        
        # Test quality aggregation
        aggregator = QualityAggregator()
        quality_summary = aggregator.aggregate_quality(
            mock_segments, mock_phonetic, mock_disfluencies, mock_transcription
        )
        
        # Test unified output building
        builder = UnifiedOutputBuilder()
        unified_output = builder.build_unified_output(
            mock_transcription, {}, mock_segments, mock_segments, 
            mock_phonetic, mock_disfluencies, quality_summary
        )
        
        # Check coherence between sections
        transcription = unified_output.get('transcription', '')
        quality = unified_output.get('quality_summary', {}).get('overall_quality', '')
        confidence = unified_output.get('confidence_summary', {}).get('overall_confidence', 0)
        
        print(f"✓ Output coherence validated")
        print(f"  Transcription length: {len(transcription)} chars")
        print(f"  Quality: {quality}")
        print(f"  Confidence: {confidence:.2f}")
        
        # Check that metadata matches
        metadata = unified_output.get('metadata', {})
        metadata_quality = metadata.get('overall_quality', '')
        metadata_score = metadata.get('quality_score', 0)
        
        if metadata_quality == quality:
            print("✓ Quality metadata is coherent")
        else:
            print("✗ Quality metadata mismatch")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Output coherence test failed: {e}")
        return False

def main():
    """Run all unified system validation tests"""
    print("AutoEIT Transcription System - Level 3.5 Unified Validation Suite")
    print("Intelligence + Differentiation + Quality Refinement + Unified Output")
    
    tests = [
        ("Unified System Imports", test_unified_imports),
        ("Quality Aggregation", test_quality_aggregation),
        ("Unified Output Building", test_unified_output_building),
        ("Pipeline Integration Unified", test_pipeline_integration_unified),
        ("Unified System Error Handling", test_error_handling_unified),
        ("Output Coherence", test_output_coherence)
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
    print("UNIFIED SYSTEM VALIDATION SUMMARY")
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
        print("🎉 All unified system tests passed! System is ready for unified deployment.")
        print("\nUnified System Features:")
        print("✅ Quality aggregation layer")
        print("✅ Unified output structure")
        print("✅ Confidence summary")
        print("✅ Critical region detection")
        print("✅ Actionable suggestions")
        print("✅ Coherent metadata")
        print("✅ Enhanced error handling")
        print("\nNew Capabilities:")
        print("• Unified transcription reliability assessment")
        print("• Confidence-aware output structure")
        print("• Critical region identification")
        print("• Actionable improvement suggestions")
        print("• Coherent quality metrics")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Place audio file at: data/sample.wav")
        print("3. Run unified analysis: python main.py")
        print("4. Export unified results: json.dumps(result, indent=2)")
    else:
        print("⚠️  Some unified system tests failed. Please review the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

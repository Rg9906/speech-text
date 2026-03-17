import sys
import os
import time
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pipeline.full_pipeline import TranscriptionPipeline


def main():
    try:
        # Define audio path
        audio_path = "data/sample.wav"
        
        print("=" * 60)
        print("AutoEIT Transcription System - Level 3.5 Unified")
        print("Intelligence + Differentiation + Quality Refinement")
        print("=" * 60)
        print(f"Target audio file: {audio_path}")
        print()
        
        # Validate audio path
        if not audio_path or not isinstance(audio_path, str):
            print("Error: Invalid audio path specified")
            return
        
        # Check if file exists
        if not os.path.exists(audio_path):
            print(f"Error: Audio file not found: {audio_path}")
            print("Please ensure that audio file exists at the specified path.")
            return
        
        # Get file info
        try:
            file_size = os.path.getsize(audio_path)
            print(f"File size: {file_size} bytes")
        except Exception as size_error:
            print(f"Warning: Could not get file size: {size_error}")
        
        print("Starting intelligence-enhanced transcription pipeline...")
        print()
        
        # Initialize pipeline
        try:
            pipeline = TranscriptionPipeline(audio_path)
        except Exception as init_error:
            print(f"Error: Failed to initialize pipeline: {init_error}")
            return
        
        # Run pipeline with timing
        start_time = time.time()
        result = pipeline.run()
        end_time = time.time()
        
        # Calculate duration
        duration = end_time - start_time
        print(f"Processing time: {duration:.2f} seconds")
        print()
        
        # Display results
        print("=" * 60)
        print("LEVEL 3.5 UNIFIED INTELLIGENCE RESULTS")
        print("=" * 60)
        
        if result is None:
            print("Status: FAILED")
            print("Transcription and analysis failed.")
            print("Please check the error messages above.")
        
        elif isinstance(result, dict):
            # Level 3: Structured annotated output
            print("Status: SUCCESS")
            print()
            
            # Display confidence summary
            confidence_summary = result.get("confidence_summary", {})
            if confidence_summary:
                print("🔍 Confidence Summary:")
                overall_conf = confidence_summary.get('overall_confidence', 0)
                conf_level = confidence_summary.get('confidence_level', 'unknown')
                print(f"  Overall Confidence: {overall_conf:.2f} ({conf_level.upper()})")
                
                low_regions = confidence_summary.get('low_confidence_regions', [])
                if low_regions:
                    print(f"  Low Confidence Regions: {len(low_regions)}")
                    for region in low_regions[:3]:
                        rtype = region.get('type', 'unknown')
                        text = region.get('text', '')[:30]
                        print(f"    {rtype}: '{text}...'")
                    if len(low_regions) > 3:
                        print(f"    ... and {len(low_regions) - 3} more")
                print()
            
            # Display quality summary
            quality_summary = result.get("quality_summary", {})
            if quality_summary:
                print("📊 Quality Summary:")
                overall_quality = quality_summary.get('overall_quality', 'unknown')
                overall_score = quality_summary.get('overall_score', 0)
                print(f"  Overall Quality: {overall_quality.upper()} (Score: {overall_score:.2f})")
                
                component_scores = quality_summary.get('component_scores', {})
                if component_scores:
                    print("  Component Scores:")
                    print(f"    Segment Quality: {component_scores.get('segment_quality', 0):.2f}")
                    print(f"    Phonetic Quality: {component_scores.get('phonetic_quality', 0):.2f}")
                    print(f"    Disfluency Quality: {component_scores.get('disfluency_quality', 0):.2f}")
                
                critical_regions = quality_summary.get('critical_regions', [])
                if critical_regions:
                    print(f"  Critical Regions: {len(critical_regions)}")
                    for region in critical_regions[:3]:
                        text = region.get('text', '')[:30]
                        reasons = region.get('reason', [])
                        print(f"    '{text}...' - {', '.join(reasons)}")
                    if len(critical_regions) > 3:
                        print(f"    ... and {len(critical_regions) - 3} more")
                
                suggestions = quality_summary.get('suggestions', [])
                if suggestions:
                    print("  Suggestions:")
                    for suggestion in suggestions[:3]:
                        print(f"    • {suggestion}")
                    if len(suggestions) > 3:
                        print(f"    ... and {len(suggestions) - 3} more suggestions")
                print()
            
            # Display linguistic analysis summary
            linguistic_analysis = result.get("linguistic_analysis", {})
            if linguistic_analysis:
                ling_summary = linguistic_analysis.get('linguistic_summary', {})
                if ling_summary:
                    print("🔬 Linguistic Analysis Summary:")
                    print(f"  Total Words: {ling_summary.get('total_words', 0)}")
                    print(f"  Segments Analyzed: {ling_summary.get('segments_analyzed', 0)}")
                    print(f"  Phonetic Issues: {ling_summary.get('phonetic_issues', 0)}")
                    print(f"  Disfluencies Detected: {ling_summary.get('disfluencies_detected', 0)}")
                    
                    languages = ling_summary.get('languages_detected', {})
                    if languages:
                        print("  Languages:")
                        for lang, count in languages.items():
                            print(f"    {lang}: {count}")
                    
                    word_types = ling_summary.get('word_types', {})
                    if word_types:
                        print("  Word Types:")
                        for wtype, count in word_types.items():
                            print(f"    {wtype}: {count}")
                    print()
            
            # Display detailed word analysis
            word_analysis = result.get("linguistic_analysis", {}).get("word_analysis", [])
            if word_analysis:
                print("� Word-Level Analysis:")
                for word_info in word_analysis[:8]:  # Show first 8 words
                    word = word_info.get("word", "")
                    lang = word_info.get("language", "unknown")
                    wtype = word_info.get("type", "unknown")
                    confidence = word_info.get("confidence", 0)
                    print(f"  '{word}' | Lang: {lang} | Type: {wtype} | Conf: {confidence:.2f}")
                
                if len(word_analysis) > 8:
                    print(f"  ... and {len(word_analysis) - 8} more words")
                print()
            
            # Display speech analysis
            speech_analysis = result.get("speech_analysis", {})
            if speech_analysis:
                print("🎤 Speech Dynamics:")
                print(f"  Duration: {speech_analysis.get('duration', 0):.2f} seconds")
                print(f"  Speech Rate: {speech_analysis.get('speech_rate', 'unknown')}")
                print(f"  Pauses Detected: {speech_analysis.get('pauses_detected', 0)}")
                print()
            
            # Display metadata
            metadata = result.get("metadata", {})
            if metadata:
                print("📊 Processing Metadata:")
                print(f"  Total Words: {metadata.get('total_words', 0)}")
                print(f"  Unique Words: {metadata.get('unique_words', 0)}")
                print(f"  Overall Quality: {metadata.get('overall_quality', 'unknown')}")
                print(f"  Quality Score: {metadata.get('quality_score', 0):.2f}")
                print(f"  Issues Detected: {metadata.get('issues_count', 0)}")
                print(f"  System Version: {metadata.get('system_version', 'unknown')}")
                
                completeness = metadata.get('analysis_completeness', {})
                if completeness:
                    percentage = completeness.get('percentage', 0)
                    print(f"  Analysis Completeness: {percentage:.1f}%")
                
                timestamp = metadata.get('processing_timestamp', 'unknown')
                print(f"  Processed: {timestamp}")
                print()
            
            # Option to save full results
            print("💾 Full unified structured output available.")
            print("   Use json.dumps(result, indent=2) to export.")
        
        else:
            # Fallback for unexpected result types
            print("Status: UNEXPECTED RESULT")
            print(f"Result type: {type(result)}")
            print(f"Result: {result}")
        
        print("=" * 60)
        print("Level 3.5 Unified transcription system complete.")
        
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
    except Exception as e:
        print(f"\nUnexpected error in main: {e}")
        print("Please check your setup and try again.")


if __name__ == "__main__":
    main()
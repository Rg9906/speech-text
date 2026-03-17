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
        print("AutoEIT Transcription System - Level 3")
        print("Intelligence + Differentiation Layer")
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
        print("INTELLIGENCE-ENHANCED RESULTS")
        print("=" * 60)
        
        if result is None:
            print("Status: FAILED")
            print("Transcription and analysis failed.")
            print("Please check the error messages above.")
        
        elif isinstance(result, dict):
            # Level 3: Structured annotated output
            print("Status: SUCCESS")
            print()
            
            # Display transcription
            transcription = result.get("transcription", "")
            print(f"📝 Transcription: {transcription}")
            print()
            
            # Display speech analysis
            speech_analysis = result.get("speech_analysis", {})
            if speech_analysis:
                print("🎤 Speech Dynamics:")
                print(f"  Duration: {speech_analysis.get('duration', 0):.2f} seconds")
                print(f"  Speech Rate: {speech_analysis.get('speech_rate', 'unknown')}")
                print(f"  Pauses Detected: {speech_analysis.get('pauses_detected', 0)}")
                print()
            
            # Display word analysis
            word_analysis = result.get("word_analysis", [])
            if word_analysis:
                print("🔤 Word-Level Analysis:")
                for word_info in word_analysis[:10]:  # Show first 10 words
                    word = word_info.get("word", "")
                    lang = word_info.get("language", "unknown")
                    wtype = word_info.get("type", "unknown")
                    confidence = word_info.get("confidence", 0)
                    print(f"  '{word}' | Lang: {lang} | Type: {wtype} | Conf: {confidence:.2f}")
                
                if len(word_analysis) > 10:
                    print(f"  ... and {len(word_analysis) - 10} more words")
                print()
            
            # Display metadata
            metadata = result.get("metadata", {})
            if metadata:
                print("📊 Metadata Summary:")
                print(f"  Total Words: {metadata.get('total_words', 0)}")
                print(f"  Unique Words: {metadata.get('unique_words', 0)}")
                
                languages = metadata.get("languages_detected", {})
                if languages:
                    print("  Languages Detected:")
                    for lang, count in languages.items():
                        print(f"    {lang}: {count}")
                
                word_types = metadata.get("word_type_distribution", {})
                if word_types:
                    print("  Word Types:")
                    for wtype, count in word_types.items():
                        print(f"    {wtype}: {count}")
                
                timestamp = metadata.get("processing_timestamp", "unknown")
                print(f"  Processed: {timestamp}")
                print()
            
            # Option to save full results
            print("💾 Full structured output available.")
            print("   Use json.dumps(result, indent=2) to export.")
        
        else:
            # Fallback for unexpected result types
            print("Status: UNEXPECTED RESULT")
            print(f"Result type: {type(result)}")
            print(f"Result: {result}")
        
        print("=" * 60)
        print("Intelligence analysis complete.")
        
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
    except Exception as e:
        print(f"\nUnexpected error in main: {e}")
        print("Please check your setup and try again.")


if __name__ == "__main__":
    main()
import sys
import os
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pipeline.full_pipeline import TranscriptionPipeline


def main():
    try:
        # Define audio path
        audio_path = "data/sample.wav"
        
        print("=" * 50)
        print("AutoEIT Transcription System - Level 2")
        print("=" * 50)
        print(f"Target audio file: {audio_path}")
        print()
        
        # Validate audio path
        if not audio_path or not isinstance(audio_path, str):
            print("Error: Invalid audio path specified")
            return
        
        # Check if file exists
        if not os.path.exists(audio_path):
            print(f"Error: Audio file not found: {audio_path}")
            print("Please ensure the audio file exists at the specified path.")
            return
        
        # Get file info
        try:
            file_size = os.path.getsize(audio_path)
            print(f"File size: {file_size} bytes")
        except Exception as size_error:
            print(f"Warning: Could not get file size: {size_error}")
        
        print("Starting transcription pipeline...")
        print()
        
        # Initialize pipeline
        try:
            pipeline = TranscriptionPipeline(audio_path)
        except Exception as init_error:
            print(f"Error: Failed to initialize pipeline: {init_error}")
            return
        
        # Run pipeline with timing
        start_time = time.time()
        transcription = pipeline.run()
        end_time = time.time()
        
        # Calculate duration
        duration = end_time - start_time
        print(f"Processing time: {duration:.2f} seconds")
        print()
        
        # Display results
        print("=" * 50)
        print("RESULTS")
        print("=" * 50)
        
        if transcription is None:
            print("Status: FAILED")
            print("Transcription failed.")
            print("Please check the error messages above.")
        elif transcription == "":
            print("Status: EMPTY RESULT")
            print("Transcription completed but returned empty text.")
            print("This might indicate:")
            print("- Silent audio file")
            print("- Unrecognizable speech")
            print("- Audio processing issues")
        else:
            print("Status: SUCCESS")
            print(f"Transcription: {transcription}")
            print(f"Character count: {len(transcription)}")
            print(f"Word count: {len(transcription.split())}")
        
        print("=" * 50)
        print("Process complete.")
        
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
    except Exception as e:
        print(f"\nUnexpected error in main: {e}")
        print("Please check your setup and try again.")


if __name__ == "__main__":
    main()
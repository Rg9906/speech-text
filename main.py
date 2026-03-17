import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pipeline.full_pipeline import TranscriptionPipeline


def main():
    audio_path = "data/sample.wav"
    
    pipeline = TranscriptionPipeline(audio_path)
    transcription = pipeline.run()
    
    if transcription is None:
        print("Transcription failed.")
    else:
        print(f"Transcription: {transcription}")


if __name__ == "__main__":
    main()
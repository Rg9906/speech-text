import sys
import os
import soundfile as sf
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from preprocessing.audio_normalization import AudioLoader
from models.base_asr.whisper_model import WhisperModel


class TranscriptionPipeline:
    def __init__(self, audio_path):
        self.audio_path = audio_path
        self.audio_loader = AudioLoader(audio_path)
        self.whisper_model = WhisperModel()
    
    def run(self):
        # Validate input file exists
        if not os.path.exists(self.audio_path):
            print("Error: Audio file not found")
            return None
        
        try:
            # Step 1: Load audio
            print("Step 1: Loading audio...")
            audio, sr = self.audio_loader.load_audio()
            
            if audio is None or sr is None:
                print("Error: Failed to load audio")
                return None
            
            # Step 2: Save processed audio
            print("Step 2: Saving processed audio...")
            temp_file = "temp_processed.wav"
            sf.write(temp_file, audio, sr)
            
            # Step 3: Run transcription
            print("Step 3: Running transcription...")
            transcription = self.whisper_model.transcribe(temp_file)
            
            # Step 4: Complete
            print("Step 4: Transcription complete.")
            
            # Clean up temp file
            if os.path.exists(temp_file):
                os.remove(temp_file)
            
            return transcription
            
        except Exception as e:
            print(f"Error during transcription: {e}")
            # Clean up temp file if it exists
            if os.path.exists("temp_processed.wav"):
                os.remove("temp_processed.wav")
            return None
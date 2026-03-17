import sys
import os
import soundfile as sf
import numpy as np
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from preprocessing.audio_normalization import AudioLoader
from preprocessing.noise_reduction import NoiseReducer
from preprocessing.audio_enhancer import AudioEnhancer
from models.base_asr.whisper_model import WhisperModel


class TranscriptionPipeline:
    def __init__(self, audio_path):
        # Validate audio path
        if not audio_path or not isinstance(audio_path, str):
            raise ValueError("Audio path must be a non-empty string")
        
        self.audio_path = audio_path
        self.audio_loader = AudioLoader(audio_path)
        self.noise_reducer = NoiseReducer()
        self.enhancer = AudioEnhancer()
        self.whisper_model = WhisperModel()
        self.temp_file = "temp_processed.wav"
    
    def _cleanup_temp_file(self):
        """Clean up temporary file safely"""
        try:
            if os.path.exists(self.temp_file):
                os.remove(self.temp_file)
        except Exception as cleanup_error:
            print(f"Warning: Failed to clean up temp file: {cleanup_error}")
    
    def run(self):
        # Validate input file exists
        if not os.path.exists(self.audio_path):
            print("Error: Audio file not found")
            return None
        
        # Clean up any existing temp file
        self._cleanup_temp_file()
        
        try:
            # Step 1: Load audio
            print("Step 1: Loading audio...")
            audio, sr = self.audio_loader.load_audio()
            
            if audio is None or sr is None:
                print("Error: Failed to load audio")
                return None
            
            # Validate audio data
            if len(audio) == 0:
                print("Warning: Empty audio file, proceeding with transcription")
            
            # Step 2: Apply noise reduction
            print("Step 2: Reducing noise...")
            audio = self.noise_reducer.reduce_noise(audio, sr)
            
            # Validate audio after noise reduction
            if audio is None:
                print("Error: Noise reduction returned None")
                return None
            
            # Step 3: Normalize volume
            print("Step 3: Normalizing audio...")
            audio = self.enhancer.normalize_volume(audio)
            
            # Validate audio after normalization
            if audio is None:
                print("Error: Volume normalization returned None")
                return None
            
            # Step 4: Save processed audio
            print("Step 4: Saving processed audio...")
            try:
                # Validate audio before saving
                if not np.isfinite(audio).all():
                    print("Warning: Audio contains invalid values before saving, cleaning...")
                    audio = np.nan_to_num(audio, nan=0.0, posinf=0.95, neginf=-0.95)
                
                # Ensure audio is in valid range
                audio = np.clip(audio, -1.0, 1.0)
                
                sf.write(self.temp_file, audio, sr)
                
                # Verify file was created
                if not os.path.exists(self.temp_file):
                    print("Error: Failed to create temporary audio file")
                    return None
                    
            except Exception as save_error:
                print(f"Error: Failed to save processed audio: {save_error}")
                return None
            
            # Step 5: Run transcription
            print("Step 5: Running transcription...")
            try:
                transcription = self.whisper_model.transcribe(self.temp_file)
                
                # Validate transcription result
                if transcription is None:
                    print("Warning: Whisper returned None transcription")
                    transcription = ""
                elif not isinstance(transcription, str):
                    print(f"Warning: Whisper returned non-string result: {type(transcription)}")
                    transcription = str(transcription) if transcription else ""
                
            except Exception as whisper_error:
                print(f"Error: Whisper transcription failed: {whisper_error}")
                return None
            
            # Step 6: Complete
            print("Step 6: Transcription complete.")
            
            # Clean up temp file
            self._cleanup_temp_file()
            
            return transcription
            
        except Exception as e:
            print(f"Error during transcription: {e}")
            # Clean up temp file if it exists
            self._cleanup_temp_file()
            return None
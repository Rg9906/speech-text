import librosa
import os
import numpy as np


class AudioLoader:
    def __init__(self, file_path):
        self.file_path = file_path
    
    def load_audio(self):
        try:
            # Validate file path
            if not self.file_path or not isinstance(self.file_path, str):
                print("Error: Invalid file path")
                return None, None
            
            # Check if file exists
            if not os.path.exists(self.file_path):
                print(f"Error: File does not exist: {self.file_path}")
                return None, None
            
            # Check if file is readable
            if not os.access(self.file_path, os.R_OK):
                print(f"Error: Cannot read file: {self.file_path}")
                return None, None
            
            # Load audio with validation
            audio, sample_rate = librosa.load(self.file_path, sr=16000)
            
            # Validate loaded audio
            if audio is None:
                print("Error: Failed to load audio - audio is None")
                return None, None
            
            if sample_rate is None or sample_rate <= 0:
                print(f"Error: Invalid sample rate: {sample_rate}")
                return None, None
            
            if len(audio) == 0:
                print("Warning: Audio file is empty")
                return audio, sample_rate
            
            # Check for invalid audio data
            if not np.isfinite(audio).all():
                print("Warning: Audio contains invalid values (NaN/Inf)")
                # Replace invalid values
                audio = np.nan_to_num(audio, nan=0.0, posinf=1.0, neginf=-1.0)
            
            return audio, sample_rate
            
        except Exception as e:
            print(f"Error loading audio file: {e}")
            return None, None
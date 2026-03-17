import numpy as np


class AudioEnhancer:
    def __init__(self):
        pass
    
    def normalize_volume(self, audio):
        try:
            # Validate input
            if audio is None:
                print("Warning: Audio is None, skipping volume normalization")
                return audio
            
            if len(audio) == 0:
                print("Warning: Empty audio, skipping volume normalization")
                return audio
            
            # Check for invalid audio data
            if not np.isfinite(audio).all():
                print("Warning: Audio contains invalid values, cleaning before normalization")
                audio = np.nan_to_num(audio, nan=0.0, posinf=1.0, neginf=-1.0)
            
            # Normalize audio amplitude to prevent clipping and improve consistency
            # Scale audio so max amplitude is near 0.95 (slightly below 1.0 to avoid clipping)
            
            # Find peak amplitude
            max_amplitude = np.max(np.abs(audio))
            
            # Avoid division by zero
            if max_amplitude == 0:
                print("Warning: Silent audio detected, skipping normalization")
                return audio
            
            # Check if normalization is needed
            if abs(max_amplitude - 0.95) < 0.01:  # Already close to target
                return audio
            
            # Scale to 0.95 to prevent clipping
            target_amplitude = 0.95
            normalized_audio = audio * (target_amplitude / max_amplitude)
            
            # Validate output
            if not np.isfinite(normalized_audio).all():
                print("Warning: Normalized audio contains invalid values, using original")
                return audio
            
            # Check for clipping after normalization
            if np.max(np.abs(normalized_audio)) > 1.0:
                print("Warning: Clipping detected after normalization, applying safety limit")
                normalized_audio = np.clip(normalized_audio, -0.95, 0.95)
            
            return normalized_audio
            
        except Exception as e:
            print(f"Warning: Volume normalization failed, using original audio: {e}")
            return audio

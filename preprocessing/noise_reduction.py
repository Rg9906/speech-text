import librosa
import numpy as np


class NoiseReducer:
    def __init__(self):
        pass
    
    def reduce_noise(self, audio, sr):
        try:
            # Validate inputs
            if audio is None:
                print("Warning: Audio is None, skipping noise reduction")
                return audio
            
            if sr is None or sr <= 0:
                print(f"Warning: Invalid sample rate {sr}, skipping noise reduction")
                return audio
            
            if len(audio) == 0:
                print("Warning: Empty audio, skipping noise reduction")
                return audio
            
            # Check for invalid audio data
            if not np.isfinite(audio).all():
                print("Warning: Audio contains invalid values, cleaning before noise reduction")
                audio = np.nan_to_num(audio, nan=0.0, posinf=1.0, neginf=-1.0)
            
            # Simple noise reduction using spectral gating
            # Estimate noise from first 0.5 seconds
            noise_sample_length = int(0.5 * sr)
            if len(audio) > noise_sample_length:
                noise_sample = audio[:noise_sample_length]
            else:
                # If audio is too short, use the whole audio as noise reference
                noise_sample = audio
            
            # Compute STFT of audio and noise
            try:
                stft_audio = librosa.stft(audio)
                stft_noise = librosa.stft(noise_sample)
            except Exception as stft_error:
                print(f"Warning: STFT computation failed: {stft_error}, skipping noise reduction")
                return audio
            
            # Compute magnitude spectra
            mag_audio = np.abs(stft_audio)
            mag_noise = np.abs(stft_noise)
            
            # Estimate noise floor (average noise magnitude)
            noise_floor = np.mean(mag_noise, axis=1, keepdims=True)
            
            # Handle edge case: zero noise floor
            if noise_floor.max() == 0:
                print("Warning: Zero noise floor detected, skipping noise reduction")
                return audio
            
            # Create spectral gate (simple thresholding)
            # Use a multiplier to control noise reduction strength
            gate_multiplier = 2.0
            mask = mag_audio > (noise_floor * gate_multiplier)
            
            # Apply mask to original STFT
            stft_clean = stft_audio * mask
            
            # Convert back to time domain
            try:
                clean_audio = librosa.istft(stft_clean)
                
                # Validate output
                if clean_audio is None or len(clean_audio) == 0:
                    print("Warning: ISTFT returned empty audio, using original")
                    return audio
                
                # Check for invalid values in result
                if not np.isfinite(clean_audio).all():
                    print("Warning: Cleaned audio contains invalid values, using original")
                    return audio
                
                return clean_audio
                
            except Exception as istft_error:
                print(f"Warning: ISTFT computation failed: {istft_error}, using original audio")
                return audio
            
        except Exception as e:
            print(f"Warning: Noise reduction failed, using original audio: {e}")
            return audio

import numpy as np


class SpeechDynamicsAnalyzer:
    def __init__(self):
        pass
    
    def analyze_speech(self, audio, sr, transcription=""):
        """
        Analyze speech dynamics from audio and transcription
        
        Args:
            audio: numpy array of audio samples
            sr: sample rate
            transcription: transcribed text (optional, for speech rate estimation)
            
        Returns:
            dict: {
                "duration": float,
                "speech_rate": "slow" | "normal" | "fast",
                "pauses_detected": int
            }
        """
        try:
            # Validate inputs
            if audio is None or sr is None or sr <= 0:
                return self._get_fallback_output()
            
            if len(audio) == 0:
                return self._get_fallback_output()
            
            # Check for invalid audio data
            if not np.isfinite(audio).all():
                print("Warning: Audio contains invalid values in speech analysis")
                audio = np.nan_to_num(audio, nan=0.0, posinf=1.0, neginf=-1.0)
            
            # Calculate duration
            duration = len(audio) / sr
            
            # Detect pauses using energy threshold
            pauses_detected = self._detect_pauses(audio, sr)
            
            # Estimate speech rate
            speech_rate = self._estimate_speech_rate(transcription, duration)
            
            return {
                "duration": round(duration, 2),
                "speech_rate": speech_rate,
                "pauses_detected": pauses_detected
            }
            
        except Exception as e:
            print(f"Warning: Speech dynamics analysis failed: {e}")
            return self._get_fallback_output()
    
    def _detect_pauses(self, audio, sr):
        """
        Detect pauses in audio using energy threshold
        
        Args:
            audio: numpy array of audio samples
            sr: sample rate
            
        Returns:
            int: number of pauses detected
        """
        try:
            # Calculate RMS energy
            frame_length = int(0.025 * sr)  # 25ms frames
            hop_length = int(0.01 * sr)     # 10ms hop
            
            # Compute energy for each frame
            energy = []
            for i in range(0, len(audio) - frame_length, hop_length):
                frame = audio[i:i + frame_length]
                rms = np.sqrt(np.mean(frame ** 2))
                energy.append(rms)
            
            if not energy:
                return 0
            
            # Threshold for silence (very low energy)
            energy = np.array(energy)
            threshold = np.mean(energy) * 0.1  # 10% of average energy
            
            # Find silent regions
            silent_frames = energy < threshold
            
            # Count transitions from speech to silence
            pauses = 0
            in_speech = False
            
            for is_silent in silent_frames:
                if not is_silent and not in_speech:
                    in_speech = True
                elif is_silent and in_speech:
                    pauses += 1
                    in_speech = False
            
            return pauses
            
        except Exception as e:
            print(f"Warning: Pause detection failed: {e}")
            return 0
    
    def _estimate_speech_rate(self, transcription, duration):
        """
        Estimate speech rate based on transcription duration
        
        Args:
            transcription: transcribed text
            duration: audio duration in seconds
            
        Returns:
            str: "slow", "normal", or "fast"
        """
        try:
            if not transcription or duration <= 0:
                return "normal"
            
            # Count words
            words = transcription.split()
            word_count = len(words)
            
            # Calculate words per minute
            wpm = (word_count / duration) * 60
            
            # Classify speech rate
            if wpm < 120:
                return "slow"
            elif wpm > 180:
                return "fast"
            else:
                return "normal"
                
        except Exception as e:
            print(f"Warning: Speech rate estimation failed: {e}")
            return "normal"
    
    def _get_fallback_output(self):
        """Return fallback output for error cases"""
        return {
            "duration": 0.0,
            "speech_rate": "normal",
            "pauses_detected": 0
        }

import librosa


class AudioLoader:
    def __init__(self, file_path):
        self.file_path = file_path
    
    def load_audio(self):
        try:
            audio, sample_rate = librosa.load(self.file_path, sr=16000)
            return audio, sample_rate
        except Exception as e:
            print(f"Error loading audio file: {e}")
            return None, None
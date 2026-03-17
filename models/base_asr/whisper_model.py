import whisper
import os


class WhisperModel:
    def __init__(self, model_size="base"):
        try:
            # Validate model size
            valid_models = ["tiny", "base", "small", "medium", "large"]
            if model_size not in valid_models:
                print(f"Warning: Invalid model size '{model_size}', using 'base'")
                model_size = "base"
            
            print(f"Loading Whisper model: {model_size}")
            self.model = whisper.load_model(model_size)
            print("Whisper model loaded successfully")
            
        except Exception as e:
            print(f"Error loading Whisper model: {e}")
            # Try to load base model as fallback
            try:
                print("Attempting to load base model as fallback...")
                self.model = whisper.load_model("base")
                print("Fallback model loaded successfully")
            except Exception as fallback_error:
                print(f"Critical error: Failed to load any Whisper model: {fallback_error}")
                raise RuntimeError("Failed to initialize Whisper model")
    
    def transcribe(self, audio_path):
        try:
            # Validate input
            if not audio_path or not isinstance(audio_path, str):
                print("Error: Invalid audio path provided to Whisper")
                return ""
            
            # Check if file exists
            if not os.path.exists(audio_path):
                print(f"Error: Audio file not found: {audio_path}")
                return ""
            
            # Check if file is readable
            if not os.access(audio_path, os.R_OK):
                print(f"Error: Cannot read audio file: {audio_path}")
                return ""
            
            # Transcribe audio
            result = self.model.transcribe(audio_path)
            
            # Validate result
            if result is None:
                print("Warning: Whisper returned None result")
                return ""
            
            if not isinstance(result, dict):
                print(f"Warning: Whisper returned unexpected result type: {type(result)}")
                return ""
            
            # Extract text
            text = result.get("text", "")
            
            if text is None:
                print("Warning: Whisper result contains None text")
                return ""
            
            if not isinstance(text, str):
                print(f"Warning: Whisper text is not string: {type(text)}")
                return str(text) if text else ""
            
            return text.strip()
            
        except Exception as e:
            print(f"Error during Whisper transcription: {e}")
            return ""
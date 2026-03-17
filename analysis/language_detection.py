class LanguageDetector:
    def __init__(self):
        pass
    
    def detect_languages(self, text):
        """
        Detect language for each word in the transcription
        
        Args:
            text: transcribed text
            
        Returns:
            list: [{"word": "...", "lang": "..."}]
        """
        try:
            # Validate input
            if not text or not isinstance(text, str):
                return []
            
            # Split into words, preserving punctuation
            words = self._split_into_words(text)
            
            if not words:
                return []
            
            # Detect language for each word
            result = []
            for word in words:
                lang = self._detect_word_language(word)
                result.append({"word": word, "lang": lang})
            
            return result
            
        except Exception as e:
            print(f"Warning: Language detection failed: {e}")
            return self._get_fallback_output(text)
    
    def _split_into_words(self, text):
        """
        Split text into words while preserving basic punctuation
        
        Args:
            text: input text
            
        Returns:
            list: list of words
        """
        try:
            # Simple word splitting - can be enhanced later
            import re
            # Split on whitespace, keep punctuation attached to words
            words = re.findall(r'\b\w+\b|[^\w\s]', text)
            return [word for word in words if word.strip()]
            
        except Exception as e:
            print(f"Warning: Word splitting failed: {e}")
            return text.split()
    
    def _detect_word_language(self, word):
        """
        Detect language of a single word using heuristics
        
        Args:
            word: single word
            
        Returns:
            str: language code ("en", "es", "fr", etc.) or "unknown"
        """
        try:
            if not word or len(word.strip()) == 0:
                return "unknown"
            
            word = word.lower().strip()
            
            # Remove punctuation for language detection
            import re
            clean_word = re.sub(r'[^\w\s]', '', word)
            
            if not clean_word:
                return "unknown"
            
            # Simple heuristic-based language detection
            # This is a lightweight approach without heavy ML models
            
            # English common words and patterns
            if self._is_english_word(clean_word):
                return "en"
            
            # Spanish patterns
            if self._is_spanish_word(clean_word):
                return "es"
            
            # French patterns
            if self._is_french_word(clean_word):
                return "fr"
            
            # Check for common characters
            if self._has_spanish_chars(clean_word):
                return "es"
            
            if self._has_french_chars(clean_word):
                return "fr"
            
            # Default to English for common English words
            if self._is_common_english(clean_word):
                return "en"
            
            return "unknown"
            
        except Exception as e:
            print(f"Warning: Word language detection failed for '{word}': {e}")
            return "unknown"
    
    def _is_english_word(self, word):
        """Check if word appears to be English"""
        # Common English word endings and patterns
        english_endings = ['ing', 'ed', 'ly', 'tion', 'ment', 'ness', 'er', 'est']
        english_words = {
            'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 
            'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his',
            'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy',
            'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use'
        }
        
        if word in english_words:
            return True
        
        for ending in english_endings:
            if word.endswith(ending):
                return True
        
        return False
    
    def _is_spanish_word(self, word):
        """Check if word appears to be Spanish"""
        # Common Spanish word endings and patterns
        spanish_endings = ['ar', 'er', 'ir', 'ando', 'iendo', 'ación', 'sión', 'mente']
        spanish_words = {
            'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'es', 'se', 'no',
            'te', 'lo', 'le', 'da', 'su', 'por', 'son', 'con', 'para', 'como',
            'las', 'del', 'los', 'una', 'mi', 'me', 'si', 'ya', 'muy', 'más'
        }
        
        if word in spanish_words:
            return True
        
        for ending in spanish_endings:
            if word.endswith(ending):
                return True
        
        return False
    
    def _is_french_word(self, word):
        """Check if word appears to be French"""
        # Common French word endings and patterns
        french_endings = ['er', 'é', 'ée', 'ement', 'tion', 'sion', 'eur', 'euse']
        french_words = {
            'le', 'de', 'et', 'à', 'un', 'il', 'être', 'et', 'en', 'avoir',
            'que', 'pour', 'dans', 'ce', 'son', 'une', 'sur', 'avec', 'ne',
            'se', 'pas', 'tout', 'plus', 'par', 'grand', 'mais', 'me', 'te'
        }
        
        if word in french_words:
            return True
        
        for ending in french_endings:
            if word.endswith(ending):
                return True
        
        return False
    
    def _has_spanish_chars(self, word):
        """Check for Spanish-specific characters"""
        spanish_chars = ['ñ', 'á', 'é', 'í', 'ó', 'ú', 'ü']
        return any(char in word for char in spanish_chars)
    
    def _has_french_chars(self, word):
        """Check for French-specific characters"""
        french_chars = ['à', 'â', 'ä', 'é', 'è', 'ê', 'ë', 'î', 'ï', 'ô', 'ù', 'û', 'ü', 'ç']
        return any(char in word for char in french_chars)
    
    def _is_common_english(self, word):
        """Check if it's a very common English word"""
        common_english = {
            'i', 'you', 'he', 'she', 'it', 'we', 'they', 'what', 'when', 'where',
            'why', 'how', 'who', 'which', 'that', 'this', 'these', 'those'
        }
        return word in common_english
    
    def _get_fallback_output(self, text):
        """Return fallback output for error cases"""
        try:
            if not text:
                return []
            
            words = text.split()
            return [{"word": word, "lang": "unknown"} for word in words]
            
        except Exception:
            return []

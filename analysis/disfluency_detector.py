import re


class DisfluencyDetector:
    def __init__(self):
        # Filler words and phrases
        self.filler_words = ['uh', 'um', 'ah', 'er', 'like', 'you know', 'i mean', 'well', 'so', 'actually']
        self.filler_phrases = ['you know', 'i mean', 'you see', 'i guess', 'i think', 'kind of', 'sort of']
        
        # Restart indicators
        self.restart_markers = ['-', '—', 'i mean', 'actually', 'no wait', 'sorry']
        self.correction_phrases = ['i mean', 'i meant', 'rather', 'actually', 'no', 'wait']
        
        # Repetition patterns
        self.max_repetition_distance = 3  # Max words between repetitions
    
    def detect_disfluencies(self, transcription):
        """
        Detect speech disfluencies in transcription
        
        Args:
            transcription: transcribed text
            
        Returns:
            list: disfluency detection results
        """
        try:
            # Validate input
            if not transcription or not isinstance(transcription, str):
                return []
            
            # Step 1: Tokenize words
            words = self._tokenize_words(transcription)
            
            if not words:
                return []
            
            # Step 2: Detect patterns
            disfluencies = []
            
            # Detect fillers
            filler_disfluencies = self._detect_fillers(words)
            disfluencies.extend(filler_disfluencies)
            
            # Detect repetitions
            repetition_disfluencies = self._detect_repetitions(words)
            disfluencies.extend(repetition_disfluencies)
            
            # Detect restarts
            restart_disfluencies = self._detect_restarts(transcription, words)
            disfluencies.extend(restart_disfluencies)
            
            return disfluencies
            
        except Exception as e:
            print(f"Warning: Disfluency detection failed: {e}")
            return self._get_fallback_output(transcription)
    
    def _tokenize_words(self, transcription):
        """
        Tokenize transcription into words with position info
        
        Args:
            transcription: input text
            
        Returns:
            list: word tokens with position information
        """
        try:
            # Split by whitespace, keep punctuation separate
            tokens = re.findall(r'\\b\\w+\\b|[^\\w\\s]', transcription.lower())
            
            # Add position information
            word_tokens = []
            for i, token in enumerate(tokens):
                if token.strip() and not token.isspace():
                    word_tokens.append({
                        'word': token,
                        'position': i,
                        'original': token
                    })
            
            return word_tokens
            
        except Exception as e:
            print(f"Warning: Tokenization failed: {e}")
            return []
    
    def _detect_fillers(self, words):
        """
        Detect filler words and phrases
        
        Args:
            words: tokenized words
            
        Returns:
            list: filler disfluency results
        """
        try:
            fillers = []
            
            # Check single word fillers
            for word_info in words:
                word = word_info['word']
                
                if word in self.filler_words:
                    fillers.append({
                        'type': 'filler',
                        'word': word,
                        'position': word_info['position'],
                        'confidence': 0.9
                    })
            
            # Check multi-word filler phrases
            phrase_fillers = self._detect_filler_phrases(words)
            fillers.extend(phrase_fillers)
            
            return fillers
            
        except Exception as e:
            print(f"Warning: Filler detection failed: {e}")
            return []
    
    def _detect_filler_phrases(self, words):
        """
        Detect multi-word filler phrases
        
        Args:
            words: tokenized words
            
        Returns:
            list: filler phrase results
        """
        try:
            phrase_fillers = []
            
            for phrase in self.filler_phrases:
                phrase_words = phrase.split()
                phrase_len = len(phrase_words)
                
                # Look for phrase in word sequence
                for i in range(len(words) - phrase_len + 1):
                    window = [words[j]['word'] for j in range(i, i + phrase_len)]
                    
                    if window == phrase_words:
                        phrase_fillers.append({
                            'type': 'filler_phrase',
                            'phrase': phrase,
                            'words': window,
                            'start_position': words[i]['position'],
                            'end_position': words[i + phrase_len - 1]['position'],
                            'confidence': 0.8
                        })
            
            return phrase_fillers
            
        except Exception as e:
            print(f"Warning: Filler phrase detection failed: {e}")
            return []
    
    def _detect_repetitions(self, words):
        """
        Detect word repetitions
        
        Args:
            words: tokenized words
            
        Returns:
            list: repetition disfluency results
        """
        try:
            repetitions = []
            
            # Check for immediate consecutive repetitions
            for i in range(len(words) - 1):
                current_word = words[i]['word']
                next_word = words[i + 1]['word']
                
                if current_word == next_word and current_word not in self.filler_words:
                    repetitions.append({
                        'type': 'repetition',
                        'word': current_word,
                        'positions': [words[i]['position'], words[i + 1]['position']],
                        'count': 2,
                        'confidence': 0.9
                    })
            
            # Check for delayed repetitions (within max distance)
            delayed_reps = self._detect_delayed_repetitions(words)
            repetitions.extend(delayed_reps)
            
            return repetitions
            
        except Exception as e:
            print(f"Warning: Repetition detection failed: {e}")
            return []
    
    def _detect_delayed_repetitions(self, words):
        """
        Detect delayed repetitions (words repeated within short distance)
        
        Args:
            words: tokenized words
            
        Returns:
            list: delayed repetition results
        """
        try:
            delayed_reps = []
            
            for i in range(len(words)):
                current_word = words[i]['word']
                
                # Skip filler words
                if current_word in self.filler_words:
                    continue
                
                # Look for same word within max distance
                for j in range(i + 1, min(i + self.max_repetition_distance + 1, len(words))):
                    next_word = words[j]['word']
                    
                    if current_word == next_word:
                        # Check if it's not already caught as consecutive
                        if j != i + 1:
                            delayed_reps.append({
                                'type': 'delayed_repetition',
                                'word': current_word,
                                'positions': [words[i]['position'], words[j]['position']],
                                'distance': j - i,
                                'confidence': 0.7
                            })
                        break
            
            return delayed_reps
            
        except Exception as e:
            print(f"Warning: Delayed repetition detection failed: {e}")
            return []
    
    def _detect_restarts(self, transcription, words):
        """
        Detect speech restarts and corrections
        
        Args:
            transcription: original text
            words: tokenized words
            
        Returns:
            list: restart disfluency results
        """
        try:
            restarts = []
            
            # Check for dash-based restarts
            dash_restarts = self._detect_dash_restarts(transcription)
            restarts.extend(dash_restarts)
            
            # Check for phrase-based restarts
            phrase_restarts = self._detect_phrase_restarts(transcription, words)
            restarts.extend(phrase_restarts)
            
            # Check for correction patterns
            corrections = self._detect_corrections(transcription, words)
            restarts.extend(corrections)
            
            return restarts
            
        except Exception as e:
            print(f"Warning: Restart detection failed: {e}")
            return []
    
    def _detect_dash_restarts(self, transcription):
        """
        Detect restarts marked with dashes
        
        Args:
            transcription: original text
            
        Returns:
            list: dash restart results
        """
        try:
            dash_restarts = []
            
            # Split by dashes
            parts = re.split(r'[-—]', transcription)
            
            if len(parts) > 1:
                for i, part in enumerate(parts):
                    part = part.strip()
                    if part and len(part) > 2:
                        dash_restarts.append({
                            'type': 'restart',
                            'text': part,
                            'restart_type': 'dash_restart',
                            'position': i,
                            'confidence': 0.8
                        })
            
            return dash_restarts
            
        except Exception as e:
            print(f"Warning: Dash restart detection failed: {e}")
            return []
    
    def _detect_phrase_restarts(self, transcription, words):
        """
        Detect restarts using restart marker phrases
        
        Args:
            transcription: original text
            words: tokenized words
            
        Returns:
            list: phrase restart results
        """
        try:
            phrase_restarts = []
            
            # Look for restart markers in text
            for marker in self.restart_markers:
                if marker in transcription.lower():
                    # Find the context around the marker
                    marker_pos = transcription.lower().find(marker)
                    
                    # Extract some context
                    start_context = max(0, marker_pos - 20)
                    end_context = min(len(transcription), marker_pos + len(marker) + 20)
                    context = transcription[start_context:end_context]
                    
                    phrase_restarts.append({
                        'type': 'restart',
                        'text': context,
                        'restart_type': 'phrase_restart',
                        'marker': marker,
                        'position': marker_pos,
                        'confidence': 0.7
                    })
            
            return phrase_restarts
            
        except Exception as e:
            print(f"Warning: Phrase restart detection failed: {e}")
            return []
    
    def _detect_corrections(self, transcription, words):
        """
        Detect correction patterns
        
        Args:
            transcription: original text
            words: tokenized words
            
        Returns:
            list: correction results
        """
        try:
            corrections = []
            
            # Look for correction phrases
            for correction in self.correction_phrases:
                if correction in transcription.lower():
                    # Find the context
                    correction_pos = transcription.lower().find(correction)
                    
                    # Extract context
                    start_context = max(0, correction_pos - 30)
                    end_context = min(len(transcription), correction_pos + len(correction) + 30)
                    context = transcription[start_context:end_context]
                    
                    corrections.append({
                        'type': 'correction',
                        'text': context,
                        'correction_type': 'self_correction',
                        'marker': correction,
                        'position': correction_pos,
                        'confidence': 0.8
                    })
            
            return corrections
            
        except Exception as e:
            print(f"Warning: Correction detection failed: {e}")
            return []
    
    def _get_fallback_output(self, transcription):
        """Return fallback output for error cases"""
        try:
            if not transcription:
                return []
            
            return []
            
        except Exception:
            return []

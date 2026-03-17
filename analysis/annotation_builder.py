class AnnotationBuilder:
    def __init__(self):
        pass
    
    def build_annotated_output(self, transcription, speech_analysis, language_tags, lexical_classification):
        """
        Combine all intelligence into structured annotated output
        
        Args:
            transcription: raw transcribed text
            speech_analysis: speech dynamics analysis results
            language_tags: language detection results
            lexical_classification: word classification results
            
        Returns:
            dict: structured annotated output
        """
        try:
            # Validate inputs
            if not transcription:
                transcription = ""
            
            if not speech_analysis:
                speech_analysis = self._get_fallback_speech_analysis()
            
            if not language_tags:
                language_tags = []
            
            if not lexical_classification:
                lexical_classification = []
            
            # Build word-level analysis
            word_analysis = self._build_word_analysis(
                language_tags, lexical_classification
            )
            
            # Build complete annotated output
            annotated_output = {
                "transcription": transcription,
                "speech_analysis": speech_analysis,
                "word_analysis": word_analysis,
                "metadata": self._build_metadata(
                    transcription, speech_analysis, language_tags, lexical_classification
                )
            }
            
            return annotated_output
            
        except Exception as e:
            print(f"Warning: Annotation building failed: {e}")
            return self._get_fallback_output(transcription)
    
    def _build_word_analysis(self, language_tags, lexical_classification):
        """
        Build word-level analysis combining language and lexical information
        
        Args:
            language_tags: list of {"word": "...", "lang": "..."}
            lexical_classification: list of {"word": "...", "type": "..."}
            
        Returns:
            list: combined word analysis
        """
        try:
            # Create word lookup dictionaries
            lang_dict = {item["word"]: item["lang"] for item in language_tags if "word" in item}
            type_dict = {item["word"]: item["type"] for item in lexical_classification if "word" in item}
            
            # Get all unique words
            all_words = set()
            all_words.update(lang_dict.keys())
            all_words.update(type_dict.keys())
            
            # Build combined analysis
            word_analysis = []
            for word in sorted(all_words):
                analysis = {
                    "word": word,
                    "language": lang_dict.get(word, "unknown"),
                    "type": type_dict.get(word, "unknown"),
                    "confidence": self._calculate_confidence(word, lang_dict, type_dict)
                }
                word_analysis.append(analysis)
            
            return word_analysis
            
        except Exception as e:
            print(f"Warning: Word analysis building failed: {e}")
            return []
    
    def _calculate_confidence(self, word, lang_dict, type_dict):
        """
        Calculate confidence score for word analysis
        
        Args:
            word: the word
            lang_dict: language lookup dictionary
            type_dict: type lookup dictionary
            
        Returns:
            float: confidence score (0.0 to 1.0)
        """
        try:
            confidence = 0.5  # Base confidence
            
            # Higher confidence for known languages
            if word in lang_dict:
                lang = lang_dict[word]
                if lang != "unknown":
                    confidence += 0.2
            
            # Higher confidence for known word types
            if word in type_dict:
                word_type = type_dict[word]
                if word_type == "known":
                    confidence += 0.3
                elif word_type in ["slang_like", "possible_merged"]:
                    confidence += 0.1
            
            # Cap at 1.0
            return min(confidence, 1.0)
            
        except Exception as e:
            print(f"Warning: Confidence calculation failed for '{word}': {e}")
            return 0.5
    
    def _build_metadata(self, transcription, speech_analysis, language_tags, lexical_classification):
        """
        Build metadata summary
        
        Args:
            transcription: transcribed text
            speech_analysis: speech dynamics
            language_tags: language detection results
            lexical_classification: word classification results
            
        Returns:
            dict: metadata summary
        """
        try:
            metadata = {
                "total_words": len(transcription.split()) if transcription else 0,
                "unique_words": len(set(transcription.split())) if transcription else 0,
                "languages_detected": self._count_languages(language_tags),
                "word_type_distribution": self._count_word_types(lexical_classification),
                "processing_timestamp": self._get_timestamp()
            }
            
            return metadata
            
        except Exception as e:
            print(f"Warning: Metadata building failed: {e}")
            return {
                "total_words": 0,
                "unique_words": 0,
                "languages_detected": {},
                "word_type_distribution": {},
                "processing_timestamp": self._get_timestamp()
            }
    
    def _count_languages(self, language_tags):
        """
        Count occurrences of each detected language
        
        Args:
            language_tags: list of language detection results
            
        Returns:
            dict: language counts
        """
        try:
            lang_counts = {}
            for item in language_tags:
                if "lang" in item:
                    lang = item["lang"]
                    lang_counts[lang] = lang_counts.get(lang, 0) + 1
            
            return lang_counts
            
        except Exception as e:
            print(f"Warning: Language counting failed: {e}")
            return {}
    
    def _count_word_types(self, lexical_classification):
        """
        Count occurrences of each word type
        
        Args:
            lexical_classification: list of word classification results
            
        Returns:
            dict: word type counts
        """
        try:
            type_counts = {}
            for item in lexical_classification:
                if "type" in item:
                    word_type = item["type"]
                    type_counts[word_type] = type_counts.get(word_type, 0) + 1
            
            return type_counts
            
        except Exception as e:
            print(f"Warning: Word type counting failed: {e}")
            return {}
    
    def _get_timestamp(self):
        """Get current timestamp"""
        try:
            import datetime
            return datetime.datetime.now().isoformat()
        except Exception:
            return "unknown"
    
    def _get_fallback_speech_analysis(self):
        """Get fallback speech analysis"""
        return {
            "duration": 0.0,
            "speech_rate": "normal",
            "pauses_detected": 0
        }
    
    def _get_fallback_output(self, transcription):
        """Get fallback annotated output"""
        return {
            "transcription": transcription or "",
            "speech_analysis": self._get_fallback_speech_analysis(),
            "word_analysis": [],
            "metadata": {
                "total_words": 0,
                "unique_words": 0,
                "languages_detected": {},
                "word_type_distribution": {},
                "processing_timestamp": self._get_timestamp()
            }
        }

import re


class SegmentQualityAnalyzer:
    def __init__(self):
        # Segment delimiters
        self.punctuation_delimiters = ['.', '!', '?', ',', ';']
        self.conjunction_delimiters = ['and', 'but', 'or', 'so', 'because', 'however', 'therefore']
        self.filler_words = ['uh', 'um', 'ah', 'er', 'like', 'you know']
    
    def analyze_segments(self, transcription, language_tags=None, word_analysis=None):
        """
        Analyze transcription quality in segments
        
        Args:
            transcription: transcribed text
            language_tags: language detection results
            word_analysis: word classification results
            
        Returns:
            list: segment analysis with quality labels
        """
        try:
            # Validate inputs
            if not transcription or not isinstance(transcription, str):
                return []
            
            # Create lookup dictionaries
            lang_dict = {}
            if language_tags:
                lang_dict = {item.get('word', ''): item.get('lang', 'unknown') 
                           for item in language_tags if isinstance(item, dict)}
            
            type_dict = {}
            if word_analysis:
                type_dict = {item.get('word', ''): item.get('type', 'unknown') 
                           for item in word_analysis if isinstance(item, dict)}
            
            # Step 1: Segment the transcription
            segments = self._segment_transcription(transcription)
            
            if not segments:
                return []
            
            # Step 2: Evaluate each segment
            segment_analysis = []
            for segment in segments:
                quality_info = self._evaluate_segment_quality(segment, lang_dict, type_dict)
                segment_analysis.append(quality_info)
            
            return segment_analysis
            
        except Exception as e:
            print(f"Warning: Segment quality analysis failed: {e}")
            return self._get_fallback_output(transcription)
    
    def _segment_transcription(self, transcription):
        """
        Split transcription into meaningful segments
        
        Args:
            transcription: input text
            
        Returns:
            list: text segments
        """
        try:
            segments = []
            
            # Split by major punctuation first
            major_punct_pattern = r'[.!?]'
            major_splits = re.split(major_punct_pattern, transcription)
            
            for split in major_splits:
                split = split.strip()
                if not split:
                    continue
                
                # Further split by conjunctions and minor punctuation
                minor_splits = self._split_by_conjunctions(split)
                
                for segment in minor_splits:
                    segment = segment.strip()
                    if segment and len(segment) > 2:  # Minimum meaningful length
                        segments.append(segment)
            
            return segments
            
        except Exception as e:
            print(f"Warning: Segmentation failed: {e}")
            return [transcription] if transcription else []
    
    def _split_by_conjunctions(self, text):
        """
        Split text by conjunctions and minor punctuation
        
        Args:
            text: input text
            
        Returns:
            list: split segments
        """
        try:
            # Create pattern for conjunctions and minor punctuation
            conjunction_pattern = r'\\b(?:' + '|'.join(self.conjunction_delimiters) + r')\\b'
            minor_punct_pattern = r'[,;]'
            
            # Combine patterns
            split_pattern = f'(?:{conjunction_pattern}|{minor_punct_pattern})'
            
            segments = re.split(split_pattern, text)
            
            # Clean and filter segments
            clean_segments = []
            for segment in segments:
                segment = segment.strip()
                if segment and len(segment) > 2:
                    clean_segments.append(segment)
            
            return clean_segments
            
        except Exception as e:
            print(f"Warning: Conjunction splitting failed: {e}")
            return [text] if text else []
    
    def _evaluate_segment_quality(self, segment, lang_dict, type_dict):
        """
        Evaluate quality of a single segment
        
        Args:
            segment: text segment
            lang_dict: language lookup
            type_dict: word type lookup
            
        Returns:
            dict: segment quality analysis
        """
        try:
            words = segment.split()
            
            if not words:
                return {
                    "segment": segment,
                    "quality": "medium",
                    "reason": ["empty_segment"]
                }
            
            # Step 2: Calculate quality metrics
            word_count = len(words)
            unknown_count = 0
            non_english_count = 0
            disfluency_count = 0
            filler_count = 0
            
            for word in words:
                clean_word = word.lower().strip('.,!?;:')
                
                # Check unknown words
                word_type = type_dict.get(clean_word, 'unknown')
                if word_type == 'unknown':
                    unknown_count += 1
                
                # Check non-English words
                lang = lang_dict.get(clean_word, 'unknown')
                if lang != 'en' and lang != 'unknown':
                    non_english_count += 1
                
                # Check disfluencies
                if clean_word in self.filler_words:
                    filler_count += 1
                    disfluency_count += 1
            
            # Calculate percentages
            unknown_percentage = (unknown_count / word_count) * 100 if word_count > 0 else 0
            non_english_percentage = (non_english_count / word_count) * 100 if word_count > 0 else 0
            disfluency_percentage = (disfluency_count / word_count) * 100 if word_count > 0 else 0
            
            # Step 3: Assign quality label
            quality, reasons = self._assign_quality_label(
                unknown_percentage, non_english_percentage, disfluency_percentage,
                word_count, filler_count
            )
            
            return {
                "segment": segment,
                "quality": quality,
                "reason": reasons,
                "metrics": {
                    "word_count": word_count,
                    "unknown_percentage": round(unknown_percentage, 1),
                    "non_english_percentage": round(non_english_percentage, 1),
                    "disfluency_percentage": round(disfluency_percentage, 1),
                    "filler_count": filler_count
                }
            }
            
        except Exception as e:
            print(f"Warning: Segment quality evaluation failed: {e}")
            return {
                "segment": segment,
                "quality": "medium",
                "reason": ["evaluation_error"]
            }
    
    def _assign_quality_label(self, unknown_pct, non_english_pct, disfluency_pct, word_count, filler_count):
        """
        Assign quality label based on metrics
        
        Args:
            unknown_pct: percentage of unknown words
            non_english_pct: percentage of non-English words
            disfluency_pct: percentage of disfluencies
            word_count: number of words in segment
            filler_count: number of filler words
            
        Returns:
            tuple: (quality_label, reasons)
        """
        reasons = []
        
        # HIGH quality conditions
        if (unknown_pct <= 10 and 
            non_english_pct <= 20 and 
            disfluency_pct <= 10 and
            word_count >= 3):
            
            quality = "high"
            if unknown_pct == 0:
                reasons.append("clear_speech")
            if non_english_pct == 0:
                reasons.append("consistent_language")
            if disfluency_pct == 0:
                reasons.append("fluent")
                
        # LOW quality conditions
        elif (unknown_pct >= 40 or 
              disfluency_pct >= 30 or
              word_count < 2):
            
            quality = "low"
            if unknown_pct >= 40:
                reasons.append("many_unknown_words")
            if disfluency_pct >= 30:
                reasons.append("high_disfluency")
            if word_count < 2:
                reasons.append("fragment")
            if non_english_pct >= 50:
                reasons.append("heavy_code_switch")
                
        # MEDIUM quality (everything else)
        else:
            quality = "medium"
            
            if unknown_pct > 10:
                reasons.append("some_unknown_words")
            if non_english_pct > 20:
                reasons.append("code_switch")
            if disfluency_pct > 10:
                reasons.append("some_disfluency")
            if filler_count > 0:
                reasons.append("fillers_present")
        
        # Ensure at least one reason
        if not reasons:
            reasons.append("standard_quality")
        
        return quality, reasons
    
    def _get_fallback_output(self, transcription):
        """Return fallback output for error cases"""
        try:
            if not transcription:
                return []
            
            return [{
                "segment": transcription,
                "quality": "medium",
                "reason": ["fallback_analysis"]
            }]
            
        except Exception:
            return []

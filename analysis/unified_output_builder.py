class UnifiedOutputBuilder:
    def __init__(self):
        pass
    
    def build_unified_output(self, transcription, speech_analysis, word_analysis, 
                           segment_analysis, phonetic_analysis, disfluencies, quality_summary):
        """
        Build unified, coherent output structure
        
        Args:
            transcription: raw transcribed text
            speech_analysis: speech dynamics results
            word_analysis: word-level analysis results
            segment_analysis: segment quality results
            phonetic_analysis: phonetic error results
            disfluencies: disfluency detection results
            quality_summary: aggregated quality summary
            
        Returns:
            dict: unified output structure
        """
        try:
            # Validate inputs
            if not transcription:
                transcription = ""
            
            # Calculate confidence summary
            confidence_summary = self._calculate_confidence_summary(
                word_analysis, phonetic_analysis, segment_analysis
            )
            
            # Organize linguistic analysis
            linguistic_analysis = self._organize_linguistic_analysis(
                word_analysis, segment_analysis, phonetic_analysis, disfluencies
            )
            
            # Build final unified output
            unified_output = {
                "transcription": transcription,
                "confidence_summary": confidence_summary,
                "speech_analysis": self._clean_speech_analysis(speech_analysis),
                "linguistic_analysis": linguistic_analysis,
                "quality_summary": quality_summary,
                "metadata": self._build_enhanced_metadata(
                    transcription, word_analysis, segment_analysis, 
                    phonetic_analysis, disfluencies, quality_summary
                )
            }
            
            return unified_output
            
        except Exception as e:
            print(f"Warning: Unified output building failed: {e}")
            return self._get_fallback_unified_output(transcription)
    
    def _calculate_confidence_summary(self, word_analysis, phonetic_analysis, segment_analysis):
        """Calculate overall confidence summary"""
        try:
            # Calculate overall confidence
            word_confidences = []
            if word_analysis:
                word_confidences = [w.get('confidence', 0.5) for w in word_analysis]
            
            phonetic_impact = 0
            if phonetic_analysis:
                # Phonetic issues reduce confidence
                phonetic_impact = len(phonetic_analysis) * 0.1
            
            segment_impact = 0
            if segment_analysis:
                low_segments = [s for s in segment_analysis if s.get('quality') == 'low']
                segment_impact = len(low_segments) * 0.15
            
            # Calculate overall confidence
            base_confidence = sum(word_confidences) / len(word_confidences) if word_confidences else 0.5
            overall_confidence = max(0.1, base_confidence - phonetic_impact - segment_impact)
            overall_confidence = min(1.0, overall_confidence)
            
            # Identify low confidence regions
            low_confidence_regions = []
            
            # Low confidence words
            if word_analysis:
                for word_info in word_analysis:
                    confidence = word_info.get('confidence', 0.5)
                    if confidence < 0.6:
                        low_confidence_regions.append({
                            "type": "low_confidence_word",
                            "text": word_info.get('word', ''),
                            "confidence": confidence,
                            "reason": "low_word_confidence"
                        })
            
            # Phonetic uncertainty regions
            if phonetic_analysis:
                for phonetic in phonetic_analysis:
                    confidence = phonetic.get('confidence', 0.5)
                    if confidence < 0.7:
                        low_confidence_regions.append({
                            "type": "phonetic_uncertainty",
                            "text": f"{phonetic.get('word', '')} → {phonetic.get('phonetic_match', '')}",
                            "confidence": confidence,
                            "reason": "phonetic_variation_detected"
                        })
            
            # Low quality segments
            if segment_analysis:
                for segment in segment_analysis:
                    if segment.get('quality') == 'low':
                        low_confidence_regions.append({
                            "type": "low_quality_segment",
                            "text": segment.get('segment', ''),
                            "confidence": 0.4,
                            "reason": "segment_quality_issues"
                        })
            
            return {
                "overall_confidence": round(overall_confidence, 2),
                "confidence_level": self._get_confidence_level(overall_confidence),
                "low_confidence_regions": low_confidence_regions,
                "confidence_breakdown": {
                    "word_confidence_avg": round(base_confidence, 2),
                    "phonetic_impact": round(phonetic_impact, 2),
                    "segment_impact": round(segment_impact, 2),
                    "total_words_analyzed": len(word_analysis) if word_analysis else 0
                }
            }
            
        except Exception as e:
            print(f"Warning: Confidence summary calculation failed: {e}")
            return self._get_fallback_confidence_summary()
    
    def _get_confidence_level(self, confidence):
        """Get confidence level from confidence score"""
        if confidence >= 0.8:
            return "high"
        elif confidence >= 0.6:
            return "medium"
        else:
            return "low"
    
    def _organize_linguistic_analysis(self, word_analysis, segment_analysis, phonetic_analysis, disfluencies):
        """Organize all linguistic analysis into coherent structure"""
        try:
            return {
                "word_analysis": word_analysis or [],
                "segment_analysis": segment_analysis or [],
                "phonetic_analysis": phonetic_analysis or [],
                "disfluencies": disfluencies or [],
                "linguistic_summary": {
                    "total_words": len(word_analysis) if word_analysis else 0,
                    "segments_analyzed": len(segment_analysis) if segment_analysis else 0,
                    "phonetic_issues": len(phonetic_analysis) if phonetic_analysis else 0,
                    "disfluencies_detected": len(disfluencies) if disfluencies else 0,
                    "languages_detected": self._extract_languages(word_analysis),
                    "word_types": self._extract_word_types(word_analysis)
                }
            }
            
        except Exception as e:
            print(f"Warning: Linguistic analysis organization failed: {e}")
            return {
                "word_analysis": [],
                "segment_analysis": [],
                "phonetic_analysis": [],
                "disfluencies": [],
                "linguistic_summary": {}
            }
    
    def _extract_languages(self, word_analysis):
        """Extract language distribution from word analysis"""
        try:
            if not word_analysis:
                return {}
            
            languages = {}
            for word_info in word_analysis:
                lang = word_info.get('language', 'unknown')
                languages[lang] = languages.get(lang, 0) + 1
            
            return languages
            
        except Exception:
            return {}
    
    def _extract_word_types(self, word_analysis):
        """Extract word type distribution from word analysis"""
        try:
            if not word_analysis:
                return {}
            
            word_types = {}
            for word_info in word_analysis:
                wtype = word_info.get('type', 'unknown')
                word_types[wtype] = word_types.get(wtype, 0) + 1
            
            return word_types
            
        except Exception:
            return {}
    
    def _clean_speech_analysis(self, speech_analysis):
        """Clean and standardize speech analysis output"""
        try:
            if not speech_analysis:
                return {
                    "duration": 0.0,
                    "speech_rate": "normal",
                    "pauses_detected": 0,
                    "analysis_status": "unavailable"
                }
            
            # Ensure all expected fields are present
            cleaned = {
                "duration": speech_analysis.get('duration', 0.0),
                "speech_rate": speech_analysis.get('speech_rate', 'normal'),
                "pauses_detected": speech_analysis.get('pauses_detected', 0),
                "analysis_status": "complete"
            }
            
            # Add any additional fields from original analysis
            for key, value in speech_analysis.items():
                if key not in cleaned:
                    cleaned[key] = value
            
            return cleaned
            
        except Exception as e:
            print(f"Warning: Speech analysis cleaning failed: {e}")
            return {
                "duration": 0.0,
                "speech_rate": "normal",
                "pauses_detected": 0,
                "analysis_status": "error"
            }
    
    def _build_enhanced_metadata(self, transcription, word_analysis, segment_analysis, 
                               phonetic_analysis, disfluencies, quality_summary):
        """Build enhanced metadata with quality information"""
        try:
            import datetime
            
            base_metadata = {
                "total_words": len(transcription.split()) if transcription else 0,
                "unique_words": len(set(transcription.split())) if transcription else 0,
                "processing_timestamp": datetime.datetime.now().isoformat(),
                "system_version": "3.5_unified",
                "analysis_completeness": self._calculate_completeness(
                    word_analysis, segment_analysis, phonetic_analysis, disfluencies
                )
            }
            
            # Add quality-related metadata
            quality_metadata = {
                "overall_quality": quality_summary.get('overall_quality', 'medium'),
                "quality_score": quality_summary.get('overall_score', 0.5),
                "issues_count": len(quality_summary.get('issues_detected', [])),
                "critical_regions_count": len(quality_summary.get('critical_regions', [])),
                "suggestions_count": len(quality_summary.get('suggestions', []))
            }
            
            # Merge metadata
            base_metadata.update(quality_metadata)
            
            return base_metadata
            
        except Exception as e:
            print(f"Warning: Enhanced metadata building failed: {e}")
            return {
                "total_words": 0,
                "unique_words": 0,
                "processing_timestamp": "unknown",
                "system_version": "3.5_unified",
                "analysis_completeness": "partial"
            }
    
    def _calculate_completeness(self, word_analysis, segment_analysis, phonetic_analysis, disfluencies):
        """Calculate analysis completeness percentage"""
        try:
            components = {
                'word_analysis': bool(word_analysis),
                'segment_analysis': bool(segment_analysis),
                'phonetic_analysis': bool(phonetic_analysis),
                'disfluency_analysis': bool(disfluencies)
            }
            
            completed = sum(components.values())
            total = len(components)
            
            completeness = (completed / total) * 100
            
            return {
                "percentage": round(completeness, 1),
                "completed_components": completed,
                "total_components": total,
                "missing_components": [k for k, v in components.items() if not v]
            }
            
        except Exception:
            return {
                "percentage": 0.0,
                "completed_components": 0,
                "total_components": 4,
                "missing_components": []
            }
    
    def _get_fallback_confidence_summary(self):
        """Get fallback confidence summary"""
        return {
            "overall_confidence": 0.5,
            "confidence_level": "medium",
            "low_confidence_regions": [],
            "confidence_breakdown": {
                "word_confidence_avg": 0.5,
                "phonetic_impact": 0.0,
                "segment_impact": 0.0,
                "total_words_analyzed": 0
            }
        }
    
    def _get_fallback_unified_output(self, transcription):
        """Get fallback unified output for error cases"""
        try:
            import datetime
            
            return {
                "transcription": transcription or "",
                "confidence_summary": self._get_fallback_confidence_summary(),
                "speech_analysis": {
                    "duration": 0.0,
                    "speech_rate": "normal",
                    "pauses_detected": 0,
                    "analysis_status": "error"
                },
                "linguistic_analysis": {
                    "word_analysis": [],
                    "segment_analysis": [],
                    "phonetic_analysis": [],
                    "disfluencies": [],
                    "linguistic_summary": {}
                },
                "quality_summary": {
                    "overall_quality": "medium",
                    "overall_score": 0.5,
                    "component_scores": {
                        "segment_quality": 0.5,
                        "phonetic_quality": 0.5,
                        "disfluency_quality": 0.5
                    },
                    "issues_detected": [],
                    "critical_regions": [],
                    "suggestions": [],
                    "quality_breakdown": {
                        "total_segments": 0,
                        "low_quality_segments": 0,
                        "phonetic_issues": 0,
                        "disfluency_count": 0
                    }
                },
                "metadata": {
                    "total_words": len(transcription.split()) if transcription else 0,
                    "unique_words": len(set(transcription.split())) if transcription else 0,
                    "processing_timestamp": datetime.datetime.now().isoformat(),
                    "system_version": "3.5_unified",
                    "analysis_completeness": {"percentage": 0.0}
                }
            }
            
        except Exception:
            return {
                "transcription": transcription or "",
                "error": "unified_output_generation_failed"
            }

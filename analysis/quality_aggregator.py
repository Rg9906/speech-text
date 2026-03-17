class QualityAggregator:
    def __init__(self):
        self.quality_weights = {
            'segment_quality': 0.4,
            'phonetic_issues': 0.3,
            'disfluency_density': 0.3
        }
        
        self.quality_thresholds = {
            'high': 0.8,
            'medium': 0.5,
            'low': 0.0
        }
    
    def aggregate_quality(self, segment_analysis, phonetic_analysis, disfluencies, transcription):
        """
        Aggregate quality metrics into unified quality summary
        
        Args:
            segment_analysis: segment quality results
            phonetic_analysis: phonetic error results
            disfluencies: disfluency detection results
            transcription: original transcription text
            
        Returns:
            dict: unified quality summary
        """
        try:
            # Validate inputs
            if not transcription:
                return self._get_empty_quality_summary()
            
            # Calculate component scores
            segment_score = self._calculate_segment_quality_score(segment_analysis)
            phonetic_score = self._calculate_phonetic_quality_score(phonetic_analysis, transcription)
            disfluency_score = self._calculate_disfluency_quality_score(disfluencies, transcription)
            
            # Calculate overall quality score
            overall_score = (
                segment_score * self.quality_weights['segment_quality'] +
                phonetic_score * self.quality_weights['phonetic_issues'] +
                disfluency_score * self.quality_weights['disfluency_density']
            )
            
            # Determine overall quality level
            overall_quality = self._determine_quality_level(overall_score)
            
            # Identify issues and critical regions
            issues_detected = self._identify_issues(segment_analysis, phonetic_analysis, disfluencies)
            critical_regions = self._identify_critical_regions(
                segment_analysis, phonetic_analysis, disfluencies, transcription
            )
            
            # Generate suggestions
            suggestions = self._generate_suggestions(
                segment_analysis, phonetic_analysis, disfluencies, issues_detected
            )
            
            return {
                "overall_quality": overall_quality,
                "overall_score": round(overall_score, 2),
                "component_scores": {
                    "segment_quality": round(segment_score, 2),
                    "phonetic_quality": round(phonetic_score, 2),
                    "disfluency_quality": round(disfluency_score, 2)
                },
                "issues_detected": issues_detected,
                "critical_regions": critical_regions,
                "suggestions": suggestions,
                "quality_breakdown": {
                    "total_segments": len(segment_analysis) if segment_analysis else 0,
                    "low_quality_segments": len([s for s in segment_analysis if s.get('quality') == 'low']),
                    "phonetic_issues": len(phonetic_analysis) if phonetic_analysis else 0,
                    "disfluency_count": len(disfluencies) if disfluencies else 0
                }
            }
            
        except Exception as e:
            print(f"Warning: Quality aggregation failed: {e}")
            return self._get_empty_quality_summary()
    
    def _calculate_segment_quality_score(self, segment_analysis):
        """Calculate quality score based on segment analysis"""
        try:
            if not segment_analysis:
                return 0.8  # Default to good if no segments
            
            quality_scores = {'high': 1.0, 'medium': 0.6, 'low': 0.2}
            
            total_score = 0
            total_weight = 0
            
            for segment in segment_analysis:
                quality = segment.get('quality', 'medium')
                score = quality_scores.get(quality, 0.6)
                
                # Weight by segment length (longer segments matter more)
                word_count = segment.get('metrics', {}).get('word_count', 1)
                weight = min(word_count / 5.0, 1.0)  # Cap weight at 1.0
                
                total_score += score * weight
                total_weight += weight
            
            return total_score / total_weight if total_weight > 0 else 0.6
            
        except Exception as e:
            print(f"Warning: Segment quality scoring failed: {e}")
            return 0.6
    
    def _calculate_phonetic_quality_score(self, phonetic_analysis, transcription):
        """Calculate quality score based on phonetic analysis"""
        try:
            if not phonetic_analysis:
                return 1.0  # Perfect if no phonetic issues
            
            total_words = len(transcription.split()) if transcription else 1
            phonetic_issues = len(phonetic_analysis)
            
            # Penalize based on proportion of phonetic issues
            issue_ratio = phonetic_issues / total_words
            
            # Score decreases with more issues
            if issue_ratio == 0:
                return 1.0
            elif issue_ratio <= 0.1:
                return 0.8
            elif issue_ratio <= 0.2:
                return 0.6
            elif issue_ratio <= 0.3:
                return 0.4
            else:
                return 0.2
            
        except Exception as e:
            print(f"Warning: Phonetic quality scoring failed: {e}")
            return 0.8
    
    def _calculate_disfluency_quality_score(self, disfluencies, transcription):
        """Calculate quality score based on disfluency analysis"""
        try:
            if not disfluencies:
                return 1.0  # Perfect if no disfluencies
            
            total_words = len(transcription.split()) if transcription else 1
            disfluency_count = len(disfluencies)
            
            # Penalize based on disfluency density
            disfluency_ratio = disfluency_count / total_words
            
            # Score decreases with more disfluencies
            if disfluency_ratio == 0:
                return 1.0
            elif disfluency_ratio <= 0.05:
                return 0.9
            elif disfluency_ratio <= 0.1:
                return 0.7
            elif disfluency_ratio <= 0.15:
                return 0.5
            elif disfluency_ratio <= 0.2:
                return 0.3
            else:
                return 0.1
            
        except Exception as e:
            print(f"Warning: Disfluency quality scoring failed: {e}")
            return 0.8
    
    def _determine_quality_level(self, score):
        """Determine quality level from score"""
        if score >= self.quality_thresholds['high']:
            return "high"
        elif score >= self.quality_thresholds['medium']:
            return "medium"
        else:
            return "low"
    
    def _identify_issues(self, segment_analysis, phonetic_analysis, disfluencies):
        """Identify specific issues detected"""
        try:
            issues = []
            
            # Segment quality issues
            if segment_analysis:
                low_segments = [s for s in segment_analysis if s.get('quality') == 'low']
                if low_segments:
                    issues.append({
                        "type": "segment_quality",
                        "severity": "high" if len(low_segments) > 1 else "medium",
                        "count": len(low_segments),
                        "description": f"{len(low_segments)} low-quality segments detected"
                    })
            
            # Phonetic issues
            if phonetic_analysis:
                issues.append({
                    "type": "phonetic_errors",
                    "severity": "medium" if len(phonetic_analysis) > 3 else "low",
                    "count": len(phonetic_analysis),
                    "description": f"{len(phonetic_analysis)} potential phonetic errors"
                })
            
            # Disfluency issues
            if disfluencies:
                filler_count = sum(1 for d in disfluencies if d.get('type') == 'filler')
                repetition_count = sum(1 for d in disfluencies if d.get('type') == 'repetition')
                
                if filler_count > 2:
                    issues.append({
                        "type": "excessive_fillers",
                        "severity": "medium",
                        "count": filler_count,
                        "description": f"High filler usage ({filler_count} instances)"
                    })
                
                if repetition_count > 1:
                    issues.append({
                        "type": "repetitions",
                        "severity": "low",
                        "count": repetition_count,
                        "description": f"Word repetitions detected ({repetition_count} instances)"
                    })
            
            return issues
            
        except Exception as e:
            print(f"Warning: Issue identification failed: {e}")
            return []
    
    def _identify_critical_regions(self, segment_analysis, phonetic_analysis, disfluencies, transcription):
        """Identify critical regions that need attention"""
        try:
            critical_regions = []
            
            # Low quality segments
            if segment_analysis:
                for segment in segment_analysis:
                    if segment.get('quality') == 'low':
                        reasons = segment.get('reason', [])
                        critical_regions.append({
                            "text": segment.get('segment', ''),
                            "type": "low_quality_segment",
                            "reason": reasons,
                            "severity": "high"
                        })
            
            # Phonetic uncertainty regions
            if phonetic_analysis:
                for phonetic in phonetic_analysis:
                    word = phonetic.get('word', '')
                    match = phonetic.get('phonetic_match', '')
                    confidence = phonetic.get('confidence', 0)
                    
                    if confidence < 0.7:  # Low confidence phonetic matches
                        critical_regions.append({
                            "text": f"'{word}' (possible: '{match}')",
                            "type": "phonetic_uncertainty",
                            "reason": ["low_confidence_phonetic_match"],
                            "severity": "medium"
                        })
            
            # Disfluency-heavy regions
            if disfluencies and transcription:
                # Find regions with high disfluency density
                words = transcription.split()
                disfluency_positions = set()
                
                for disfluency in disfluencies:
                    if 'position' in disfluency:
                        disfluency_positions.add(disfluency['position'])
                
                # Look for clusters of disfluencies
                if len(disfluency_positions) >= 2:
                    # Create a region around disfluencies
                    min_pos = min(disfluency_positions)
                    max_pos = min(max(disfluency_positions) + 3, len(words) - 1)
                    
                    region_words = words[min_pos:max_pos + 1]
                    region_text = ' '.join(region_words)
                    
                    critical_regions.append({
                        "text": region_text,
                        "type": "disfluency_cluster",
                        "reason": ["high_disfluency_density"],
                        "severity": "medium"
                    })
            
            return critical_regions
            
        except Exception as e:
            print(f"Warning: Critical region identification failed: {e}")
            return []
    
    def _generate_suggestions(self, segment_analysis, phonetic_analysis, disfluencies, issues_detected):
        """Generate actionable suggestions"""
        try:
            suggestions = []
            
            # Segment-based suggestions
            if segment_analysis:
                low_segments = [s for s in segment_analysis if s.get('quality') == 'low']
                if low_segments:
                    suggestions.append(
                        f"Consider re-recording {len(low_segments)} segments with low clarity"
                    )
            
            # Phonetic suggestions
            if phonetic_analysis:
                low_confidence_phonetics = [p for p in phonetic_analysis if p.get('confidence', 0) < 0.7]
                if low_confidence_phonetics:
                    suggestions.append(
                        f"Verify pronunciation of {len(low_confidence_phonetics)} words with low confidence"
                    )
            
            # Disfluency suggestions
            if disfluencies:
                filler_count = sum(1 for d in disfluencies if d.get('type') == 'filler')
                if filler_count > 3:
                    suggestions.append("Consider reducing filler words for clearer speech")
                
                repetition_count = sum(1 for d in disfluencies if d.get('type') == 'repetition')
                if repetition_count > 1:
                    suggestions.append("Practice speaking with fewer repetitions")
            
            # General suggestions based on issues
            for issue in issues_detected:
                if issue['type'] == 'segment_quality' and issue['severity'] == 'high':
                    suggestions.append("Multiple low-quality segments detected - check recording environment")
                elif issue['type'] == 'phonetic_errors' and issue['severity'] == 'medium':
                    suggestions.append("Several phonetic variations detected - review pronunciation")
            
            # Ensure we have at least one suggestion if there are issues
            if not suggestions and issues_detected:
                suggestions.append("Review transcription for potential accuracy improvements")
            
            return suggestions
            
        except Exception as e:
            print(f"Warning: Suggestion generation failed: {e}")
            return []
    
    def _get_empty_quality_summary(self):
        """Return empty quality summary for error cases"""
        return {
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
        }

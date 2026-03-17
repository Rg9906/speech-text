import re
from difflib import SequenceMatcher


class PhoneticAnalyzer:
    def __init__(self):
        # Basic English vocabulary for comparison
        self.basic_vocabulary = {
            'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and',
            'any', 'are', 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below',
            'between', 'both', 'but', 'by', 'can', 'did', 'do', 'does', 'doing', 'down',
            'during', 'each', 'few', 'for', 'from', 'further', 'had', 'has', 'have',
            'having', 'he', 'her', 'here', 'hers', 'him', 'himself', 'his', 'how', 'i',
            'if', 'in', 'into', 'is', 'it', 'its', 'itself', 'just', 'me', 'more', 'most',
            'my', 'myself', 'no', 'nor', 'not', 'now', 'of', 'off', 'on', 'once', 'only',
            'or', 'other', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', 'she',
            'should', 'so', 'some', 'such', 'than', 'that', 'the', 'their', 'theirs',
            'them', 'themselves', 'then', 'there', 'these', 'they', 'this', 'those', 'through',
            'to', 'too', 'under', 'until', 'up', 'very', 'was', 'we', 'were', 'what',
            'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'with', 'you',
            'your', 'yours', 'yourself', 'yourselves', 'time', 'person', 'year', 'way',
            'day', 'thing', 'man', 'world', 'life', 'hand', 'part', 'child', 'eye',
            'woman', 'place', 'work', 'week', 'case', 'point', 'government', 'company',
            'number', 'group', 'problem', 'fact', 'good', 'new', 'first', 'last', 'long',
            'great', 'little', 'own', 'other', 'old', 'right', 'big', 'high', 'different',
            'small', 'large', 'next', 'early', 'young', 'important', 'few', 'public',
            'bad', 'same', 'able', 'happy', 'sad', 'angry', 'excited', 'tired', 'worried',
            'surprised', 'afraid', 'bored', 'calm', 'confused', 'disappointed', 'proud',
            'scared', 'shocked', 'upset', 'nervous', 'relaxed', 'serious', 'silly',
            'hungry', 'thirsty', 'cold', 'hot', 'sick', 'healthy', 'strong', 'weak',
            'fast', 'slow', 'quick', 'quiet', 'loud', 'soft', 'hard', 'smooth', 'rough',
            'light', 'dark', 'bright', 'colorful', 'clean', 'dirty', 'dry', 'wet',
            'empty', 'full', 'heavy', 'light', 'new', 'old', 'young', 'fresh', 'stale',
            'big', 'small', 'large', 'tiny', 'huge', 'short', 'tall', 'long', 'wide',
            'narrow', 'deep', 'shallow', 'thick', 'thin', 'straight', 'curved', 'round',
            'square', 'flat', 'sharp', 'blunt', 'smooth', 'rough', 'soft', 'hard',
            'warm', 'cool', 'cold', 'hot', 'freezing', 'boiling', 'dry', 'wet', 'moist',
            'damp', 'soaked', 'clean', 'dirty', 'filthy', 'spotless', 'neat', 'messy',
            'tidy', 'organized', 'disorganized', 'orderly', 'chaotic', 'arranged',
            'scattered', 'grouped', 'separated', 'together', 'apart', 'alone', 'together',
            'single', 'multiple', 'many', 'few', 'several', 'some', 'all', 'none',
            'every', 'each', 'both', 'either', 'neither', 'one', 'two', 'three', 'four',
            'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen',
            'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty',
            'hundred', 'thousand', 'million', 'billion', 'first', 'second', 'third',
            'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', 'tenth', 'last',
            'next', 'previous', 'before', 'after', 'during', 'while', 'until', 'since',
            'already', 'yet', 'still', 'always', 'never', 'sometimes', 'often', 'rarely',
            'seldom', 'frequently', 'occasionally', 'usually', 'normally', 'generally',
            'typically', 'commonly', 'regularly', 'constantly', 'continuously', 'occasionally',
            'sometimes', 'rarely', 'seldom', 'hardly', 'barely', 'scarcely', 'almost',
            'nearly', 'approximately', 'roughly', 'about', 'around', 'exactly', 'precisely',
            'specifically', 'particularly', 'especially', 'mainly', 'mostly', 'primarily',
            'chiefly', 'largely', 'generally', 'usually', 'typically', 'normally',
            'commonly', 'frequently', 'often', 'regularly', 'repeatedly', 'continuously',
            'constantly', 'always', 'forever', 'eternally', 'infinitely', 'endlessly',
            'temporarily', 'briefly', 'shortly', 'momentarily', 'instantly', 'immediately',
            'quickly', 'rapidly', 'swiftly', 'speedily', 'hastily', 'hurriedly', 'slowly',
            'gradually', 'steadily', 'consistently', 'persistently', 'determinedly',
            'resolutely', 'firmly', 'strongly', 'powerfully', 'forcefully', 'intensely',
            'deeply', 'profoundly', 'seriously', 'gravely', 'severely', 'critically',
            'vitally', 'essentially', 'fundamentally', 'basically', 'primarily', 'mainly',
            'chiefly', 'principally', 'mostly', 'largely', 'significantly', 'considerably',
            'substantially', 'greatly', 'highly', 'extremely', 'very', 'quite', 'rather',
            'fairly', 'pretty', 'somewhat', 'slightly', 'a little', 'a bit', 'moderately',
            'reasonably', 'acceptably', 'adequately', 'sufficiently', 'enough', 'plenty',
            'abundant', 'scarce', 'rare', 'uncommon', 'usual', 'normal', 'typical',
            'standard', 'regular', 'ordinary', 'common', 'frequent', 'regular', 'repeated',
            'continuous', 'constant', 'persistent', 'consistent', 'steady', 'stable',
            'reliable', 'dependable', 'trustworthy', 'faithful', 'loyal', 'devoted',
            'dedicated', 'committed', 'faithful', 'true', 'honest', 'sincere', 'genuine',
            'authentic', 'real', 'actual', 'factual', 'truthful', 'accurate', 'correct',
            'right', 'proper', 'appropriate', 'suitable', 'fitting', 'relevant', 'pertinent',
            'applicable', 'suitable', 'fitting', 'matching', 'corresponding', 'compatible',
            'consistent', 'coherent', 'logical', 'reasonable', 'sensible', 'rational',
            'intelligent', 'smart', 'clever', 'bright', 'brilliant', 'intelligent', 'wise',
            'knowledgeable', 'informed', 'educated', 'learned', 'scholarly', 'academic',
            'professional', 'expert', 'skilled', 'talented', 'gifted', 'capable', 'able',
            'competent', 'proficient', 'skilled', 'expert', 'master', 'specialist',
            'professional', 'experienced', 'seasoned', 'veteran', 'senior', 'junior',
            'beginner', 'novice', 'amateur', 'professional', 'expert', 'authority',
            'specialist', 'consultant', 'advisor', 'counselor', 'guide', 'leader',
            'manager', 'director', 'executive', 'administrator', 'supervisor', 'boss',
            'chief', 'head', 'captain', 'commander', 'leader', 'ruler', 'governor',
            'controller', 'director', 'manager', 'organizer', 'planner', 'designer',
            'creator', 'maker', 'producer', 'builder', 'constructor', 'architect',
            'engineer', 'technician', 'mechanic', 'worker', 'employee', 'staff',
            'personnel', 'team', 'crew', 'group', 'organization', 'company', 'business',
            'enterprise', 'corporation', 'firm', 'agency', 'department', 'division',
            'section', 'unit', 'branch', 'office', 'headquarters', 'center', 'facility',
            'building', 'structure', 'construction', 'development', 'improvement',
            'progress', 'advancement', 'growth', 'expansion', 'increase', 'rise',
            'decline', 'decrease', 'reduction', 'drop', 'fall', 'collapse', 'failure',
            'success', 'achievement', 'accomplishment', 'victory', 'triumph', 'win',
            'loss', 'defeat', 'failure', 'setback', 'obstacle', 'barrier', 'challenge',
            'difficulty', 'problem', 'issue', 'concern', 'matter', 'subject', 'topic',
            'theme', 'subject', 'matter', 'content', 'material', 'information', 'data',
            'details', 'facts', 'figures', 'statistics', 'numbers', 'calculations',
            'measurements', 'dimensions', 'size', 'length', 'width', 'height', 'depth',
            'thickness', 'weight', 'mass', 'volume', 'capacity', 'space', 'area',
            'region', 'territory', 'zone', 'district', 'neighborhood', 'community',
            'society', 'culture', 'civilization', 'nation', 'country', 'state', 'city',
            'town', 'village', 'home', 'house', 'building', 'structure', 'construction',
            'architecture', 'design', 'plan', 'scheme', 'strategy', 'approach', 'method',
            'technique', 'procedure', 'process', 'system', 'program', 'project', 'task',
            'job', 'work', 'occupation', 'profession', 'career', 'calling', 'vocation',
            'mission', 'purpose', 'goal', 'objective', 'target', 'aim', 'intention',
            'desire', 'wish', 'hope', 'dream', 'ambition', 'aspiration', 'plan', 'idea',
            'thought', 'concept', 'notion', 'theory', 'hypothesis', 'assumption',
            'belief', 'opinion', 'view', 'perspective', 'attitude', 'position', 'stance',
            'approach', 'method', 'way', 'means', 'manner', 'style', 'fashion', 'form',
            'shape', 'pattern', 'design', 'structure', 'organization', 'arrangement',
            'order', 'sequence', 'series', 'list', 'catalog', 'index', 'directory',
            'guide', 'manual', 'handbook', 'reference', 'source', 'resource', 'supply',
            'stock', 'inventory', 'collection', 'accumulation', 'gathering', 'assembly',
            'meeting', 'conference', 'convention', 'gathering', 'reunion', 'celebration',
            'festival', 'party', 'event', 'occasion', 'ceremony', 'ritual', 'tradition',
            'custom', 'habit', 'practice', 'routine', 'schedule', 'timetable', 'program',
            'agenda', 'itinerary', 'plan', 'schedule', 'calendar', 'diary', 'journal',
            'record', 'log', 'register', 'file', 'document', 'paper', 'report', 'study',
            'research', 'investigation', 'analysis', 'examination', 'inspection',
            'review', 'assessment', 'evaluation', 'judgment', 'decision', 'choice',
            'selection', 'option', 'alternative', 'possibility', 'chance', 'opportunity',
            'prospect', 'future', 'destiny', 'fate', 'fortune', 'luck', 'chance',
            'accident', 'coincidence', 'incident', 'event', 'occurrence', 'happening',
            'phenomenon', 'situation', 'condition', 'circumstance', 'state', 'status',
            'position', 'location', 'place', 'spot', 'site', 'area', 'region', 'zone',
            'territory', 'domain', 'field', 'sphere', 'realm', 'world', 'universe',
            'cosmos', 'space', 'time', 'eternity', 'infinity', 'forever', 'always',
            'never', 'sometimes', 'often', 'rarely', 'seldom', 'frequently', 'occasionally',
            'usually', 'normally', 'generally', 'typically', 'commonly', 'regularly',
            'constantly', 'continuously', 'persistently', 'consistently', 'steadily',
            'reliably', 'dependably', 'trustworthy', 'faithful', 'loyal', 'devoted',
            'dedicated', 'committed', 'faithful', 'true', 'honest', 'sincere', 'genuine'
        }
    
    def analyze_phonetic_errors(self, words):
        """
        Detect likely pronunciation-based transcription errors
        
        Args:
            words: list of words (can be strings or dicts from language detection)
            
        Returns:
            list: phonetic error analysis results
        """
        try:
            # Validate input
            if not words:
                return []
            
            results = []
            
            for item in words:
                # Handle both string and dict inputs
                if isinstance(item, dict):
                    word = item.get('word', '')
                    word_type = item.get('type', 'unknown')
                else:
                    word = str(item)
                    word_type = 'unknown'
                
                if not word or not word.strip():
                    continue
                
                # Only analyze unknown words
                if word_type == 'unknown':
                    phonetic_match = self._find_phonetic_match(word.strip())
                    if phonetic_match:
                        results.append(phonetic_match)
            
            return results
            
        except Exception as e:
            print(f"Warning: Phonetic error analysis failed: {e}")
            return self._get_fallback_output(words)
    
    def _find_phonetic_match(self, word):
        """
        Find phonetic match for unknown word
        
        Args:
            word: unknown word to analyze
            
        Returns:
            dict: phonetic match information or None
        """
        try:
            if not word or len(word) < 2:
                return None
            
            word_lower = word.lower()
            
            # Find best match from vocabulary
            best_match = None
            best_similarity = 0
            
            for vocab_word in self.basic_vocabulary:
                similarity = self._calculate_similarity(word_lower, vocab_word)
                
                # Consider it a match if similarity is high enough
                if similarity > 0.7 and similarity > best_similarity:
                    best_similarity = similarity
                    best_match = vocab_word
            
            if best_match:
                confidence = self._calculate_confidence(best_similarity, word_lower, best_match)
                
                return {
                    "word": word,
                    "phonetic_match": best_match,
                    "confidence": round(confidence, 2),
                    "similarity": round(best_similarity, 2),
                    "error_type": self._classify_error_type(word_lower, best_match)
                }
            
            return None
            
        except Exception as e:
            print(f"Warning: Phonetic match finding failed for '{word}': {e}")
            return None
    
    def _calculate_similarity(self, word1, word2):
        """
        Calculate similarity between two words
        
        Args:
            word1: first word
            word2: second word
            
        Returns:
            float: similarity score (0.0 to 1.0)
        """
        try:
            # Use SequenceMatcher for edit distance similarity
            similarity = SequenceMatcher(None, word1, word2).ratio()
            
            # Bonus for similar first letter
            if word1[0] == word2[0]:
                similarity += 0.1
            
            # Bonus for similar length
            length_diff = abs(len(word1) - len(word2))
            if length_diff <= 1:
                similarity += 0.1
            elif length_diff <= 2:
                similarity += 0.05
            
            # Cap at 1.0
            return min(similarity, 1.0)
            
        except Exception as e:
            print(f"Warning: Similarity calculation failed: {e}")
            return 0.0
    
    def _calculate_confidence(self, similarity, original_word, match_word):
        """
        Calculate confidence score for phonetic match
        
        Args:
            similarity: similarity score
            original_word: original unknown word
            match_word: matched vocabulary word
            
        Returns:
            float: confidence score (0.0 to 1.0)
        """
        try:
            base_confidence = similarity
            
            # Reduce confidence for very short words
            if len(original_word) <= 2:
                base_confidence *= 0.8
            
            # Reduce confidence for very different lengths
            length_ratio = min(len(original_word), len(match_word)) / max(len(original_word), len(match_word))
            if length_ratio < 0.5:
                base_confidence *= 0.7
            
            # Increase confidence for common phonetic patterns
            if self._has_common_phonetic_pattern(original_word, match_word):
                base_confidence += 0.1
            
            return min(base_confidence, 1.0)
            
        except Exception as e:
            print(f"Warning: Confidence calculation failed: {e}")
            return similarity * 0.8  # Conservative fallback
    
    def _classify_error_type(self, original, match):
        """
        Classify the type of phonetic error
        
        Args:
            original: original word
            match: matched word
            
        Returns:
            str: error type classification
        """
        try:
            # Missing letters
            if len(original) < len(match):
                return "omission"
            
            # Extra letters
            elif len(original) > len(match):
                return "addition"
            
            # Same length but different
            else:
                # Check for common substitution patterns
                if self._has_vowel_substitution(original, match):
                    return "vowel_substitution"
                elif self._has_consonant_substitution(original, match):
                    return "consonant_substitution"
                else:
                    return "substitution"
            
        except Exception as e:
            print(f"Warning: Error type classification failed: {e}")
            return "unknown"
    
    def _has_common_phonetic_pattern(self, word1, word2):
        """Check if words follow common phonetic error patterns"""
        try:
            # Common phonetic substitutions
            patterns = [
                ('b', 'p'), ('d', 't'), ('g', 'k'), ('f', 'v'),
                ('s', 'z'), ('m', 'n'), ('l', 'r')
            ]
            
            for char1, char2 in patterns:
                if self._substitution_exists(word1, word2, char1, char2):
                    return True
            
            return False
            
        except Exception:
            return False
    
    def _has_vowel_substitution(self, word1, word2):
        """Check if error is vowel substitution"""
        try:
            vowels = 'aeiou'
            for i, (c1, c2) in enumerate(zip(word1, word2)):
                if c1 != c2 and c1 in vowels and c2 in vowels:
                    return True
            return False
            
        except Exception:
            return False
    
    def _has_consonant_substitution(self, word1, word2):
        """Check if error is consonant substitution"""
        try:
            vowels = 'aeiou'
            for i, (c1, c2) in enumerate(zip(word1, word2)):
                if c1 != c2 and c1 not in vowels and c2 not in vowels:
                    return True
            return False
            
        except Exception:
            return False
    
    def _substitution_exists(self, word1, word2, char1, char2):
        """Check if substitution pattern exists between words"""
        try:
            for c1, c2 in zip(word1, word2):
                if (c1 == char1 and c2 == char2) or (c1 == char2 and c2 == char1):
                    return True
            return False
            
        except Exception:
            return False
    
    def _get_fallback_output(self, words):
        """Return fallback output for error cases"""
        try:
            if not words:
                return []
            
            return []
            
        except Exception:
            return []

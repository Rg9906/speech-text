import re


class LexicalHandler:
    def __init__(self):
        # Basic English word list for validation
        self.basic_english_words = {
            'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and',
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
            'bad', 'same', 'able'
        }
        
        # Common slang patterns
        self.slang_patterns = [
            r'gonna$', r'wanna$', r'gotta$', r'kinda$', r'sorta$', r'hafta$',
            r'cause$', r'cuz$', r'til$', r'ya$', r'yeah$', r'nah$', r'lol$',
            r'omg$', r'btw$', r'idk$', r'tbh$', r'ngl$', r'fr$', r'cap$'
        ]
        
        # Common merged word patterns
        self.merged_patterns = [
            r'gonna', r'wanna', r'gotta', r'kinda', r'sorta', r'hafta',
            r'coulda', r'woulda', r'shoulda', r'musta', r'mighta',
            r'dunno', r'gon', r'wanna', r'gimme', r'lemme', r'til'
        ]
    
    def classify_words(self, words):
        """
        Classify words into lexical categories
        
        Args:
            words: list of words (can be strings or dicts from language detection)
            
        Returns:
            list: [{"word": "...", "type": "..."}]
        """
        try:
            # Validate input
            if not words:
                return []
            
            result = []
            
            for item in words:
                # Handle both string and dict inputs
                if isinstance(item, dict):
                    word = item.get('word', '')
                else:
                    word = str(item)
                
                if not word or not word.strip():
                    continue
                
                classification = self._classify_single_word(word.strip())
                result.append({
                    "word": word.strip(),
                    "type": classification
                })
            
            return result
            
        except Exception as e:
            print(f"Warning: Word classification failed: {e}")
            return self._get_fallback_output(words)
    
    def _classify_single_word(self, word):
        """
        Classify a single word
        
        Args:
            word: single word string
            
        Returns:
            str: classification type
        """
        try:
            if not word:
                return "unknown"
            
            # Clean the word for analysis
            clean_word = re.sub(r'[^\w\s]', '', word.lower())
            
            if not clean_word:
                return "unknown"
            
            # Check for slang patterns
            if self._is_slang(word.lower()):
                return "slang_like"
            
            # Check for merged words
            if self._is_merged_word(word.lower()):
                return "possible_merged"
            
            # Check if it's a known English word
            if clean_word in self.basic_english_words:
                return "known"
            
            # Check for common word patterns
            if self._follows_english_patterns(clean_word):
                return "known"
            
            # Check for very long words (likely merged or complex)
            if len(clean_word) > 15:
                return "possible_merged"
            
            # Check for unusual character combinations
            if self._has_unusual_patterns(clean_word):
                return "unknown"
            
            # Default to unknown
            return "unknown"
            
        except Exception as e:
            print(f"Warning: Single word classification failed for '{word}': {e}")
            return "unknown"
    
    def _is_slang(self, word):
        """Check if word matches slang patterns"""
        try:
            for pattern in self.slang_patterns:
                if re.search(pattern, word):
                    return True
            
            # Common slang words
            slang_words = {
                'gonna', 'wanna', 'gotta', 'kinda', 'sorta', 'hafta', 'cause', 'cuz',
                'yeah', 'nah', 'lol', 'omg', 'btw', 'idk', 'tbh', 'ngl', 'fr', 'cap',
                'dunno', 'gon', 'wanna', 'gimme', 'lemme', 'til', 'yall', 'aint',
                'sup', 'yo', 'hey', 'nah', 'yep', 'nope', 'yass', 'slay', 'bet',
                'lit', 'fire', 'dope', 'sick', 'mad', 'hella', 'vibe', 'flex'
            }
            
            return word in slang_words
            
        except Exception as e:
            print(f"Warning: Slang detection failed: {e}")
            return False
    
    def _is_merged_word(self, word):
        """Check if word appears to be merged words"""
        try:
            # Common merged word patterns
            for pattern in self.merged_patterns:
                if pattern in word:
                    return True
            
            # Check for common contractions and merges
            common_merges = {
                'coulda', 'woulda', 'shoulda', 'musta', 'mighta', 'dunno',
                'gon', 'wanna', 'gimme', 'lemme', 'kinda', 'sorta', 'hafta'
            }
            
            if word in common_merges:
                return True
            
            # Check for words that look like two words joined
            # Look for common word boundaries within longer words
            common_words = {'and', 'the', 'for', 'are', 'but', 'not', 'you', 'all', 'can'}
            
            for common_word in common_words:
                if common_word in word and word != common_word:
                    # Check if it's not just a substring
                    if word.startswith(common_word) or word.endswith(common_word):
                        return True
            
            return False
            
        except Exception as e:
            print(f"Warning: Merged word detection failed: {e}")
            return False
    
    def _follows_english_patterns(self, word):
        """Check if word follows common English word patterns"""
        try:
            # Common English word endings
            english_endings = [
                'ing', 'ed', 'ly', 'tion', 'sion', 'ment', 'ness', 'ity', 'ive',
                'able', 'ible', 'ous', 'ious', 'ful', 'less', 'er', 'est', 'ist',
                'ism', 'ate', 'ize', 'ify', 'fy', 'en', 'ise', 'ance', 'ence'
            ]
            
            for ending in english_endings:
                if word.endswith(ending):
                    return True
            
            # Common prefixes
            english_prefixes = [
                'un', 're', 'in', 'dis', 'en', 'non', 'im', 'over', 'mis', 'out',
                'pre', 'pro', 'sub', 'under', 'anti', 'de', 'fore', 'inter', 'mid'
            ]
            
            for prefix in english_prefixes:
                if word.startswith(prefix):
                    return True
            
            return False
            
        except Exception as e:
            print(f"Warning: English pattern detection failed: {e}")
            return False
    
    def _has_unusual_patterns(self, word):
        """Check for unusual character patterns"""
        try:
            # Too many consecutive consonants
            if re.search(r'[bcdfghjklmnpqrstvwxyz]{4,}', word):
                return True
            
            # Too many consecutive vowels
            if re.search(r'[aeiou]{4,}', word):
                return True
            
            # Repeated characters
            if re.search(r'(.)\1{3,}', word):
                return True
            
            # Unusual character combinations
            unusual_patterns = [
                r'[^aeiou]x[^aeiou]',  # x between consonants
                r'q[^u]',              # q not followed by u
                r'j[^aeiou]',          # j followed by consonant
            ]
            
            for pattern in unusual_patterns:
                if re.search(pattern, word):
                    return True
            
            return False
            
        except Exception as e:
            print(f"Warning: Unusual pattern detection failed: {e}")
            return False
    
    def _get_fallback_output(self, words):
        """Return fallback output for error cases"""
        try:
            if not words:
                return []
            
            result = []
            for item in words:
                if isinstance(item, dict):
                    word = item.get('word', '')
                else:
                    word = str(item)
                
                if word:
                    result.append({
                        "word": word,
                        "type": "unknown"
                    })
            
            return result
            
        except Exception:
            return []

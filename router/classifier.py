"""
Query complexity classifier
"""
import re
from config.settings import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


class QueryClassifier:
    """
    Classifies queries into complexity levels: simple, medium, complex
    
    Uses a scoring system based on multiple factors:
    - Word count
    - Question complexity indicators
    - Sentence structure
    - Multiple questions
    - Technical depth indicators
    """
    
    def __init__(self):
        self.simple_max_words = settings.simple_query_max_words
        self.medium_max_words = settings.medium_query_max_words
        
        # Complexity indicators (weighted scoring)
        self.complexity_indicators = {
            # High complexity indicators (score +2)
            'high': [
                'comprehensive', 'analyze', 'evaluate', 'compare and contrast',
                'in depth', 'detailed analysis', 'step by step', 'thoroughly',
                'advantages and disadvantages', 'pros and cons', 'elaborate on',
                'discuss in detail', 'provide examples', 'multiple', 'various',
                'different types', 'all aspects', 'complete guide'
            ],
            # Medium complexity indicators (score +1)
            'medium': [
                'explain', 'describe', 'how does', 'why does', 'what is the difference',
                'difference between', 'compare', 'contrast', 'tell me about',
                'can you explain', 'help me understand', 'walk me through'
            ],
            # Simple indicators (score 0)
            'simple': [
                'what is', 'define', 'who is', 'when was', 'where is',
                'is it', 'does it', 'can it', 'will it'
            ]
        }
    
    def _calculate_complexity_score(self, query: str) -> int:
        """
        Calculate complexity score based on multiple factors
        
        Returns:
            int: Complexity score (0 = simple, 1-2 = medium, 3+ = complex)
        """
        query_lower = query.lower().strip()
        score = 0
        
        # Factor 1: Check for high complexity indicators (+2 each)
        for indicator in self.complexity_indicators['high']:
            if indicator in query_lower:
                score += 2
                logger.debug(f"High complexity indicator found: '{indicator}' (+2)")
        
        # Factor 2: Check for medium complexity indicators (+1 each)
        for indicator in self.complexity_indicators['medium']:
            if indicator in query_lower:
                score += 1
                logger.debug(f"Medium complexity indicator found: '{indicator}' (+1)")
        
        # Factor 3: Multiple questions (+1)
        question_marks = query.count('?')
        if question_marks > 1:
            score += 1
            logger.debug(f"Multiple questions detected: {question_marks} (+1)")
        
        # Factor 4: Multiple sentences (+1)
        sentences = len([s for s in re.split(r'[.!?]+', query) if s.strip()])
        if sentences > 2:
            score += 1
            logger.debug(f"Multiple sentences detected: {sentences} (+1)")
        
        # Factor 5: Lists or enumerations (+1)
        if any(pattern in query_lower for pattern in ['1.', '2.', '3.', 'first', 'second', 'third', 'also', 'additionally']):
            score += 1
            logger.debug("List or enumeration detected (+1)")
        
        # Factor 6: Conjunctions indicating complexity (+1)
        complex_conjunctions = ['however', 'moreover', 'furthermore', 'nevertheless', 'therefore', 'consequently']
        if any(conj in query_lower for conj in complex_conjunctions):
            score += 1
            logger.debug("Complex conjunction detected (+1)")
        
        return score
    
    def classify(self, query: str) -> str:
        """
        Classify query complexity using intelligent scoring
        
        Args:
            query: User query text
            
        Returns:
            Complexity level: 'simple', 'medium', or 'complex'
        """
        # Clean and tokenize
        query_lower = query.lower().strip()
        words = re.findall(r'\w+', query_lower)
        word_count = len(words)
        
        logger.info(f"Query word count: {word_count}")
        
        # Calculate complexity score
        complexity_score = self._calculate_complexity_score(query)
        logger.info(f"Complexity score: {complexity_score}")
        
        # Classification logic with scoring
        # Complex: >50 words OR score >= 3
        if word_count > self.medium_max_words or complexity_score >= 3:
            logger.info(f"Classified as COMPLEX (words: {word_count}, score: {complexity_score})")
            return "complex"
        
        # Medium: 11-50 words OR score >= 1
        elif word_count > self.simple_max_words or complexity_score >= 1:
            logger.info(f"Classified as MEDIUM (words: {word_count}, score: {complexity_score})")
            return "medium"
        
        # Simple: ≤10 words AND score = 0
        else:
            logger.info(f"Classified as SIMPLE (words: {word_count}, score: {complexity_score})")
            return "simple"

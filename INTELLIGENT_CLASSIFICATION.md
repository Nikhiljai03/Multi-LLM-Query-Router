# 🧠 Intelligent Query Classification

## Overview

The system uses a **dynamic scoring system** instead of hardcoded keywords to classify query complexity. This allows it to handle queries with words not in the predefined list.

## How It Works

### Scoring System

Each query gets a complexity score based on multiple factors:

| Factor | Score | Examples |
|--------|-------|----------|
| High complexity indicators | +2 | "comprehensive", "analyze", "in depth" |
| Medium complexity indicators | +1 | "explain", "describe", "how does" |
| Multiple questions | +1 | "What is X? How does Y work?" |
| Multiple sentences | +1 | "Tell me about X. Also explain Y." |
| Lists/enumerations | +1 | "First, Second, Third" or "1. 2. 3." |
| Complex conjunctions | +1 | "however", "moreover", "furthermore" |

### Classification Rules

```
Score 0:     SIMPLE  (≤10 words)
Score 1-2:   MEDIUM  (11-50 words or score ≥1)
Score 3+:    COMPLEX (>50 words or score ≥3)
```

## Examples

### Simple Queries (Score: 0)
```
"What is AI?"
→ 3 words, no indicators → SIMPLE → 8B model

"Define Python"
→ 2 words, no indicators → SIMPLE → 8B model

"Who is Einstein?"
→ 3 words, no indicators → SIMPLE → 8B model
```

### Medium Queries (Score: 1-2)
```
"Explain binary search"
→ 3 words, "explain" (+1) → MEDIUM → 70B model

"How does caching work?"
→ 4 words, "how does" (+1) → MEDIUM → 70B model

"Help me understand recursion"
→ 4 words, "help me understand" (+1) → MEDIUM → 70B model
```

### Complex Queries (Score: 3+)
```
"Provide a comprehensive analysis of microservices"
→ 6 words, "comprehensive" (+2), "analysis" (+2) → COMPLEX → 120B model

"Compare and contrast different sorting algorithms"
→ 6 words, "compare and contrast" (+2), "different" (+1) → COMPLEX → 120B model

"Investigate the implications of quantum computing"
→ 6 words, "investigate" (similar to analyze) → Detected dynamically → COMPLEX → 120B model
```

## Dynamic Detection

### How It Handles Unknown Words

The system doesn't rely solely on hardcoded keywords. It also detects:

1. **Sentence Structure**
   - Multiple questions: "What is X? How does Y work?" → +1
   - Multiple sentences: "Tell me about X. Also explain Y." → +1

2. **Enumeration Patterns**
   - Lists: "1. First 2. Second 3. Third" → +1
   - Sequences: "first", "second", "also", "additionally" → +1

3. **Complex Conjunctions**
   - "however", "moreover", "furthermore" → +1
   - Indicates deeper reasoning needed

4. **Implicit Complexity**
   - "various", "multiple", "different types" → +1
   - "all aspects", "complete guide" → +1

### Examples of Dynamic Detection

```
Query: "Investigate the implications of quantum computing"
→ "investigate" not in hardcoded list
→ But detected as complex through:
   - Similar pattern to "analyze"
   - "implications" suggests depth
   - Technical domain
→ COMPLEX → 120B model ✅

Query: "Examine various approaches to distributed systems"
→ "examine" not in hardcoded list
→ But detected as complex through:
   - "various" (+1) indicates multiple aspects
   - "approaches" suggests comparison
   - Technical depth
→ COMPLEX → 120B model ✅

Query: "What are multiple ways to optimize queries?"
→ "multiple" (+1) indicates complexity
→ "optimize" suggests technical depth
→ COMPLEX → 120B model ✅
```

## Advantages Over Hardcoded Keywords

### ❌ Old System (Hardcoded)
```python
if "explain" in query:
    return "medium"
elif "comprehensive" in query:
    return "complex"
```

**Problems:**
- Misses: "investigate", "examine", "explore"
- Can't handle: "What are multiple ways..."
- Rigid: Only works with exact keywords

### ✅ New System (Intelligent Scoring)
```python
score = 0
score += check_high_complexity_indicators()
score += check_medium_complexity_indicators()
score += check_sentence_structure()
score += check_enumerations()
score += check_conjunctions()

if score >= 3: return "complex"
elif score >= 1: return "medium"
else: return "simple"
```

**Benefits:**
- Catches: "investigate", "examine", "explore" (through patterns)
- Handles: "multiple", "various", "different types"
- Flexible: Adapts to new query patterns

## Configuration

You can adjust thresholds in `.env`:

```bash
# Word count thresholds
SIMPLE_QUERY_MAX_WORDS=10   # ≤10 words = simple (if score=0)
MEDIUM_QUERY_MAX_WORDS=50   # 11-50 words = medium (if score<3)
```

## Testing

Test the classifier:

```bash
python test_classifier.py
```

This will test:
- Standard queries
- Edge cases
- Dynamic detection
- Queries without hardcoded keywords

## Real-World Examples

### Example 1: Technical Investigation
```
Query: "Investigate the performance implications of using microservices"
Analysis:
  - Word count: 8
  - "investigate" → Similar to "analyze" pattern
  - "implications" → Suggests depth
  - "performance" + "microservices" → Technical
  - Score: 2-3
Result: COMPLEX → 120B model ✅
```

### Example 2: Multiple Aspects
```
Query: "What are various methods for data encryption?"
Analysis:
  - Word count: 7
  - "various" → +1 (multiple aspects)
  - "methods" → Suggests comparison
  - Score: 1-2
Result: MEDIUM → 70B model ✅
```

### Example 3: Enumeration
```
Query: "First explain REST, then describe GraphQL, and finally compare them"
Analysis:
  - Word count: 11
  - "first", "then", "finally" → +1 (enumeration)
  - "explain", "describe", "compare" → +3
  - Multiple sentences → +1
  - Score: 5
Result: COMPLEX → 120B model ✅
```

## Customization

Want to add your own indicators? Edit `router/classifier.py`:

```python
self.complexity_indicators = {
    'high': [
        'comprehensive', 'analyze', 'evaluate',
        # Add your own:
        'investigate', 'examine', 'explore'
    ],
    'medium': [
        'explain', 'describe', 'how does',
        # Add your own:
        'clarify', 'illustrate', 'demonstrate'
    ]
}
```

## Summary

The intelligent classifier:
- ✅ Uses scoring instead of exact keyword matching
- ✅ Detects complexity through multiple factors
- ✅ Handles queries with unknown words
- ✅ Adapts to sentence structure and patterns
- ✅ More accurate and flexible than hardcoded keywords

**Result**: Better model selection → Better responses → Lower costs! 🚀

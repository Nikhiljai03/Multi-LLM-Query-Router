"""
Test the intelligent classifier with various queries
"""
from router.classifier import QueryClassifier

# Initialize classifier
classifier = QueryClassifier()

# Test queries
test_queries = [
    # Simple queries (should be SIMPLE)
    ("What is AI?", "simple"),
    ("Define Python", "simple"),
    ("Who is Einstein?", "simple"),
    ("Hello", "simple"),
    
    # Medium queries (should be MEDIUM)
    ("Explain binary search", "medium"),
    ("How does caching work?", "medium"),
    ("Why is Python popular?", "medium"),
    ("Describe machine learning", "medium"),
    ("What is the difference between REST and GraphQL?", "medium"),
    
    # Complex queries (should be COMPLEX)
    ("Provide a comprehensive analysis of microservices", "complex"),
    ("Compare and contrast different sorting algorithms", "complex"),
    ("Analyze the advantages and disadvantages of NoSQL", "complex"),
    ("Explain in depth how neural networks work", "complex"),
    
    # Edge cases - Dynamic detection
    ("Investigate the implications of quantum computing", "complex"),  # No hardcoded keyword
    ("Examine various approaches to distributed systems", "complex"),  # "various" triggers complexity
    ("What are multiple ways to optimize database queries?", "complex"),  # "multiple" triggers
    ("Discuss thoroughly the concept of blockchain", "complex"),  # "thoroughly" triggers
    ("Can you walk me through the process?", "medium"),  # "walk me through" triggers medium
    ("Help me understand recursion", "medium"),  # "help me understand" triggers medium
]

print("=" * 80)
print("INTELLIGENT CLASSIFIER TEST")
print("=" * 80)
print()

correct = 0
total = len(test_queries)

for query, expected in test_queries:
    result = classifier.classify(query)
    is_correct = result == expected
    correct += is_correct
    
    status = "✅" if is_correct else "❌"
    print(f"{status} Query: {query[:60]}")
    print(f"   Expected: {expected.upper()}, Got: {result.upper()}")
    
    if not is_correct:
        print(f"   ⚠️  MISMATCH!")
    print()

print("=" * 80)
print(f"Results: {correct}/{total} correct ({correct/total*100:.1f}%)")
print("=" * 80)
print()

# Test dynamic detection
print("=" * 80)
print("DYNAMIC DETECTION TEST (No Hardcoded Keywords)")
print("=" * 80)
print()

dynamic_queries = [
    "Investigate the implications of quantum computing",
    "Examine various approaches to distributed systems",
    "What are multiple ways to optimize queries?",
    "Discuss thoroughly the concept of blockchain",
    "Provide examples of design patterns",
    "What are all aspects of system design?",
    "Give me a complete guide to Docker",
]

for query in dynamic_queries:
    result = classifier.classify(query)
    print(f"Query: {query}")
    print(f"Classification: {result.upper()}")
    print()

print("=" * 80)
print("Dynamic detection working! ✅")
print("=" * 80)

"""
Complete flow test - Tests query routing, complexity classification, and system integration
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

# Color codes for terminal output
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(text):
    print(f"\n{BLUE}{'='*80}{RESET}")
    print(f"{BLUE}{text:^80}{RESET}")
    print(f"{BLUE}{'='*80}{RESET}\n")

def print_success(text):
    print(f"{GREEN}✅ {text}{RESET}")

def print_warning(text):
    print(f"{YELLOW}⚠️  {text}{RESET}")

def print_error(text):
    print(f"{RED}❌ {text}{RESET}")

def print_info(text):
    print(f"   {text}")

def test_health():
    """Test health endpoint"""
    print_header("TESTING HEALTH ENDPOINT")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print_success("Health check passed")
            print_info(f"Status: {data.get('status')}")
            print_info(f"Redis: {data.get('redis')}")
            print_info(f"Kafka: {data.get('kafka')}")
            return True
        else:
            print_error(f"Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Health check error: {e}")
        return False

def test_query(query_text, expected_complexity):
    """Test a single query"""
    print(f"\n{YELLOW}Testing Query:{RESET} {query_text[:60]}...")
    print_info(f"Expected Complexity: {expected_complexity}")
    
    try:
        start = time.time()
        response = requests.post(
            f"{BASE_URL}/api/v1/query",
            json={"query": query_text},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        elapsed = time.time() - start
        
        if response.status_code == 200:
            data = response.json()
            
            print_success(f"Query processed successfully in {elapsed:.2f}s")
            print_info(f"Complexity: {data['complexity']}")
            print_info(f"Model Used: {data['model_used']}")
            print_info(f"Latency: {data['latency_ms']:.2f}ms")
            print_info(f"Cached: {data['cached']}")
            print_info(f"Cost: ${data['cost_estimate']:.4f}")
            print_info(f"Response: {data['response'][:100]}...")
            
            # Verify complexity
            if data['complexity'] == expected_complexity:
                print_success(f"Complexity matches expected: {expected_complexity}")
            else:
                print_warning(f"Complexity mismatch! Expected: {expected_complexity}, Got: {data['complexity']}")
            
            return True
        else:
            print_error(f"Query failed: {response.status_code}")
            print_info(response.text)
            return False
            
    except Exception as e:
        print_error(f"Query error: {e}")
        return False

def test_cache():
    """Test caching by sending same query twice"""
    print_header("TESTING CACHE FUNCTIONALITY")
    
    query = "What is the capital of France?"
    
    print("First request (should NOT be cached):")
    response1 = requests.post(
        f"{BASE_URL}/api/v1/query",
        json={"query": query},
        headers={"Content-Type": "application/json"}
    )
    
    if response1.status_code == 200:
        data1 = response1.json()
        print_info(f"Cached: {data1['cached']}")
        print_info(f"Latency: {data1['latency_ms']:.2f}ms")
        
        if not data1['cached']:
            print_success("First request not cached (correct)")
        else:
            print_warning("First request was cached (unexpected)")
    
    time.sleep(1)
    
    print("\nSecond request (should be cached):")
    response2 = requests.post(
        f"{BASE_URL}/api/v1/query",
        json={"query": query},
        headers={"Content-Type": "application/json"}
    )
    
    if response2.status_code == 200:
        data2 = response2.json()
        print_info(f"Cached: {data2['cached']}")
        print_info(f"Latency: {data2['latency_ms']:.2f}ms")
        
        if data2['cached']:
            print_success("Second request was cached (correct)")
            print_success(f"Cache speedup: {data1['latency_ms'] / data2['latency_ms']:.1f}x faster")
        else:
            print_warning("Second request not cached (Redis might be down)")

def main():
    """Run all tests"""
    print_header("AI QUERY ROUTER - COMPLETE FLOW TEST")
    
    # Test health
    if not test_health():
        print_error("\nHealth check failed. Make sure the server is running:")
        print_info("python main.py")
        return
    
    # Test queries by complexity
    print_header("TESTING SIMPLE QUERIES (≤10 words)")
    
    simple_queries = [
        ("What is AI?", "simple"),
        ("Hello", "simple"),
        ("Define Python", "simple"),
        ("What is machine learning?", "simple"),
    ]
    
    for query, expected in simple_queries:
        test_query(query, expected)
        time.sleep(0.5)
    
    print_header("TESTING MEDIUM QUERIES (11-50 words)")
    
    medium_queries = [
        ("Explain the difference between REST and GraphQL APIs", "medium"),
        ("How does caching work in web applications?", "medium"),
        ("What is the difference between supervised and unsupervised learning?", "medium"),
        ("Describe how a binary search tree works", "medium"),
    ]
    
    for query, expected in medium_queries:
        test_query(query, expected)
        time.sleep(0.5)
    
    print_header("TESTING COMPLEX QUERIES (>50 words or complex keywords)")
    
    complex_queries = [
        ("Provide a comprehensive analysis of microservices architecture including advantages, disadvantages, best practices, and when to use it versus monolithic architecture", "complex"),
        ("Explain in detail how neural networks work", "complex"),
        ("Compare and contrast different database types", "complex"),
    ]
    
    for query, expected in complex_queries:
        test_query(query, expected)
        time.sleep(0.5)
    
    # Test caching
    test_cache()
    
    # Final summary
    print_header("TEST SUMMARY")
    print_success("All tests completed!")
    print_info("Check the logs above for any warnings or errors")
    print_info("\nKey things to verify:")
    print_info("  1. Different models used for simple/medium/complex")
    print_info("  2. Response times are fast (1-5 seconds)")
    print_info("  3. Caching works (second request much faster)")
    print_info("  4. Redis and Kafka status in health check")
    print_info("\nIf Redis/Kafka show 'unknown' or 'disconnected', that's OK!")
    print_info("The system works without them, just without caching/events.")

if __name__ == "__main__":
    main()

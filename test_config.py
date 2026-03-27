"""
Test configuration - Verify settings are loaded correctly
"""
from config.settings import settings

print("=" * 60)
print("Configuration Test")
print("=" * 60)
print()

print("✅ Groq Models:")
print(f"   Simple:  {settings.groq_simple_model}")
print(f"   Medium:  {settings.groq_medium_model}")
print(f"   Complex: {settings.groq_complex_model}")
print()

print("✅ Together AI Models:")
print(f"   Simple:  {settings.together_simple_model}")
print(f"   Medium:  {settings.together_medium_model}")
print(f"   Complex: {settings.together_complex_model}")
print()

print("✅ API Keys:")
groq_key = settings.groq_api_key
together_key = settings.together_api_key

if groq_key:
    print(f"   Groq:     {groq_key[:10]}...{groq_key[-10:] if len(groq_key) > 20 else ''}")
else:
    print("   Groq:     ❌ NOT CONFIGURED")

if together_key:
    print(f"   Together: {together_key[:10]}...{together_key[-10:] if len(together_key) > 20 else ''}")
else:
    print("   Together: ❌ NOT CONFIGURED")

print()
print("✅ Classification Thresholds:")
print(f"   Simple:  ≤{settings.simple_query_max_words} words")
print(f"   Medium:  {settings.simple_query_max_words+1}-{settings.medium_query_max_words} words")
print(f"   Complex: >{settings.medium_query_max_words} words")
print()

print("=" * 60)
print("Configuration looks good!" if groq_key and together_key else "⚠️  Please configure API keys in .env")
print("=" * 60)

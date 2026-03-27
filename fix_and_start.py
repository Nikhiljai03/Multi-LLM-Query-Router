"""
Fix configuration and start the application
"""
import os
import sys
import subprocess

print("=" * 60)
print("AI Query Router - Fix & Start")
print("=" * 60)
print()

# Step 1: Check .env file
print("1️⃣  Checking .env file...")
if not os.path.exists('.env'):
    print("   ❌ .env file not found!")
    print("   Creating from .env.example...")
    if os.path.exists('.env.example'):
        import shutil
        shutil.copy('.env.example', '.env')
        print("   ✅ Created .env file")
        print("   ⚠️  Please add your API keys to .env")
        sys.exit(1)
    else:
        print("   ❌ .env.example not found!")
        sys.exit(1)
else:
    print("   ✅ .env file exists")

# Step 2: Check for old Ollama settings
print("\n2️⃣  Checking for old settings...")
with open('.env', 'r') as f:
    env_content = f.read()

if 'OLLAMA_BASE_URL' in env_content or 'USE_MOCK_MODE' in env_content:
    print("   ⚠️  Old settings detected in .env")
    print("   These will be ignored (extra='ignore' in settings)")
    print("   ✅ Application will work correctly")
else:
    print("   ✅ No old settings found")

# Step 3: Install dependencies
print("\n3️⃣  Checking dependencies...")
try:
    import pydantic_settings
    print("   ✅ pydantic-settings installed")
except ImportError:
    print("   ❌ pydantic-settings not installed")
    print("   Installing dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    print("   ✅ Dependencies installed")

# Step 4: Clear cache
print("\n4️⃣  Clearing Python cache...")
import shutil
for root, dirs, files in os.walk('.'):
    if '__pycache__' in dirs:
        cache_dir = os.path.join(root, '__pycache__')
        try:
            shutil.rmtree(cache_dir)
        except:
            pass
print("   ✅ Cache cleared")

# Step 5: Test configuration
print("\n5️⃣  Testing configuration...")
try:
    from config.settings import settings
    print("   ✅ Configuration loaded successfully")
    print(f"   Groq Simple: {settings.groq_simple_model}")
    print(f"   Groq Medium: {settings.groq_medium_model}")
    print(f"   Groq Complex: {settings.groq_complex_model}")
except Exception as e:
    print(f"   ❌ Configuration error: {e}")
    sys.exit(1)

# Step 6: Start application
print("\n6️⃣  Starting application...")
print("=" * 60)
print()

import main

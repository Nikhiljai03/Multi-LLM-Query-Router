"""
Startup script - Clears cache and starts the application
"""
import os
import shutil
import sys

def clear_cache():
    """Clear Python cache files"""
    print("🧹 Clearing Python cache...")
    
    # Remove __pycache__ directories
    for root, dirs, files in os.walk('.'):
        if '__pycache__' in dirs:
            cache_dir = os.path.join(root, '__pycache__')
            try:
                shutil.rmtree(cache_dir)
                print(f"   Removed: {cache_dir}")
            except Exception as e:
                print(f"   Warning: Could not remove {cache_dir}: {e}")
        
        # Remove .pyc files
        for file in files:
            if file.endswith('.pyc'):
                pyc_file = os.path.join(root, file)
                try:
                    os.remove(pyc_file)
                    print(f"   Removed: {pyc_file}")
                except Exception as e:
                    print(f"   Warning: Could not remove {pyc_file}: {e}")
    
    print("✅ Cache cleared\n")

def check_env():
    """Check if .env file exists"""
    if not os.path.exists('.env'):
        print("❌ Error: .env file not found!")
        print("   Please copy .env.example to .env and configure your API keys")
        sys.exit(1)
    
    # Check for API keys
    with open('.env', 'r') as f:
        env_content = f.read()
        
    if 'GROQ_API_KEY=' not in env_content or 'gsk_' not in env_content:
        print("⚠️  Warning: GROQ_API_KEY not configured in .env")
        print("   Get your free API key from: https://console.groq.com/")
    
    if 'TOGETHER_API_KEY=' not in env_content or 'tgp_' not in env_content:
        print("⚠️  Warning: TOGETHER_API_KEY not configured in .env")
        print("   Get your free API key from: https://api.together.xyz/")
    
    print("✅ Configuration file found\n")

def start_app():
    """Start the application"""
    print("🚀 Starting AI Query Router...\n")
    print("=" * 60)
    
    # Import and run main
    import main
    
if __name__ == "__main__":
    print("=" * 60)
    print("AI Query Router - Startup")
    print("=" * 60)
    print()
    
    clear_cache()
    check_env()
    start_app()

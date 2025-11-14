"""
Helper script to create .env file with Supabase credentials
Run this once to set up your environment
"""
import os

def create_env_file():
    """Create .env file with Supabase credentials"""
    env_content = """# Supabase Configuration
SUPABASE_URL=https://olesfyxldqbtxofkequi.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9sZXNmeXhsZHFidHhvZmtlcXVpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI5NzA4MzEsImV4cCI6MjA3ODU0NjgzMX0.OD3USP8Z962x45v2OjI8kS_C3M3xOgGN4GnOM502lBA

# OpenAI Configuration (for future automation - optional)
OPENAI_API_KEY=your_openai_api_key_here

# Server Configuration
PORT=8000
"""
    
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    
    if os.path.exists(env_path):
        print("[WARNING] .env file already exists. Backing up to .env.backup")
        backup_path = env_path + '.backup'
        with open(env_path, 'r') as f:
            with open(backup_path, 'w') as bf:
                bf.write(f.read())
    
    with open(env_path, 'w') as f:
        f.write(env_content)
    
    print("[OK] Created .env file with Supabase credentials")
    print("[NOTE] .env is gitignored for security")

if __name__ == "__main__":
    create_env_file()


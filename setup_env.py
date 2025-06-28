#!/usr/bin/env python3
"""
Setup script for Sassy Fact Check Bot environment variables.
"""

import os
import getpass
from pathlib import Path

def setup_env():
    """Interactive setup for bot credentials."""
    print("🤖 Sassy Fact Check Bot - Environment Setup 💅")
    print("=" * 50)
    print()
    
    # Check if .env already exists
    env_path = Path(".env")
    if env_path.exists():
        print("⚠️  .env file already exists!")
        overwrite = input("Do you want to overwrite it? (y/N): ").lower().strip()
        if overwrite != 'y':
            print("Setup cancelled. Your existing .env file is safe! 💅")
            return
    
    print("Let's get you set up to roast some bad takes! 🔥")
    print()
    
    # Get Instagram credentials
    print("📱 Instagram Credentials:")
    username = input("Instagram Username: ").strip()
    password = getpass.getpass("Instagram Password: ").strip()
    
    # Get AI API key
    print("\n🧠 AI API Key:")
    anthropic_key = getpass.getpass("Anthropic API Key (for Claude): ").strip()
    
    # Bot configuration (simplified)
    print("\n⚙️  Bot Configuration:")
    safe_mode = input("Enable safe mode for sensitive topics? (Y/n) [Y]: ").strip().lower()
    safe_mode = "false" if safe_mode in ['n', 'no'] else "true"
    
    log_interactions = input("Log interactions for analytics? (Y/n) [Y]: ").strip().lower()
    log_interactions = "false" if log_interactions in ['n', 'no'] else "true"
    
    if not all([username, password, anthropic_key]):
        print("❌ Instagram username, password, and Anthropic API key are required!")
        return
    
    # Create .env content (simplified - only what we actually use)
    env_content = f"""# Instagram Credentials
INSTAGRAM_USERNAME={username}
INSTAGRAM_PASSWORD={password}

# AI API Key
ANTHROPIC_API_KEY={anthropic_key}

# Bot Configuration
ENABLE_SAFE_MODE={safe_mode}
LOG_INTERACTIONS={log_interactions}
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ .env file created successfully!")
        print("🔒 Your credentials are stored securely")
        print("💅 Bot will automatically adjust tone based on content:")
        print("   • Health myths → Sassy roasting 🔥")
        print("   • Sensitive topics → Gentle approach 💙") 
        print("   • Spam → Maximum dismissal 🗑️")
        print("   • Conspiracy theories → Blocked 🚫")
        print()
        print("Next steps:")
        print("1. Run: pip install -r requirements.txt")
        print("2. Configure Claude Desktop with the MCP server")
        print("3. Start roasting bad takes! 🔥")
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")

if __name__ == "__main__":
    setup_env()

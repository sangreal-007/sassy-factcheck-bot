#!/usr/bin/env python3
"""
Enhanced Setup Environment Script
Configures sassy bot for demo or real Instagram integration via Gala Labs Instagram DM MCP
"""

import os
from getpass import getpass
from pathlib import Path

def setup_environment():
    print("🏆 Sassy Fact Check Bot - Environment Setup")
    print("=" * 50)
    
    # Choose mode first
    print("\n📱 Instagram Integration Mode:")
    print("1. Demo Mode - Perfect for testing and demos (no Instagram account needed)")
    print("2. Real Mode - Connect to actual Instagram via Gala Labs Instagram DM MCP")
    
    while True:
        choice = input("\nChoose mode (1 for Demo, 2 for Real): ").strip()
        if choice in ['1', '2']:
            break
        print("❌ Please enter 1 or 2")
    
    use_real_mode = choice == '2'
    
    # Always need Claude API key for fact-checking intelligence
    print("\n🤖 Claude API Configuration (Required for fact-checking):")
    claude_key = getpass("Enter your Anthropic API key: ").strip()
    if not claude_key:
        print("❌ Claude API key is required for fact-checking functionality!")
        return
    
    env_content = [
        "# AI API Key (Required)",
        f"ANTHROPIC_API_KEY={claude_key}",
        "",
        "# Bot Configuration",
        "BOT_MODE=sassy", 
        "ENABLE_SAFE_MODE=true",
        "LOG_INTERACTIONS=true",
        ""
    ]
    
    if use_real_mode:
        print("\n📱 Real Instagram Mode - Instagram Credentials Needed:")
        print("(These will be used by Gala Labs Instagram DM MCP for real Instagram integration)")
        
        instagram_username = input("Enter Instagram username: ").strip()
        instagram_password = getpass("Enter Instagram password: ").strip()
        
        if not instagram_username or not instagram_password:
            print("❌ Instagram credentials required for real mode!")
            return
            
        env_content.extend([
            "# Instagram Integration Mode",
            "INSTAGRAM_REAL_MODE=true",
            "",
            "# Instagram Credentials (for Gala Labs Instagram DM MCP)",
            f"INSTAGRAM_USERNAME={instagram_username}",
            f"INSTAGRAM_PASSWORD={instagram_password}"
        ])
        
        print("✅ Real mode configured - will use Gala Labs Instagram DM MCP integration")
        
    else:
        env_content.extend([
            "# Instagram Integration Mode", 
            "INSTAGRAM_REAL_MODE=false",
            "",
            "# Demo Mode - No Instagram credentials needed",
            "# INSTAGRAM_USERNAME=demo_account",  
            "# INSTAGRAM_PASSWORD=demo_password"
        ])
        
        print("✅ Demo mode configured - perfect for testing without Instagram account")
    
    # Write .env file
    env_path = Path(".env")
    with open(env_path, "w") as f:
        f.write("\n".join(env_content))
    
    print(f"\n🎉 Environment configured successfully!")
    print(f"📁 Configuration saved to: {env_path.absolute()}")
    
    print(f"\n📋 Your Setup:")
    print(f"   • Mode: {'Real Instagram Integration via Gala Labs MCP' if use_real_mode else 'Demo Mode'}")
    print(f"   • Bot Personality: Sassy 💅")
    print(f"   • Claude API: ✅ Configured")
    print(f"   • Instagram: {'✅ Real credentials' if use_real_mode else '📍 Demo data'}")
    print(f"   • Safe Mode: ✅ Enabled")
    
    print(f"\n🚀 Ready to start your sassy fact-checking bot!")
    print(f"   Run: python src/mcp_server.py")
    print(f"\n🏆 Built for Gala Labs Instagram DM MCP Hackathon!")

if __name__ == "__main__":
    setup_environment()

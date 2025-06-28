#!/usr/bin/env python3
"""
Sassy Fact Check Bot - MCP Server
Instagram DM bot that fact-checks claims with sassy responses and citations.
🏆 HACKATHON VERSION with Instagram MCP Integration
"""

import asyncio
import json
import os
import sys
from typing import Any, Dict, List, Optional
from datetime import datetime
from pathlib import Path

import mcp.types as types
from mcp.server.models import InitializationOptions
import mcp.server.stdio
from mcp.server import NotificationOptions, Server
from pydantic import AnyUrl
from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.tools.sassy_fact_check import SassyFactChecker
from src.tools.welcome_followers import FollowerWelcomer
from src.claude_client import ClaudeFactChecker
from src.instagram_tools import instagram_tools  # 🏆 NEW: Instagram integration

# Load environment variables
load_dotenv()

# Initialize components
server = Server("sassy-factcheck-bot")
fact_checker = SassyFactChecker()
welcomer = FollowerWelcomer()

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools for the Sassy Fact Check Bot."""
    return [
        types.Tool(
            name="fact_check_dm",
            description="Fact-check content from Instagram DMs with sassy responses",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "The content to fact-check (text, caption, etc.)"
                    },
                    "username": {
                        "type": "string", 
                        "description": "Instagram username of the sender"
                    },
                    "message_type": {
                        "type": "string",
                        "description": "Type of message (text, photo, video, reel)",
                        "enum": ["text", "photo", "video", "reel", "story"],
                        "default": "text"
                    }
                },
                "required": ["content", "username"]
            }
        ),
        
        # 🏆 NEW: Instagram MCP Integration Tools
        types.Tool(
            name="send_sassy_instagram_dm",
            description="🏆 HACKATHON: Send sassy fact-check response via Instagram DM",
            inputSchema={
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string", 
                        "description": "Instagram username to send response to"
                    },
                    "content": {
                        "type": "string",
                        "description": "Original claim/content to fact-check"
                    }
                },
                "required": ["username", "content"]
            }
        ),
        
        types.Tool(
            name="check_instagram_dms",
            description="📱 Check Instagram DMs for new fact-check requests",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of DMs to check",
                        "default": 5
                    }
                }
            }
        ),
        
        types.Tool(
            name="instagram_integration_status",
            description="🔍 Show Instagram MCP integration status and capabilities",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        
        types.Tool(
            name="welcome_new_followers", 
            description="Send welcome messages to new Instagram followers",
            inputSchema={
                "type": "object",
                "properties": {
                    "followers_list": {
                        "type": "array",
                        "description": "List of current followers with username/user_id",
                        "items": {
                            "type": "object",
                            "properties": {
                                "username": {"type": "string"},
                                "user_id": {"type": "string"}
                            }
                        }
                    }
                },
                "required": ["followers_list"]
            }
        ),
        
        types.Tool(
            name="get_bot_stats",
            description="Get daily statistics and analytics for the bot",
            inputSchema={
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "description": "Date in YYYY-MM-DD format (optional, defaults to today)"
                    }
                }
            }
        ),
        
        types.Tool(
            name="test_bot_system",
            description="Test all bot components (Claude API, filters, logging)",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        
        types.Tool(
            name="update_bot_settings",
            description="Update bot personality and behavior settings",
            inputSchema={
                "type": "object", 
                "properties": {
                    "bot_mode": {
                        "type": "string",
                        "description": "Bot personality mode",
                        "enum": ["sassy", "neutral", "unhinged"],
                        "default": "sassy"
                    },
                    "safe_mode": {
                        "type": "boolean",
                        "description": "Enable safe mode for sensitive topics",
                        "default": True
                    },
                    "log_interactions": {
                        "type": "boolean", 
                        "description": "Enable interaction logging",
                        "default": True
                    }
                }
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool calls for the Sassy Fact Check Bot."""
    
    if arguments is None:
        arguments = {}
    
    try:
        if name == "fact_check_dm":
            return await handle_fact_check_dm(arguments)
        elif name == "send_sassy_instagram_dm":  # 🏆 NEW
            return await handle_send_sassy_instagram_dm(arguments)
        elif name == "check_instagram_dms":  # 🏆 NEW
            return await handle_check_instagram_dms(arguments)
        elif name == "instagram_integration_status":  # 🏆 NEW
            return await handle_instagram_integration_status(arguments)
        elif name == "welcome_new_followers":
            return await handle_welcome_new_followers(arguments)
        elif name == "get_bot_stats":
            return await handle_get_bot_stats(arguments)
        elif name == "test_bot_system":
            return await handle_test_bot_system(arguments)
        elif name == "update_bot_settings":
            return await handle_update_bot_settings(arguments)
        else:
            raise ValueError(f"Unknown tool: {name}")
            
    except Exception as e:
        error_msg = f"Error in {name}: {str(e)}"
        return [types.TextContent(type="text", text=error_msg)]

# 🏆 NEW: Instagram Integration Handlers
async def handle_send_sassy_instagram_dm(arguments: dict) -> list[types.TextContent]:
    """Handle sending sassy Instagram DM"""
    username = arguments.get("username", "")
    content = arguments.get("content", "")
    
    if not username or not content:
        return [types.TextContent(
            type="text",
            text="❌ Username and content required for Instagram DM!"
        )]
    
    # Generate sassy response using your existing fact checker
    fact_result = await fact_checker.process_dm_content(content, username, "text")
    sassy_response = fact_result.get("response", "No response generated")
    
    # Send via Instagram (demo mode)
    send_result = await instagram_tools.send_instagram_dm(username, sassy_response)
    
    response_text = f"""🏆 **HACKATHON: Instagram DM Integration** 💅

**Fact-Check Request:**
• From: @{username}
• Claim: "{content}"

**Sassy Response Generated:**
"{sassy_response}"

**Instagram DM Status:**
• Sent: {'✅' if send_result['success'] else '❌'}
• Mode: {send_result['mode'].upper()}
• Status: {send_result['status']}

**Integration Details:**
• Tone Used: {fact_result.get('tone_used', 'sassy')}
• Sources: {', '.join(fact_result.get('sources', [])) or 'None cited'}
• Safe Mode: {fact_result.get('category', 'safe')}

🎉 Perfect Instagram MCP integration demonstration!"""
    
    return [types.TextContent(type="text", text=response_text)]

async def handle_check_instagram_dms(arguments: dict) -> list[types.TextContent]:
    """Handle checking Instagram DMs"""
    limit = arguments.get("limit", 5)
    
    # Get demo DMs
    dms = await instagram_tools.check_instagram_dms()
    
    if not dms:
        return [types.TextContent(
            type="text",
            text="✅ No new Instagram DMs to fact-check!"
        )]
    
    response_text = f"📱 **New Instagram DMs Found!** ({len(dms)} messages)\n\n"
    
    for i, dm in enumerate(dms[:limit], 1):
        # Preview fact-check for each
        preview_result = await fact_checker.process_dm_content(
            dm['message'], dm['username'], "text"
        )
        
        response_text += f"**{i}. @{dm['username']}:**\n"
        response_text += f"Claim: \"{dm['message']}\"\n"
        response_text += f"Sassy Preview: \"{preview_result.get('response', 'No response')}\"\n"
        response_text += f"Tone: {preview_result.get('tone_used', 'unknown')}\n\n"
    
    response_text += f"💅 Use `send_sassy_instagram_dm` to reply to any of these!"
    
    return [types.TextContent(type="text", text=response_text)]

async def handle_instagram_integration_status(arguments: dict) -> list[types.TextContent]:
    """Handle Instagram integration status check"""
    status = instagram_tools.get_integration_status()
    
    response_text = f"""🏆 **HACKATHON: Instagram MCP Integration Status** 

**Core Integration:**
• Instagram MCP: {'✅ Connected' if status['instagram_mcp_connected'] else '❌ Disconnected'}
• Demo Mode: {'✅ Active' if status['demo_mode'] else '❌ Inactive'}
• Hackathon Ready: {'✅ YES' if status['ready_for_hackathon'] else '❌ NO'}

**Available Features:**
{chr(10).join([f"• {feature}" for feature in status['features']])}

**Available Tools:**
• `send_sassy_instagram_dm` - Send responses via Instagram
• `check_instagram_dms` - Monitor incoming fact-check requests  
• `instagram_integration_status` - Show this status
• Plus all your existing sassy fact-check tools!

**Integration Note:**
{status['note']}

🎉 Perfect for hackathon demonstration - shows complete Instagram DM MCP workflow!"""
    
    return [types.TextContent(type="text", text=response_text)]

# Original handlers (unchanged)
async def handle_fact_check_dm(arguments: dict) -> list[types.TextContent]:
    """Handle fact-checking DM content."""
    
    content = arguments.get("content", "")
    username = arguments.get("username", "unknown_user")
    message_type = arguments.get("message_type", "text")
    
    if not content.strip() and message_type == "text":
        return [types.TextContent(
            type="text",
            text="❌ No content provided to fact-check. Send me some juicy claims! 🔥"
        )]
    
    # Process the content
    result = await fact_checker.process_dm_content(content, username, message_type)
    
    # Format response with metadata
    response_text = f"""🤖 **Sassy Fact Check Response** 💅

**For:** @{username}
**Content Type:** {message_type}
**Tone Used:** {result.get('tone_used', 'unknown')}
**Category:** {result.get('category', 'unknown')}

**Response:**
{result.get('response', 'No response generated')}

**Sources Found:** {', '.join(result.get('sources', [])) or 'None cited'}
**Should Send:** {'✅ Yes' if result.get('should_send', False) else '❌ No'}
"""

    return [types.TextContent(type="text", text=response_text)]

async def handle_welcome_new_followers(arguments: dict) -> list[types.TextContent]:
    """Handle welcoming new followers."""
    
    followers_list = arguments.get("followers_list", [])
    
    if not followers_list:
        return [types.TextContent(
            type="text", 
            text="❌ No followers list provided"
        )]
    
    # Check for new followers
    new_followers = await welcomer.check_for_new_followers(followers_list)
    
    if not new_followers:
        return [types.TextContent(
            type="text",
            text="✅ No new followers to welcome! Everyone's already been greeted 👋"
        )]
    
    # Generate welcome messages
    welcome_messages = []
    for username in new_followers:
        message = welcomer.get_welcome_message_for_user(username)
        welcome_messages.append({
            "username": username,
            "message": message
        })
    
    # Format response
    response_text = f"🎉 **New Followers Detected!** 🎉\n\n"
    response_text += f"Found {len(new_followers)} new followers to welcome:\n\n"
    
    for welcome in welcome_messages:
        response_text += f"**@{welcome['username']}:**\n"
        response_text += f"{welcome['message']}\n\n"
    
    response_text += f"💅 Ready to slide into {len(new_followers)} DMs with sass and science!"
    
    return [types.TextContent(type="text", text=response_text)]

async def handle_get_bot_stats(arguments: dict) -> list[types.TextContent]:
    """Handle getting bot statistics."""
    
    # Get daily stats from fact checker
    daily_stats = await fact_checker.get_daily_stats()
    
    # Get follower stats
    follower_stats = welcomer.get_stats()
    
    # Format comprehensive stats
    response_text = f"""📊 **Sassy Fact Check Bot Stats** 📊

**Daily Activity:**
• Total Interactions: {daily_stats.get('total_interactions', 0)}
• Top Categories: {', '.join([f"{cat} ({count})" for cat, count in daily_stats.get('top_categories', [])[:3]])}

**Follower Management:**
• Total Followers Seen: {follower_stats.get('total_seen_followers', 0)}
• Welcome Messages Available: {follower_stats.get('messages_available', 0)}
• Last Updated: {follower_stats.get('last_updated', 'Never')}

**Recent Sassy Responses:**
"""
    
    for i, response in enumerate(daily_stats.get('sassiest_responses', [])[:3], 1):
        response_text += f"{i}. @{response['username']}: {response['response']}\n"
    
    if not daily_stats.get('sassiest_responses'):
        response_text += "No sassy responses yet today - send me some bad takes! 🔥\n"
    
    response_text += f"\n🤖 Bot Status: Ready to roast misinformation! 💅"
    
    return [types.TextContent(type="text", text=response_text)]

async def handle_test_bot_system(arguments: dict) -> list[types.TextContent]:
    """Handle testing bot system components."""
    
    print("🧪 Testing bot system components...")
    
    # Test all components
    test_results = await fact_checker.test_system()
    
    # Format test results
    response_text = "🧪 **Bot System Test Results** 🧪\n\n"
    
    for component, status in test_results.items():
        emoji = "✅" if status else "❌"
        response_text += f"{emoji} {component.replace('_', ' ').title()}: {'PASS' if status else 'FAIL'}\n"
    
    # Overall status
    all_passed = all(test_results.values())
    overall_emoji = "✅" if all_passed else "⚠️"
    overall_status = "All systems operational!" if all_passed else "Some issues detected"
    
    response_text += f"\n{overall_emoji} **Overall Status:** {overall_status}\n"
    
    if not all_passed:
        response_text += "\n🔧 Check your .env file and API keys if tests are failing."
    else:
        response_text += "\n💅 Ready to serve facts with maximum sass!"
    
    return [types.TextContent(type="text", text=response_text)]

async def handle_update_bot_settings(arguments: dict) -> list[types.TextContent]:
    """Handle updating bot settings."""
    
    bot_mode = arguments.get("bot_mode", "sassy")
    safe_mode = arguments.get("safe_mode", True)
    log_interactions = arguments.get("log_interactions", True)
    
    # Update environment variables (in memory)
    os.environ["BOT_MODE"] = bot_mode
    os.environ["ENABLE_SAFE_MODE"] = str(safe_mode).lower()
    os.environ["LOG_INTERACTIONS"] = str(log_interactions).lower()
    
    response_text = f"""⚙️ **Bot Settings Updated** ⚙️

**Personality Mode:** {bot_mode.upper()} 💅
**Safe Mode:** {'Enabled' if safe_mode else 'Disabled'} 🛡️
**Interaction Logging:** {'Enabled' if log_interactions else 'Disabled'} 📝

Settings updated for this session! To make permanent changes, update your .env file.
"""
    
    return [types.TextContent(type="text", text=response_text)]

async def main():
    """Main entry point for the MCP server."""
    
    # Check required environment variables
    required_vars = ["INSTAGRAM_USERNAME", "INSTAGRAM_PASSWORD", "ANTHROPIC_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("Run 'python setup_env.py' to configure your bot!")
        return
    
    print("🏆 Starting Sassy Fact Check Bot with Instagram MCP Integration... 💅")
    print(f"Bot Mode: {os.getenv('BOT_MODE', 'sassy').upper()}")
    print(f"Safe Mode: {os.getenv('ENABLE_SAFE_MODE', 'true')}")
    print("📱 Instagram Integration: DEMO MODE - Perfect for hackathon!")
    
    # Test Claude connection on startup
    claude_client = ClaudeFactChecker()
    if await claude_client.test_connection():
        print("✅ Claude API connection successful!")
    else:
        print("⚠️ Claude API connection failed - check your API key")
    
    # Test Instagram integration
    status = instagram_tools.get_integration_status()
    print(f"📱 Instagram MCP: {'✅ Ready' if status['ready_for_hackathon'] else '❌ Not Ready'}")
    
    # Run the server
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="sassy-factcheck-bot-instagram",
                server_version="1.0.0-hackathon",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n💅 Sassy Fact Check Bot shutting down gracefully...")
    except Exception as e:
        print(f"❌ Server error: {e}")
        sys.exit(1)

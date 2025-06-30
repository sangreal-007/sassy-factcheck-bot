#!/usr/bin/env python3
"""
Sassy Fact Check Bot - MCP Server - PERFECT VERSION
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

from tools.sassy_fact_check import SassyFactChecker
from tools.welcome_followers import FollowerWelcomer
from claude_client import ClaudeFactChecker
from instagram_dm_mcp import instagram_tools

# Load environment variables
load_dotenv()

# Initialize components
server = Server("sassy-factcheck-bot")
fact_checker = SassyFactChecker()
welcomer = FollowerWelcomer()

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools for the Sassy Fact Check Bot."""
    
    real_mode = os.getenv("INSTAGRAM_REAL_MODE", "false").lower() == "true"
    
    tools = [
        types.Tool(
            name="generate_sassy_response",
            description="🔥 Generate sassy fact-check response (don't send - just generate)",
            inputSchema={
                "type": "object",
                "properties": {
                    "username": {"type": "string", "description": "Instagram username"},
                    "content": {"type": "string", "description": "Content to fact-check"}
                },
                "required": ["username", "content"]
            }
        ),
        
        types.Tool(
            name="generate_welcome_message",
            description="💅 Generate welcome message (don't send - just generate)",
            inputSchema={
                "type": "object",
                "properties": {
                    "username": {"type": "string", "description": "Instagram username"}
                },
                "required": ["username"]
            }
        ),
        
        types.Tool(
            name="instagram_integration_status",
            description="🔍 Show Instagram MCP integration status",
            inputSchema={"type": "object", "properties": {}}
        )
    ]
    
    # Only add check_instagram_dms in DEMO mode
    if not real_mode:
        tools.append(
            types.Tool(
                name="check_instagram_dms",
                description="📱 Check Instagram DMs - Demo practice claims only",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "limit": {"type": "integer", "description": "Maximum number of DMs to check", "default": 5}
                    }
                }
            )
        )
    
    return tools

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    """Handle tool calls."""
    
    if arguments is None:
        arguments = {}
    
    try:
        if name == "generate_sassy_response":
            return await handle_generate_sassy_response(arguments)
        elif name == "generate_welcome_message":
            return await handle_generate_welcome_message(arguments)
        elif name == "check_instagram_dms":
            return await handle_check_instagram_dms(arguments)
        elif name == "instagram_integration_status":
            return await handle_instagram_integration_status(arguments)
        else:
            raise ValueError(f"Unknown tool: {name}")
            
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error in {name}: {str(e)}")]

async def handle_generate_sassy_response(arguments: dict) -> list[types.TextContent]:
    """Generate sassy response only - don't send"""
    username = arguments.get("username", "")
    content = arguments.get("content", "")
    
    if not username or not content:
        return [types.TextContent(type="text", text="❌ Username and content required!")]
    
    # Generate sassy response
    fact_result = await fact_checker.process_dm_content(content, username, "text")
    sassy_response = fact_result.get("response", "No response generated")
    
    response_text = f"💅 **Generated sassy response for @{username}:**\n\n{sassy_response}\n\n✅ Ready to send via Instagram MCP!"
    
    return [types.TextContent(type="text", text=response_text)]

async def handle_generate_welcome_message(arguments: dict) -> list[types.TextContent]:
    """Generate welcome message only - don't send"""
    username = arguments.get("username", "")
    
    if not username:
        return [types.TextContent(type="text", text="❌ Username required!")]
    
    # Generate welcome message
    welcome_message = welcomer.get_welcome_message_for_user(username)
    
    response_text = f"💅 **Generated welcome message for @{username}:**\n\n{welcome_message}\n\n✅ Ready to send via Instagram MCP!"
    
    return [types.TextContent(type="text", text=response_text)]

async def handle_check_instagram_dms(arguments: dict) -> list[types.TextContent]:
    """Handle checking Instagram DMs - Demo mode only"""
    limit = arguments.get("limit", 5)
    
    # This function only gets called in demo mode now
    dms = await instagram_tools.check_instagram_dms()
    
    if not dms:
        return [types.TextContent(type="text", text="✅ No demo claims available!")]
    
    response_text = f"📱 **Demo Mode - Practice Claims!** ({len(dms)} available)\n\n"
    
    for i, dm in enumerate(dms[:limit], 1):
        response_text += f"**{i}. @{dm['username']}:**\n"
        response_text += f"Claim: \"{dm['message']}\"\n\n"
    
    response_text += f"💅 Use `generate_sassy_response` to practice roasting these!"
    
    return [types.TextContent(type="text", text=response_text)]

async def handle_instagram_integration_status(arguments: dict) -> list[types.TextContent]:
    """Handle Instagram integration status check"""
    status = instagram_tools.get_integration_status()
    real_mode = os.getenv("INSTAGRAM_REAL_MODE", "false").lower() == "true"
    
    response_text = f"""🔍 **Instagram MCP Integration Status**

**Core Integration:**
- Instagram MCP: {'✅ Connected' if status['instagram_mcp_connected'] else '❌ Disconnected'}
- Mode: {'🔥 REAL MODE' if real_mode else '📱 DEMO MODE'}
- Ready: {'✅ YES' if status['ready_for_hackathon'] else '❌ NO'}

**Available Tools:**
- generate_sassy_response - Create sassy fact-checks
- generate_welcome_message - Create welcome messages"""

    if not real_mode:
        response_text += "\n- check_instagram_dms - Practice claims (demo mode only)"
    
    response_text += f"\n- instagram_integration_status - This status\n\n{status['note']}"
    
    return [types.TextContent(type="text", text=response_text)]

async def main():
    """Main entry point for the MCP server."""
    
    print("🔧 Starting Perfect Sassy Fact Check Bot...")
    
    real_mode = os.getenv("INSTAGRAM_REAL_MODE", "false").lower() == "true"
    mode_display = "REAL MODE - Connected to Gala Labs MCP!" if real_mode else "DEMO MODE - Perfect for hackathon!"
    print(f"📱 Instagram Integration: {mode_display}")
    
    # Run the server
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="sassy-factcheck-bot-perfect",
                server_version="1.0.2-perfect",
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
        print("\n💅 Sassy Fact Check Bot shutting down...")
    except Exception as e:
        print(f"❌ Server error: {e}")
        sys.exit(1)

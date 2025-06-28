"""
Instagram Demo Tools for Hackathon Submission
Perfect Instagram MCP integration without real Instagram connection
"""

import asyncio
from typing import Dict, List, Any
from datetime import datetime
import mcp.types as types

class InstagramDemoTools:
    """Demo Instagram tools that work perfectly for hackathon"""
    
    def __init__(self):
        self.demo_mode = True
        self.demo_dms = [
            {
                "username": "wellness_guru_fake",
                "message": "Apple cider vinegar burns belly fat instantly! 🔥",
                "timestamp": "2025-01-27T13:30:00Z",
                "thread_id": "demo_thread_001"
            },
            {
                "username": "fitness_influencer", 
                "message": "Lemon water detoxes your liver completely!",
                "timestamp": "2025-01-27T13:25:00Z",
                "thread_id": "demo_thread_002"
            },
            {
                "username": "health_coach_sus",
                "message": "Essential oils cure everything! Big pharma doesn't want you to know!",
                "timestamp": "2025-01-27T13:20:00Z",
                "thread_id": "demo_thread_003"
            }
        ]
    
    async def send_instagram_dm(self, username: str, message: str) -> Dict[str, Any]:
        """Send DM via Instagram (demo mode)"""
        return {
            "success": True,
            "mode": "demo",
            "username": username,
            "message": message,
            "sent_at": datetime.now().isoformat(),
            "status": f"✅ Sassy response sent to @{username} via Instagram DM!",
            "demo_note": "In production, this would use real Instagram API"
        }
    
    async def check_instagram_dms(self) -> List[Dict[str, Any]]:
        """Check for new Instagram DMs (demo data)"""
        return self.demo_dms
    
    async def get_user_profile(self, username: str) -> Dict[str, Any]:
        """Get Instagram user profile (demo data)"""
        profiles = {
            "wellness_guru_fake": {
                "username": username,
                "followers": 45000,
                "following": 1200,
                "bio": "🌱 Wellness coach | Natural healing ✨ | DM for detox tips",
                "is_verified": False,
                "is_business": True
            },
            "fitness_influencer": {
                "username": username,
                "followers": 125000,
                "following": 890,
                "bio": "💪 Fitness coach | Transform your body naturally! 🔥",
                "is_verified": True,
                "is_business": True
            }
        }
        
        return profiles.get(username, {
            "username": username,
            "followers": 15000,
            "following": 500,
            "bio": "Living my best life 💫",
            "is_verified": False,
            "is_business": False
        })
    
    def get_integration_status(self) -> Dict[str, Any]:
        """Get Instagram MCP integration status"""
        return {
            "instagram_mcp_connected": True,
            "demo_mode": True,
            "tools_available": ["send_dm", "check_dms", "get_profile", "get_status"],
            "ready_for_hackathon": True,
            "features": [
                "✅ Receive Instagram DMs",
                "✅ Send sassy fact-check responses", 
                "✅ User profile analysis",
                "✅ Content safety filtering",
                "✅ Citation integration"
            ],
            "note": "Perfect demo mode - shows full Instagram integration workflow!"
        }

    def get_tools_for_mcp(self) -> List[types.Tool]:
        """Get MCP tool definitions for Instagram integration"""
        return [
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
                        },
                        "custom_response": {
                            "type": "string",
                            "description": "Optional custom sassy response (will auto-generate if not provided)"
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
                name="get_instagram_user_profile",
                description="👤 Get Instagram user profile for context",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "username": {
                            "type": "string",
                            "description": "Instagram username to analyze"
                        }
                    },
                    "required": ["username"]
                }
            ),
            
            types.Tool(
                name="instagram_integration_status",
                description="🔍 Show Instagram MCP integration status and capabilities",
                inputSchema={
                    "type": "object",
                    "properties": {}
                }
            )
        ]

# Global instance
instagram_tools = InstagramDemoTools()

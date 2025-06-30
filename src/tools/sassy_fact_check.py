"""
Sassy Fact Check Tool - Core fact-checking functionality.
"""

import asyncio
import json
import os
import re
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

from claude_client import ClaudeFactChecker
from filters import ContentFilter, ContentCategory, ToneMode

class SassyFactChecker:
    """Main fact-checking engine with sassy personality."""
    
    def __init__(self):
        self.claude_client = ClaudeFactChecker()
        self.filter = ContentFilter()
        self.interaction_log = []
        self.log_file = Path("interactions.json")
        
    async def process_dm_content(
        self, 
        content: str, 
        username: str,
        message_type: str = "text"
    ) -> Dict[str, Any]:
        """
        Process incoming DM content and generate response.
        
        Args:
            content: The content to fact-check
            username: Instagram username of sender
            message_type: Type of message (text, photo, video, etc.)
            
        Returns:
            Dict with response and metadata
        """
        
        print(f"📨 Processing {message_type} from @{username}")
        print(f"Content: {content[:100]}...")
        
        # Handle different message types
        if message_type == "photo" and not content.strip():
            return await self._handle_photo_without_text(username)
        
        if message_type == "video" and not content.strip():
            return await self._handle_video_without_text(username)
            
        if not content.strip():
            return await self._handle_empty_content(username)
        
        # Fact-check the content
        result = await self.claude_client.fact_check(content, message_type)
        
        # Log interaction
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "username": username,
            "content": content,
            "message_type": message_type,
            "response": result["response"],
            "tone_used": result["tone_used"],
            "category": result["category"],
            "sources": result.get("sources", [])
        }
        
        await self._log_interaction(interaction)
        
        # Add some metadata for the response
        result["username"] = username
        result["should_send"] = True
        
        return result
    
    async def _handle_photo_without_text(self, username: str) -> Dict[str, Any]:
        """Handle photo messages without extractable text."""
        responses = [
            "Cute photo, but I need some claims to fact-check! Send me the tea ☕",
            "Pretty picture, but where are the questionable health facts? 💅",
            "I see the aesthetic but not the misinformation. Try again! 📸",
            "Visual content with no text to roast? My talents are wasted! 🎭"
        ]
        
        import random
        response = random.choice(responses)
        
        return {
            "response": response,
            "tone_used": "sassy",
            "category": "no_text",
            "should_send": True,
            "username": username,
            "sources": []
        }
    
    async def _handle_video_without_text(self, username: str) -> Dict[str, Any]:
        """Handle video/reel messages without extractable text."""
        responses = [
            "Your Reel is vibing but I need captions to roast! Add some text 🎬",
            "Great moves, but where are the dubious health claims? 💃",
            "I can't fact-check dance moves (yet). Send me some wild claims! 🕺",
            "Video looks fire but my expertise is in roasting misinformation, not content! 🔥"
        ]
        
        import random
        response = random.choice(responses)
        
        return {
            "response": response,
            "tone_used": "sassy", 
            "category": "no_text",
            "should_send": True,
            "username": username,
            "sources": []
        }
    
    async def _handle_empty_content(self, username: str) -> Dict[str, Any]:
        """Handle completely empty messages."""
        responses = [
            "Did you send me the void? I need actual content to fact-check! ⚫",
            "Your message is emptier than a juice cleanse promise. Try again! 🤷‍♀️",
            "I got nothing because you sent nothing. Send me some hot takes! 🔥",
            "Error 404: Content not found. Please try again with actual text! 💻"
        ]
        
        import random
        response = random.choice(responses)
        
        return {
            "response": response,
            "tone_used": "sassy",
            "category": "empty",
            "should_send": True,
            "username": username,
            "sources": []
        }
    
    async def _log_interaction(self, interaction: Dict[str, Any]) -> None:
        """Log interaction to file for analytics."""
        
        if not os.getenv("LOG_INTERACTIONS", "true").lower() == "true":
            return
        
        self.interaction_log.append(interaction)
        
        # Save to file
        try:
            # Load existing logs
            existing_logs = []
            if self.log_file.exists():
                with open(self.log_file, 'r') as f:
                    existing_logs = json.load(f)
            
            # Append new interaction
            existing_logs.append(interaction)
            
            # Keep only last 1000 interactions to prevent huge files
            if len(existing_logs) > 1000:
                existing_logs = existing_logs[-1000:]
            
            # Save back to file
            with open(self.log_file, 'w') as f:
                json.dump(existing_logs, f, indent=2)
                
        except Exception as e:
            print(f"Failed to log interaction: {e}")
    
    async def get_daily_stats(self) -> Dict[str, Any]:
        """Get daily interaction statistics."""
        
        if not self.log_file.exists():
            return {"total_interactions": 0, "top_categories": [], "sassiest_responses": []}
        
        try:
            with open(self.log_file, 'r') as f:
                logs = json.load(f)
            
            today = datetime.now().date()
            today_logs = [
                log for log in logs 
                if datetime.fromisoformat(log["timestamp"]).date() == today
            ]
            
            # Count categories
            categories = {}
            for log in today_logs:
                cat = log.get("category", "unknown")
                categories[cat] = categories.get(cat, 0) + 1
            
            # Find sassiest responses (sassy tone + longer responses)
            sassy_responses = [
                {
                    "username": log["username"],
                    "response": log["response"][:100] + "..." if len(log["response"]) > 100 else log["response"],
                    "category": log["category"]
                }
                for log in today_logs 
                if log.get("tone_used") == "sassy"
            ]
            
            return {
                "total_interactions": len(today_logs),
                "top_categories": sorted(categories.items(), key=lambda x: x[1], reverse=True)[:5],
                "sassiest_responses": sassy_responses[:5]
            }
            
        except Exception as e:
            print(f"Failed to get daily stats: {e}")
            return {"error": str(e)}
    
    def extract_text_from_caption(self, caption: str) -> str:
        """Extract meaningful text from Instagram captions."""
        if not caption:
            return ""
        
        # Remove hashtags and mentions for cleaner fact-checking
        text = re.sub(r'#\w+', '', caption)
        text = re.sub(r'@\w+', '', text)
        
        # Remove excessive emojis (keep some for context)
        # This is a basic emoji removal - could be improved
        text = re.sub(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]{3,}', '✨', text)
        
        # Clean up whitespace
        text = ' '.join(text.split())
        
        return text.strip()
    
    async def test_system(self) -> Dict[str, bool]:
        """Test all system components."""
        results = {}
        
        # Test Claude API
        results["claude_api"] = await self.claude_client.test_connection()
        
        # Test content filter
        try:
            test_content = "Essential oils cure cancer"
            category, tone, reason = self.filter.analyze_content(test_content)
            results["content_filter"] = True
        except Exception:
            results["content_filter"] = False
        
        # Test logging
        try:
            test_interaction = {
                "timestamp": datetime.now().isoformat(),
                "username": "test_user",
                "content": "test",
                "response": "test response",
                "tone_used": "sassy"
            }
            await self._log_interaction(test_interaction)
            results["logging"] = True
        except Exception:
            results["logging"] = False
        
        return results

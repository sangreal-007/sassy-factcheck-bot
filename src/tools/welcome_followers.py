"""
Welcome new followers with a sassy introduction message.
"""

import json
import asyncio
from datetime import datetime
from typing import Set, List, Dict, Any
from pathlib import Path

class FollowerWelcomer:
    """Manages welcoming new followers with sassy introduction."""
    
    def __init__(self):
        self.seen_followers_file = Path("seen_followers.json")
        self.seen_followers: Set[str] = self._load_seen_followers()
        
    def _load_seen_followers(self) -> Set[str]:
        """Load previously seen followers from file."""
        if self.seen_followers_file.exists():
            try:
                with open(self.seen_followers_file, 'r') as f:
                    data = json.load(f)
                    return set(data.get('followers', []))
            except Exception as e:
                print(f"Error loading seen followers: {e}")
        return set()
    
    def _save_seen_followers(self) -> None:
        """Save seen followers to file."""
        try:
            data = {
                'followers': list(self.seen_followers),
                'last_updated': datetime.now().isoformat()
            }
            with open(self.seen_followers_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving seen followers: {e}")
    
    def get_welcome_messages(self) -> List[str]:
        """Get pool of welcome messages to rotate through."""
        return [
            "Hey! 👋 I'm your new favorite fact-checking bestie! Send me some questionable health claims and watch me roast them with CITATIONS 🔥📚",
            
            "Welcome to the fact-check squad! 💅 I specialize in destroying bad takes with sass and science. DM me your wildest health 'facts' and let's see what happens! ✨",
            
            "New follower alert! 🚨 I'm here to serve facts with a side of attitude. Send me those 'doctors hate this one trick' posts and watch me work my magic! 🎭",
            
            "Hi gorgeous! 💖 I fact-check nonsense for a living and I'm REALLY good at it. Try me with your most unhinged health claims - I dare you! 😈",
            
            "Welcome to the chaos! 🌪️ I'm the bot that makes misinformation cry. DM me anything that sounds too good to be true and I'll tell you why it probably is! 💯",
        ]
    
    async def check_for_new_followers(self, current_followers: List[Dict]) -> List[str]:
        """
        Check for new followers and return list of usernames to welcome.
        """
        new_followers = []
        
        # Extract usernames from current followers
        current_usernames = {
            follower.get('username', '') for follower in current_followers
            if follower.get('username')
        }
        
        # Find new followers
        for username in current_usernames:
            if username not in self.seen_followers:
                new_followers.append(username)
                self.seen_followers.add(username)
        
        # Save updated seen followers
        if new_followers:
            self._save_seen_followers()
            print(f"Found {len(new_followers)} new followers: {new_followers}")
        
        return new_followers
    
    def get_welcome_message_for_user(self, username: str) -> str:
        """Get a personalized welcome message for a specific user."""
        import random
        
        messages = self.get_welcome_messages()
        base_message = random.choice(messages)
        
        # Add some personality based on username patterns
        if any(word in username.lower() for word in ['health', 'wellness', 'fitness', 'nutrition']):
            bonus = " I see you're in the health space - perfect! I LIVE for debunking wellness myths! 💪"
            base_message += bonus
        elif any(word in username.lower() for word in ['mama', 'mom', 'mother']):
            bonus = " Fellow parent vibes! I'm here to help you sort through all that parenting 'advice' floating around! 👶✨"
            base_message += bonus
        
        return base_message
    
    def get_stats(self) -> Dict[str, Any]:
        """Get follower welcome statistics."""
        return {
            "total_seen_followers": len(self.seen_followers),
            "messages_available": len(self.get_welcome_messages()),
            "last_updated": self._get_last_updated()
        }
    
    def _get_last_updated(self) -> str:
        """Get last updated timestamp from file."""
        if self.seen_followers_file.exists():
            try:
                with open(self.seen_followers_file, 'r') as f:
                    data = json.load(f)
                    return data.get('last_updated', 'Never')
            except Exception:
                pass
        return 'Never'

"""
Claude API client for fact-checking.
"""

import asyncio
import os
from typing import Dict, Any
from anthropic import Anthropic

class ClaudeFactChecker:
    """Claude API client for fact-checking with sassy responses."""
    
    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable required")
        self.client = Anthropic(api_key=api_key)
    
    async def test_connection(self) -> bool:
        """Test Claude API connection."""
        try:
            response = self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=10,
                messages=[{"role": "user", "content": "Hi"}]
            )
            return True
        except Exception as e:
            print(f"Claude API test failed: {e}")
            return False
    
    async def fact_check(self, content: str, message_type: str = "text") -> Dict[str, Any]:
        """Fact-check content with Claude."""
        try:
            from filters import ContentFilter, ToneMode
            
            filter_instance = ContentFilter()
            category, tone_mode, reason = filter_instance.analyze_content(content)
            
            if not filter_instance.should_respond(category):
                return {
                    "response": filter_instance.get_fallback_response(category),
                    "tone_used": "blocked",
                    "category": category.value,
                    "sources": [],
                    "should_send": False
                }
            
            # Build Claude prompt with MAXIMUM SASS
            claude_prompt = f"""You are a fact-checking queen with MAXIMUM sass. Be witty, dramatic, and use Gen Z language.

TONE EXAMPLES:
- "Bestie, who taught you [topic]? 💀"
- "That's like, literal [Basic Topic] 101"
- "You're literally SO RIGHT for once! 👑✨" (when they're correct)
- "This [fact] has been [established/known] since [time period]"

CRITICAL: ALWAYS end with 'Source: [Authority]' like 'Source: Mayo Clinic'

LENGTH: 25-40 words INCLUDING the source
STYLE: Dramatic, educational sass with proper citations
EMOJIS: Use 2-3 relevant emojis (💀, 👑, ✨, 😤, 🤡)

Claim to roast: "{content}"

Generate a sassy fact-check with full attitude!"""

            # Call Claude API
            response = self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=150,
                messages=[{"role": "user", "content": claude_prompt}]
            )
            
            fact_check_response = response.content[0].text.strip()
            
            return {
                "response": fact_check_response,
                "tone_used": tone_mode.value,
                "category": category.value,
                "sources": self._extract_sources(fact_check_response),
                "should_send": True
            }
            
        except Exception as e:
            print(f"Claude fact-check failed: {e}")
            return {
                "response": "Oops! My fact-checking brain had a glitch. Try again! 🤖",
                "tone_used": "error",
                "category": "error",
                "sources": [],
                "should_send": True
            }
    
    def _extract_sources(self, response: str) -> list:
        """Extract source citations from response."""
        import re
        sources = re.findall(r'Source:\s*([^.!?\n]+)', response)
        return sources[:3]

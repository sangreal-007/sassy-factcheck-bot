"""
Claude API client for generating sassy fact-check responses.
"""

import asyncio
import os
from typing import Optional, Dict, Any
import anthropic
from anthropic import AsyncAnthropic
from dotenv import load_dotenv

from .filters import ContentFilter, ToneMode, ContentCategory

load_dotenv()

class ClaudeFactChecker:
    """Claude-powered fact checker with sassy personality."""
    
    def __init__(self):
        self.client = AsyncAnthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )
        self.filter = ContentFilter()
        self.model = "claude-3-5-sonnet-20241022"
        
    async def fact_check(
        self, 
        content: str, 
        content_type: str = "text"
    ) -> Dict[str, Any]:
        """
        Fact-check content and return a sassy response.
        
        Args:
            content: The content to fact-check
            content_type: Type of content (text, image, video, etc.)
            
        Returns:
            Dict with response, tone_used, sources, etc.
        """
        
        # Analyze content for safety and tone
        category, tone_mode, reason = self.filter.analyze_content(content)
        
        # Check if we should respond
        if not self.filter.should_respond(category):
            return {
                "response": self.filter.get_fallback_response(category),
                "tone_used": "blocked",
                "category": category.value,
                "reason": reason,
                "sources": []
            }
        
        # Get appropriate prompt for tone
        system_prompt = self.filter.get_tone_prompt(tone_mode, category)
        
        # Create the user message
        user_prompt = f"""
        Please fact-check this claim or statement:
        
        "{content}"
        
        Content type: {content_type}
        
        Provide your response in the requested tone and include at least one credible source.
        If this is clearly false, roast it appropriately for the tone.
        If it's true or partially true, acknowledge that while maintaining the tone.
        If it's unclear or needs more context, say so.
        """
        
        try:
            # Call Claude API
            message = await self.client.messages.create(
                model=self.model,
                max_tokens=200,  # Keep responses short and punchy
                temperature=0.8,  # Some creativity for sass
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ]
            )
            
            response_text = message.content[0].text
            
            # Extract potential sources (basic regex)
            sources = self._extract_sources(response_text)
            
            return {
                "response": response_text,
                "tone_used": tone_mode.value,
                "category": category.value,
                "reason": reason,
                "sources": sources,
                "model_used": self.model
            }
            
        except Exception as e:
            # Fallback response if API fails
            fallback = self._get_api_error_fallback(tone_mode)
            return {
                "response": fallback,
                "tone_used": "error",
                "category": category.value,
                "reason": f"API Error: {str(e)}",
                "sources": [],
                "error": str(e)
            }
    
    def _extract_sources(self, text: str) -> list:
        """Extract mentioned sources from the response."""
        # Common source patterns
        source_patterns = [
            r'(?:Source|According to|Per|Via):\s*([^.]+)',
            r'(?:CDC|WHO|Mayo Clinic|WebMD|PubMed|NIH|FDA|Harvard|Stanford)',
            r'(?:American Journal|New England Journal|Journal of)',
            r'(?:Study published|Research from|According to researchers)'
        ]
        
        sources = []
        text_lower = text.lower()
        
        # Look for common medical/scientific sources
        known_sources = [
            'CDC', 'WHO', 'Mayo Clinic', 'WebMD', 'PubMed', 'NIH', 'FDA',
            'Harvard Medical School', 'Johns Hopkins', 'Cleveland Clinic'
        ]
        
        for source in known_sources:
            if source.lower() in text_lower:
                sources.append(source)
        
        return list(set(sources))  # Remove duplicates
    
    def _get_api_error_fallback(self, tone_mode: ToneMode) -> str:
        """Get fallback response when API fails."""
        
        fallbacks = {
            ToneMode.SASSY: "My fact-checking brain is buffering. Try again, or just Google it like a normal person! 🤷‍♀️",
            ToneMode.NEUTRAL: "I'm experiencing technical difficulties. Please try your request again.",
            ToneMode.SOFT: "I'm having trouble processing that right now. Please try again in a moment.",
        }
        
        return fallbacks.get(tone_mode, fallbacks[ToneMode.NEUTRAL])

    async def test_connection(self) -> bool:
        """Test if Claude API is working."""
        try:
            test_message = await self.client.messages.create(
                model=self.model,
                max_tokens=50,
                messages=[{
                    "role": "user", 
                    "content": "Say 'Bot is ready to roast bad takes!' in a sassy way."
                }]
            )
            return True
        except Exception as e:
            print(f"Claude API test failed: {e}")
            return False

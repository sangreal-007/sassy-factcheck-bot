"""
Content filters and safety mechanisms for Sassy Fact Check Bot.
Handles sensitive content detection and tone moderation.
"""

import re
from typing import Dict, List, Tuple
from enum import Enum

class ContentCategory(Enum):
    SAFE = "safe"
    SENSITIVE = "sensitive"  
    BLOCKED = "blocked"
    HEALTH_PANIC = "health_panic"
    SPAM = "spam"

class ToneMode(Enum):
    SASSY = "sassy"
    NEUTRAL = "neutral"
    SOFT = "soft"
    BLOCKED = "blocked"

class ContentFilter:
    """Filters content and determines appropriate response tone."""
    
    def __init__(self):
        # Sensitive topics that require neutral tone
        self.sensitive_keywords = {
            'war', 'death', 'suicide', 'trauma', 'grief', 'funeral', 'shooting',
            'terrorism', 'murder', 'cancer', 'terminal', 'dying', 'miscarriage',
            'abuse', 'violence', 'assault', 'rape', 'depression', 'anxiety',
            'mental health crisis', 'self harm', 'cutting', 'overdose'
        }
        
        # Health panic keywords that get special treatment
        self.health_panic_keywords = {
            'detox', 'cleanse', 'toxins', 'miracle cure', 'doctors hate',
            'big pharma', 'natural healing', 'alternative medicine gone wrong',
            'essential oils cure', 'alkaline water', 'raw diet', 'juice cleanse'
        }
        
        # Blocked content - we won't engage
        self.blocked_keywords = {
            'nazi', 'hitler', 'holocaust denial', 'qanon', 'pizzagate',
            'flat earth', 'chemtrails', 'lizard people', 'illuminati'
        }
        
        # Spam indicators
        self.spam_patterns = [
            r'\b(?:buy now|click here|limited time|act fast)\b',
            r'\b(?:make money|earn \$|work from home)\b',
            r'(?:http[s]?://|www\.)[^\s]+',  # URLs
            r'\b(?:dm me|message me|link in bio)\b'
        ]

    def analyze_content(self, text: str) -> Tuple[ContentCategory, ToneMode, str]:
        """
        Analyze content and return category, recommended tone, and reason.
        
        Returns:
            (ContentCategory, ToneMode, explanation)
        """
        text_lower = text.lower()
        
        # Check for blocked content first
        if any(keyword in text_lower for keyword in self.blocked_keywords):
            return (
                ContentCategory.BLOCKED, 
                ToneMode.BLOCKED,
                "Content contains blocked conspiracy theories or hate speech"
            )
        
        # Check for spam
        if any(re.search(pattern, text_lower) for pattern in self.spam_patterns):
            return (
                ContentCategory.SPAM,
                ToneMode.SASSY,
                "Content appears to be spam or promotional"
            )
        
        # Check for sensitive content
        if any(keyword in text_lower for keyword in self.sensitive_keywords):
            return (
                ContentCategory.SENSITIVE,
                ToneMode.SOFT,
                "Content contains sensitive topics requiring gentle approach"
            )
        
        # Check for health panic content
        if any(keyword in text_lower for keyword in self.health_panic_keywords):
            return (
                ContentCategory.HEALTH_PANIC,
                ToneMode.SASSY,
                "Health misinformation detected - sass mode with facts"
            )
        
        # Default to safe content with sassy tone
        return (
            ContentCategory.SAFE,
            ToneMode.SASSY,
            "Safe content ready for sassy fact-checking"
        )

    def get_tone_prompt(self, tone_mode: ToneMode, content_category: ContentCategory) -> str:
        """Get the appropriate prompt based on tone and content category."""
        
        base_instruction = """You are a fact-checking assistant. Analyze the claim and provide accurate information with a reliable source citation."""
        
        tone_instructions = {
            ToneMode.SASSY: """
                Be witty and sassy in 1-2 short sentences max. Use emojis.
                Roast the claim briefly, give ONE quick fact, cite source name only.
                TOTAL LIMIT: 25-35 words maximum including emojis.
                NO long explanations. NO URLs. NO study details.
                Format: [Quick roast emoji] [Brief fact] Source: [Short name]
            """,
            
            ToneMode.NEUTRAL: """
                Provide a straightforward correction in 1-2 sentences max.
                Be informative but concise. Minimal emojis.
                TOTAL LIMIT: 30-40 words maximum.
                Format: [Brief correction] Source: [Name]
            """,
            
            ToneMode.SOFT: """
                Be gentle and understanding in 1-2 sentences max.
                Acknowledge difficulty, provide brief accurate info.
                TOTAL LIMIT: 35-45 words maximum.
                Use compassionate language, no humor.
                Format: [Gentle acknowledgment] [Brief fact] Source: [Name]
            """,
            
            ToneMode.BLOCKED: """
                Politely decline in one short sentence.
                TOTAL LIMIT: 15-20 words maximum.
                Suggest focusing on constructive topics.
            """
        }
        
        category_additions = {
            ContentCategory.HEALTH_PANIC: """
                Add brief "consult your doctor" reminder. Keep total response under word limit.
            """,
            
            ContentCategory.SPAM: """
                Give a witty dismissal only. Don't engage with claims.
                TOTAL LIMIT: 20-25 words maximum.
            """
        }
        
        prompt = base_instruction + tone_instructions.get(tone_mode, "")
        
        if content_category in category_additions:
            prompt += category_additions[content_category]
        
        return prompt.strip()

    def should_respond(self, content_category: ContentCategory) -> bool:
        """Determine if the bot should respond to this content."""
        return content_category != ContentCategory.BLOCKED

    def get_fallback_response(self, content_category: ContentCategory) -> str:
        """Get a fallback response for edge cases."""
        
        fallbacks = {
            ContentCategory.BLOCKED: "I don't engage with that type of content. Let's keep it factual! 📚",
            ContentCategory.SPAM: "Your post is emptier than a juice cleanse. Try again with actual content. 💅",
            ContentCategory.SENSITIVE: "I understand this is a difficult topic. For accurate information, please consult appropriate professional resources.",
        }
        
        return fallbacks.get(
            content_category, 
            "Couldn't extract anything fact-checkable from that. Send me some juicy claims to roast! 🔥"
        )

# Sassy Fact Check 💅 — The Unhinged Fact-Check Bot

> *Where bad takes go to die, with a side of sass.*

**Sassy Fact Check** is an Instagram DM MCP server that roasts health myths and viral misinformation with spicy, unhinged facts. Think MythBusters meets Mean Girls with a PubMed subscription! 🔥📚

![Bot Demo](https://img.shields.io/badge/Status-Roasting%20Bad%20Takes-ff69b4)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Claude](https://img.shields.io/badge/Powered%20by-Claude%20AI-purple)
![MCP](https://img.shields.io/badge/MCP-Server-orange)

## 👑 Meet Valentina

<table>
<tr>
  <td>
    <img src="images/profile-pic.png" alt="Valentina" width="140" style="border-radius: 50%;" />
  </td>
  <td style="padding-left: 20px; vertical-align: top;">
    <strong>Valentina Factcheck 💅</strong> <code>she/her</code><br>
    💅 AI with attitude, facts with flavor<br>
    🚫 No BS. No sugarcoating.<br>
    ✉️ DM a claim — I snap back with sources
  </td>
</tr>
</table>

## ✨ Features

- **Sassy Fact-Checking**: Roasts misinformation with citations and attitude (25-35 words max!)
- **Smart Content Filtering**: Auto-adjusts tone for sensitive topics  
- **Multi-Response Modes**: Sassy, soft, neutral, and blocked responses
- **Claude Desktop Integration**: Works as MCP server with Claude Desktop
- **Analytics Tracking**: Logs interactions for daily sass statistics
- **Safety First**: Blocks conspiracy theories, softens for grief/trauma

## 🎬 Demo Video

*I built a sassy fact-checking AI that integrates with Instagram DMs. Watch it analyze health myths and generate perfect responses with citations and attitude!*

🎬 **Watch the full demo here** → [https://youtu.be/T88oVghXzVw](https://youtu.be/T88oVghXzVw)

### Demo Highlights:
- 🔥 **Health Myth Busting** - Apple cider vinegar claims demolished
- ⚡ **Safety Alerts** - Dangerous advice shut down instantly  
- 💙 **Smart Filtering** - Auto-softens for sensitive topics
- ✅ **System Status** - All components working perfectly

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- [Claude Desktop App](https://claude.ai/desktop)
- Instagram account (for future DM integration)
- Anthropic API key

### Installation

1. **Clone and setup virtual environment**
   ```bash
   git clone https://github.com/sangreal-007/sassy-factcheck-bot.git
   cd sassy-factcheck-bot
   
   # Create and activate virtual environment (required on macOS)
   python3 -m venv venv
   source venv/bin/activate
   
   # You should see (venv) in your terminal prompt
   
   # Interactive credential setup
   python setup_env.py
   
   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Configure Claude Desktop**
   
   First, get your exact paths:
   ```bash
   # Navigate to your project and get exact paths
   cd sassy-factcheck-bot
   pwd  # Shows your project directory
   echo "Python path: $(pwd)/venv/bin/python"
   echo "Script path: $(pwd)/src/mcp_server.py"
   ```

   Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:
   ```bash
   open -a TextEdit ~/Library/"Application Support"/Claude/claude_desktop_config.json
   ```
   ```json
   {
     "mcpServers": {
       "sassy_factcheck": {
         "command": "/Users/yourusername/sassy-factcheck-bot/venv/bin/python",
         "args": ["/Users/yourusername/sassy-factcheck-bot/src/mcp_server.py"]
       }
     }
   }
   ```

   **⚠️ Important:** Replace `/Users/yourusername/` with your actual path from the `pwd` command above. Don't use `/full/path/to/` - use your real paths!

   

4. **Test the bot**
   ```bash
   python src/mcp_server.py
   ```

5. **Restart Claude Desktop** and start roasting bad takes!

## 💬 How It Works

### Fact-Checking Flow
1. Use `fact_check_dm` tool in Claude Desktop
2. Bot analyzes content for safety and tone  
3. Claude generates short, sassy response with citation
4. Response: *"🙄 Vinegar burns fat like I burn calories watching Netflix! Takes 12 weeks for 2 lbs 💅 Source: Mayo Clinic"*

### Auto-Tone Detection
- **Health myths** → Sassy roasting 🔥
- **Sensitive topics** → Gentle approach 💙  
- **Conspiracy theories** → Blocked 🚫
- **Spam** → Maximum dismissal 🗑️

## 🎭 Response Modes (Auto-Selected)

| Mode | Trigger | Style | Example |
|------|---------|-------|---------|
| **Sassy** | Health myths, general claims | Witty, emoji-heavy, 25-35 words | "🙄 If that worked, we'd all be supermodels!" |
| **Soft** | Cancer, grief, mental health | Gentle, understanding | "I understand this is difficult. Please consult..." |
| **Neutral** | Professional contexts | Educational, minimal emojis | "Research shows this claim is inaccurate." |
| **Blocked** | Conspiracy theories | Polite refusal | "I don't engage with that content." |

## 📱 Instagram MCP Integration (HACKATHON FEATURE!)

Complete Instagram DM workflow integration using MCP server!

### Instagram-Specific Tools:

- **`send_sassy_instagram_dm`** - 🏆 Send sassy fact-check responses via Instagram DM
- **`check_instagram_dms`** - 📱 Monitor incoming Instagram DMs for fact-check requests
- **`instagram_integration_status`** - 🔍 Show Instagram MCP integration status

### Demo the Instagram Integration:

```bash
# Check integration status
Use instagram_integration_status

# Monitor for new claims
Use check_instagram_dms

# Send sassy response
Use send_sassy_instagram_dm with:
- username: "wellness_guru_fake"
- content: "Apple cider vinegar burns belly fat instantly"
```

**Result:** "🙄 If vinegar burned fat instantly, we'd all be supermodels! Reality: 2-4 lbs over 12 weeks 💅 Source: Mayo Clinic"

## 🛠️ Available MCP Tools

Once connected to Claude Desktop, you'll have access to these tools:

### Sassy Fact-Check Bot Tools:
- **`fact_check_dm`** - Fact-check Instagram DM content with sassy responses
- **`welcome_new_followers`** - Send welcome messages to new Instagram followers  
- **`get_bot_stats`** - Get daily statistics and analytics for the bot
- **`test_bot_system`** - Test all bot components (Claude API, filters, logging)
- **`update_bot_settings`** - Update bot personality and behavior settings

### Usage Examples:

```bash
Use fact_check_dm with:
- content: "Apple cider vinegar burns belly fat instantly"
- username: "wellness_guru_fake"
- message_type: "text"
```

```bash
Use test_bot_system to check all components
```

```bash
Use get_bot_stats to view daily analytics
```

## 🔧 Configuration

### Simple Setup (Only What You Need)
```bash
# Required
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password  
ANTHROPIC_API_KEY=your_claude_key

# Optional
ENABLE_SAFE_MODE=true  # Auto-soften for sensitive topics
LOG_INTERACTIONS=true  # Track daily stats
```

### Customize Filters
Edit `src/filters.py` to adjust:
- Sensitive topic keywords (auto-triggers soft mode)
- Health panic keywords (extra sassy)
- Blocked content (conspiracy theories)
- Response length limits

## 🧪 Testing Examples

Try these in Claude Desktop:

```bash
Use fact_check_dm with:
- content: "Green tea burns 100 calories per cup"
- username: "tea_fanatic"
```

```bash
Use fact_check_dm with:
- content: "Essential oils cure cancer naturally"  
- username: "wellness_guru"
```

```bash
Use test_bot_system to check all components
```

## 🎯 Example Responses

### Health Myth (Sassy Mode):
> **Input:** "Apple cider vinegar burns belly fat instantly"
> 
> **Output:** "🙄 If vinegar burned fat instantly, we'd all be supermodels! Reality: 2-4 lbs over 12 weeks 💅 Source: Mayo Clinic"

### Sensitive Topic (Auto-Soft Mode):
> **Input:** "My friend died of cancer because she didn't try natural healing"
> 
> **Output:** "I'm sorry for your loss. Cancer treatment is complex. For evidence-based information, please consult oncology professionals. Source: American Cancer Society"

### Conspiracy Theory (Blocked):
> **Input:** "Chemtrails are poisoning us all"
> 
> **Output:** "I don't engage with that type of content. Let's keep it factual! 📚"

## 🏆 Hackathon Submission

Built for the **Instagram DM MCP Hackathon** by Gala Labs!

### Categories targeting:
- 🌍 **Breaking the Internet** ($5k) - Viral sassy responses with scientific backing
- 🔮 **Technical Sorcery** ($2.5k) - Advanced AI integration + smart content filtering  
- 😱 **Holy Sh*t Award** ($2.5k) - Because fact-checking has never been this entertaining!

**Key Innovation:** Automatic tone adjustment based on content sensitivity while maintaining maximum sass for health misinformation.

## 🛠️ Technical Architecture

- **MCP Server**: Integrates with Claude Desktop as tool provider
- **Content Filtering**: Smart categorization with tone recommendation
- **AI Integration**: Claude 3.5 Sonnet for fact-checking and response generation
- **Safety Layer**: Multi-level filtering for sensitive content
- **Analytics**: JSON-based interaction logging with daily stats

## ⚠️ Important Notes

- **Virtual Environment Required**: macOS users must use virtual environments due to system Python restrictions
- **Instagram Integration**: Designed to work with Instagram DM MCP server (login issues may occur)
- **Demo Mode**: Bot can be tested via Claude Desktop tools even without Instagram connection
- **Response Length**: Optimized for 25-35 word responses perfect for social media

## 🤝 Contributing

1. Fork the repo
2. Create feature branch: `git checkout -b feature/more-sass`
3. Add your roasting capabilities
4. Test with: `python src/mcp_server.py`
5. Submit PR with maximum sass level 💅

## 📜 License

MIT License - Go forth and fact-check responsibly! 

## 💌 Contact

Built with 💅 and citations by **sangreal-007**

- GitHub: [@sangreal-007](https://github.com/sangreal-007)
- Repository: [sassy-factcheck-bot](https://github.com/sangreal-007/sassy-factcheck-bot)

---

*"In a world full of misinformation, be the citation." — Sassy Fact Check Bot* ✨

## 🚀 Hackathon Demo

Ready to roast some bad takes? Clone this repo, follow the setup, and start serving facts with attitude through Claude Desktop! 🔥📚💅

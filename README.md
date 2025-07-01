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
- **Dual MCP Architecture**: Instagram MCP + Sassy Bot MCP working together
- **Analytics Tracking**: Logs interactions for daily sass statistics
- **Safety First**: Blocks conspiracy theories, softens for grief/trauma

## 🎬 Demo Video

*I built a sassy fact-checking AI that integrates with Instagram DMs. Watch it analyze health myths and generate perfect responses with citations and attitude!*

🔥 **[Real Mode Demo](https://youtu.be/9XXiM9s8u8Q)**  
🎯 **[Demo Mode Demo](https://youtu.be/T88oVghXzVw)**

### Demo Highlights:
- 🔥 **Health Myth Busting** — Apple cider vinegar claims demolished  
- ⚡ **Safety Alerts** — Dangerous advice shut down instantly  
- 💙 **Smart Filtering** — Auto-softens for sensitive topics  
- ✅ **System Status** — All components working perfectly

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- [Claude Desktop App](https://claude.ai/desktop)
- [Instagram DM MCP](https://github.com/gala-labs/instagram-dm-mcp) by Gala Labs
- Instagram account (for real mode)
- Anthropic API key

### Installation

1. **Clone and set up virtual environment**
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

2. **Configure Claude Desktop for Dual MCP Setup**
   
   You need BOTH servers running for full functionality:
   
   First, get your exact paths:
   ```bash
   # Navigate to your project and get exact paths
   cd sassy-factcheck-bot
   pwd  # Shows your project directory
   ```

   Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:
   ```bash
   open -a TextEdit ~/Library/"Application Support"/Claude/claude_desktop_config.json
   ```
   ```json
   {
     "mcpServers": {
       "instagram_dms": {
         "command": "/Users/yourusername/.local/bin/uv",
         "args": [
           "run",
           "--directory",
           "/Users/yourusername/instagram_dm_mcp",
           "python",
           "src/mcp_server.py"
         ]
       },
       "sassy_factcheck": {
         "command": "/Users/yourusername/sassy-factcheck-bot/venv/bin/python",
         "args": ["/Users/yourusername/sassy-factcheck-bot/src/mcp_server.py"],
         "cwd": "/Users/yourusername/sassy-factcheck-bot"
       }
     }
   }
   ```

   **⚠️ Important:** Replace `/Users/yourusername/` with your actual path from the `pwd` command above.

3. **Test Both Servers**
   ```bash
   # Terminal 1: Start Instagram MCP (Gala Labs)
   cd ../instagram_dm_mcp
   uv run python src/mcp_server.py
   
   # Terminal 2: Start Sassy Bot
   cd sassy-factcheck-bot
   source venv/bin/activate
   python src/mcp_server.py
   ```

4. **Restart Claude Desktop** and start the complete dual MCP workflow!

## 🎛️ Demo vs Real Mode

Your bot supports both demo and real Instagram integration:

### Demo Mode (Default - Perfect for Testing)
```bash
# In your .env file
INSTAGRAM_REAL_MODE=false

# Features:
# ✅ Practice with fake health claims
# ✅ Test sassy response generation  
# ✅ Safe for development
# ✅ No Instagram account needed
```

### Real Mode (Live Instagram Integration)
```bash
# In your .env file  
INSTAGRAM_REAL_MODE=true

# Features:
# ✅ Real Instagram API via Gala Labs MCP
# ✅ Actual DM conversations
# ✅ Live fact-checking responses
# ✅ Production-ready deployment
```

### Switching Modes
```bash
# Edit your .env file
nano .env

# Change this line:
INSTAGRAM_REAL_MODE=false  # Demo mode
# OR
INSTAGRAM_REAL_MODE=true   # Real mode

# Restart your sassy bot server
python src/mcp_server.py
```

## ⚠️ Security Notice
**🛡️ For Real Mode: Use a dedicated test Instagram account, never your main account!**

Instagram actively detects automation and may restrict accounts. Create a throwaway account specifically for testing to protect your personal Instagram.

## 💬 How It Works

### Complete Dual MCP Workflow
1. **Instagram MCP**: `list_chats` → See real conversations
2. **Sassy Bot**: `generate_sassy_response` → Create viral response with source
3. **Instagram MCP**: `send_message` → Send to real Instagram user

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


## 🛠️ Available MCP Tools

### Sassy Bot MCP Tools (Response Generation):
- **`generate_sassy_response`** - Create viral fact-check responses with sources
- **`generate_welcome_message`** - Create welcome messages for new followers
- **`check_instagram_dms`** - Show practice claims (demo mode) or guide to Instagram MCP (real mode)
- **`instagram_integration_status`** - Show dual MCP integration status

### Instagram MCP Tools (Messaging - via Gala Labs):
- **`list_chats`** - See real Instagram conversations
- **`send_message`** - Send responses to real Instagram users
- **`get_user_followers`** - Check follower lists
- **`get_thread_details`** - Get full conversation history

### Usage Examples:

```bash
Use generate_sassy_response with:
- content: "Apple cider vinegar burns belly fat instantly"
- username: "wellness_guru_fake"
```

```bash
Use instagram_integration_status to check dual MCP setup
```

```bash
Use list_chats to see real Instagram conversations
```

## 🔧 Configuration

### Simple Setup (Only What You Need)
```bash
# Required
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password  
ANTHROPIC_API_KEY=your_claude_key

# Mode Selection
INSTAGRAM_REAL_MODE=true  # true for real Instagram, false for demo

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
# Demo Mode Testing
Use generate_sassy_response with:
- content: "Green tea burns 100 calories per cup"
- username: "tea_fanatic"
```

```bash
# Real Mode Testing
Use list_chats to see real conversations
Use generate_sassy_response for real claims
Use send_message to send responses
```

```bash
Use instagram_integration_status to check setup
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

**Key Innovation:** Dual MCP architecture with automatic tone adjustment based on content sensitivity while maintaining maximum sass for health misinformation.

## 🛠️ Technical Architecture

- **Dual MCP Setup**: Instagram MCP (Gala Labs) + Sassy Bot MCP working together
- **Instagram Operations**: Real Instagram API via Gala Labs Instagram DM MCP  
- **Response Generation**: Sassy Bot MCP with Claude API integration
- **Content Filtering**: Smart categorization with tone recommendation
- **Safety Layer**: Multi-level filtering for sensitive content
- **Mode Switching**: Demo/Real mode for development and production

## ⚠️ Important Notes

- **Dual MCP Required**: Both Instagram MCP and Sassy Bot MCP must be running
- **Virtual Environment Required**: macOS users must use virtual environments due to system Python restrictions
- **Demo Mode**: Perfect for testing without Instagram account - uses practice claims
- **Real Mode**: Connects to actual Instagram via Gala Labs MCP for live conversations
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

Ready to roast some bad takes? Clone this repo, follow the dual MCP setup, and start serving facts with attitude through Claude Desktop! 🔥📚💅

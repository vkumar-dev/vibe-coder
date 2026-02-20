# Vibe Coder - Autonomous App Factory

**Ship 6 products per day while you sleep.**

Vibe Coder is an agentic AI system that researches market trends, checks for duplicates, and autonomously builds 1 vibe app every 4 hours using Qwen CLI.

**Strategy:** 70% AI-infused apps + 30% viral-potential apps = Maximum innovation

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Vibe Coder System                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │   Research   │    │   Duplicate  │    │   Vibe App   │      │
│  │   Agent      │───▶│   Checker    │───▶│   Generator  │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│         │                   │                   │               │
│         ▼                   ▼                   ▼               │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │  trends.json │    │  duplicates  │    │  projects/   │      │
│  │  (research)  │    │  checked.json│    │  (built apps)│      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│                              │                                  │
│                              ▼                                  │
│                       ┌──────────────┐                          │
│                       │   Ralph Loop │                          │
│                       │   Scheduler  │                          │
│                       │   (4 hours)  │                          │
│                       └──────────────┘                          │
│                              │                                  │
│                              ▼                                  │
│                       ┌──────────────┐                          │
│                       │   GitHub     │                          │
│                       │   Auto-Push  │                          │
│                       └──────────────┘                          │
└─────────────────────────────────────────────────────────────────┘
```

## Core Agents

### 1. Research Agent
- Scans trending topics on GitHub, Product Hunt, Hacker News
- **Generates 70% AI-infused app ideas** (NLP, CV, ML, GenAI, Agents)
- **Generates 30% viral-potential apps** (simple, addictive, shareable)
- Prioritizes AI apps with higher scores

### 2. Duplicate Checker
- Queries your GitHub repos for similar projects
- Checks against built apps in `projects/`
- Uses fuzzy matching (0.7 threshold = skip)
- Saves you from rebuilding the same app

### 3. Vibe App Generator
- Uses Qwen CLI to autonomously build apps
- **AI-infused apps**: Include LangChain, AI service layer, API integrations
- **Standard apps**: Clean React + Node.js + SQLite stack
- Commits to GitHub automatically

## Ralph Loop Integration

Runs on a **4-hour cycle** (6 apps per day):
- Uses supervisor/worker architecture for resilience
- Auto-restarts on failure
- Comprehensive logging and monitoring

## Quick Start

### One-Liner Install (Recommended)

```bash
# Using curl
curl -sSL https://github.com/vkumar-dev/vibe-coder/raw/main/install.sh | bash

# Using wget
wget -qO- https://github.com/vkumar-dev/vibe-coder/raw/main/install.sh | bash
```

### Manual Install

```bash
git clone https://github.com/vkumar-dev/vibe-coder.git
cd vibe-coder
./setup.sh
source venv/bin/activate
```

### Run Locally (Free - No Hosting Needed)

```bash
# Single cycle
python vibe_coder.py run

# Continuous (1 app every 4 hours)
python vibe_coder.py daemon --interval 4

# Ralph Loop (resilient, auto-restart)
./supervisor.sh
```

### Free Cloud Hosting

#### GitHub Actions (100% Free)

Automatically runs every 4 hours:

1. Fork the repo
2. Enable GitHub Actions
3. Add secrets: `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`
4. It runs on schedule!

**Limit:** 2000 minutes/month (enough for ~16 days of 4-hour cycles)

#### Render (Free Tier)

- Free: 750 hours/month
- Auto-deploy from GitHub
- Use `Procfile` for deployment

#### Fly.io (Free Allowance)

```bash
docker build -t vibe-coder .
flyctl launch
flyctl deploy
```

Free allowance includes 3 shared VMs.

#### Self-Host (Always Free Options)

- **Oracle Cloud Always Free** - Free ARM VPS
- **Google Cloud Free Tier** - e2-micro instance
- **AWS Free Tier** - 12 months free

```bash
# Docker deployment
docker run -d \
  -v $(pwd)/projects:/app/projects \
  -v $(pwd)/logs:/app/logs \
  -e GITHUB_USER=your-user \
  -e ANTHROPIC_API_KEY=your-key \
  vibe-coder
```

### Paid Hosting (If You Have Budget)

#### Railway ($5/month)

```bash
railway login
railway init
railway up
```

Simplest deployment, but costs $5/month.

## Configuration

```yaml
# config.yaml
loop:
  interval_hours: 4
  max_restarts: 3

research:
  sources:
    - github_trending
    - product_hunt
    - hacker_news
  min_score: 7.0

duplicate_check:
  github_user: vkumar-dev
  check_local: true

generator:
  ai_tool: qwen-code
  auto_push: true
  repo_prefix: vibe-
```

## Output

Each cycle produces:
- New app in `projects/vibe-{name}/`
- Research report in `logs/research-{timestamp}.json`
- Build log in `logs/build-{timestamp}.log`
- GitHub repo: `vkumar-dev/vibe-{name}`

## Monitoring

```bash
# Check status
python vibe_coder.py status

# View logs
tail -f logs/vibe-coder.log

# List built apps
python vibe_coder.py list
```

## The Vibe

Build apps. Ship fast. Let the loop run.

**That's the vibe coder life.**

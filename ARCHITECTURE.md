# Vibe Coder - Architecture

## System Overview

Vibe Coder is an autonomous app factory that researches trends, checks for duplicates, and generates 1 vibe app every 4 hours using Qwen CLI.

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

## Core Components

### 1. Research Agent (`core/research.py`)

Researches trending topics from multiple sources:

- **GitHub Trending**: Uses `gh search repos` to find popular repositories
- **Hacker News**: Fetches top stories via Firebase API
- **Product Hunt**: (Optional) Monitors new product launches

Generates app ideas based on trend scores and patterns.

```python
agent = ResearchAgent()
result = agent.run_full_research()
# Returns: List[AppIdea]
```

### 2. Duplicate Checker (`core/duplicate_checker.py`)

Prevents building the same app twice:

- **GitHub Check**: Queries your repos via `gh repo list`
- **Local Check**: Scans `projects/` directory
- **Similarity Scoring**: Uses SequenceMatcher for fuzzy matching
- **Threshold**: 0.7 similarity = duplicate

```python
checker = DuplicateChecker(github_user="vkumar-dev")
check = checker.check_duplicate(idea_id, title, description)
# Returns: DuplicateCheck(is_duplicate, similarity_score, matches)
```

### 3. App Generator (`core/generator.py`)

Builds complete apps using AI:

- **Qwen CLI Integration**: Uses `qwen-code` for AI-powered generation
- **Template Fallback**: Creates React + Node.js + SQLite app if Qwen unavailable
- **Git Auto-Init**: Initializes git repo with commit
- **GitHub Auto-Push**: Creates repo and pushes via `gh repo create`

```python
generator = AppGenerator(config)
result = generator.generate_app(title, description, features, idea_id)
# Returns: AppGenerationResult(success, app_path, github_repo, files_created)
```

## Ralph Loop Architecture

### Worker (`worker.sh`)

Executes the vibe coding cycle every 4 hours:

```bash
while : do
  python3 vibe_coder.py run --max-ideas 5
  sleep 14400  # 4 hours
done
```

**Responsibilities:**
- Run research phase
- Check duplicates
- Generate 1 app
- Write heartbeat file
- Log output

### Supervisor (`supervisor.sh`)

Monitors worker health and restarts on failure:

```bash
while : do
  check_worker_status()
  if worker_failed:
    diagnose_failure()
    restart_worker()
  sleep 3600  # Check every 1 hour
done
```

**Responsibilities:**
- Check worker PID every 1 hour
- Verify heartbeat freshness (< 4.5 hours)
- Diagnose failures with AI
- Restart worker (max 3 attempts)
- Log all events

### State Machine

```
Worker:  STOPPED → STARTING → EXECUTING → SLEEPING → EXECUTING → ...
                          ↑                    │
                          └───── (4 hours) ────┘

Supervisor: STARTING → MONITORING → DIAGNOSING → RESTARTING → MONITORING
                         ↑              │
                         └──────────────┘
```

## Data Flow

### Cycle Execution

```
1. Research Phase
   ├─ Fetch GitHub trending (10 repos)
   ├─ Fetch Hacker News top stories (10 stories)
   └─ Generate 5 app ideas

2. Duplicate Check Phase
   ├─ Check GitHub repos (similarity > 0.7 = skip)
   ├─ Check local projects (similarity > 0.7 = skip)
   └─ Select first non-duplicate idea

3. Generation Phase
   ├─ Create project directory
   ├─ Generate code (Qwen CLI or template)
   ├─ Initialize git repo
   ├─ Push to GitHub
   └─ Log results

4. Sleep Phase
   └─ Wait 4 hours for next cycle
```

### File Structure

```
vibe-coder/
├── core/
│   ├── research.py         # Research agent
│   ├── duplicate_checker.py # Duplicate detection
│   ├── generator.py        # App generation
│   └── __init__.py
├── projects/               # Generated apps
├── logs/                   # Generation logs
├── state/                  # State files
│   ├── trends.json
│   ├── duplicates.json
│   ├── history.json
│   └── last_cycle.txt
├── .vibe-loop/             # Ralph Loop state
│   ├── worker.pid
│   ├── worker.heartbeat
│   ├── worker.output
│   ├── worker.error
│   └── restart_count
├── vibe_coder.py           # Main entry point
├── worker.sh               # Worker script
├── supervisor.sh           # Supervisor script
├── setup.sh                # Setup script
├── quickstart.sh           # Quick start
├── config.yaml             # Configuration
└── requirements.txt        # Dependencies
```

## Configuration

```yaml
loop:
  interval_hours: 4       # Cycle frequency
  max_restarts: 3         # Max restart attempts

research:
  sources:
    - github_trending
    - hacker_news
  min_score: 7.0
  max_trends: 10

duplicate_check:
  github_user: "vkumar-dev"
  similarity_threshold: 0.7

generator:
  ai_tool: "qwen-code"
  auto_push: true
  repo_prefix: "vibe-"
```

## Usage

### Single Cycle

```bash
cd vibe-coder
source venv/bin/activate
python vibe_coder.py run
```

### Daemon Mode (1 app every 4 hours)

```bash
python vibe_coder.py daemon --interval 4
```

### Ralph Loop (Resilient)

```bash
./supervisor.sh
```

### Quick Start

```bash
./quickstart.sh
```

## Monitoring

### Status

```bash
python vibe_coder.py status
```

### Logs

```bash
tail -f .vibe-loop/worker.output
tail -f .vibe-loop/supervisor.log
```

### History

```bash
cat state/history.json | jq '.[].apps_generated'
```

## Failure Scenarios

### 1. Network Timeout

- Worker times out on API call
- Heartbeat becomes stale
- Supervisor detects (> 4.5 hours)
- Supervisor restarts worker

### 2. GitHub API Rate Limit

- `gh` commands fail
- Duplicate check skips GitHub
- Local check still works
- Generation continues with template

### 3. Qwen CLI Unavailable

- Falls back to template generation
- Creates standard React + Node.js app
- Still pushes to GitHub

### 4. Max Restarts Exceeded

- Supervisor exits with code 1
- Manual intervention required
- Check `supervisor.log` for diagnosis

## Extending

### Add Research Source

```python
def research_custom_source(self) -> List[Trend]:
    # Fetch from your source
    return trends
```

### Add Tech Stack

```python
# In config.yaml
generator:
  stack:
    frontend: "vue"      # or "svelte", "react"
    backend: "python"    # or "node", "go"
    database: "postgres" # or "sqlite", "mysql"
```

### Add Notification

```python
# In supervisor.sh diagnose_failure()
curl -X POST "$SLACK_WEBHOOK" -d "{\"text\": \"Vibe Coder failed\"}"
```

## The Vibe

Build apps. Ship fast. Let the loop run.

**6 apps per day. 42 apps per week. Infinite possibilities.**

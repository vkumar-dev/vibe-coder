# Vibe Coder - Deployment Guide

## Quick Decision Guide

**No money for hosting?** → Use **GitHub Actions** (free) or run **locally**

**Have $5/month?** → Use **Railway** (easiest)

**Want free cloud?** → Use **Render** or **Fly.io**

**Have your own server?** → Use **Docker**

---

## Option 1: GitHub Actions (100% Free, Recommended)

Best for: Running automatically without managing servers

### Setup

1. **Fork the repository**
   ```bash
   gh repo fork vkumar-dev/vibe-coder --clone
   cd vibe-coder
   ```

2. **Enable GitHub Actions**
   - Go to your fork on GitHub
   - Click "Actions" tab
   - Click "Enable Actions"

3. **Add API Keys (Secrets)**
   - Go to Settings → Secrets and variables → Actions
   - Add these secrets:
     - `ANTHROPIC_API_KEY` (from https://console.anthropic.com)
     - `OPENAI_API_KEY` (from https://platform.openai.com)
     - `GITHUB_USER` (your GitHub username)

4. **Customize Schedule (Optional)**
   
   Edit `.github/workflows/vibe-coder.yml`:
   ```yaml
   on:
     schedule:
       # Run every 4 hours
       - cron: '0 */4 * * *'
   ```

5. **Commit and Push**
   ```bash
   git add .
   git commit -m "Setup vibe coder"
   git push
   ```

6. **Trigger First Run**
   - Go to Actions tab
   - Click "Vibe Coder - Scheduled App Generation"
   - Click "Run workflow"

### Pros
- ✅ Completely free (2000 minutes/month)
- ✅ No server management
- ✅ Auto-pushes generated apps to GitHub
- ✅ Built-in logging and artifacts

### Cons
- ⚠️ Limited to 2000 minutes/month (~16 days of 4-hour cycles)
- ⚠️ Can't run continuously (only on schedule)
- ⚠️ Need to monitor minute usage

### Cost Optimization

To maximize free minutes:
- Run every 6 hours instead of 4: `0 */6 * * *`
- Or run once daily: `0 0 * * *`
- Cancel long-running jobs if stuck

---

## Option 2: Render (Free Tier)

Best for: Free cloud hosting with minimal setup

### Setup

1. **Create Render Account**
   - Go to https://render.com
   - Sign up with GitHub

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repo

3. **Configure Service**
   ```
   Name: vibe-coder
   Region: Choose closest to you
   Branch: main
   Root Directory: (leave blank)
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: python run_worker.py
   ```

4. **Choose Free Plan**
   - Select "Free" tier
   - 750 hours/month free

5. **Add Environment Variables**
   ```
   GITHUB_USER=your-username
   ANTHROPIC_API_KEY=your-key
   OPENAI_API_KEY=your-key
   VIBE_INTERVAL=4
   ```

6. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment

### Keep Alive (Important!)

Free instances sleep after 15 minutes of inactivity. To keep alive:

```bash
# Use a free uptime monitor
https://cron-job.org
https://uptimerobot.com

# Ping your Render URL every 5 minutes
GET https://your-app.onrender.com/health
```

### Pros
- ✅ 750 hours/month free (enough for continuous running)
- ✅ Auto-deploy from Git
- ✅ Built-in logging

### Cons
- ⚠️ Free tier sleeps after inactivity
- ⚠️ Need external pinger to keep alive
- ⚠️ Limited resources on free tier

---

## Option 3: Fly.io (Free Allowance)

Best for: Docker-based deployment

### Setup

1. **Install Fly CLI**
   ```bash
   curl -L https://fly.io/install.sh | sh
   fly auth login
   ```

2. **Launch App**
   ```bash
   cd vibe-coder
   fly launch --name vibe-coder
   ```

3. **Configure**
   - Choose region
   - Select "No" for Postgres/Redis
   - Choose free allowance

4. **Set Secrets**
   ```bash
   fly secrets set GITHUB_USER=your-user
   fly secrets set ANTHROPIC_API_KEY=your-key
   fly secrets set OPENAI_API_KEY=your-key
   ```

5. **Deploy**
   ```bash
   fly deploy
   ```

### Free Allowance

- Up to 3 shared VMs free
- 25GB persistent volume free
- 160GB outbound transfer free

### Pros
- ✅ Free allowance generous
- ✅ Global edge locations
- ✅ Docker-based

### Cons
- ⚠️ Need credit card for signup
- ⚠️ Free tier can run out

---

## Option 4: Railway ($5/month)

Best for: Easiest paid deployment

### Setup

1. **Install Railway CLI**
   ```bash
   npm i -g @railway/cli
   railway login
   ```

2. **Initialize Project**
   ```bash
   railway init
   ```

3. **Add Variables**
   ```bash
   railway variables set GITHUB_USER=your-user
   railway variables set ANTHROPIC_API_KEY=your-key
   railway variables set OPENAI_API_KEY=your-key
   ```

4. **Deploy**
   ```bash
   railway up
   ```

### Pricing

- $5/month minimum
- Usage-based after that
- Usually stays around $5-7/month

### Pros
- ✅ Simplest deployment
- ✅ No sleeping
- ✅ Great DX

### Cons
- ⚠️ Costs $5/month minimum
- ⚠️ No free tier

---

## Option 5: Self-Host (Always Free Options)

### Oracle Cloud Always Free

Free ARM VPS (up to 4 OCPUs, 24GB RAM!)

1. **Sign up**: https://oracle.com/cloud/free
2. **Create VM instance** (Ampere A1)
3. **SSH into VM**
4. **Install vibe-coder**:
   ```bash
   curl -sSL https://github.com/vkumar-dev/vibe-coder/raw/main/install.sh | bash
   cd ~/vibe-coder
   ./quickstart.sh
   ```

### Google Cloud Free Tier

Free e2-micro instance (2 vCPU, 1GB RAM)

1. **Sign up**: https://cloud.google.com/free
2. **Create Compute Engine instance**
3. **Deploy vibe-coder**

### Docker Deployment

Works on any VPS:

```bash
docker build -t vibe-coder .

docker run -d \
  --name vibe-coder \
  -v $(pwd)/projects:/app/projects \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/state:/app/state \
  -e GITHUB_USER=your-user \
  -e ANTHROPIC_API_KEY=your-key \
  -e OPENAI_API_KEY=your-key \
  --restart unless-stopped \
  vibe-coder
```

### Docker Compose

```yaml
version: '3.8'

services:
  vibe-coder:
    build: .
    container_name: vibe-coder
    volumes:
      - ./projects:/app/projects
      - ./logs:/app/logs
      - ./state:/app/state
    environment:
      - GITHUB_USER=${GITHUB_USER}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - VIBE_INTERVAL=4
    restart: unless-stopped
```

---

## Option 6: Run Locally (Free, Most Control)

Best for: Development, testing, or if you have a spare computer

### Setup

```bash
curl -sSL https://github.com/vkumar-dev/vibe-coder/raw/main/install.sh | bash
cd ~/vibe-coder
source venv/bin/activate
```

### Run Continuously

```bash
# Terminal session 1
python vibe_coder.py daemon --interval 4

# Or use Ralph Loop (auto-restart)
./supervisor.sh
```

### Run in Background

```bash
# Using tmux (recommended)
tmux new -s vibe-coder
python vibe_coder.py daemon
# Ctrl+B, D to detach

# Reattach later
tmux attach -t vibe-coder

# Or using nohup
nohup python vibe_coder.py daemon > vibe-coder.log 2>&1 &
```

### Pros
- ✅ 100% free
- ✅ Full control
- ✅ No rate limits
- ✅ Fast iteration

### Cons
- ⚠️ Need to keep computer running
- ⚠️ Uses your bandwidth
- ⚠️ No automatic restarts (unless using supervisor)

---

## Comparison Table

| Method | Cost | Setup Time | Maintenance | Best For |
|--------|------|------------|-------------|----------|
| **GitHub Actions** | Free | 10 min | None | Automated runs |
| **Render** | Free* | 15 min | Low (need pinger) | Free cloud |
| **Fly.io** | Free* | 15 min | Low | Docker fans |
| **Railway** | $5/mo | 5 min | None | Easiest paid |
| **Oracle Cloud** | Free | 30 min | Medium | Power users |
| **Local** | Free | 5 min | Low | Dev/testing |

\* With limitations

---

## Monitoring & Maintenance

### Check Status

```bash
# Local
python vibe_coder.py status

# Logs
tail -f logs/vibe-coder.log

# GitHub Actions
# Check Actions tab on GitHub
```

### Common Issues

**Issue: Out of disk space**
```bash
# Clean old logs
find logs/ -name "*.log" -mtime +7 -delete

# Clean old artifacts
find projects/ -name ".git" -prune -o -type f -mtime +30 -delete
```

**Issue: API rate limits**
```bash
# Reduce frequency
# Edit config.yaml: interval_hours: 6
```

**Issue: Failed builds**
```bash
# Check logs
tail -f .vibe-loop/worker.error

# Restart worker
./supervisor.sh
```

---

## Recommended Setup

**For most users:**
1. Start with **local** to test
2. Move to **GitHub Actions** for automation
3. Upgrade to **Railway** if you have $5/month

**For zero budget:**
1. **GitHub Actions** (free, automated)
2. **Render** + uptime monitor (free cloud)
3. **Local** on spare computer

**For production:**
1. **Railway** ($5/month, hassle-free)
2. **Oracle Cloud** (free VPS, more setup)
3. **Your own server**

---

## Next Steps

1. **Choose deployment method** from above
2. **Get API keys**:
   - Anthropic: https://console.anthropic.com
   - OpenAI: https://platform.openai.com
3. **Deploy and monitor**
4. **Watch apps get generated!**

---

## Support

- Issues: https://github.com/vkumar-dev/vibe-coder/issues
- Discussions: https://github.com/vkumar-dev/vibe-coder/discussions

**Happy deploying! 🎨**

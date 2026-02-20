#!/bin/bash

################################################################################
# Setup GitHub Pages for Vibe Coder
#
# Usage: ./setup-pages.sh
################################################################################

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo ""
echo "========================================"
echo "  📄 Setting up GitHub Pages"
echo "========================================"
echo ""

# Check if gh CLI is available
if ! command -v gh &> /dev/null; then
    echo "❌ gh CLI not found. Please install from https://cli.github.com/"
    exit 1
fi

# Check authentication
echo "📦 Checking GitHub authentication..."
if ! gh auth status &> /dev/null; then
    echo "❌ Not authenticated with GitHub"
    echo "   Run: gh auth login"
    exit 1
fi
echo "✅ GitHub authenticated"

# Get repo info
REPO=$(gh repo view --json nameWithOwner -q '.nameWithOwner' 2>/dev/null || echo "")
if [ -z "$REPO" ]; then
    echo "❌ Not in a GitHub repository or repo not found"
    exit 1
fi
echo "✅ Repository: $REPO"

# Create docs directory for GitHub Pages
echo ""
echo "📁 Creating docs directory for GitHub Pages..."
mkdir -p docs

# Create index.html
cat > docs/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vibe Coder - Autonomous App Factory</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #fff;
        }
        
        .container {
            text-align: center;
            padding: 2rem;
            max-width: 800px;
        }
        
        h1 {
            font-size: 3.5rem;
            margin-bottom: 1rem;
            animation: fadeInDown 0.8s ease;
        }
        
        .subtitle {
            font-size: 1.5rem;
            opacity: 0.9;
            margin-bottom: 2rem;
            animation: fadeInUp 0.8s ease;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1.5rem;
            margin: 3rem 0;
            animation: fadeIn 1s ease;
        }
        
        .stat-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .stat-number {
            font-size: 2.5rem;
            font-weight: bold;
            display: block;
        }
        
        .stat-label {
            font-size: 0.9rem;
            opacity: 0.8;
            margin-top: 0.5rem;
        }
        
        .features {
            text-align: left;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            padding: 2rem;
            border-radius: 12px;
            margin: 2rem 0;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .features h2 {
            margin-bottom: 1rem;
        }
        
        .features ul {
            list-style: none;
        }
        
        .features li {
            padding: 0.5rem 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .features li:last-child {
            border-bottom: none;
        }
        
        .features li:before {
            content: "✨ ";
            margin-right: 0.5rem;
        }
        
        .buttons {
            display: flex;
            gap: 1rem;
            justify-content: center;
            flex-wrap: wrap;
            margin-top: 2rem;
        }
        
        .btn {
            display: inline-block;
            padding: 1rem 2rem;
            background: #fff;
            color: #667eea;
            text-decoration: none;
            border-radius: 8px;
            font-weight: bold;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
        }
        
        .btn-secondary {
            background: rgba(255, 255, 255, 0.2);
            color: #fff;
        }
        
        .status {
            margin-top: 2rem;
            padding: 1rem;
            background: rgba(76, 175, 80, 0.2);
            border-radius: 8px;
            border: 1px solid rgba(76, 175, 80, 0.4);
        }
        
        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes fadeIn {
            from {
                opacity: 0;
            }
            to {
                opacity: 1;
            }
        }
        
        @media (max-width: 600px) {
            h1 {
                font-size: 2rem;
            }
            .subtitle {
                font-size: 1.2rem;
            }
            .stat-number {
                font-size: 2rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎨 Vibe Coder</h1>
        <p class="subtitle">Ship 6 products per day while you sleep</p>
        
        <div class="stats">
            <div class="stat-card">
                <span class="stat-number">1</span>
                <span class="stat-label">App every 4 hours</span>
            </div>
            <div class="stat-card">
                <span class="stat-number">6</span>
                <span class="stat-label">Apps per day</span>
            </div>
            <div class="stat-card">
                <span class="stat-number">42</span>
                <span class="stat-label">Apps per week</span>
            </div>
            <div class="stat-card">
                <span class="stat-number">70%</span>
                <span class="stat-label">AI-infused</span>
            </div>
        </div>
        
        <div class="features">
            <h2>Features</h2>
            <ul>
                <li>Autonomous app generation with AI</li>
                <li>Duplicate detection (GitHub + local)</li>
                <li>70% AI-infused apps, 30% viral apps</li>
                <li>Auto-push to GitHub</li>
                <li>Ralph Loop supervisor/worker architecture</li>
                <li>Free hosting with GitHub Actions</li>
            </ul>
        </div>
        
        <div class="buttons">
            <a href="https://github.com/vkumar-dev/vibe-coder" class="btn">View on GitHub</a>
            <a href="https://github.com/vkumar-dev/vibe-coder/blob/main/README.md" class="btn btn-secondary">Documentation</a>
        </div>
        
        <div class="status">
            <strong>✅ Status:</strong> Generating apps autonomously
        </div>
    </div>
</body>
</html>
EOF

echo "✅ Created docs/index.html"

# Commit and push the docs folder
echo ""
echo "📦 Committing GitHub Pages..."
git add docs/
git commit -m "📄 Add GitHub Pages landing page" || echo "No changes to commit"
git push

# Enable GitHub Pages using API
echo ""
echo "🔧 Enabling GitHub Pages..."

# Use GitHub API to enable Pages (use -F for proper JSON formatting)
RESPONSE=$(gh api --method POST \
    /repos/{owner}/{repo}/pages \
    -F source[branch]=master \
    -F source[path]=/docs 2>&1 || true)

if echo "$RESPONSE" | grep -q "already enabled\|Invalid request"; then
    echo "✅ GitHub Pages already enabled"
elif echo "$RESPONSE" | grep -q "html_url"; then
    echo "✅ GitHub Pages enabled successfully"
else
    echo "⚠️  Response: $RESPONSE"
fi

# Get Pages URL
echo ""
echo "🌐 Getting Pages URL..."
PAGES_URL=$(gh api \
    -H "Accept: application/vnd.github.v3+json" \
    /repos/{owner}/{repo}/pages \
    -q '.html_url' 2>/dev/null || echo "https://vkumar-dev.github.io/vibe-coder/")

echo ""
echo "========================================"
echo "  ✅ GitHub Pages Setup Complete!"
echo "========================================"
echo ""
echo "🌐 Your site will be live at:"
echo "   $PAGES_URL"
echo ""
echo "⏱️  It may take 1-2 minutes to propagate"
echo ""
echo "📁 Files location: docs/"
echo ""
echo "To update the site:"
echo "   1. Edit docs/index.html"
echo "   2. git add docs/ && git commit && git push"
echo ""
echo "========================================"
echo ""

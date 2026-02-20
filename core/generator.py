#!/usr/bin/env python3
"""
Vibe Coder - App Generator Agent

Uses Qwen CLI to autonomously build vibe apps.
"""

import json
import os
import subprocess
import shutil
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class AppGenerationResult:
    """Result of app generation."""
    idea_id: str
    app_name: str
    app_path: str
    success: bool
    files_created: List[str] = field(default_factory=list)
    github_repo: Optional[str] = None
    error: Optional[str] = None
    duration_seconds: float = 0.0
    generated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class AppGenerator:
    """Generates apps using Qwen CLI."""
    
    def __init__(self, config: dict = None):
        self.config = config or {}
        self.projects_dir = os.path.join(os.path.dirname(__file__), '..', 'projects')
        self.logs_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
        self.ai_tool = self.config.get('generator', {}).get('ai_tool', 'qwen-code')
        self.repo_prefix = self.config.get('generator', {}).get('repo_prefix', 'vibe-')
        self.auto_push = self.config.get('generator', {}).get('auto_push', True)
        
        # Ensure directories exist
        os.makedirs(self.projects_dir, exist_ok=True)
        os.makedirs(self.logs_dir, exist_ok=True)
    
    def generate_app(self, idea_title: str, idea_description: str, idea_features: List[str], 
                     idea_id: str, is_ai_infused: bool = True, ai_capabilities: List[str] = None) -> AppGenerationResult:
        """Generate a complete app using Qwen CLI."""
        print(f"\n🚀 Generating app: {idea_title[:50]}...")
        print(f"   Type: {'🤖 AI-Infused' if is_ai_infused else '📱 Viral App'}")
        if is_ai_infused and ai_capabilities:
            print(f"   AI Capabilities: {', '.join(ai_capabilities)}")
        
        start_time = datetime.utcnow()
        
        # Create app name from title
        app_name = self._sanitize_name(idea_title)
        app_path = os.path.join(self.projects_dir, app_name)
        
        # Create project directory
        os.makedirs(app_path, exist_ok=True)
        
        try:
            # Build the prompt for Qwen CLI
            prompt = self._build_generation_prompt(idea_title, idea_description, idea_features, is_ai_infused, ai_capabilities)
            
            # Run Qwen CLI to generate the app
            files_created = self._run_qwen_code(prompt, app_path, is_ai_infused)
            
            # Initialize git repo
            self._init_git_repo(app_path)
            
            # Push to GitHub if enabled
            github_repo = None
            if self.auto_push:
                github_repo = self._push_to_github(app_path, app_name)
            
            duration = (datetime.utcnow() - start_time).total_seconds()
            
            result = AppGenerationResult(
                idea_id=idea_id,
                app_name=app_name,
                app_path=app_path,
                success=True,
                files_created=files_created,
                github_repo=github_repo,
                duration_seconds=duration
            )
            
            print(f"✅ App generated successfully in {duration:.1f}s")
            print(f"   Path: {app_path}")
            if github_repo:
                print(f"   Repo: {github_repo}")
            
        except Exception as e:
            duration = (datetime.utcnow() - start_time).total_seconds()
            
            result = AppGenerationResult(
                idea_id=idea_id,
                app_name=app_name,
                app_path=app_path,
                success=False,
                error=str(e),
                duration_seconds=duration
            )
            
            print(f"❌ App generation failed: {e}")
        
        # Save generation log
        self._save_generation_log(result)
        
        return result
    
    def _build_generation_prompt(self, title: str, description: str, features: List[str], 
                                   is_ai_infused: bool = True, ai_capabilities: List[str] = None) -> str:
        """Build the prompt for Qwen CLI."""
        
        ai_section = ""
        if is_ai_infused and ai_capabilities:
            ai_section = f"""
**AI Capabilities to Implement**:
{chr(10).join(f"- {cap}" for cap in ai_capabilities)}

**AI Integration Requirements**:
1. Use LangChain or similar framework for AI orchestration
2. Implement AI service layer for model inference
3. Add prompt templates for AI interactions
4. Include fallback responses when AI is unavailable
5. Log AI interactions for improvement
6. Add rate limiting for AI API calls

**AI Dependencies to Include**:
- langchain or langchain-core
- @anthropic/sdk or openai (for API access)
- transformers (for local models if needed)
- vector-store for embeddings (optional)
"""
        
        prompt = f"""
You are an expert full-stack developer. Build a complete, production-ready web application.

## App Requirements

**Title**: {title}
**Description**: {description}
**Type**: {'AI-Infused Application with intelligent features' if is_ai_infused else 'Viral Web Application'}

**Features to implement**:
{chr(10).join(f"- {f}" for f in features)}
{ai_section}
**Tech Stack**:
- Frontend: React with modern hooks
- Backend: Node.js with Express
- Database: SQLite for simplicity
- Styling: TailwindCSS for modern UI
{'- AI: LangChain for orchestration, API integration for LLM access' if is_ai_infused else ''}

**Requirements**:
1. Create a complete, runnable application
2. Include package.json with all dependencies
3. Create a README.md with setup instructions
4. Implement responsive design
5. Add error handling
6. Include example data or seed script
{'7. Implement AI service layer with proper abstraction' if is_ai_infused else ''}
{'8. Add AI-powered features that provide real value to users' if is_ai_infused else ''}

**File Structure**:
```
project/
├── package.json
├── README.md
├── server.js (or index.js)
├── services/
│   └── ai-service.js    {'# AI integration layer' if is_ai_infused else ''}
├── client/
│   ├── package.json
│   ├── public/
│   │   └── index.html
│   └── src/
│       ├── index.js
│       ├── App.js
│       └── components/
└── database/
    └── schema.sql
```

Generate all necessary files to make this app fully functional.
Focus on clean, maintainable code with proper error handling.
{'Make the AI features feel magical and seamless to users.' if is_ai_infused else ''}
"""
        return prompt
    
    def _run_qwen_code(self, prompt: str, output_dir: str, is_ai_infused: bool = False) -> List[str]:
        """Run Qwen CLI to generate code."""
        print(f"🤖 Running Qwen CLI to generate code...")
        
        files_created = []
        log_file = os.path.join(self.logs_dir, f"generation-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}.log")
        
        try:
            # Try using qwen-code CLI if available
            # First check if it's installed
            check_result = subprocess.run(
                ["which", "qwen-code"],
                capture_output=True,
                text=True
            )
            
            if check_result.returncode == 0:
                # qwen-code is available
                with open(log_file, 'w') as log:
                    log.write(f"Generation started at {datetime.utcnow().isoformat()}\n")
                    log.write(f"Prompt: {prompt[:500]}...\n")
                    log.write(f"Type: {'AI-Infused' if is_ai_infused else 'Standard'}\n\n")
                    
                    # Run qwen-code with the prompt
                    # Note: Adjust command based on actual qwen-code CLI interface
                    result = subprocess.run(
                        ["qwen-code", "--prompt", prompt, "--output", output_dir],
                        capture_output=True,
                        text=True,
                        timeout=600  # 10 minute timeout
                    )
                    
                    log.write(f"Exit code: {result.returncode}\n")
                    log.write(f"Stdout: {result.stdout}\n")
                    log.write(f"Stderr: {result.stderr}\n")
                
                # Scan for created files
                for root, dirs, files in os.walk(output_dir):
                    for file in files:
                        rel_path = os.path.relpath(os.path.join(root, file), output_dir)
                        files_created.append(rel_path)
            else:
                # qwen-code not available, create a template app
                print("⚠️  qwen-code CLI not found, creating template app...")
                files_created = self._create_template_app(output_dir, prompt, is_ai_infused)
                
                with open(log_file, 'w') as log:
                    log.write(f"Template app created at {datetime.utcnow().isoformat()}\n")
                    log.write(f"Type: {'AI-Infused' if is_ai_infused else 'Standard'}\n")
                    log.write(f"Files: {files_created}\n")
        
        except subprocess.TimeoutExpired:
            raise Exception("Qwen CLI timed out after 10 minutes")
        except Exception as e:
            # Fallback to template
            print(f"⚠️  Qwen CLI failed, using template: {e}")
            files_created = self._create_template_app(output_dir, prompt, is_ai_infused)
        
        return files_created
    
    def _create_template_app(self, output_dir: str, prompt: str, is_ai_infused: bool = False) -> List[str]:
        """Create a template app structure when Qwen CLI is unavailable."""
        files_created = []
        
        if is_ai_infused:
            return self._create_ai_template_app(output_dir, files_created)
        else:
            return self._create_standard_template_app(output_dir, files_created)
    
    def _create_ai_template_app(self, output_dir: str, files_created: List[str]) -> List[str]:
        """Create an AI-infused template app."""
        
        # Create package.json with AI dependencies
        package_json = {
            "name": os.path.basename(output_dir),
            "version": "1.0.0",
            "description": "AI-powered vibe-coded app",
            "main": "server.js",
            "scripts": {
                "start": "node server.js",
                "dev": "nodemon server.js",
                "client": "cd client && npm start",
                "build": "cd client && npm run build"
            },
            "dependencies": {
                "express": "^4.18.2",
                "cors": "^2.8.5",
                "better-sqlite3": "^9.0.0",
                "langchain": "^0.1.0",
                "@anthropic-ai/sdk": "^0.10.0",
                "openai": "^4.20.0",
                "dotenv": "^16.3.0"
            },
            "devDependencies": {
                "nodemon": "^3.0.0"
            }
        }
        
        package_path = os.path.join(output_dir, 'package.json')
        with open(package_path, 'w') as f:
            json.dump(package_json, f, indent=2)
        files_created.append('package.json')
        
        # Create AI service layer
        ai_service_js = """const { LangChain } = require('langchain');

class AIService {
  constructor() {
    this.apiKey = process.env.ANTHROPIC_API_KEY || process.env.OPENAI_API_KEY;
    this.enabled = !!this.apiKey;
    
    if (!this.enabled) {
      console.log('⚠️  AI service disabled - set API key in .env');
    }
  }

  async generate(prompt, context = {}) {
    if (!this.enabled) {
      return this.getFallbackResponse(prompt, context);
    }

    try {
      // Using LangChain for orchestration
      const response = await this.callAI(prompt, context);
      return {
        success: true,
        data: response,
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      console.error('AI service error:', error);
      return this.getFallbackResponse(prompt, context);
    }
  }

  async callAI(prompt, context) {
    // Implement actual AI call here
    // This is a placeholder for the AI integration
    return {
      message: 'AI response placeholder',
      suggestions: ['Suggestion 1', 'Suggestion 2', 'Suggestion 3']
    };
  }

  getFallbackResponse(prompt, context) {
    // Smart fallback when AI is unavailable
    return {
      success: true,
      data: {
        message: 'AI temporarily unavailable. Here are some suggestions based on your input.',
        suggestions: this.generateSimpleSuggestions(prompt)
      },
      fallback: true
    };
  }

  generateSimpleSuggestions(input) {
    // Simple rule-based suggestions as fallback
    const keywords = input.toLowerCase().split(' ');
    const suggestions = [];
    
    if (keywords.includes('create') || keywords.includes('build')) {
      suggestions.push('Start with a template');
      suggestions.push('Break down into smaller tasks');
    }
    if (keywords.includes('help') || keywords.includes('how')) {
      suggestions.push('Check the documentation');
      suggestions.push('Try our interactive tutorial');
    }
    
    return suggestions.length > 0 ? suggestions : ['Get started now', 'Explore features', 'View examples'];
  }

  async analyze(text) {
    // Sentiment analysis, categorization, etc.
    return {
      sentiment: 'neutral',
      categories: ['general'],
      confidence: 0.8
    };
  }

  async summarize(text) {
    // Text summarization
    return text.substring(0, 200) + '...';
  }
}

module.exports = new AIService();
"""
        ai_service_path = os.path.join(output_dir, 'services', 'ai-service.js')
        os.makedirs(os.path.dirname(ai_service_path), exist_ok=True)
        with open(ai_service_path, 'w') as f:
            f.write(ai_service_js)
        files_created.append('services/ai-service.js')
        
        # Create .env template
        env_content = """# AI API Keys (get from https://console.anthropic.com or https://platform.openai.com)
ANTHROPIC_API_KEY=
OPENAI_API_KEY=

# App Configuration
PORT=3000
NODE_ENV=development
"""
        env_path = os.path.join(output_dir, '.env.example')
        with open(env_path, 'w') as f:
            f.write(env_content)
        files_created.append('.env.example')
        
        # Create standard app files
        files_created.extend(self._create_standard_app_files(output_dir, True))
        
        return files_created
    
    def _create_standard_template_app(self, output_dir: str, files_created: List[str]) -> List[str]:
        """Create a standard (non-AI) template app."""
        
        # Create package.json
        package_json = {
            "name": os.path.basename(output_dir),
            "version": "1.0.0",
            "description": "Vibe-coded app",
            "main": "server.js",
            "scripts": {
                "start": "node server.js",
                "dev": "nodemon server.js",
                "client": "cd client && npm start",
                "build": "cd client && npm run build"
            },
            "dependencies": {
                "express": "^4.18.2",
                "cors": "^2.8.5",
                "better-sqlite3": "^9.0.0"
            },
            "devDependencies": {
                "nodemon": "^3.0.0"
            }
        }
        
        package_path = os.path.join(output_dir, 'package.json')
        with open(package_path, 'w') as f:
            json.dump(package_json, f, indent=2)
        files_created.append('package.json')
        
        # Create standard app files
        files_created.extend(self._create_standard_app_files(output_dir, False))
        
        return files_created
    
    def _create_standard_app_files(self, output_dir: str, is_ai: bool = False) -> List[str]:
        """Create standard app files (server, client, etc)."""
        files_created = []
        
        # Create server.js
        server_js = """const express = require('express');
const cors = require('cors');
const Database = require('better-sqlite3');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'client/build')));

// Initialize database
const db = new Database('./database/app.db');

// Create tables
db.exec(`
  CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
  )
`);

// API Routes
app.get('/api/items', (req, res) => {
  const items = db.prepare('SELECT * FROM items').all();
  res.json(items);
});

app.post('/api/items', (req, res) => {
  const { name, description } = req.body;
  const stmt = db.prepare('INSERT INTO items (name, description) VALUES (?, ?)');
  const result = stmt.run(name, description);
  res.json({ id: result.lastInsertRowid, name, description });
});

// Serve React app
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'client/build/index.html'));
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
"""
        server_path = os.path.join(output_dir, 'server.js')
        with open(server_path, 'w') as f:
            f.write(server_js)
        files_created.append('server.js')
        
        # Create README.md
        app_type = "AI-powered " if is_ai else ""
        readme = f"""# {os.path.basename(output_dir)}

{app_type}Vibe-coded application generated by Vibe Coder.

## Quick Start

```bash
# Install dependencies
npm install

# Run server
npm start

# Or development mode
npm run dev
```

## API Endpoints

- `GET /api/items` - Get all items
- `POST /api/items` - Create new item

## Tech Stack

- Express.js (Backend)
- React (Frontend)
- SQLite (Database)
{('- LangChain (AI Orchestration)\n- Anthropic/OpenAI (AI Models)' if is_ai else '')}

Generated by Vibe Coder - Autonomous App Factory
"""
        readme_path = os.path.join(output_dir, 'README.md')
        with open(readme_path, 'w') as f:
            f.write(readme)
        files_created.append('README.md')
        
        # Create client directory structure
        client_dir = os.path.join(output_dir, 'client')
        os.makedirs(client_dir, exist_ok=True)
        os.makedirs(os.path.join(client_dir, 'public'), exist_ok=True)
        os.makedirs(os.path.join(client_dir, 'src'), exist_ok=True)
        
        # Create client package.json
        client_package = {
            "name": "client",
            "version": "0.1.0",
            "private": True,
            "dependencies": {
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "react-scripts": "5.0.1"
            },
            "scripts": {
                "start": "react-scripts start",
                "build": "react-scripts build"
            },
            "browserslist": {
                "production": [">0.2%", "not dead", "not op_mini all"],
                "development": ["last 1 chrome version", "last 1 firefox version"]
            }
        }
        
        client_package_path = os.path.join(client_dir, 'package.json')
        with open(client_package_path, 'w') as f:
            json.dump(client_package, f, indent=2)
        files_created.append('client/package.json')
        
        # Create public/index.html
        index_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Vibe App</title>
</head>
<body>
  <noscript>You need to enable JavaScript to run this app.</noscript>
  <div id="root"></div>
</body>
</html>
"""
        index_path = os.path.join(client_dir, 'public', 'index.html')
        with open(index_path, 'w') as f:
            f.write(index_html)
        files_created.append('client/public/index.html')
        
        # Create src/index.js
        index_js = """import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
"""
        src_index_path = os.path.join(client_dir, 'src', 'index.js')
        with open(src_index_path, 'w') as f:
            f.write(index_js)
        files_created.append('client/src/index.js')
        
        # Create src/App.js
        app_js = """import React, { useState, useEffect } from 'react';

function App() {
  const [items, setItems] = useState([]);
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');

  useEffect(() => {
    fetch('/api/items')
      .then(res => res.json())
      .then(data => setItems(data));
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    fetch('/api/items', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, description })
    })
      .then(res => res.json())
      .then(item => {
        setItems([...items, item]);
        setName('');
        setDescription('');
      });
  };

  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
      <h1>Vibe App</h1>
      <form onSubmit={handleSubmit} style={{ marginBottom: '20px' }}>
        <input
          type="text"
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          style={{ display: 'block', width: '100%', marginBottom: '10px', padding: '8px' }}
        />
        <textarea
          placeholder="Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          style={{ display: 'block', width: '100%', marginBottom: '10px', padding: '8px' }}
        />
        <button type="submit" style={{ padding: '10px 20px' }}>Add Item</button>
      </form>
      <h2>Items</h2>
      <ul>
        {items.map(item => (
          <li key={item.id}>
            <strong>{item.name}</strong>: {item.description}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
"""
        app_js_path = os.path.join(client_dir, 'src', 'App.js')
        with open(app_js_path, 'w') as f:
            f.write(app_js)
        files_created.append('client/src/App.js')
        
        # Create database directory
        db_dir = os.path.join(output_dir, 'database')
        os.makedirs(db_dir, exist_ok=True)
        
        # Create .gitignore
        gitignore = """node_modules/
*.db
.DS_Store
client/build/
.env
"""
        gitignore_path = os.path.join(output_dir, '.gitignore')
        with open(gitignore_path, 'w') as f:
            f.write(gitignore)
        files_created.append('.gitignore')
        
        return files_created
    
    def _init_git_repo(self, app_path: str):
        """Initialize git repository."""
        print(f"📦 Initializing git repo...")
        
        subprocess.run(
            ["git", "init"],
            cwd=app_path,
            capture_output=True
        )
        subprocess.run(
            ["git", "add", "."],
            cwd=app_path,
            capture_output=True
        )
        subprocess.run(
            ["git", "commit", "-m", "Initial commit: Vibe-coded app"],
            cwd=app_path,
            capture_output=True
        )
    
    def _push_to_github(self, app_path: str, app_name: str) -> str:
        """Push to GitHub."""
        print(f"🚀 Pushing to GitHub...")
        
        repo_name = f"{self.repo_prefix}{app_name}"
        
        try:
            # Create repo via gh CLI
            subprocess.run(
                ["gh", "repo", "create", repo_name, "--public", "--source", app_path, "--push"],
                cwd=app_path,
                capture_output=True,
                timeout=60
            )
            return f"{self.config.get('github_user', 'vkumar-dev')}/{repo_name}"
        except Exception as e:
            print(f"⚠️  GitHub push failed: {e}")
            return None
    
    def _sanitize_name(self, title: str) -> str:
        """Sanitize app name for filesystem and GitHub."""
        # Remove special characters and spaces
        name = title.lower()
        name = ''.join(c if c.isalnum() else '-' for c in name)
        name = '-'.join(filter(None, name.split('-')))  # Remove consecutive dashes
        name = name[:50]  # Limit length
        return f"{self.repo_prefix}{name}"
    
    def _save_generation_log(self, result: AppGenerationResult):
        """Save generation result to log."""
        log_file = os.path.join(self.logs_dir, 'generations.json')
        
        # Load existing logs
        logs = []
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r') as f:
                    logs = json.load(f)
            except Exception:
                logs = []
        
        # Add new result
        logs.append({
            'idea_id': result.idea_id,
            'app_name': result.app_name,
            'app_path': result.app_path,
            'success': result.success,
            'files_created': result.files_created,
            'github_repo': result.github_repo,
            'error': result.error,
            'duration_seconds': result.duration_seconds,
            'generated_at': result.generated_at
        })
        
        # Save
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)


if __name__ == "__main__":
    generator = AppGenerator()
    
    # Test generation
    result = generator.generate_app(
        idea_title="Task Management Dashboard",
        idea_description="A simple task manager with drag-and-drop",
        idea_features=["Create tasks", "Drag and drop", "Due dates"],
        idea_id="test-001"
    )
    
    print(f"\nResult: Success={result.success}, Files={len(result.files_created)}")

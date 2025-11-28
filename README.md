# 🚀 AI DevOps Agent – Autonomous DevOps Agent

> ⚡ **AI DevOps Agent** – Automating code fixes, testing, and pull requests with intelligent backend + AI reasoning.

AI DevOps Agent is an intelligent automation tool that seamlessly integrates with GitHub repositories to streamline the entire development workflow. It leverages AI to detect and repair broken code, refactor for readability and style, and validate changes through automated testing. Once verified, it raises clean, well‑structured pull requests, all with minimal human intervention.

---

## About Project
- **Connects to GitHub**: Securely links to your repository using a personal access token.
- **Fetches Python files**: Reads source code directly from your repo.
- **AI Refactoring & Bug Fixing**: Uses Ollama + CodeLlama to:
  - Refactor messy code
  - Fix broken logic when tests fail
  - Ensure valid Python output (sanitized before saving)
- **Formatting**: Runs **Black** to enforce consistent style.
- **Testing**: Executes **pytest** to validate correctness.
- **Pull Requests**: Automatically commits changes and raises a PR back to your repo.
- **Frontend Dashboard**: React UI to connect repos, trigger checks and view PR status.

---

## 🛠️ How the Code Works
### Backend (FastAPI + Python)
- **`services/github_client.py`**  
  Handles GitHub API calls: branch creation, file updates, PR creation, file listing.
- **`services/fixers.py`**  
  Runs Black, pytest, and AI refactoring. Sanitizes Ollama output to strip markdown fences and explanations.
- **`routes/code.py`**  
  FastAPI route `/fix-and-pr`:
  1. Clones repo locally
  2. Iterates over Python files
  3. Calls AI to refactor/fix code
  4. Runs Black + pytest
  5. If tests fail, re-prompts AI with feedback
  6. Commits changes and raises PR

### AI Integration
- **Ollama + CodeLlama**  
  - Input: raw code + optional test failure feedback  
  - Output: corrected/refactored Python code only  
  - Sanitization ensures only valid code is saved  

### Frontend (React + Vite)
- **Components**:  
  - `RepoConnect` → Connect GitHub repo  
  - `CodeCheck` → Trigger AI refactor + tests  
  - `PRStatus` → Show PR creation status  

---

## ✨ Features
- 🔗 GitHub Integration
- 🤖 AI-Powered Code Fixes
- 🛠️ Automated Formatting (Black)
- ✅ Testing Automation (pytest)
- 📦 Pull Request Creation
- 🎨 Futuristic Dashboard UI

---

## ⚙️ Installation

```bash
# Clone the repo
git clone https://github.com/sakshisemalti/ai-devops-agent.git
cd frosttech

# Backend setup
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend setup
npm install
npm run dev
```
---

## Usage
- Connect your GitHub repo in the UI.

- Trigger Code Check to refactor, format and fix broken code.

- Backend runs Black and pytest automatically.

- If tests fail, AI re-prompts with feedback to fix the code.

- Review and merge the auto-generated PR.

---

## Contributing
Contributions are welcome!This project is open for changes.

- Fork the repository

- Create a feature branch (git checkout -b feature-name)

- Commit your changes (git commit -m "Add feature")

- Push to your branch (git push origin feature-name)

- Open a Pull Request
Please ensure your code passes Black formatting and pytest before submitting.
⚠️ Note: Only high-quality PRs that follow project standards and improve functionality will be accepted. Low-effort or untested contributions will be reject

---

## License
MIT License – free to use, modify and distribute.


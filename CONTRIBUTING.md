# Contributing to Shadow Swarm

First, thank you for your interest in contributing! **Shadow Swarm** is built by the community, for the community, to ensure the next generation of Agentic AI systems are secure, robust, and hardened against adversarial threats.

We welcome contributions of all kinds: bug fixes, new agent personas, UI enhancements, and documentation improvements.

## 🧠 Philosophy
We are building an elite Red Teaming framework. Code contributed here should be:
1. **Modular**: Agents in the Hive Mind should be easily swappable.
2. **Performant**: WebSockets and frontend transitions should remain buttery smooth.
3. **Well-Documented**: New features should include clear docstrings and comments explaining the *why*, not just the *how*.

---

## 🛠️ How to Contribute

### 1. Fork & Clone
Start by forking the repository to your own GitHub account, then clone it locally:
```bash
git clone https://github.com/YOUR_USERNAME/shadow-swarm.git
cd shadow-swarm
```

### 2. Create a Branch
Create a branch for your feature or bug fix. Use a descriptive name:
```bash
git checkout -b feature/new-infiltrator-payload
# or
git checkout -b fix/websocket-reconnection
```

### 3. Setup Your Environment
Follow the Installation instructions in the `README.md` to set up both the `backend` (FastAPI) and `shadow-console` (Next.js) environments.

### 4. Make Your Changes
- **Backend changes**: Ensure you are using type hints (Pydantic models) and handling async operations correctly to avoid blocking the Hive Mind.
- **Frontend changes**: Stick to the cyberpunk/glassmorphism aesthetic. Avoid adding unnecessary heavy libraries unless absolutely necessary.

### 5. Adding a New Agent Persona
If you are adding a new agent to the Hive Mind:
1. Create a new file in `backend/agents/`.
2. Define its specific system prompt and payload logic.
3. Register the agent in the main orchestration loop (`backend/main.py` or equivalent router).
4. Update the frontend if the new agent requires a unique badge color or icon.

### 6. Commit & Push
Write clear, concise commit messages.
```bash
git commit -m "feat: Add new prompt injection payload to INFILTRATOR agent"
git push origin feature/new-infiltrator-payload
```

### 7. Open a Pull Request (PR)
Go to the original Shadow Swarm repository and open a Pull Request. Provide a clear description of what you changed, why you changed it, and any testing you performed. Screenshots of frontend changes are highly appreciated!

---

## 🐞 Reporting Bugs
If you find a bug, please open an issue on GitHub. Include:
- A clear description of the problem.
- Steps to reproduce it.
- Your OS, Python version, and Node version.
- Any relevant logs from the backend or browser console.

## 💡 Requesting Features
Have an idea for a killer new feature? Open an issue with the `enhancement` tag and let's discuss it before you start coding!

---
*Welcome to the Swarm. Let's break some AI.*

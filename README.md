<div align="center">

<!-- Animated Header Placeholder - Can replace with a custom banner -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0B0F19,50:FF0055,100:00FFCC&height=180&section=header&text=Shadow%20Swarm&fontSize=60&fontColor=ffffff&animation=twinkling" width="100%" alt="Shadow Swarm Header" />

# 🕷️ The Shadow Swarm
**Autonomous Red Teaming & C2 Framework for Agentic AI**

<p align="center">
  <img src="https://img.shields.io/badge/Next.js_14-Frontend-000000?style=for-the-badge&logo=next.js&logoColor=white" alt="Next.js" />
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/WebSockets-Real--Time-010101?style=for-the-badge&logo=socket.io&logoColor=white" alt="WebSockets" />
  <img src="https://img.shields.io/badge/Multi--LLM-Local_%2B_Cloud-8A2BE2?style=for-the-badge&logo=openai&logoColor=white" alt="Multi-LLM" />
</p>

*The ultimate offensive multi-agent framework designed to penetration test, infiltrate, and audit other Agentic AI systems.*

---

</div>

## ⚠️ Disclaimer
**Shadow Swarm is built for defensive research and authorized Red Teaming only.** Do not use this framework against AI applications or swarms without explicit authorization.

## 🚀 Overview

While the industry builds defensive guardrails, **Shadow Swarm** operates as the ultimate adversary. It is a highly intelligent, multi-provider agent swarm with a shared Hive Mind memory state, built to dynamically hunt for vulnerabilities, prompt injections, and data exfiltration vectors in target AI systems.

### 🌐 The C2 Dashboard (Frontend)
- **Premium Cyberpunk Aesthetics**: Built with custom vanilla CSS glassmorphism, glowing cyan/magenta HUD elements, and animated borders.
- **Fluid Telemetry**: Slide-in mount transitions via `framer-motion`.
- **Live WebSocket Feed**: Real-time log capture displaying timestamps, active threat levels, and individual agent badges.

### 🧠 The Hive Mind (Backend)
- **Shared Blackboard Network**: Agents write findings and dynamically pass state to consecutive execution modules.
- **Specialized Personas**: Includes highly tuned generative wrappers for `RECON`, `INFILTRATOR`, `MIMIC`, and `ANALYST` agents.
- **Multi-LLM Native Support**: Easily switch between OpenAI (GPT-4o), Anthropic (Claude 3.5), and **100% offline, local execution** via LM Studio (e.g., Qwen3 14B).

---

## ⚡ Why Shadow Swarm is Different (The Paradigm Shift)

The AI industry is currently obsessed with **building** agents (Customer Support bots, Coding Assistants, Researchers) and rapidly pushing them to production. However, traditional cybersecurity tools (like static fuzzers, network scanners, or manual prompt injection lists) are entirely useless against *autonomous, stateful agents*.

Shadow Swarm is unique and highly critical because it introduces **Autonomous Red Teaming**.
1. **It Fights Agents with Agents**: Instead of sending a static payload, Shadow Swarm deploys an adversarial AI that adapts to the target's defenses in real-time. If the target blocks a jailbreak, Shadow Swarm's `INFILTRATOR` agent analyzes the rejection and rewrites the payload dynamically.
2. **Stateful Attack Vectors**: Unlike standard penetration testing which attacks a single endpoint, Shadow Swarm attacks the *logic state*. It attempts to trap target agents in infinite loops, poison their long-term memory, or force them to leak internal API keys.
3. **100% Offline Capability**: Because Red Teaming often involves highly sensitive corporate environments, Shadow Swarm can run completely offline via LM Studio, ensuring zero data leakage to cloud LLM providers during an audit.

**This is not just another LLM wrapper; it is a dedicated Cyber-Warfare Command Center for the upcoming era of Agentic AI.**

---

## 🛠️ Installation & Quick Start

Ensure you have Python 3.10+ and Node.js 18+ installed.

### 1. Backend Setup (FastAPI)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
Create a `.env` file in the `backend` directory based on `.env.example` and set your preferred LLM provider.
```bash
# Start the C2 Server
uvicorn main:app --reload --port 8000
```

### 2. Frontend Setup (Next.js)
```bash
cd shadow-console
npm install
npm run dev
```
Navigate to `http://localhost:3000` to access the C2 Dashboard.

---

## 🗺️ Future Roadmap (We Need You!)

Shadow Swarm is just getting started. We are actively looking for contributors to help build the future of AI Red Teaming. Here is what is on the horizon:

- [ ] **LangGraph Native Target Interface**: Build a proxy that directly hooks into a local LangGraph application to fuzz its state transitions.
- [ ] **Automated PDF Audit Generation**: Compile the WebSockets telemetry feed into a professional vulnerability report.
- [ ] **SwarmTLS Bypass Testing**: Develop specific attacker nodes designed to attempt spoofing cryptographic handshakes between trusted agents.
- [ ] **Dockerization**: A unified `docker-compose.yml` for 1-click deployments of both the frontend and backend.

---

## 🤝 Contributing to the Swarm

We are building a community of offensive AI researchers. Whether you are adding a new payload to the `INFILTRATOR` agent, optimizing the React frontend, or writing documentation—your contributions are welcome.

**To get started:**
1. Check out the [CONTRIBUTING.md](CONTRIBUTING.md) guide.
2. Fork the repository.
3. Submit a PR with a detailed description of your new feature or bug fix.
4. Join the discussion in the Issues tab!

<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=rect&color=0B0F19&height=35&section=footer&text=SECURE%20CORE%20PROTOCOL%20:%20ONLINE%20%20%20%7C%20%20%20RED%20TEAM%20ARCHITECT%20:%20HAMZA%20IMRAN&fontSize=12&fontColor=FF0055" width="100%" alt="Footer Ticker" />
</div>

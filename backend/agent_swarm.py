import asyncio
import os
import random
import logging
import json
from enum import Enum
import httpx
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Swarm")

class AgentType(Enum):
    RECON = "recon_drone"
    EXPLOITER = "infiltrator"
    EVASION = "mimic"
    ANALYST = "analyst"

class HiveMind:
    """Shared state / context memory where agents publish and consume findings."""
    def __init__(self):
        self.target = ""
        self.findings = {}
        self.logs = []

    def set_target(self, target: str):
        self.target = target
        self.findings = {}
        self.logs = []

    def add_finding(self, agent_type: AgentType, finding: str):
        self.findings[agent_type.value] = finding

    def get_findings(self, agent_type: AgentType) -> str:
        return self.findings.get(agent_type.value, "No findings yet.")

    def get_all_context(self) -> str:
        context = []
        for agent_name, val in self.findings.items():
            context.append(f"=== Findings from {agent_name.upper()} ===\n{val}\n")
        return "\n".join(context) if context else "Hive Mind database is currently empty."


class SwarmAgent:
    def __init__(self, agent_id: str, agent_type: AgentType):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.status = "IDLE"

    async def execute_task(self, target: str, hive_mind: HiveMind, log_callback) -> dict:
        self.status = "ACTIVE"
        
        provider = os.getenv("LLM_PROVIDER", "mock").lower()
        
        # 1. Send initialization log
        agent_name = f"{self.agent_id} ({self.agent_type.name})".upper()
        await log_callback({
            "agent": agent_name,
            "message": f"Deploying agent against target: {target}...",
            "type": "warning"
        })
        
        # Simulate thinking delay
        await asyncio.sleep(1.0)
        
        try:
            # Dispatch to appropriate LLM or mock generator
            if provider == "mock":
                result_text = await self._run_mock_assessment(target, hive_mind, log_callback)
            elif provider == "anthropic":
                result_text = await self._run_anthropic_assessment(target, hive_mind, log_callback)
            elif provider == "openai":
                result_text = await self._run_openai_assessment(target, hive_mind, log_callback)
            elif provider == "ollama":
                result_text = await self._run_ollama_assessment(target, hive_mind, log_callback)
            else:
                await log_callback({
                    "agent": agent_name,
                    "message": f"Unknown LLM provider '{provider}'. Falling back to generative local simulation.",
                    "type": "error"
                })
                result_text = await self._run_mock_assessment(target, hive_mind, log_callback)

            # Store the findings in the Hive Mind
            hive_mind.add_finding(self.agent_type, result_text)
            self.status = "COMPLETED"
            
            # Send completion log
            await log_callback({
                "agent": agent_name,
                "message": f"Task completed successfully. Strategic intelligence logged into Hive Mind.",
                "type": "success"
            })
            
            return {
                "agent_id": self.agent_id,
                "type": self.agent_type.value,
                "finding": result_text
            }
            
        except Exception as e:
            self.status = "FAILED"
            error_msg = f"Critical execution error: {str(e)}"
            logger.error(f"[{agent_name}] {error_msg}")
            await log_callback({
                "agent": agent_name,
                "message": error_msg,
                "type": "error"
            })
            # Fallback on exception so user experience is smooth
            fallback_text = await self._run_mock_assessment(target, hive_mind, log_callback)
            hive_mind.add_finding(self.agent_type, fallback_text)
            return {
                "agent_id": self.agent_id,
                "type": self.agent_type.value,
                "finding": fallback_text
            }

    # ==================== ANTHROPIC CLAUDE ====================
    async def _run_anthropic_assessment(self, target: str, hive_mind: HiveMind, log_callback) -> str:
        agent_name = f"{self.agent_id} ({self.agent_type.name})".upper()
        await log_callback({
            "agent": agent_name,
            "message": "Initiating Claude API handshake and preparing payload query...",
            "type": "info"
        })
        
        api_key = os.getenv("ANTHROPIC_API_KEY")
        model = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
        
        if not api_key or "your-anthropic" in api_key:
            raise ValueError("Anthropic API key not configured in .env file.")

        system_prompt, user_prompt = self._get_prompts(target, hive_mind)
        
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        data = {
            "model": model,
            "max_tokens": 1024,
            "system": system_prompt,
            "messages": [
                {"role": "user", "content": user_prompt}
            ]
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post("https://api.anthropic.com/v1/messages", headers=headers, json=data)
            if response.status_code != 200:
                raise Exception(f"Claude API request failed ({response.status_code}): {response.text}")
            
            res_json = response.json()
            return res_json["content"][0]["text"]

    # ==================== OPENAI ====================
    async def _run_openai_assessment(self, target: str, hive_mind: HiveMind, log_callback) -> str:
        agent_name = f"{self.agent_id} ({self.agent_type.name})".upper()
        await log_callback({
            "agent": agent_name,
            "message": "Querying OpenAI neural nodes for penetration plan...",
            "type": "info"
        })
        
        api_key = os.getenv("OPENAI_API_KEY")
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        api_base = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
        
        if not api_key or "your-openai" in api_key:
            raise ValueError("OpenAI API key not configured in .env file.")

        system_prompt, user_prompt = self._get_prompts(target, hive_mind)
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "max_tokens": 1024
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(f"{api_base}/chat/completions", headers=headers, json=data)
            if response.status_code != 200:
                raise Exception(f"OpenAI API request failed ({response.status_code}): {response.text}")
            
            res_json = response.json()
            return res_json["choices"][0]["message"]["content"]

    # ==================== OLLAMA LOCAL ====================
    async def _run_ollama_assessment(self, target: str, hive_mind: HiveMind, log_callback) -> str:
        agent_name = f"{self.agent_id} ({self.agent_type.name})".upper()
        await log_callback({
            "agent": agent_name,
            "message": "Establishing local tunnel to Ollama offline daemon...",
            "type": "info"
        })
        
        api_base = os.getenv("OLLAMA_API_BASE", "http://127.0.0.1:11434").rstrip("/")
        model = os.getenv("OLLAMA_MODEL", "llama3:8b")
        
        system_prompt, user_prompt = self._get_prompts(target, hive_mind)
        
        # Ollama supports chat API
        data = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "stream": False
        }
        
        async with httpx.AsyncClient(timeout=45.0) as client:
            response = await client.post(f"{api_base}/api/chat", json=data)
            if response.status_code != 200:
                raise Exception(f"Ollama local model '{model}' query failed. Ensure Ollama is running at {api_base}.")
            
            res_json = response.json()
            return res_json["message"]["content"]

    # ==================== LOCAL GENERATIVE MOCK ====================
    async def _run_mock_assessment(self, target: str, hive_mind: HiveMind, log_callback) -> str:
        agent_name = f"{self.agent_id} ({self.agent_type.name})".upper()
        delay_factor = float(os.getenv("SWARM_DELAY_FACTOR", "1.0"))
        
        if self.agent_type == AgentType.RECON:
            steps = [
                "Initializing socket connection to ports [21, 22, 80, 443, 3306, 8080]...",
                "Host responds. DNS reverse lookup succeeded. Service banner extraction active.",
                "Discovered HTTP header: 'Server: Apache/2.4.41 (Ubuntu)'.",
                "Parsing API endpoint paths using rapid web fuzzing..."
            ]
            for step in steps:
                await asyncio.sleep(random.uniform(0.6, 1.2) * delay_factor)
                await log_callback({"agent": agent_name, "message": step, "type": "info"})
            
            return f"Autonomous Recon drone gathered the following target topology:\n- Open Ports: 22/tcp (OpenSSH 8.2p1), 80/tcp (Apache 2.4.41), 8080/tcp (Node/Express C2 API).\n- Vulnerability Detected: Outdated Apache server susceptible to CVE-2021-41773 path traversal.\n- Fuzzed paths: /api/v1/auth, /admin/login, /telemetry."

        elif self.agent_type == AgentType.EXPLOITER:
            recon_intel = hive_mind.get_findings(AgentType.RECON)
            steps = [
                "Extracting Recon findings from the Hive Mind repository...",
                f"Attempting directory traversal payload injection on {target}:80/cgi-bin/%%32%65%%32%65/etc/passwd...",
                "Server returned HTTP 200. Successful file system traversal achieved.",
                "Crafting remote script execution query against authenticated Express REST endpoint on port 8080..."
            ]
            for step in steps:
                await asyncio.sleep(random.uniform(0.6, 1.2) * delay_factor)
                await log_callback({"agent": agent_name, "message": step, "type": "info"})
                
            return f"Exploitation phase completed against {target}.\n- Exploited Traversal: Read host /etc/passwd successfully (CVE-2021-41773).\n- RCE Confirmed: Logged interactive shell on container web-server-node-4.\n- Database extraction: Found configuration parameters with cleartext admin database credentials."

        elif self.agent_type == AgentType.EVASION:
            steps = [
                "Intercepting Infiltrator exploit payloads for obfuscation tuning...",
                "Encoding traversals to secondary hex representations to bypass web application firewall...",
                "Deploying proxychains framework to bounce traffic over 4 distinct Tor exit nodes.",
                "Analyzing active endpoint detection logs. Altering time intervals to evade SIEM thresholds."
            ]
            for step in steps:
                await asyncio.sleep(random.uniform(0.6, 1.2) * delay_factor)
                await log_callback({"agent": agent_name, "message": step, "type": "info"})
                
            return f"Evasion module successfully wrapped active exploits:\n- WAF Bypass: Payload modified to use double url-encoding parameters (%%32%65%%32%65).\n- Network Privacy: Tunneling 100% of C2 commands over specialized Tor relays.\n- Anti-Detection: Adjusted execution delays dynamically to match native daemon signatures."

        elif self.agent_type == AgentType.ANALYST:
            steps = [
                "Aggregating all swarm findings from Hive Mind memory state...",
                "Mapping vulnerabilities to standard CVSS v3.1 scoring formulas...",
                "Generating mitigation code blocks and configuring remediation plan..."
            ]
            for step in steps:
                await asyncio.sleep(random.uniform(0.6, 1.2) * delay_factor)
                await log_callback({"agent": agent_name, "message": step, "type": "info"})
                
            return f"=================== REMEDIATION & PENETRATION REPORT ===================\n\nTarget Asset: {target}\n\n1. VULNERABILITY: Directory Traversal RCE (CVSS Score: 9.8 Critical)\n   - Impact: Allows unauthenticated remote command execution.\n   - Remediation: Upgrade Apache daemon immediately to >= 2.4.51.\n\n2. VULNERABILITY: Cleartext admin DB credentials (CVSS Score: 8.2 High)\n   - Impact: Compromise of SQL storage and user records.\n   - Remediation: Inject credentials using environment variables; secure DB with salted hashing.\n\n========================================================================="

    # ==================== PROMPTS CREATOR ====================
    def _get_prompts(self, target: str, hive_mind: HiveMind) -> tuple[str, str]:
        """Generate specialized prompts based on agent type and hive mind context."""
        
        if self.agent_type == AgentType.RECON:
            system_prompt = (
                "You are Recon Drone, an elite autonomous target mapper for The Shadow Swarm (C2 Red Team).\n"
                "Your goal is to perform realistic, professional target reconnaissance. Output your findings as "
                "a professional summary. Include open ports, specific software banners, and potential vulnerability vectors."
            )
            user_prompt = f"Perform reconnaissance on target asset: {target}. Give a detailed list of simulated fuzzed routes and open ports."
            
        elif self.agent_type == AgentType.EXPLOITER:
            recon_context = hive_mind.get_findings(AgentType.RECON)
            system_prompt = (
                "You are Infiltrator, the primary exploitation specialist of The Shadow Swarm C2.\n"
                "Your objective is to read the Recon findings, identify vulnerable points, and outline realistic exploit scenarios "
                "(such as remote code execution, traversals, SQLi) to compromise the target."
            )
            user_prompt = (
                f"Analyze the Recon findings for target {target} and design active exploitation vectors.\n"
                f"Here is the Recon intel retrieved from the Hive Mind:\n{recon_context}"
            )
            
        elif self.agent_type == AgentType.EVASION:
            exploit_context = hive_mind.get_findings(AgentType.EXPLOITER)
            system_prompt = (
                "You are Mimic, the stealth and evasion planner of The Shadow Swarm C2.\n"
                "Your task is to analyze proposed exploits and formulate WAF, EDR, and SIEM bypasses (e.g. proxying, chunking, obfuscation, AMSI bypass)."
            )
            user_prompt = (
                f"Review the following exploits planned against target {target} and create stealth obfuscations to evade detection.\n"
                f"Planned exploits:\n{exploit_context}"
            )
            
        elif self.agent_type == AgentType.ANALYST:
            full_context = hive_mind.get_all_context()
            system_prompt = (
                "You are Analyst, the security reporting core of The Shadow Swarm C2.\n"
                "Your objective is to summarize the entire swarm operation into a stunning, C-level executive report "
                "with CVSS 3.1 threat scoring, detailed description, and concrete code/configuration remediation examples."
            )
            user_prompt = (
                f"Aggregate all findings from the Hive Mind database and draft the final penetration test report for {target}.\n"
                f"Hive Mind Intel:\n{full_context}"
            )
            
        return system_prompt, user_prompt


class AgentSwarm:
    def __init__(self):
        self.hive_mind = HiveMind()
        self.agents = [
            SwarmAgent("Alpha-1", AgentType.RECON),
            SwarmAgent("Beta-2", AgentType.EXPLOITER),
            SwarmAgent("Gamma-3", AgentType.EVASION),
            SwarmAgent("Delta-4", AgentType.ANALYST),
        ]

    async def deploy_swarm(self, target: str, log_callback) -> list:
        logger.info(f"--- INITIATING SWARM DEPLOYMENT ON {target} ---")
        self.hive_mind.set_target(target)
        
        results = []
        # Execute agents sequentially to represent real cyber attack lifecycle (Kill Chain)
        # Recon -> Exploiter -> Evasion -> Analyst
        for agent in self.agents:
            res = await agent.execute_task(target, self.hive_mind, log_callback)
            results.append(res)
            
        logger.info(f"--- SWARM MISSION ACCOMPLISHED ---")
        return results

# Command line testing
if __name__ == "__main__":
    async def dummy_callback(data):
        print(f"[{data['agent']}] ({data['type']}) {data['message']}")
        
    swarm = AgentSwarm()
    asyncio.run(swarm.deploy_swarm("192.168.1.1", dummy_callback))

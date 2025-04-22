# INFORMATION:
# - Tool: Nmap
# - Description: Network scanning tool
# - Usage: Scans networks for hosts and services
# - Parameters: target (required), ports (optional)

import subprocess
import logging
import re
from typing import List, Optional, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define dynamic mappings of phrases to Nmap options
KEYWORD_MAP = {
    "no ping": "-Pn",
    "skip ping": "-Pn",
    "version": "-sV",
    "service detection": "-sV",
    "os detection": "-O",
    "aggressive": "-A",
    "verbose": "-v",
    "top ports": "--top-ports 100",
    "udp": "-sU",
    "quick": "-T4",
}

def parse_nmap_prompt(prompt: str) -> Tuple[str, Optional[str], List[str]]:
    prompt = prompt.lower()
    options = []
    ports = None

    # Extract IP address (supports v4 only here)
    ip_match = re.search(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", prompt)
    target = ip_match.group(0) if ip_match else ""

    # Extract ports if mentioned like 'ports 22,80' or 'scan port 443'
    port_match = re.search(r"port[s]?\s*(\d{1,5}(?:\s*,\s*\d{1,5})*)", prompt)
    if port_match:
        ports = port_match.group(1).replace(" ", "")

    # Match keywords to options
    for phrase, option in KEYWORD_MAP.items():
        if phrase in prompt:
            options.append(option)

    return target, ports, options

def ExecNmap(
    target: str,
    ports: Optional[str] = None,
    options: Optional[List[str]] = None,
) -> str:
    """Run an Nmap network scan on the specified target."""
    logger.debug("Running Nmap with target=%s, ports=%s, options=%s", target, ports, options)

    if subprocess.run(["which", "nmap"], capture_output=True).returncode != 0:
        return {"error": "Nmap is not installed. Install it with 'sudo apt install nmap'."}

    cmd = ["nmap", target]
    if ports:
        cmd += ["-p", ports]
    if options:
        cmd += options

    logger.info("Executing command: %s", ' '.join(cmd))

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return {"success": True, "output": result.stdout}
    except subprocess.CalledProcessError as e:
        logger.error("Nmap command failed: %s", e.stderr)
        return {"success": False, "error": e.stderr.strip()}
    except Exception as e:
        logger.exception("Unexpected error during Nmap execution")
        return {"success": False, "error": f"Error executing Nmap scan: {str(e)}"}

def scan_from_prompt(prompt: str) -> str:
    target, ports, options = parse_nmap_prompt(prompt)
    if not target:
        return {"success": False, "error": "Could not detect a valid IP address in the prompt."}
    return ExecNmap(target, ports, options)


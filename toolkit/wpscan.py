# INFORMATION:
# - Tool: WPScan
# - Description: WordPress vulnerability scanner
# - Usage: Scans WordPress sites for vulnerabilities and security issues
# - Parameters: url (required), format (optional), api_token (optional)

import subprocess
import logging
from typing import Any, Dict, List, Optional
import json

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("wpscan-tool")

class WPScan:
    """WPScan tool wrapper class."""

    def __init__(self):
        """Initialize WPScan wrapper."""
        self._check_installed()

    def _check_installed(self) -> None:
        """Verify WPScan is installed."""
        try:
            subprocess.run(["wpscan", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            logger.info("WPScan installation verified.")
        except (subprocess.SubprocessError, FileNotFoundError):
            logger.warning("wpscan command not found. Make sure WPScan is installed and in your PATH.")
            raise RuntimeError("WPScan is not installed or not in PATH.")

    def get_version(self) -> Optional[str]:
        """Get installed WPScan version."""
        try:
            result = subprocess.run(["wpscan", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            version_line = result.stdout.strip().split('\n')[-1]
            logger.info(f"WPScan version: {version_line}")
            return version_line
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logger.error(f"WPScan version check failed: {e}")
            return None

    def scan(self, url: str, **kwargs: Any) -> Dict[str, Any]:
        """Run the WPScan scan."""
        if not url:
            raise ValueError("Target URL must be provided.")

        cmd = ["wpscan", "--url", url,"--random-user-agent","--ignore-main-redirect"]

        # Append additional options to the command
        if "format" in kwargs:
            cmd.append("--format")
            cmd.append(kwargs["format"])
        if kwargs.get("verbose", False):
            cmd.append("--verbose")
        if kwargs.get("random_user_agent", False):
            cmd.append("--random-user-agent")
        if "max_threads" in kwargs:
            cmd.append("--max-threads")
            cmd.append(str(kwargs["max_threads"]))
        if "api_token" in kwargs:
            cmd.append("--api-token")
            cmd.append(kwargs["api_token"])
        if "enumerate_opts" in kwargs:
            cmd.append("--enumerate")
            cmd.append(",".join(kwargs["enumerate_opts"]))
        
        logger.info(f"Preparing WPScan command: {' '.join(cmd)}")

        # Run the scan
        try:
            result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output = result.stdout
            # If format is json, parse it
            if kwargs.get("format", "json") == "json":
                return json.loads(output)
            return {"status": "success", "output": output}
        except subprocess.SubprocessError as e:
            logger.error(f"Error during WPScan scan: {e}")
            return {"status": "error", "message": str(e)}

# Example usage (optional convenience function)
def ExecWpscan(url: str, **kwargs: Any) -> Dict[str, Any]:
    """Convenience wrapper to run a WPScan scan."""
    scanner = WPScan()
    try:
        return scanner.scan(url, **kwargs)
    except Exception as e:
        logger.error(f"WPScan scan failed: {e}")
        return {"error": str(e)}

# INFORMATION:
# - Tool: Holehe
# - Description: Email account checker
# - Usage: Checks if an email address is registered on various websites
# - Parameters: email (required)

import subprocess
import logging
from typing import Dict, Any
# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("holehe-tool")


class Holehe:
    """
    Holehe wrapper class for checking email registrations.
    """

    def __init__(self):
        """Initialize Holehe wrapper."""
        logger.info("Holehe wrapper initialized.")

    def scan(self, email: str) -> Dict[str, Any]:
        """
        Run the holehe scan for a given email.
        
        Args:
            email (str): The email address to check.
        
        Returns:
            Dict[str, Any]: Result or error from the holehe command.
        """
        logger.info(f"Running Holehe scan for: {email}")
        try:
            result = subprocess.run(["holehe", email], capture_output=True, text=True, check=True)
            output = result.stdout.strip()
            return {
                "email": email,
                "success": True,
                "output": output
            }
        except subprocess.CalledProcessError as e:
            logger.error(f"Holehe scan failed: {e.stderr.strip()}")
            return {
                "email": email,
                "success": False,
                "error": e.stderr.strip()
            }


def ExecHolehe(email: str) -> Dict[str, Any]:
    """
    Convenience wrapper to run a holehe scan.
    
    Args:
        email (str): Email address to scan.
    
    Returns:
        Dict[str, Any]: Holehe scan results.
    """
    scanner = Holehe()
    return scanner.scan(email)

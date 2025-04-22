# INFORMATION:
# - Tool: Sublist3r
# - Description: Fast subdomain enumeration tool
# - Usage: Finds subdomains via search engines
# - Parameters: domain (required), output_dir (optional)

import subprocess
import os
import json
import logging
import re
from typing import List, Dict, Any

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("sublist3r-tool")


class Sublist3r:
    """
    Sublist3r wrapper class for subdomain enumeration.
    """

    def __init__(self):
        """Initialize Sublist3r wrapper."""
        logger.info("Sublist3r wrapper initialized.")

    def extract_subdomains_from_output(self, output: str) -> List[str]:
        """
        Extract subdomains from the command output.
        
        Args:
            output (str): Command output text
            
        Returns:
            List[str]: List of extracted subdomains
        """
        # Remove ANSI color codes
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        clean_output = ansi_escape.sub('', output)
        
        # Extract subdomains using regex
        # Look for lines that appear to be domains (contain at least one dot and no special chars)
        domain_pattern = re.compile(r'^(?:[\w-]+\.)+[\w-]+$', re.MULTILINE)
        return domain_pattern.findall(clean_output)

    def scan(self, domain: str, output_dir: str) -> Dict[str, Any]:
        """
        Run Sublist3r tool to enumerate subdomains of a given domain.

        Args:
            domain (str): The target domain to enumerate subdomains for.
            output_dir (str): The directory to save the output files.

        Returns:
            Dict[str, Any]: Results or error from the Sublist3r command.
        """
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        output_file = os.path.join(output_dir, f"{domain}_subdomains.txt")
        
        logger.info(f"Running Sublist3r scan for domain: {domain}")
        try:
            # Run without output file first to capture stdout
            result = subprocess.run(
                ["sublist3r", "-d", domain],
                capture_output=True, 
                text=True,
                check=True
            )
            output = result.stdout.strip()
            
            # Try to extract subdomains from the output
            subdomains_from_output = self.extract_subdomains_from_output(output)
            
            # Also try to run with output file as fallback
            subprocess.run(
                ["sublist3r", "-d", domain, "-o", output_file],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Parse the output file to get subdomains
            subdomains_from_file = []
            if os.path.exists(output_file):
                with open(output_file, 'r') as f:
                    subdomains_from_file = [line.strip() for line in f if line.strip()]
            
            # Combine subdomains from both sources
            subdomains = list(set(subdomains_from_output + subdomains_from_file))
            
            # Save results to JSON file
            json_output_file = os.path.join(output_dir, f"{domain}_subdomains.json")
            with open(json_output_file, 'w') as f:
                json.dump(subdomains, f)
                
            logger.info(f"Sublist3r found {len(subdomains)} subdomains for {domain}")
            logger.info(f"Sublist3r results saved to {json_output_file}")
            
            return {
                "domain": domain,
                "success": True,
                "subdomains": subdomains,
                "output": output
            }
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Sublist3r scan failed: {e.stderr.strip()}")
            return {
                "domain": domain,
                "success": False,
                "error": e.stderr.strip()
            }


def ExecSublist3r(domain: str, output_dir: str = "results") -> Dict[str, Any]:
    """
    Convenience wrapper to run a Sublist3r scan.
    
    Args:
        domain (str): The target domain to enumerate subdomains for.
        output_dir (str): The directory to save the output files, defaults to "results".
    
    Returns:
        Dict[str, Any]: Sublist3r scan results.
    """
    scanner = Sublist3r()
    return scanner.scan(domain, output_dir)
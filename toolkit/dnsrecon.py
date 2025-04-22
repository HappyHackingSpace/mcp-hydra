# INFORMATION:
# - Tool: DNSRecon
# - Description: DNS reconnaissance tool
# - Usage: Performs various DNS-related scans and enumeration
# - Parameters: domain (required), scan_type (optional), name_server (optional), range (optional), dictionary (optional)

import subprocess
import logging
from typing import Any, Dict, List, Optional
import json

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("dnsrecon-tool")

class DNSRecon:
    """DNSRecon tool wrapper class."""

    def __init__(self):
        """Initialize DNSRecon wrapper."""
        self._check_installed()

    def _check_installed(self) -> None:
        """Verify DNSRecon is installed."""
        try:
            subprocess.run(["dnsrecon", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            logger.info("DNSRecon installation verified.")
        except (subprocess.SubprocessError, FileNotFoundError):
            logger.warning("dnsrecon command not found. Make sure DNSRecon is installed and in your PATH.")
            raise RuntimeError("DNSRecon is not installed or not in PATH.")

    def get_version(self) -> Optional[str]:
        """Get installed DNSRecon version."""
        try:
            result = subprocess.run(["dnsrecon", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            version = result.stdout.strip() if result.stdout else result.stderr.strip()
            logger.info(f"DNSRecon version: {version}")
            return version
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logger.error(f"DNSRecon version check failed: {e}")
            return None

    def scan(self, domain: Optional[str] = None, scan_type: Optional[str] = "std", **kwargs: Any) -> Dict[str, Any]:
        """Run the DNSRecon scan."""
        cmd = ["dnsrecon"]
        
        # Handle required parameters based on scan type
        if scan_type == "rvl":
            if "range" not in kwargs:
                raise ValueError("IP range must be provided for reverse lookup scan type.")
            cmd.extend(["-t", scan_type, "-r", kwargs["range"]])
        elif scan_type not in ["tld", "zonewalk"]:
            if not domain:
                raise ValueError("Target domain must be provided for this scan type.")
            cmd.extend(["-t", scan_type, "-d", domain])
        else:
            if not domain:
                raise ValueError("Target domain must be provided.")
            cmd.extend(["-t", scan_type, "-d", domain])
            
        # Handle optional parameters
        if "name_server" in kwargs:
            cmd.extend(["-n", kwargs["name_server"]])
        if "dictionary" in kwargs:
            cmd.extend(["-D", kwargs["dictionary"]])
        if kwargs.get("filter_wildcard", False):
            cmd.append("-f")
        if kwargs.get("axfr", False):
            cmd.append("-a")
        if kwargs.get("spf", False):
            cmd.append("-s")
        if kwargs.get("bing", False):
            cmd.append("-b")
        if kwargs.get("yandex", False):
            cmd.append("-y")
        if kwargs.get("crt", False):
            cmd.append("-k")
        if kwargs.get("whois", False):
            cmd.append("-w")
        if kwargs.get("dnssec", False):
            cmd.append("-z")
        if "threads" in kwargs:
            cmd.extend(["--threads", str(kwargs["threads"])])
        if "lifetime" in kwargs:
            cmd.extend(["--lifetime", str(kwargs["lifetime"])])
        if kwargs.get("tcp", False):
            cmd.append("--tcp")
        if "db" in kwargs:
            cmd.extend(["--db", kwargs["db"]])
        if "xml" in kwargs:
            cmd.extend(["-x", kwargs["xml"]])
        if "csv" in kwargs:
            cmd.extend(["-c", kwargs["csv"]])
        if "json" in kwargs:
            cmd.extend(["-j", kwargs["json"]])
        if kwargs.get("ignore_wildcard", False):
            cmd.append("--iw")
        if kwargs.get("disable_check_recursion", False):
            cmd.append("--disable_check_recursion")
        if kwargs.get("disable_check_bindversion", False):
            cmd.append("--disable_check_bindversion")
        if kwargs.get("verbose", False):
            cmd.append("-v")
            
        logger.info(f"Preparing DNSRecon command: {' '.join(cmd)}")

        # Run the scan
        try:
            result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output = result.stdout
            
            # Parse results
            parse_result = self._parse_output(output)
            return {
                "status": "success",
                "command": " ".join(cmd),
                "raw_output": output,
                "results": parse_result
            }
        except subprocess.SubprocessError as e:
            logger.error(f"Error during DNSRecon scan: {e}")
            return {
                "status": "error",
                "message": str(e),
                "command": " ".join(cmd),
                "stderr": e.stderr if hasattr(e, 'stderr') else ""
            }
            
    def _parse_output(self, output: str) -> List[Dict[str, Any]]:
        """Parse the output from DNSRecon into structured data."""
        results = []
        lines = output.strip().split('\n')
        
        for line in lines:
            if '[*]' in line or '[-]' in line or '[+]' in line:
                # Skip the log/status lines
                continue
                
            parts = line.strip().split()
            if len(parts) >= 4:
                try:
                    record = {
                        "record_type": parts[0],
                        "name": parts[1],
                        "data": " ".join(parts[2:])
                    }
                    results.append(record)
                except Exception as e:
                    logger.error(f"Error parsing output line: {line}, error: {e}")
        
        return results

# Example usage (optional convenience function)
def ExecDNSRecon(domain: Optional[str] = None, scan_type: str = "std", **kwargs: Any) -> Dict[str, Any]:
    """Convenience wrapper to run a DNSRecon scan."""
    scanner = DNSRecon()
    try:
        return scanner.scan(domain, scan_type, **kwargs)
    except Exception as e:
        logger.error(f"DNSRecon scan failed: {e}")
        return {"error": str(e)}

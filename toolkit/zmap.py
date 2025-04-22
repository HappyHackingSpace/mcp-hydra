# INFORMATION:
# - Tool: ZMap
# - Description: High-speed network scanner
# - Usage: Scans large network ranges quickly
# - Parameters: target (required), port (required), bandwidth (optional)

from typing import Any, Dict, List
import ipaddress
import logging
import subprocess
import re
import random

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("zmap-tool")


class ZMap:
    """ZMap scanner class for network scanning operations."""

    def __init__(self):
        """Initialize ZMap scanner."""
        self.interface = "eth0"
        self.gateway_mac = self._generate_random_mac()
        self._check_installed()

    def _check_installed(self) -> None:
        """Verify ZMap is installed."""
        try:
            subprocess.run(["zmap", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except (subprocess.SubprocessError, FileNotFoundError):
            logger.warning("ZMap is not installed or not in PATH.")

    def _generate_random_mac(self) -> str:
        """Generate a random locally administered unicast MAC address."""
        mac = [0x02, 0x00, 0x00,
               random.randint(0x00, 0x7F),
               random.randint(0x00, 0xFF),
               random.randint(0x00, 0xFF)]
        return ':'.join(f'{b:02x}' for b in mac)

    def _convert_ip_range_to_cidr(self, ip_range: str) -> str:
        """Convert IP range or CIDR to canonical CIDR format."""
        try:
            network = ipaddress.IPv4Network(ip_range, strict=False)
            return str(network)
        except ValueError:
            pass

        match = re.match(r'(\d+\.\d+\.\d+\.\d+)-(\d+\.\d+\.\d+\.\d+)', ip_range)
        if not match:
            raise ValueError(f"Invalid IP range format: {ip_range}")

        start_ip, end_ip = match.group(1), match.group(2)
        start, end = ipaddress.IPv4Address(start_ip), ipaddress.IPv4Address(end_ip)

        for prefixlen in range(32, -1, -1):
            network = ipaddress.IPv4Network(f"{start_ip}/{prefixlen}", strict=False)
            if network[0] <= start and network[-1] >= end:
                return str(network)

        raise ValueError(f"Could not convert IP range {ip_range} to CIDR notation")

    def get_version(self) -> str:
        """Get installed ZMap version."""
        try:
            result = subprocess.run(["zmap", "--version"], check=True, stdout=subprocess.PIPE, text=True)
            return result.stdout.strip()
        except subprocess.SubprocessError as e:
            logger.error(f"ZMap version check failed: {e}")
            raise RuntimeError("ZMap is not installed or misconfigured.")

    def scan(self, target_port: int, subnets: List[str], bandwidth: str = "1M") -> Dict[str, Any]:
        """Run the ZMap scan."""
        cidr_subnets = [self._convert_ip_range_to_cidr(subnet) for subnet in subnets]

        if not (0 < target_port <= 65535):
            raise ValueError("Port must be between 1 and 65535")

        cmd = [
            "zmap",
            "-p", str(target_port),
            "-B", bandwidth,
            "-i", self.interface,
            "-G", self.gateway_mac,
            "--blacklist-file=/dev/null",
            "-o", "-"
        ]
        cmd.extend(cidr_subnets)

        logger.info(f"Running ZMap scan: {' '.join(cmd)}")

        try:
            result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            hosts = [line.strip() for line in result.stdout.splitlines() if line.strip()]
            return {
                "port": target_port,
                "hosts": hosts,
                "total_hosts": len(hosts),
                "subnets_scanned": cidr_subnets
            }
        except subprocess.CalledProcessError as e:
            logger.error(f"ZMap scan failed: {e.stderr.strip()}")
            return {
                "error": "Scan failed",
                "details": e.stderr,
                "exit_code": e.returncode
            }


def ExecZmap(target: str, port: int, bandwidth: str = "1M") -> Dict[str, Any]:
    """Convenience wrapper to run a ZMap scan."""
    zmap = ZMap()
    try:
        return zmap.scan(target_port=port, subnets=[target], bandwidth=bandwidth)
    except Exception as e:
        logger.error(f"Scan error: {e}")
        return {"error": str(e)}

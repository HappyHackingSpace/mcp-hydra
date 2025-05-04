from typing import List, Optional, Dict, Any

from mcp.server.fastmcp import FastMCP

from toolkit.holehe import ExecHolehe
from toolkit.nmap import ExecNmap
from toolkit.wpscan import ExecWpscan
from toolkit.zmap import ExecZmap
from toolkit.sqlmap import ExecSqlmap
from toolkit.ocr2text import ExecOcr2Text
from toolkit.sublist3r import ExecSublist3r
from toolkit.dnsrecon import ExecDNSRecon
from toolkit.sherlock import ExecSherlock

# Create server
mcp = FastMCP(name="HydraΜCP",
    version="0.1.0"
)


@mcp.tool()
def ZmapScanner(
    target: str,
    port: int,
    bandwidth: Optional[str] = "1M",
) -> Dict[str, Any]:
    """Wrapper for running ZMap network scanning."""
    return ExecZmap(target, port, bandwidth)


@mcp.tool()
def WPScanScanner(
    url: str,
) -> Dict[str, Any]:
    """Wrapper for running WPScan vulnerability scanning."""
    return ExecWpscan(url)


@mcp.tool()
def HoleheScanner(
    email: str,
) -> Dict[str, Any]:
    """Wrapper for running Holehe email registration checking."""
    return ExecHolehe(email)


@mcp.tool()
def NmapScanner(
    target: str,
    ports: Optional[str] = None,
) -> Dict[str, Any]:
    """Wrapper for running Nmap network scanning."""
    return ExecNmap(target, ports)


@mcp.tool()
def SqlmapScanner(
    url: str,
    data: Optional[str] = None,
) -> Dict[str, Any]:
    """Wrapper for running Sqlmap vulnerability scanning."""
    return ExecSqlmap(url, data)

@mcp.tool()
def OcrScanner(
    file_path: str,
) -> Dict[str, Any]:
    """Wrapper for running OCR (Optical Character Recognition) on images and PDFs.
    
    The file_path can be:
    - A local file path
    - A direct URL (http/https)
    - A URL prefixed with @ symbol
    """
    return ExecOcr2Text(file_path)

@mcp.tool()
def Sublist3rScanner(
    domain: str,
    output_dir: Optional[str] = "output",
) -> List[str]:
    """Wrapper for running Sublist3r subdomain enumeration."""
    return ExecSublist3r(domain, output_dir)

@mcp.tool()
def DNSReconScanner(
    domain: str,
    scan_type: Optional[str] = "std",
    name_server: Optional[str] = None,
    range: Optional[str] = None,
    dictionary: Optional[str] = None,
) -> Dict[str, Any]:
    """Wrapper for running DNSRecon for DNS reconnaissance."""
    kwargs = {}
    if name_server:
        kwargs["name_server"] = name_server
    if range:
        kwargs["range"] = range
    if dictionary:
        kwargs["dictionary"] = dictionary
    
    return ExecDNSRecon(domain, scan_type, **kwargs)

@mcp.tool()
def SherlockScanner(
    usernames: List[str],
) -> Dict[str, Any]:
    """Wrapper for running Sherlock username enumeration."""
    return ExecSherlock(usernames)


if __name__ == "__main__":
    mcp.run(transport="stdio")
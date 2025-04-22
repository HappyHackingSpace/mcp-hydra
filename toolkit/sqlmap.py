# INFORMATION:
# - Tool: SQLMap
# - Description: SQL injection vulnerability scanner
# - Usage: Detects and exploits SQL injection vulnerabilities in web applications
# - Parameters: url (required), data (optional)

import subprocess
import json
import logging
import re
from typing import List, Optional, Dict, Any, Union

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database Management System (DBMS) info variables
isDbmsFound = False
dbms = ""
dbmsVersion = ""
dbmsVersionFound = False

# Tamper scripts for various DBMS
tamperscripts = {
    "MySQL": [
        "union2urls", "randomcase", "space2comment", "between", "charencode"
    ],
    "PostgreSQL": [
        "randomcase", "space2comment", "postgreSQLbool"
    ],
    "Microsoft SQL Server": [
        "charencode", "space2comment", "union2urls", "mssql08"
    ],
    "Oracle": [
        "oracle2", "space2comment", "union2urls"
    ],
    "SQLite": [
        "randomcase", "space2comment", "union2urls", "sqliteunicode"
    ],
    "Generic": [
        "charencode", "space2comment", "union2urls"
    ]
}


def run_sqlmap(cmd: List[str]) -> subprocess.CompletedProcess:
    """
    Helper function to run the sqlmap command.
    
    Args:
        cmd: List of command-line arguments for sqlmap.
    
    Returns:
        subprocess.CompletedProcess: The result of running sqlmap.
    """
    logger.debug("Running sqlmap command: %s", " ".join(cmd))
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        return result
    except subprocess.CalledProcessError as e:
        logger.error("SQLMap command failed: %s", e.stderr)
        raise e


def check_sqlmap_installed() -> bool:
    """
    Check if sqlmap is installed on the system.
    
    Returns:
        bool: True if sqlmap is installed, False otherwise
    """
    try:
        subprocess.run(["which", "sqlmap"], capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def gather_information(url: str) -> bool:
    """
    Gather information about the target URL by running sqlmap with the --batch and -v 0 options.
    
    Args:
        url: Target URL to scan
    
    Returns:
        bool: True if the operation was successful, False otherwise
    """
    cmd = ["sqlmap", "-u", url, "--batch", "-v", "0"]
    
    try:
        result = run_sqlmap(cmd)
        return result.returncode == 0
    except subprocess.CalledProcessError:
        return False


def try_tamper(url: str, tamper: str) -> bool:
    """
    Try a specific tamper script on the target URL by running sqlmap with the --batch and -v 0 options.
    
    Args:
        url: Target URL to scan
        tamper: Tamper script to use
    
    Returns:
        bool: True if the operation was successful, False otherwise
    """
    cmd = ["sqlmap", "-u", url, "--batch", "-v", "0", "--tamper", tamper]
    
    try:
        result = run_sqlmap(cmd)
        return result.returncode == 0
    except subprocess.CalledProcessError:
        return False


def try_with_risk_and_level(url: str, risk: int, level: int) -> bool:
    """
    Try a specific risk and level on the target URL by running sqlmap with the --batch and -v 0 options.
    
    Args:
        url: Target URL to scan
        risk: Risk level (1-3)
        level: Level (1-5)
    
    Returns:
        bool: True if the operation was successful, False otherwise
    """
    cmd = ["sqlmap", "-u", url, "--batch", "-v", "0", "--level", str(level), "--risk", str(risk)]
    
    try:
        result = run_sqlmap(cmd)
        return result.returncode == 0
    except subprocess.CalledProcessError:
        return False


def try_with_technique(url: str, technique: str) -> bool:
    """
    Try a specific technique on the target URL by running sqlmap with the --batch and -v 0 options.
    
    Args:
        url: Target URL to scan
        technique: Technique to use (e.g., "B", "E", "T", "U")
    
    Returns:
        bool: True if the operation was successful, False otherwise
    """
    cmd = ["sqlmap", "-u", url, "--batch", "-v", "0", "--technique", technique]
    
    try:
        result = run_sqlmap(cmd)
        return result.returncode == 0
    except subprocess.CalledProcessError:
        return False


def ExecSqlmap(url: str, data: Optional[str] = None) -> Dict[str, Any]:
    """
    Run sqlmap with the given URL and data.
    
    Args:
        url: Target URL to scan
        data: POST data to include in the request
    
    Returns:
        Dict[str, Any]: Result or error from the sqlmap command
    """
    options = []
    if data:
        options.extend(["--data", data])
    
    cmd = ["sqlmap", "-u", url, "--batch", "-v", "0", "--output-dir=/tmp/sqlmap"]
    cmd.extend(options)
    
    try:
        result = run_sqlmap(cmd)
        parsed_output = parse_sqlmap_output(result.stdout)
        return {
            "success": True,
            "url": url,
            "results": parsed_output
        }
    except subprocess.CalledProcessError as e:
        return {
            "success": False,
            "error": str(e),
            "stderr": e.stderr
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def categorize_tamperscript(db_tech: str) -> str:
    """
    Categorizes tamper scripts by database technology.
    
    Args:
        db_tech: The name of the database technology (e.g., MySQL, PostgreSQL, etc.)
    
    Returns:
        str: JSON string containing the tamper scripts for the provided DB technology.
    """
    try:
        if db_tech in tamperscripts:
            return json.dumps({
                "success": True,
                "database": db_tech,
                "tamper_scripts": tamperscripts[db_tech]
            })
        else:
            return json.dumps({
                "success": False,
                "error": f"Tamper scripts for {db_tech} not found."
            })
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })


def parse_sqlmap_output(output: str) -> Dict[str, Any]:
    """
    Parse the output from sqlmap to extract useful information.
    
    Args:
        output: The stdout from sqlmap
    
    Returns:
        Dict: A dictionary containing parsed information
    """
    result = {
        "vulnerable": False,
        "dbms": None,
        "payloads": [],
        "tables": [],
        "raw_output": output
    }
    
    # Check if any vulnerability was found
    if "is vulnerable to" in output:
        result["vulnerable"] = True
    
    # Try to extract DBMS information
    dbms_match = re.search(r"back-end DBMS: (.+?)(?:\n|\[)", output)
    if dbms_match:
        result["dbms"] = dbms_match.group(1).strip()
    
    # Try to extract payload information
    payload_matches = re.findall(r"Payload: (.+?)(?:\n|$)", output)
    result["payloads"] = [p.strip() for p in payload_matches]
    
    # Extract tables if available
    tables_section = re.search(r"Database: .*?\nTable: (.*?)(?:\n\n|\Z)", output, re.DOTALL)
    if tables_section:
        tables_text = tables_section.group(1)
        tables = re.findall(r"\|\s+([^\|]+?)\s+\|", tables_text)
        result["tables"] = [t.strip() for t in tables]
    
    return result


def ExecSqlmap(url: str, data: Optional[str] = None) -> Dict[str, Any]:
    """
    Run sqlmap vulnerability scan on a specified target URL.
    Main entry point for the MCP server to call this tool.
    
    Args:
        url: Target URL to scan
        data: Optional POST data to include in the request
    
    Returns:
        Dict: JSON-serializable dictionary with scan results
    """
    logger.info(f"Starting SQLMap scan on {url}")
    
    # Check if sqlmap is installed
    if not check_sqlmap_installed():
        return {
            "success": False,
            "error": "SQLMap is not installed. Install it with 'pip install sqlmap' or 'apt-get install sqlmap'."
        }
    
    # Define base command
    cmd = ["sqlmap", "-u", url, "--batch", "--forms", "--json-output"]
    
    # Add data parameter if provided
    if data:
        cmd.extend(["--data", data])
    
    # Run initial scan
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        # Check if JSON output is available
        try:
            # Try to parse JSON output
            json_output_path = re.search(r"JSON report saved to: (.+)", result.stdout)
            if json_output_path:
                with open(json_output_path.group(1), 'r') as json_file:
                    json_data = json.load(json_file)
                    return {
                        "success": True,
                        "url": url,
                        "vulnerable": bool(json_data.get("vulnerabilities", [])),
                        "data": json_data
                    }
        except (json.JSONDecodeError, FileNotFoundError):
            pass
        
        # If JSON parsing failed, parse the output manually
        parsed_results = parse_sqlmap_output(result.stdout)
        return {
            "success": True,
            "url": url,
            "vulnerable": parsed_results["vulnerable"],
            "dbms": parsed_results["dbms"],
            "payloads": parsed_results["payloads"],
            "tables": parsed_results["tables"],
            "output": result.stdout
        }
    
    except subprocess.CalledProcessError as e:
        logger.error(f"SQLMap scan failed: {e.stderr}")
        return {
            "success": False,
            "error": "SQLMap scan failed",
            "details": e.stderr
        }
    except Exception as e:
        logger.exception("Unexpected error during SQLMap execution")
        return {
            "success": False,
            "error": f"Error executing SQLMap scan: {str(e)}"
        }



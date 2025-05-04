# INFORMATION:
# - Tool: Sherlock
# - Description: Username hunter for social networks
# - Usage: Finds usernames across multiple social networks
# - Parameters: usernames (required), various optional parameters

import subprocess
import logging
from typing import Dict, Any, List, Optional

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("sherlock-tool")


class Sherlock:
    """
    Sherlock wrapper class for hunting usernames across social networks.
    """

    def __init__(self):
        """Initialize Sherlock wrapper."""
        logger.info("Sherlock wrapper initialized.")

    def hunt(self, 
             usernames: List[str], 
             output: Optional[str] = None,
             folderoutput: Optional[str] = None,
             verbose: bool = False,
             tor: bool = False,
             unique_tor: bool = False,
             csv: bool = False,
             xlsx: bool = False,
             sites: Optional[List[str]] = None,
             proxy: Optional[str] = None,
             json_file: Optional[str] = None,
             timeout: Optional[int] = None,
             print_all: bool = False,
             print_found: bool = False,
             no_color: bool = False,
             browse: bool = False,
             local: bool = False,
             nsfw: bool = False
             ) -> Dict[str, Any]:
        """
        Run the sherlock hunt for given usernames.
        
        Args:
            usernames (List[str]): List of usernames to check.
            output (Optional[str]): Output file for single username results.
            folderoutput (Optional[str]): Output folder for multiple username results.
            verbose (bool): Display extra debugging information.
            tor (bool): Make requests over Tor.
            unique_tor (bool): Make requests over Tor with new circuit per request.
            csv (bool): Create CSV output file.
            xlsx (bool): Create XLSX output file.
            sites (Optional[List[str]]): Specific sites to check.
            proxy (Optional[str]): Proxy URL to use.
            json_file (Optional[str]): JSON file for data input.
            timeout (Optional[int]): Request timeout in seconds.
            print_all (bool): Output sites where username was not found.
            print_found (bool): Output sites where username was found.
            no_color (bool): Disable colored terminal output.
            browse (bool): Open results in browser.
            local (bool): Force use of local data.json file.
            nsfw (bool): Include NSFW sites in checks.
            
        Returns:
            Dict[str, Any]: Result or error from the sherlock command.
        """
        logger.info(f"Running Sherlock hunt for: {', '.join(usernames)}")
        
        cmd = ["sherlock"]
        
        # Add all flags and their values
        if verbose:
            cmd.append("--verbose")
        if folderoutput:
            cmd.extend(["--folderoutput", folderoutput])
        if output:
            cmd.extend(["--output", output])
        if tor:
            cmd.append("--tor")
        if unique_tor:
            cmd.append("--unique-tor")
        if csv:
            cmd.append("--csv")
        if xlsx:
            cmd.append("--xlsx")
        if sites:
            for site in sites:
                cmd.extend(["--site", site])
        if proxy:
            cmd.extend(["--proxy", proxy])
        if json_file:
            cmd.extend(["--json", json_file])
        if timeout:
            cmd.extend(["--timeout", str(timeout)])
        if print_all:
            cmd.append("--print-all")
        if print_found:
            cmd.append("--print-found")
        if no_color:
            cmd.append("--no-color")
        if browse:
            cmd.append("--browse")
        if local:
            cmd.append("--local")
        if nsfw:
            cmd.append("--nsfw")
        
        # Add usernames
        cmd.extend(usernames)
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            output = result.stdout.strip()
            return {
                "usernames": usernames,
                "success": True,
                "output": output
            }
        except subprocess.CalledProcessError as e:
            logger.error(f"Sherlock hunt failed: {e.stderr.strip()}")
            return {
                "usernames": usernames,
                "success": False,
                "error": e.stderr.strip()
            }


def ExecSherlock(usernames: List[str], **kwargs) -> Dict[str, Any]:
    """
    Convenience wrapper to run a sherlock username hunt.
    
    Args:
        usernames (List[str]): Usernames to hunt.
        **kwargs: Additional parameters to pass to Sherlock.hunt().
    
    Returns:
        Dict[str, Any]: Sherlock hunt results.
    """
    scanner = Sherlock()
    return scanner.hunt(usernames, **kwargs) 
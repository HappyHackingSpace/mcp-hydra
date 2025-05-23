# HydraΜCP — The Model Context Protocol (MCP) Pentesting Toolkit
```
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠿⠿⢿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣿⣿⠟⠙⠻⠿⠋⠙⠻⠷⠄⠀⠀⠀⠀⠀⠀⢸⣿
⣿⣿⣿⣿⣿⣿⠿⢿⠿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⣿⣿
⣿⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀⢀⣀⣤⣴⣶⣾⣿⣿⣿⣿⣿⣇⡀⠀⠈⠻⠿⣿⣿
⣿⣿⣿⠉⠉⠀⠀⠀⠀⣠⣶⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣷⣶⣶⣿⣿
⣿⠿⠟⠀⠀⠀⢀⣠⣾⣿⡿⠻⠿⠟⠙⠿⠟⠻⣿⡆⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿
⣿⠀⠀⠀⠀⢀⣾⠏⠈⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿
⣿⠀⠀⠀⠀⠈⠁⠀⠀⠀⠀⣠⣤⣶⣶⣶⣶⣦⡄⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿
⣿⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀⣾⣿⣿⣆⣤⣾⣿⣿⣿
⣿⠀h⠀⠀⠀⠀⠀⠀⠘⠛⠛⠻⣿⣿⣿⣿⣿⣿⣿⣿⣦⠈⣻⣿⣿⣿⣿⣿⣿⣿
⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⢻⣿⣿⡿⠿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⠀⠀⠀⠀⢀⣠⣤⣤⣤⣄⣀⠀⠀⠈⠛⠹⣿⠷⣄⠀⠀⠀⠀⠉⠉⠉⣹⣿⣿
⣿⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣷⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣶⣶⣿⣿⣿
⣿⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣶⣶⣆⡀⠀⠈⠻⠿⣿⣿⣿
⣿⣤⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣿⣿⣿
```
A lightweight, extensible cybersecurity toolkit that connects AI assistants to security tools through the Model Context Protocol (MCP), enabling AI-assisted security research, scanning, and analysis.

## Demo - Sqlmap
### Nmap
![nmap](/demos/nmap.gif)

### Sqlmap
![sqlmap](/demos/sqlmap.gif)

### Holehe
![holehe](/demos/holehe.gif)

### Ocr2Text
![ocr2text](/demos/ocr2text.png)

### Sherlock
![Sherlock](/demos/sherlock.gif)

## Installation

Build te Docker image
```bash
git clone https://github.com/happyhackingspace/mcp-hydra.git
cd mcp-hydra
docker build -t hydramcp .
```


### Usage

Edit your `claude_desktop_config.json`
```json
{
  "mcpServers": {
    "hydramcp": {
      "command": "docker",
      "args": ["run", "--rm", "-i","--name","hydramcp", "hydramcp"]
    }
  }
}
```
Or Copilot in vscode
```bash
mkdir -p .vscode
cd .vscode
touch mcp.json
```json
{
    "servers": {
        "hydramcp": {
            "command": "docker",
            "args": [
                "run",
                "--rm",
                "-i",
                "--net=host",
                "--privileged",
                "--name",
                "hydramcp",
                "hydramcp"
            ]
        }
    }
}
```

## You can use the following prompts to test the tools:
```
Sublist3r
> Use Sublist3rScanner to find all subdomains for example.com and save results to the "recon" folder.
--
DNSRecon
> Run a DNS reconnaissance scan on example.com using DNSReconScanner with standard scan type.
--
Holehe
> Use HoleheScanner to check if the email address user@example.com is registered on various websites.
--
Nmap
> Scan 192.168.1.1 with NmapScanner to check for open ports in the range 1-1000.
--
Ocr2Text
> Use OcrScanner to extract text from the screenshot at /path/to/image.png.
--
Sqlmap 
> Run SqlmapScanner on http://testphp.vulnweb.com/listproducts.php?cat=1 to check for SQL injection vulnerabilities.
--
WPScan
> Use WPScanScanner to scan the WordPress site at https://example.com for vulnerabilities.
--
Zmap
> Scan the subnet 192.168.1.0/24 for systems with port 80 open using ZmapScanner with 1M bandwidth.
```



## Changelog
### Implemented Tools
- [x] Sublist3r - Domain enumeration tool
- [x] DNSRecon - DNS Reconnaissance tool
- [x] Holehe - Email registration checker
- [x] Nmap - Network scanner
- [x] OCR - Optical Character Recognition
- [x] Sqlmap - SQL injection scanner
- [x] WPScan - WordPress security scanner
- [x] Zmap - Internet scanner

### Planned Tools
- [ ] gobuster
- [ ] TheHarvester
- [ ] GitRecon
- [ ] Phone carrier lookup
- [ ] Netcraft
- [ ] Cloudunflare (claudflare bypass)
- [ ] Censys
- [ ] Programmable search engine
- [ ] Wayback Machine
- [ ] Shodan
- [ ] Wappalyzer
- [ ] Hunter.io
- [ ] Nuclei
- [ ] Amass
- [ ] GitSecrets - @awslabs/git-secrets or @trufflesecurity/trufflehog
- [ ] Depixelization - https://github.com/spipm/Depixelization_poc
- [ ] ExifTool 
- [ ] Sudomy https://github.com/screetsec/Sudomy


## Contributing
If you want to contribute to this project, please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).

## Disclaimer
This project is for educational purposes only. Use it at your own risk. The author is not responsible for any damages or legal issues that may arise from the use of this software.

* **Version**: 0.1.0
* **License**: MIT
* **Author**: Built with ❤️ by [@atiilla](https://github.com/atiilla)
* **Community**: [@happyhackingspace](https://github.com/happyhackingspace) | https://happyhacking.space

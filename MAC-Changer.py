import argparse
import subprocess
import re
import random
import platform
import time
import os

print("""
   ▄▄▄▄███▄▄▄▄      ▄████████  ▄████████      ▄████████    ▄█    █▄       ▄████████ ███▄▄▄▄      ▄██████▄     ▄████████    ▄████████ 
 ▄██▀▀▀███▀▀▀██▄   ███    ███ ███    ███     ███    ███   ███    ███     ███    ███ ███▀▀▀██▄   ███    ███   ███    ███   ███    ███ 
 ███   ███   ███   ███    ███ ███    █▀      ███    █▀    ███    ███     ███    ███ ███   ███   ███    █▀    ███    █▀    ███    ███ 
 ███   ███   ███   ███    ███ ███            ███         ▄███▄▄▄▄███▄▄   ███    ███ ███   ███  ▄███         ▄███▄▄▄      ▄███▄▄▄▄██▀ 
 ███   ███   ███ ▀███████████ ███            ███        ▀▀███▀▀▀▀███▀  ▀███████████ ███   ███ ▀▀███ ████▄  ▀▀███▀▀▀     ▀▀███▀▀▀▀▀   
 ███   ███   ███   ███    ███ ███    █▄      ███    █▄    ███    ███     ███    ███ ███   ███   ███    ███   ███    █▄  ▀███████████ 
 ███   ███   ███   ███    ███ ███    ███     ███    ███   ███    ███     ███    ███ ███   ███   ███    ███   ███    ███   ███    ███ 
  ▀█   ███   █▀    ███    █▀  ████████▀      ████████▀    ███    █▀      ███    █▀   ▀█   █▀    ████████▀    ██████████   ███    ███ 
                                                                                                                          ███    ███ 
                                                                                                             ~by Kanan Kenny Yusifli

""")

period=0

LOG_FILE = "mac_change.log"

def is_valid_mac(mac):
    return re.match(r"^[0-9a-fA-F]{2}(:[0-9a-fA-F]{2}){5}$", mac) is not None

def get_interfaces():
    try:
        result = subprocess.check_output(["ip", "link", "show"]).decode()
        return re.findall(r'\d+: ([^:]+):', result)
    except subprocess.CalledProcessError:
        return []

def generate_random_mac():
    oui = [0x00, 0x16, 0x3e]  # Common OUI used for virtual MACs
    mac = oui + [random.randint(0x00, 0xff) for _ in range(3)]
    return ':'.join(f"{b:02x}" for b in mac)

def get_current_mac(interface):
    try:
        result = subprocess.check_output(["cat", f"/sys/class/net/{interface}/address"]).decode().strip()
        return result
    except Exception:
        return None

def change_mac(interface, new_mac):
    try:
        subprocess.run(["ip", "link", "set", interface, "down"], check=True)
        subprocess.run(["ip", "link", "set", interface, "address", new_mac], check=True)
        subprocess.run(["ip", "link", "set", interface, "up"], check=True)
        log_action(interface, new_mac)
        print(f"[+] MAC address for {interface} changed to {new_mac}")
    except subprocess.CalledProcessError:
        print(f"[-] Failed to change MAC for {interface}")

def log_action(interface, new_mac):
    with open(LOG_FILE, "a") as f:
        f.write(f"{time.ctime()} - {interface} -> {new_mac}\n")

def restore_original_mac(interface, original_mac):
    if original_mac:
        change_mac(interface, original_mac)
        print(f"[+] MAC address for {interface} restored to {original_mac}")

def parse_time_interval(t):
    try:
        unit = t[-1].lower()
        value = int(t[:-1])
        return value * {"s":1, "m":60, "h":3600}.get(unit, 1)
    except:
        raise argparse.ArgumentTypeError("Invalid time format. Use formats like 10s, 5m, or 1h")

def main():
    parser = argparse.ArgumentParser(description="Safe MAC Address Changer")
    parser.add_argument("-I", "--interface", help="Network interface to change MAC", required=False)
    parser.add_argument("-M", "--mac", help="New MAC address (or use 'r' for random)", required=False)
    parser.add_argument("-T", "--time", help="Change interval (e.g. 10s, 5m, 1h)", type=parse_time_interval)
    parser.add_argument("--list-interfaces", action="store_true", help="List available interfaces")
    parser.add_argument("--restore", action="store_true", help="Restore original MAC")
    args = parser.parse_args()

    if platform.system().lower() not in {"linux"}:
        print("[-] This script currently supports only Linux systems.")
        return

    if args.list_interfaces:
        interfaces = get_interfaces()
        print("Available Interfaces:")
        for iface in interfaces:
            print(f" - {iface}")
        return

    if not args.interface:
        print("[-] Interface is required. Use --list-interfaces to view available.")
        return

    original_mac = get_current_mac(args.interface)

    if args.restore:
        restore_original_mac(args.interface, original_mac)
        return

    if not args.mac:
        args.mac = "r"

    if args.time:
        print("[*] Press Ctrl+C to stop looped MAC change.")
        try:
            while True:
                new_mac = generate_random_mac() if args.mac.lower() == "r" else args.mac
                if not is_valid_mac(new_mac):
                    print("[-] Invalid MAC address format.")
                    break
                change_mac(args.interface, new_mac)
                time.sleep(args.time)
        except KeyboardInterrupt:
            print("\n[!] MAC change loop interrupted.")
    else:
        new_mac = generate_random_mac() if args.mac.lower() == "r" else args.mac
        if not is_valid_mac(new_mac):
            print("[-] Invalid MAC address format.")
            return
        change_mac(args.interface, new_mac)

if __name__ == "__main__":
    main()

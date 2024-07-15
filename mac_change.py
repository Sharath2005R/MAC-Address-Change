import subprocess
import optparse
import re

def get_args():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Enter the interface to change the MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="Enter the new MAC address")
    (options, arguments) = parser.parse_args()

    if not options.interface:
        parser.error("[-] Please specify the interface. Use --help for more information.")

    if not options.new_mac:
        parser.error("[-] Please specify the new MAC address. Use --help for more information.")

    return options

def mac_changer(interface, new_mac):
    print(f"\n[+] Changing MAC address for {interface} to {new_mac}\n")

    subprocess.call(["sudo", "ifconfig", interface, "down"])
    subprocess.call(["sudo", "ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["sudo", "ifconfig", interface, "up"])

def check_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface]).decode('utf-8')
    mac_addr_search = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_addr_search:
        return mac_addr_search.group(0).upper()
    else:
        print("MAC address not found")

options = get_args()
print(f"[*] Getting current MAC address for interface {options.interface}...")
current_mac = check_mac(options.interface)
print(f"Current MAC: {current_mac}\n")

new_mac = options.new_mac.upper()
mac_changer(options.interface, new_mac)

print(f"[*] Verifying new MAC address for interface {options.interface}...")
current_mac = check_mac(options.interface)
print(f"New MAC: {current_mac}\n")

if current_mac == new_mac:
    print(f"[+] MAC address successfully changed to {current_mac}")
else:
    print("[-] MAC address not changed")

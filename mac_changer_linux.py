# Basic MAC Addr changer
# Zachary Springer
# 01/02/22
# Uses Subprocess to run system commands in terminal on linux based OS
import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    #User inputs vars when program is writen in cmd line
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) = parser.parse_args()
    #Checks for valid inputs
    if not options.interface:
        #Error handler: Interface
        parser.error("[-] Please specify a valid interface, use --help for more information.")
    elif not options.new_mac:
        #Error handler: MAC Address
        parser.error("[-] Please specify a valid MAC Address, use --help for more information.")
    return options

    

def change_mac(interface, new_mac):
    print("[+] Changing mac address for " + interface + " to " + new_mac)
    # Shuts down wifi connection
    subprocess.call(["ifconfig", interface, "down"])
    # Changes MAC Addr
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    # Turns wifi back on
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", options.interface])
    print(ifconfig_result)

    mac_addr_check_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result.decode())
    if mac_addr_check_result:
        return mac_addr_check_result.group(0)
    else:
        print("[-] Could not read the MAC Address.")

#Takes inputs and assignes them to opts and args
options = get_arguments()

current_mac = get_current_mac(options.interface)
print("Current MAC = " + str(current_mac))

#calls change_mac func
change_mac(options.interface, options.new_mac)

change_mac = get_current_mac(options.interface)
if change_mac == options.new_mac:
    print("[+] MAC Address was successfully changed to " + current_mac)
else:
    print("[-] MAC Address was not changed")
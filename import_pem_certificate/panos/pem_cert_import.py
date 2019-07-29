import requests
import argparse
import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)


parser = argparse.ArgumentParser()
parser.add_argument("--TARGET_IP", help="IP address of the firewall", type=str)
parser.add_argument("--api_key", help="Firewall API Key", type=str)
parser.add_argument("--CERT_NAME", help="Certificate Label", type=str)
parser.add_argument("--CERT_FILE", help="Certificate File Name", type=str)
args = parser.parse_args()

target_ip = args.TARGET_IP
api_key = args.api_key
cert_name = args.CERT_NAME
cert_file = args.CERT_FILE


url = 'https://{}/api/?type=import&format=pem&category=certificate&certificate-name={}&key={}'.format(target_ip, cert_name, api_key)
files = {'file': ( cert_file, open('../../working/' + cert_file, 'rb'), 'application/octet-string', {'Expires': '0'})}
r = requests.post(url, files=files, verify=False)
print(r.text)

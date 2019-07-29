import requests
import argparse
import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)


parser = argparse.ArgumentParser()
parser.add_argument("--TARGET_IP", help="IP address of the firewall", type=str)
parser.add_argument("--api_key", help="Firewall API Key", type=str)
parser.add_argument("--duo_endpoint", help="Duo API Endpoint", type=str)
parser.add_argument("--duo_integration_key", help="Duo Integration Key", type=str)
parser.add_argument("--duo_secret_key", help="Duo Secret Key", type=str)
parser.add_argument("--mfa_profile_name", help="MFA Profile Name", type=str)
parser.add_argument("--auth_profile", help="Authentication Profile Name", type=str)
args = parser.parse_args()

target_ip = args.TARGET_IP
api_key = args.api_key
duo_endpoint = args.duo_endpoint
duo_integration_key = args.duo_integration_key
duo_secret_key = args.duo_secret_key
mfa_profile_name = args.mfa_profile_name
auth_profile = args.auth_profile

url = 'https://{}/api/?type=import&format=pem&category=certificate&certificate-name=DUO-Root-skillet&key={}'.format(target_ip, api_key)
files = {'file': ('cert_DUO-root.crt', open('cert_DUO-root.crt', 'rb'), 'application/octet-string', {'Expires': '0'})}
r = requests.post(url, files=files, verify=False)
print(r.text)


url = 'https://{}/api/?type=import&format=pem&category=certificate&certificate-name=DUO-Intermedate-skillet&key={}'.format(target_ip, api_key)
files = {'file': ('cert_DUO-intermediate.crt', open('cert_DUO-intermediate.crt', 'rb'), 'application/octet-string', {'Expires': '0'})}
r = requests.post(url, files=files, verify=False)
print(r.text)

url = 'https://{}/api/?type=config&action=set&xpath=/config/shared/certificate-profile/entry[@name=\'DUO-MFA-Service-Skillet\']&element=<CA><entry name="DUO-Root-skillet"/><entry name="DUO-Intermedate-skillet"/></CA>&key={}'.format(target_ip, api_key)
r = requests.get(url, verify=False)
print(r.text)

url = 'https://{}/api/?type=config&action=set&xpath=/config/shared/server-profile/mfa-server-profile/entry[@name=\'{}\']&element=<mfa-config><entry name="duo-api-host"><value>{}</value></entry><entry name="duo-integration-key"><value>{}</value></entry><entry name="duo-secret-key"><value>{}</value></entry><entry name="duo-timeout"><value>30</value></entry><entry name="duo-baseuri"><value>/auth/v2</value></entry></mfa-config><mfa-vendor-type>duo-security-v2</mfa-vendor-type><mfa-cert-profile>DUO-MFA-Service-Skillet</mfa-cert-profile>&key={}'.format(target_ip, mfa_profile_name, duo_endpoint, duo_integration_key, duo_secret_key, api_key)
r = requests.get(url, verify=False)
print(r.text)

url = 'https://{}/api/?type=config&action=set&xpath=/config/shared/authentication-profile/entry[@name=\'{}\']&element=<multi-factor-auth><factors><member>{}</member></factors><mfa-enable>yes</mfa-enable></multi-factor-auth><method><local-database/></method><allow-list><member>all</member></allow-list>&key={}'.format(target_ip, auth_profile, mfa_profile_name, api_key)
r = requests.get(url, verify=False)
print(r.text)



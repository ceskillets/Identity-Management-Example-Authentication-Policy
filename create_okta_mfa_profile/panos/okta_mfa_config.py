import requests
import argparse
import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)


parser = argparse.ArgumentParser()
parser.add_argument("--TARGET_IP", help="IP address of the firewall", type=str)
parser.add_argument("--api_key", help="Firewall API Key", type=str)
parser.add_argument("--okta_endpoint", help="Okta API Endpoint", type=str)
parser.add_argument("--okta_token", help="Okta API Token", type=str)
parser.add_argument("--okta_org", help="okta company name", type=str)
parser.add_argument("--mfa_profile_name", help="MFA Profile Name", type=str)
parser.add_argument("--auth_profile", help="Authentication Profile Name", type=str)
args = parser.parse_args()

target_ip = args.TARGET_IP
api_key = args.api_key
okta_endpoint = args.okta_endpoint
okta_token = args.okta_token
okta_org = args.okta_org
mfa_profile_name = args.mfa_profile_name
auth_profile = args.auth_profile

url = 'https://{}/api/?type=import&format=pem&category=certificate&certificate-name=OKTA-Root-skillet&key={}'.format(target_ip, api_key)
files = {'file': ('cert_DUO-root.crt', open('cert_OKTA-root.crt', 'rb'), 'application/octet-string', {'Expires': '0'})}
r = requests.post(url, files=files, verify=False)
print(r.text)


url = 'https://{}/api/?type=import&format=pem&category=certificate&certificate-name=OKTA-Intermedate-skillet&key={}'.format(target_ip, api_key)
files = {'file': ('cert_DUO-intermediate.crt', open('cert_OKTA-intermediate.crt', 'rb'), 'application/octet-string', {'Expires': '0'})}
r = requests.post(url, files=files, verify=False)
print(r.text)

url = 'https://{}/api/?type=config&action=set&xpath=/config/shared/certificate-profile/entry[@name=\'OKTA-MFA-Service-Skillet\']&element=<CA><entry name="OKTA-Root-skillet"/><entry name="OKTA-Intermedate-skillet"/></CA>&key={}'.format(target_ip, api_key)
r = requests.get(url, verify=False)
print(r.text)

url = 'https://{}/api/?type=config&action=set&xpath=/config/shared/server-profile/mfa-server-profile/entry[@name=\'{}\']&element=<mfa-config><entry name="okta-api-host"><value>{}</value></entry><entry name="okta-token"><value>{}</value></entry><entry name="okta-org"><value>{}</value></entry><entry name="okta-timeout"><value>30</value></entry><entry name="okta-baseuri"><value>/api/v1</value></entry></mfa-config><mfa-vendor-type>okta-adaptive-v1</mfa-vendor-type><mfa-cert-profile>OKTA-MFA-Service-Skillet</mfa-cert-profile>&key={}'.format(target_ip, mfa_profile_name, okta_endpoint, okta_token, okta_org, api_key)
r = requests.get(url, verify=False)
print(r.text)

url = 'https://{}/api/?type=config&action=set&xpath=/config/shared/authentication-profile/entry[@name=\'{}\']&element=<multi-factor-auth><factors><member>{}</member></factors><mfa-enable>yes</mfa-enable></multi-factor-auth><method><local-database/></method><allow-list><member>all</member></allow-list>&key={}'.format(target_ip, auth_profile, mfa_profile_name, api_key)
r = requests.get(url, verify=False)
print(r.text)



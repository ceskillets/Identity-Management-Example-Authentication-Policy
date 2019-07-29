import requests
import argparse
import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)


parser = argparse.ArgumentParser()
parser.add_argument("--TARGET_IP", help="IP address of the firewall", type=str)
parser.add_argument("--api_key", help="Firewall API Key", type=str)
parser.add_argument("--CERT_NAME", help="Certificate Name", type=str)
parser.add_argument("--CERT_HOSTNAME", help="Certificate Hostname", type=str)
parser.add_argument("--CERT_NBITS", help="Certificate Number of Bits", type=str)
parser.add_argument("--CERT_DIGEST", help="Certificate Digest", type=str)
args = parser.parse_args()

target_ip = args.TARGET_IP
api_key = args.api_key
cert_name = args.CERT_NAME
cert_nbits = args.CERT_NBITS
cert_hostname = args.CERT_HOSTNAME
cert_digest = args.CERT_DIGEST



url = 'https://{}/api/?type=op&cmd=<request><certificate><generate><certificate-name>{}</certificate-name><name>{}</name><algorithm><RSA><rsa-nbits>{}</rsa-nbits></RSA></algorithm><digest>{}</digest><ca>no</ca><hostname><member>{}</member></hostname><signed-by>external</signed-by></generate></certificate></request>&key={}'.format(target_ip, cert_name, cert_hostname, cert_nbits, cert_digest, cert_hostname, api_key)
csr = requests.get(url, verify=False)
print(csr.text)

url = 'https://{}/api/?type=export&format=pkcs10&category=certificate&include-key=no&certificate-name={}&key={}'.format(target_ip, cert_name, api_key)
r = requests.get(url, verify=False)

with open('../../working/' + cert_hostname + '.csr', 'w') as f:  
    f.write(r.text)





from os import environ, makedirs, getenv
import configparser

vpn_ip = getenv('WG_VPN_IP', '')
pri_key = getenv('WG_PRI_KEY', '')
pub_key = getenv('WG_PUB_KEY', '')
local_ip = getenv('WG_ALLOW_IP', '')
dns = getenv('WG_DNS', '')
endpoint = getenv('WG_END_POINT', '')

config = configparser.ConfigParser()
config.optionxform = str
config['Interface'] = {}
config['Interface']['Address'] = vpn_ip
config['Interface']['DNS'] = dns
config['Interface']['PrivateKey'] = pri_key
config['Peer'] = {}
config['Peer']['PublicKey'] = pub_key
config['Peer']['Endpoint'] = endpoint
config['Peer']['AllowedIPs'] = local_ip

makedirs('/etc/wireguard/', exist_ok=True)
config.write(open('/etc/wireguard/wg0.conf', 'w'))

 
#!/usr/bin/env python
# Sets TLS properties for auto registered hosts in Zabbix

import json
import requests
import sys

zabbix_api = "http://localhost/api_jsonrpc.php"
zabbix_identity = <insert var>
zabbix_pass = <insert var>
zabbix_psk = <insert var>
zabbix_user = <insert var>

# Connect to API
logon_json = {'jsonrpc': '2.0', 'method': 'user.login', 'params': {'user': zabbix_user, 'password': zabbix_pass}, 'id': 0}
logon_request = requests.post(zabbix_api, json=logon_json)
logon_response = logon_request.json()

# Get hostid
get_host_json = {'jsonrpc': '2.0', 'method': 'host.get', 'params': {'filter': {'host': [sys.argv[1]]}}, 'auth': logon_response['result'], 'id': 0}
get_host_request = requests.post(zabbix_api, json=get_host_json)
get_host_response = json.loads(get_host_request.text)
hostid = get_host_response['result'][0]['hostid']

# Set TLS settings for host
host_tls_json = {'jsonrpc': '2.0', 'method': 'host.update', 'params': {'hostid': hostid, 'tls_connect': '2', 'tls_accept': '2', 'tls_psk_identity': zabbix_identity, 'tls_psk': zabbix_psk}, 'auth': logon_response['result'], 'id': 0}
host_tls_request = requests.post(zabbix_api, json=host_tls_json)
host_tls_response = json.loads(host_tls_request.text)

# Disconnect from API
logoff_json = {'jsonrpc': '2.0', 'method': 'user.logout', 'params': {}, 'auth': logon_response['result'], 'id': 0}
logoff_request = requests.post(zabbix_api, json=logoff_json)
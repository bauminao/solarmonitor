#!/bin/env python3 

import os
import json

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".env"))

from datetime import datetime

import requests
requests.packages.urllib3.disable_warnings()

def get_sid():
  headers = {
      'Accept': 'application/json, text/plain, */*',
      'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
      'Connection': 'keep-alive',
      'Content-Type': 'application/json;charset=UTF-8',
      'Origin': str(os.getenv("PV_IP")),
      'Referer': str(os.getenv("PV_IP")),
      'Sec-Fetch-Dest': 'empty',
      'Sec-Fetch-Mode': 'cors',
      'Sec-Fetch-Site': 'same-origin',
      'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
      'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Linux"',
  }

  json_data = {
    'right': os.getenv("PV_USER"),
    'pass': os.getenv("PV_PASS"),
  }

  raw = requests.post('https://' + str(os.getenv("PV_IP")) + '/dyn/login.json', headers=headers, json=json_data, verify=False)
  _json = json.loads(str(raw.text))
  #print (json.dumps(_json,indent=2))
  sid = False
  print (_json)
  if "result" in _json.keys():
    if "sid" in _json["result"].keys():
      sid = _json["result"]["sid"]
      return sid
    else:
      return False
  else:
    return False

def write_sid():
  return True
  

print (get_sid())



#
#headers = {
#    'Accept': 'application/json, text/plain, */*',
#    'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
#    'Connection': 'keep-alive',
#    'Content-Type': 'application/json;charset=UTF-8',
#    'Origin': 'https://192.168.55.171',
#    'Referer': 'https://192.168.55.171/',
#    'Sec-Fetch-Dest': 'empty',
#    'Sec-Fetch-Mode': 'cors',
#    'Sec-Fetch-Site': 'same-origin',
#    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
#    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138"',
#    'sec-ch-ua-mobile': '?0',
#    'sec-ch-ua-platform': '"Linux"',
#}
#
#params = {
#    'sid': 'wJ5okhhIpf-IGhB5',
#}
#
#json_data = {
#    'destDev': [],
#    'keys': [
#        '6800_00823400',
#        '6180_104A9A00',
#        '6180_104AB700',
#        '6180_084ABC00',
#        '6180_084A9600',
#        '6180_084A9800',
#        '6100_004AB600',
#        '6800_088A4D00',
#        '6180_084A6400',
#    ],
#}
#
#response = requests.post('https://192.168.55.171/dyn/getValues.json', params=params, headers=headers, json=json_data, verify=False)


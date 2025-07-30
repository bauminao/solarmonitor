import os
import json

from datetime import datetime

import requests
#requests.packages.urllib3.disable_warnings()

class SMA:
  sid = False

  def __init__(self):
    self.sid = False

  def get_new_sid(self):
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

    raw = requests.post('https://' + str(os.getenv("PV_IP")) + '/dyn/login.json',
                        headers=headers,
                        json=json_data,
                        verify=False)
    _json = json.loads(str(raw.text))
    sid = False
    #print (_json)
    if "result" in _json.keys():
      if "sid" in _json["result"].keys():
        sid = _json["result"]["sid"]
        data={}
        data["sid"] = sid
        data["time"] = datetime.now()
        with open('sid.json', 'w',encoding='utf-8') as f:
          f.write(json.dumps(data, ensure_ascii=False, indent=2, default=str))
        self.sid=sid
        return sid
      else:
        return False
    else:
      return False


  def load_sid(self):
    with open('sid.json') as f:
      _json = json.load(f)
    if "sid" in _json.keys():
      self.sid = _json["sid"]
      return _json
    else:
      return False


  def check_sid(self, sid=None):
    if not sid:
      sid = self.sid

    if not sid: 
      print ("no valid sid available")
      return False

    headers   = {
        'sec-ch-ua-mobile': '?0',
        'Content-Type': 'application/json;charset=UTF-8',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138"',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        'Referer': "https://"+str(os.getenv("PV_IP"))+"/",
        'sec-ch-ua-platform': '"Linux"',
    }
    json_data = {}
    params    = { 'sid': sid, }

    raw = requests.post('https://' + str(os.getenv("PV_IP")) + '/dyn/sessionCheck.json',
                        headers=headers,
                        params=params,
                        json=json_data,
                        verify='cert.pem')
    _json = json.loads(str(raw.text))

    #print (json.dumps(_json, indent=2,default=str))
    return  sid

  def get_data__dump(self):
    return True
    

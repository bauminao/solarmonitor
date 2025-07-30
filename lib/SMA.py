import os
import json

from datetime import datetime

import requests
requests.packages.urllib3.disable_warnings()

class SMA:
  cert = os.path.join(os.path.dirname(os.path.realpath(__file__)),"..", "cert.pem")
  cert = False
  sidjson = os.path.join(os.path.dirname(os.path.realpath(__file__)),"..", "sid.json")
  sid = False

  #################################
  ## init()
  def __init__(self,sid=None):
    if sid:
      self.sid = sid
    else:
      self.sid = self.load_sid()

    if not self.sid:                  # Something on initial loading from file failed or a wrong sid was used for init.
      self.sid = self.get_new_sid()   # We try to get a new one
      self.sid = self.check_sid()     # And check it

    if not self.sid:                  # If it still fails we have to dig deeper. Sorry.
      return False
  ## /init()
  #################################


  #################################
  ## load_sid()
  def load_sid(self):
    """
    load_sid tries to load the last session saved in self.sidjson. 
    """

    with open(self.sidjson) as f:
      _json = json.load(f)
    if "sid" in _json.keys():
      self.sid = _json["sid"]
      return _json
    else:
      return False
  ## /load_sid()
  #################################


  #################################
  ## get_new_sid()
  def get_new_sid(self):
    """
    get_new_sid tries to login to the device and fetch a new session id (sid). 

    This is saved in self.sid and written to a json-file defined as self.sidjson

    :return: returns the sid from this login.
    """

    print ("Fetching new SID")
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
    if "result" in _json.keys():
      if "sid" in _json["result"].keys():
        sid = _json["result"]["sid"]
        data={}
        data["sid"] = sid
        data["time"] = datetime.now()
        with open(self.sidjson, 'w',encoding='utf-8') as f:
          f.write(json.dumps(data, ensure_ascii=False, indent=2, default=str))
        self.sid=sid
        return sid
      else:
        return False
    else:
      return False
  ## /get_new_sid()
  ################################


  #################################
  ## check_sid()
  def check_sid(self, sid=None):
    """
    check_sid checks if a given sid is valid to use on the device.
    In case the current sid is not working, a new one is tried to get from the device. --> beware: recursive!

    :param sid: optional. If not provided, self.sid is used instead.
    :return: On success the current sid is returned. Else "False"
    """

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
                        verify=self.cert)
    _json = json.loads(str(raw.text))

    if "cntDwnGg" in _json["result"]:
      print ("Still valid")
      print (json.dumps(_json,indent=2,default=str))
      return sid
    else:
      print ("Need new SID")
      print ("Old SID was: " + str(sid))
      print (json.dumps(_json,indent=2,default=str))
      self.sid=False
      sid = False
      self.get_new_sid()
      sid = self.check_sid()
      print ("Got new SID: " + str(sid))
      if sid:
        return sid
      else:
        return False
  ## /check_sid
  ################################


  #################################
  ## logout()
  def logout(self,sid=None):
    """
    logout does a logout from the device

    :param sid: optional, the sid of your session you want to logout from
    :return: on success returns the sid that was abandoned. If something goes wrong: False
    """
    if not sid:
      sid = self.sid                  # Get sid from current run
    if not sid:                       # Try to load from file instead
      sid = load_sid()

    if not sid: 
      print ("no valid sid available to logout. Already ogged out?")
      return False

    # TO DO 
    # Request: https://192.168.55.171/dyn/logout.json?sid=TBc8CtDUAicU5tzy
    # On Sucess do: Delete sidjson
    return sid
  ## /logout
  ################################




  #################################
  ## get_data__dump()
  def get_data__dump(self):
    """
    get_data__dump returns a bunch of data from the device. 
    """
    sid = self.check_sid()
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
    params = {
        'sid':  sid,
    }
    json_data = {
        'destDev': [],
        'keys': [
            '6100_40263F00' ,
        ],
    }
    # 6100_40263F00 --> Current Solar Power
    # 

    #   = requests.post('https://192.168.55.171/dyn/getValues.json', params=params, headers=headers, json=json_data, verify=False)
    raw = requests.post('https://' + str(os.getenv("PV_IP")) + '/dyn/getValues.json',
                        headers=headers,
                        params=params,
                        json=json_data,
                        verify=self.cert)
    _json = json.loads(str(raw.text))
    #print (json.dumps(_json, indent=2,default=str))
    return True
  ## /get_data__dump()
  #################################

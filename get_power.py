#!/bin/env python3 

import os

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".env"))

from lib import SMA

if __name__ == "__main__":
  Solar = SMA.SMA()

  print ("SID: " + str(Solar.sid))
  print (Solar.get_data__dump())



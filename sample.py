from HUBII.connect import HUBIIRec, EventListenerType
import logging
import time

logging.basicConfig(level=logging.DEBUG)

ws = HUBIIRec("ws://localhost:4000")
ws.connect()

def log(item):
    print(item)

ws.addEventListener(EventListenerType.ON_MESSAGE,log)

#while True:
#    time.sleep(1)
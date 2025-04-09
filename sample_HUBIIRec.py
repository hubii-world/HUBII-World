from HUBII.HUBIIRec import HUBIIRec, EventListenerType
from HUBII.models import HubiiRecSession
import logging
import time
import threading
import asyncio

logging.basicConfig(level=logging.DEBUG)

ws = HUBIIRec("ws://localhost:4000", periodicTimer=20000)
ws.connect()

def log(item:HubiiRecSession):
    print(item)
    

ws = HUBIIRec("ws://localhost:4000")
# Periodische Aufgabe registrieren
ws.addEventListener(EventListenerType.PERIODIC_TASK,log)

async def main():
    ws.connect()  # This is NOT an async function, so we call it normally
    try:
        while True:
            await asyncio.sleep(1)  # Prevents script from exiting
    except KeyboardInterrupt:
        print("Stopping WebSocket client...")
        ws.disconnect()

if __name__ == "__main__":
    asyncio.run(main()) 
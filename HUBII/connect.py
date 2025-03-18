import asyncio
import enum
import logging
import time
from typing import Callable, Dict, List
import websocket
import threading
from .websocket_model import HubiiRec
import pandas as pd


class HUBIIRec:
    def __init__(self, url:str,periodicTimer:int=1000):
        self.periodicTaskTimer = periodicTimer
        self.periodicTimerRunning = False
        self.url = url
        self.ws = None
        self.thread = None
        self.session:HubiiRecSession = HubiiRecSession(url=self.url)
        self.event_listeners: Dict[str, List[Callable]] = {
            "on_message": [],
            "on_error": [],
            "on_close": [],
            "on_open": [],
            "periodic_task": []
        }

    def connect(self):
        def run():
            try:
                self.ws.run_forever()
            except Exception as e:
                logging.error(f"WebSocket thread error: {e}")
        self.ws = websocket.WebSocketApp(
            self.url,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
        )
        self.ws.on_open = self._on_open
        self.thread = threading.Thread(target=run)
        self.thread.daemon = True
        self.thread.start()
        self.periodicTimerRunning = True
        self._periodic_task()

    def _periodic_task(self):
        def periodic_loop():
            while self.periodicTimerRunning:
                start_time = time.time()
                for h in self.event_listeners["periodic_task"]:
                    h(self.session)  
                time.sleep(max(0, (self.periodicTimer - (time.time() - start_time) * 1000)) / 1000)
        threading.Thread(target=periodic_loop, daemon=True).start()

    
    def disconnect(self):
        self.periodicTimerRunning = False
        if self.ws:
            self.ws.close()

    def _on_open(self,ws: websocket.WebSocketApp):
        self.periodicTimerRunning = True
        self._periodic_task()
        logging.info("WebSocket and Server are connected!")
        for h in self.event_listeners["on_open"]:
            h(ws)        

    def _on_close(self, ws: websocket.WebSocketApp, close_status_code, close_msg):        
        logging.info("WebSocket and Server are disconnected.")
        for h in self.event_listeners["on_close"]:
            h(ws)    

    def _on_message(self,ws: websocket.WebSocketApp, message: str):
        item = HubiiRec.model_validate_json(message)
        for h in self.event_listeners['on_message']:
            h(item)

    def _on_error(self, ws: websocket.WebSocketApp, error: Exception):
        logging.error(f"WebSocket Error: {error}")        
        for handler in self.event_listeners["on_error"]:
            handler(str(error))

    def addEventListener(self,event_type: EventListenerType, func:Callable):
        if event_type.value in self.event_listeners:
            if event_type == EventListenerType.on_message and type(func) == Callable[HubiiRec]:
                raise ValueError("Function missmatch")
            if event_type == EventListenerType.periodic_task and type(func) == Callable[HubiiRec]:
                raise ValueError("Function missmatch")
            self.event_listeners[event_type.value].append(func)
        else:
            raise ValueError(f"Invalid event type: {event_type}") 
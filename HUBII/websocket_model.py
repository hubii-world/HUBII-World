import enum
from pydantic import BaseModel
from datetime import datetime

class EventType(enum.Enum):
    MOUSEMOVEMENT = "MouseMovementValue"
    MOUSECLICK = "MouseClickValue"
    EYEMOVEMENT = "EyeMovementValue"
    HEARTRATE = "HeartRateValue"

class MouseMovementValue(BaseModel):
    Type: EventType = EventType.MOUSEMOVEMENT
    X: int
    Y: int


class MouseKeys(enum.Enum):
    LEFT = "left"
    RIGHT = "right"

class MouseClickValue(BaseModel):
    Type: EventType = EventType.MOUSECLICK
    Timestamp: int
    Key: MouseKeys
    X: int
    Y: int

class EyeMovementValue(BaseModel):
    Type: EventType = EventType.HEARTRATE
    Timestamp: int
    Left: EyeLocation
    Right: EyeLocation


class HeartRateValue(BaseModel):
    Type: EventType = EventType.HEARTRATE
    HeartRate: int
    RRInterval: float

class HubiiRec(BaseModel):
    SystemTime: datetime
    Value: MouseMovementValue | MouseClickValue | EyeMovementValue | HeartRateValue 

class HubiiRecSession(BaseModel):
    data: Dict[str, pd.DataFrame]
    startTime: datetime
    _url: str

    def __init__(self,url:str, data: Optional[Dict[str, pd.DataFrame]] = None):
        if data is None:
            data = {
                EventType.MOUSEMOVEMENT: pd.DataFrame(columns=["SystemTime", "X", "Y"]),
                EventType.MOUSECLICK: pd.DataFrame(columns=["SystemTime", "Key", "X", "Y"]),
                EventType.EYEMOVEMENT: pd.DataFrame(columns=["SystemTime", "LeftX", "LeftY", "RightX", "RightY"]),
                EventType.HEARTRATE: pd.DataFrame(columns=["SystemTime", "HeartRate", "RRInterval"]),
            }
        super().__init__(url=url,startTime=datetime.now(),data=data)

    @property
    def url(self) -> str:
        return self._url


class EventListenerType(enum.Enum):
    ON_MESSAGE = "on_message"
    ON_ERROR = "on_error"
    ON_CLOSE = "on_close"
    ON_OPEN = "on_open"
    PERIODIC_TASK = "periodic_task"

class EventListener(BaseModel):
    on_message: Callable
    on_error: Callable
    on_close: Callable
    on_open: Callable
    periodic_task: Callable
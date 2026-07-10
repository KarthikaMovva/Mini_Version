from dataclasses import dataclass

@dataclass
class Event:
    id:int  #1
    type:str  # "refund_requested"
    order:str #"ORDER_12345"
    time:str  # "10:30 AM"
    message:str=None # "My order is late"
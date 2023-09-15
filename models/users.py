from pydantic import BaseModel
from typing import List

'''class Systems(BaseModel):
    a: str = "device id" #device id
    b: str = "Iphone11" #device name
    c: str = "IP11" #device model'''

'''class Events(BaseModel):
    gi: str #game id
    m: str = "Game over"#tên event
    t: float = 8827#tgian tạo event
    s: int = 1#sequence,
    v: dict = {"key0": "value0", "key1": "value1"} #key, value'''
    
class Users(BaseModel):
    u: str #user id
    dt: int #1 android 2 ios
    gi: str #game id
    st: int #device time
    s: dict = {"a": "device id", "b": "iphone11pro", "c": "IP11"} #thông tin system gồm a, b, c
    pw: str #password
    m: str | None # message encode

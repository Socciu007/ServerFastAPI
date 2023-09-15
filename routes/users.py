from fastapi import APIRouter, HTTPException, Request, status
#from starlette.exceptions import HTTPException as StarletteException
#from fastapi.encoders import jsonable_encoder
#from bson import ObjectId
from base64 import b64encode, b64decode
from  Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import json
import hashlib

from mongodb.configDB import CollectionEvents, CollectionUsers 
from models.users import Users
from controllers.users import serializeDict, serializeList, checkSequense

route = APIRouter()

@route.post('/users')
async def push_user(users: Users):
    user = dict(users)

    #Check exists game-id
    if user["gi"] in [field["gi"] for field in CollectionUsers.find()]:
        raise HTTPException(status_code=404, detail="Data already exists")
        
    #Encode password and create key 
    user["pw"] = hashlib.md5(user["pw"].encode('utf-8')).hexdigest()
    combine = str(user["pw"]) + str(user["s"]["a"]) + str(user["s"]["b"]) + str(user["s"]["c"])
    key = hashlib.md5(combine.encode("utf-8")).digest() #16 byte
    #encryption messages
    try:
        messages = open("./messages.json", "r")
        data = json.dumps(messages.read()).encode('utf-8')

        cipher = AES.new(key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(data, AES.block_size))  

        iv = b64encode(cipher.iv).decode('utf-8')
        ct = b64encode(ct_bytes).decode('utf-8')
        result = json.dumps({'iv': iv, 'ciphertext': ct})
        user["m"] = ct
        print(result)
    except ValueError as e:
        raise e("Incorrect AES key length (%d bytes)" % len(key))
    #save data user into MongoDB
    CollectionUsers.insert_one(user)
        
    #decryption messages
    try: 
        b64 = json.loads(result)
        iv = b64decode(str(b64["iv"]))
        ct = b64decode(str(b64["ciphertext"]))
        cipher = AES.new(key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size).decode()
        messages = eval(json.loads(pt))
        print(messages)

        #save data events decoded
        new_messages = []
        #sort messages
        sorted_messages = sorted(messages, key=lambda x: x["s"])
        for event in sorted_messages:
            if not checkSequense(new_messages, event):
                break
        
        print("Array with incorrect sequence:", new_messages)
        CollectionEvents.insert_many(new_messages)
    except (ValueError, KeyError):
        print("Incorrect decryption message")
    return {"status": "success"}

@route.post('/users/events')
def create_events(gi: str):
    #Check game-id
    if gi not in [field["gi"] for field in CollectionUsers.find()]:
        raise HTTPException(status_code=404, detail="Data error: gameID is wrong")
    
    #key decoded
    user = CollectionUsers.find_one({"gi": gi})
    combine = str(user["pw"]) + str(user["s"]["a"]) + str(user["s"]["b"]) + str(user["s"]["c"])
    key = hashlib.md5(combine.encode("utf-8")).digest() #16 byte
    #decryption messages
    try: 
        iv = b64decode("AlEUnKemL78j/22UZXSuBQ==")
        ct = b64decode(user["m"])
        cipher = AES.new(key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size).decode()
        messages = json.loads(pt)
        print(eval(messages))
        print(type(eval(messages)))
        CollectionEvents.insert_many(eval(messages))
    except (ValueError, KeyError):
        print("Incorrect decryption message")
    return {"status": "success"}

@route.get('/users')
async def extract_users():
    user = serializeList(CollectionUsers.find())
    return user

@route.put('/users/{u}')
async def update_user(u: str, user: Users):
    CollectionUsers.find_one_and_update({"u": u},{
        "$set": dict(user)
    })
    return {"status": "success"}

@route.delete('/users/{u}')
async def delete_user(u):
    return serializeDict(CollectionUsers.find_one_and_delete({"u": u}))
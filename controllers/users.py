# Normal way
def userEntity(item) -> dict:
    return {
        "id":str(item["_id"]),
        "name":item["name"],
        "email":item["email"],
        "password":item["password"]
    }

def usersEntity(entity) -> list:
    return [userEntity(item) for item in entity]

#Best way
def serializeDict(a) -> dict:
    return {
        **{i:str(a[i]) for i in a if i=='_id'},
        **{i:a[i] for i in a if i!='_id'}
    }

def serializeList(entity) -> list:
    return [serializeDict(a) for a in entity]

#Check sequence of event (messages)
def checkSequense(messages, event):
    if not messages:
        messages.append(event)
        return True

    #get sequence of event in messages
    last_sequense = messages[-1]["s"]
    #check the current sequence
    if event["s"] == last_sequense + 1:   
        messages.append(event)
        return True
    else:
        return False



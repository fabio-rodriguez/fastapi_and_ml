import json
import numpy as np
import uuid


from fastapi import APIRouter

from .constants import ADMIN_KEY, ENCRYPTION_TYPE, ML_MODEL, USERS
from .jobs import *

router = APIRouter()

@router.get("/")
async def testing_child_resource():
    Xi = [[14.34, 1.68, 2.7, 25.0, 98.0, 2.8, 1.31, 0.53, 2.7, 13.0, 0.57, 1.96, 660.0]]

    prediction = np.array2string(ML_MODEL.predict(Xi))
    return {"message": f"Hi There! {prediction}"}


@router.post("/test_prediction")
async def testing_post(Xi: list):
    
    prediction = np.array2string(ML_MODEL.predict(Xi))
    return json.dumps(prediction)


@router.post("/eval")
async def eval_model(data: dict):
    
    try:
        url = data["url"]
        token = data["user_id"]
    except:
        return json.dumps({"status": "ERROR", "info": "Keys 'url' and 'user_id' muts be specified"})

    #TODO
    if not is_valid_token(token):
        return json.dumps({"status": "ERROR", "info": "Not valid user id"})

    Xi = None
    if url.endswith(".jpg"):
        pass
    
    elif url.endswith(".mp3"):
        pass

    elif url.endswith(".mp4"):
        pass

    if data == None:
        return json.dumps({"status": "ERROR", "info": "Bad url"})

    token = queue_prediction(Xi)
    return json.dumps({"status": "SUCCESS", "info": "Prediction in process", "id_token": token})


@router.post("/generate_token")
async def adding_users(data: dict):
    '''
        data = {'admin_encripted_key': ...}
    '''

    try:
        decrypted_message = ENCRYPTION_TYPE.decrypt(data['admin_encripted_key'])
    except:
        return json.dumps({"status": "ERROR", "info": "Wrong Admin Key"})

    if decrypted_message == ADMIN_KEY:
        
        new_token = create_token(USERS)
        encrypted_token = ENCRYPTION_TYPE.encrypt(new_token.bytes) 
        USERS[new_token.bytes] = 0  
        return json.dumps({"status": "SUCCESS", "info": "User correctly added", "encrypted_token": encrypted_token})

    else:
        return json.dumps({"status": "ERROR", "info": "Wrong Admin Key"})

        
@router.post("/add_points")
async def adding_user_points(data: dict):
    '''
        data = {'admin_encripted_key': ..., 'user_encrypted_token': ..., 'user_points', ...}
    '''

    try:
        decrypted_message = ENCRYPTION_TYPE.decrypt(data['admin_encripted_key'])
    except:
        return json.dumps({"status": "ERROR", "info": "Wrong Admin Key"})

    if decrypted_message == ADMIN_KEY:
        decrypted_token = ENCRYPTION_TYPE.decrypt(token = data['user_encrypted_token'])

        if not decrypted_token in USERS:
            return json.dumps({"status": "ERROR", "info": "User doesn't exist"})
        
        USERS[decrypted_token] += int(data['user_points'])  
        return json.dumps({"status": "SUCCESS", "info": "Points correctly added"})

    else:
        return json.dumps({"status": "ERROR", "info": "Wrong Admin Key"})

import json
import numpy as np

from fastapi import APIRouter, BackgroundTasks

from .constants import *
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
async def eval_model(data: dict, background_tasks: BackgroundTasks):
    
    try:
        url = data["data_url"]
        user_token = data["user_id"]
    except:
        return json.dumps({"status": "ERROR", "info": "Keys 'data_url' and 'user_id' muts be specified"})

    #TODO
    if not user_token in USERS:
        return json.dumps({"status": "ERROR", "info": "Not valid user id"})

    if USERS[user_token] == 0:
        return json.dumps({"status": "ERROR", "info": "Not enough points"})

    Xi = None
    if url.endswith(".jpg"):
        pass
    
    elif url.endswith(".mp3"):
        pass

    elif url.endswith(".mp4"):
        pass

    if data == None:
        return json.dumps({"status": "ERROR", "info": "Bad url"})

    # Register Job in Users joblist and decrease points in 1
    job_id, st = queue_job(user_token, Xi, JOBS_QUEUE, USER_JOBS[user_token])
    status = RUNNING_STATUS if st else WAITING_STATUS
    USER_JOBS[user_token][job_id] = status
    USERS[user_token] -= 1 
    if status == RUNNING_STATUS:
        # Execute background task
        background_tasks.add_task(run_ml_model)

    return json.dumps({"status": "SUCCESS", "info": "Prediction in process", "id_token": job_id})


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
        
        ## The user token is stored, then is encrypted and returned  
        new_token = create_token(USERS)
        encrypted_token = ENCRYPTION_TYPE.encrypt(new_token.bytes) 
        USERS[new_token.bytes] = 0  
        USER_JOBS[new_token.bytes] = {}
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


def run_ml_model():
    
    while not JOBS_QUEUE.empty(): 
        job_id, user_token, Xi = queue.get()
        result = ML_MODEL.predict(Xi)
        if user_token in JOBS_RESPONSE: 
            JOBS_RESPONSE[user_token][job_id] = result
        else:
            JOBS_RESPONSE[user_token] = {job_id: result}

        USER_JOBS[user_token][job_id] = DONE_STATUS
        

@router.post("/get_results")
async def get_results(data: dict):
    '''
        data = {'user_token': ..., job_id: ...}
    '''

    user_token = data['user_token']
    job_id = data['job_id']

    if not user_token in USERS:
        return json.dumps({"status": "ERROR", "info": "User doesn't exist"})
    
    if not job_id in USER_JOBS[user_token]:
        return json.dumps({"status": "ERROR", "info": f"Job doesn't exist for user_token {user_token}"})

    if USER_JOBS[user_token][job_id] != DONE_STATUS:
        return json.dumps({"status": "SUCCESS", "info": f"The job is in {USER_JOBS[user_token][job_id]} status. Please wait."})
    
    return json.dumps({"status": "SUCCESS", "info": f"Job Complete. Thank you!", "result": JOBS_RESPONSE[user_token][job_id]})



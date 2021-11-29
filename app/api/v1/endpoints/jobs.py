import uuid


def create_token(dictionary):
    token = uuid.uuid4()
    while(token in dictionary):
        token = uuid.uuid4()
    return token


def queue_job(user_token, Xi, queue, job_ids):
    
    job_id = create_token(job_ids)
    status = True if queue.empty() else False
    queue.put((job_id, user_token, Xi))
    return job_id, status 







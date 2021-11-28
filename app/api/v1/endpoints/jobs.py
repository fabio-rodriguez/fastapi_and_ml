import uuid

def create_token(dictionary):
    token = uuid.uuid4()
    while(token in dictionary):
        token = uuid.uuid4()
    return token


def is_valid_token():
    pass


def queue_prediction():
    pass
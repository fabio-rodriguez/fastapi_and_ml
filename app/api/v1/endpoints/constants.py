import pickle
import time
import uuid

from cryptography.fernet import Fernet

# Generate encryption key
ENCRYPTION_KEY = Fernet.generate_key()
ENCRYPTION_TYPE = Fernet(ENCRYPTION_KEY)
with open("static/ADMINKEY.txt", "wb") as f:
    f.write(ENCRYPTION_KEY)

# Admin Key
ADMIN_KEY = uuid.UUID('8185e6fb-2eba-4255-a91c-92a157a0539d')
ENCRYPTED_ADMIN_KEY = ENCRYPTION_TYPE.encrypt(ADMIN_KEY.bytes) 

# Model path
modelfile = f'static/final_prediction.pickle'

# Dummy data
Xi = [[14.34, 1.68, 2.7, 25.0, 98.0, 2.8, 1.31, 0.53, 2.7, 13.0, 0.57, 1.96, 660.0]]

## Load model
ML_MODEL = pickle.load(open(modelfile, 'rb'))
time.sleep(5)

## Run model with dummy data
ML_MODEL.predict(Xi)
time.sleep(5)

def restart_model():
    ''' Restarting model in case it's necessary '''

    ## Load model
    ML_MODEL = pickle.load(open(modelfile, 'rb'))
    time.sleep(5)

    ## Run model with dummy data
    ML_MODEL.predict(Xi)
    time.sleep(5)


USERS = {}

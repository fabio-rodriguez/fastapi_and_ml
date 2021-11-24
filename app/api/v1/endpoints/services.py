import json
import numpy as np
import pickle as p

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def testing_child_resource():
    return {"message": "Hi There! This is my route endpoint."}


@router.post("/predictions")
async def testing_child_resource(data: dict):
    
    path = "" if not "path" in data.keys() else data["path"] + "/"
    # Xi = [[14.34, 1.68, 2.7, 25.0, 98.0, 2.8, 1.31, 0.53, 2.7, 13.0, 0.57, 1.96, 660.0]]
    Xi = data["data"]

    modelfile = f'{path}static/final_prediction.pickle'
    model = p.load(open(modelfile, 'rb'))
    prediction = np.array2string(model.predict(Xi))
    return json.dumps(prediction)


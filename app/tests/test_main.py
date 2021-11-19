from fastapi.testclient import TestClient
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.v1.api import router as api_router

from main import app


# app = FastAPI()

# app.mount("/app/static", StaticFiles(directory="./app/static"), name="/app/static")

# app = FastAPI(title='Serverless Lambda FastAPI')

# app.include_router(api_router, prefix="/api/v1")


client = TestClient(app)


def test_main_resource():
    response_auth = client.get(f"/")
    assert response_auth.status_code == 200


def test_child_resource():
    response_auth = client.get(f"/api/v1/test")
    assert response_auth.status_code == 200


def test_predictions():

    response_auth = client.post(
        f"/api/v1/test/predictions", 
        json={
            "data": [[14.34, 1.68, 2.7, 25.0, 98.0, 2.8, 1.31, 0.53, 2.7, 13.0, 0.57, 1.96, 660.0]],
            "path": "app"
        }
    )
    
    assert response_auth.status_code == 200
    


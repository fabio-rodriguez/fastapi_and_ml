from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from mangum import Mangum

from api.v1.api import router as api_router


app = FastAPI()
app = FastAPI(title='Serverless Lambda FastAPI')
app.include_router(api_router, prefix="/api/v1")


@app.get("/",  tags=["Endpoint Test"])
def main_endpoint_test():
    return {"message": "Welcome CI/CD Pipeline with GitHub Actions!"}


if __name__ == "__main__":
 
    app.mount("/static", StaticFiles(directory="static"), name="static")
    
    # to make it work with Amazon Lambda, we create a handler object
    handler = Mangum(app=app)

    



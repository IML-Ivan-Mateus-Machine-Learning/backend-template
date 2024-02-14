import uvicorn
from fastapi import FastAPI
from sample.view import router as sample_router

app = FastAPI()

app.include_router(sample_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8181)

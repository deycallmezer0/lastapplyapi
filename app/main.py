from fastapi import FastAPI
from functions.helpers import extract_job_info

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}



if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8000
    import uvicorn
    uvicorn.run(app, host=host, port=port)

from fastapi import FastAPI
import os

app = FastAPI(title="cloud-api-cicd-terraform")

BUILD_SHA = os.getenv("BUILD_SHA", "dev")

@app.get("/healthz")
def healthz():
    return {"status": "ok", "build": BUILD_SHA}

@app.get("/echo")
def echo(msg: str = "hi"):
    return {"msg": msg}

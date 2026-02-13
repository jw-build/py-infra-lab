from fastapi import FastAPI
from pydantic import BaseModel
from .clients import make_async_client
from .service import InferService

app = FastAPI()

class InferIn(BaseModel):
    prompt: str

@app.on_event("startup")
async def on_startup():
    app.state.http = make_async_client()
    app.state.svc = InferService(app.state.http)

@app.on_event("shutdown")
async def on_shutdown():
    await app.state.http.aclose()

@app.get("/health")
async def health():
    return {"ok": True}

@app.post("/infer")
async def infer(req: InferIn):
    return await app.state.svc.infer(req.prompt)

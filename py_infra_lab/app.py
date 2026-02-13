from fastapi import FastAPI
from pydantic import BaseModel, Field
from py_infra_lab.logic import run_infer
import logging


app = FastAPI(title="py-infra-lab")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
log = logging.getLogger("py-infra-lab")

class InferRequest(BaseModel):
    text: str = Field(min_length=1, max_length=2000)

class InferResponse(BaseModel):
    answer: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/v1/infer", response_model=InferResponse)
def infer(req: InferRequest):
    log.info("infer called text_len=%d", len(req.text))
    return {"answer": run_infer(req.text)}

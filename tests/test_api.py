from fastapi.testclient import TestClient
from py_infra_lab.app import app


client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_infer():
    r = client.post("/v1/infer", json={"text": "hi"})
    assert r.status_code == 200
    body = r.json()
    assert "answer" in body
    assert body["answer"] == "echo: hi"

def test_infer_validation_error():
    r = client.post("/v1/infer", json={"text": ""})
    assert r.status_code == 422
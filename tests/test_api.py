from fastapi.testclient import TestClient
from py_infra_lab.app import app

def test_health():
    with TestClient(app) as client:
        r = client.get("/health")
        assert r.status_code == 200
        assert r.json() == {"ok": True}

def test_infer_validation_error_wrong_field():
    with TestClient(app) as client:
        r = client.post("/infer", json={"text": "hi"})  
        assert r.status_code == 422

def test_infer_ok_schema():
    with TestClient(app) as client:
        r = client.post("/infer", json={"prompt": "hi"})
        assert r.status_code == 200
        data = r.json()
        assert "ok" in data

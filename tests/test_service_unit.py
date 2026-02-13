import asyncio
import pytest

from py_infra_lab.service import InferService


class DummyResp:
    def __init__(self, status_code=200, payload=None, raise_exc=None):
        self.status_code = status_code
        self._payload = payload or {}
        self._raise_exc = raise_exc

    def raise_for_status(self):
        if self._raise_exc:
            raise self._raise_exc

    def json(self):
        return self._payload


class DummyClient:
    def __init__(self, behavior):
        # behavior: async function(prompt)->DummyResp
        self.behavior = behavior

    async def post(self, url, json):
        return await self.behavior(json["prompt"])


@pytest.mark.asyncio
async def test_infer_ok(monkeypatch):
    async def behavior(prompt):
        return DummyResp(payload={"text": prompt[::-1]})

    svc = InferService(DummyClient(behavior))
    out = await svc.infer("abc")

    assert out["ok"] is True
    assert out["result"]["text"] == "cba"
    assert out["latency_ms"] >= 0


@pytest.mark.asyncio
async def test_infer_downstream_error():
    class Boom(Exception): ...
    async def behavior(prompt):
        return DummyResp(raise_exc=Boom("fail"))

    svc = InferService(DummyClient(behavior))
    out = await svc.infer("abc")

    assert out["ok"] is False
    assert out["error"].startswith("downstream_error:")


@pytest.mark.asyncio
async def test_infer_timeout(monkeypatch):
    # 让 asyncio.timeout 很快超时：把 REQUEST_TIMEOUT_S 改小
    import py_infra_lab.service as service_mod
    monkeypatch.setattr(service_mod, "REQUEST_TIMEOUT_S", 0.01)

    async def behavior(prompt):
        await asyncio.sleep(0.2)
        return DummyResp(payload={"text": "x"})

    svc = InferService(DummyClient(behavior))
    out = await svc.infer("abc")

    assert out["ok"] is False
    assert out["error"] == "timeout"

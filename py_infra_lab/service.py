import asyncio
import time
import httpx
from .config import MAX_CONCURRENCY, DOWNSTREAM_URL, REQUEST_TIMEOUT_S

_sema = asyncio.Semaphore(MAX_CONCURRENCY)

class InferService:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def infer(self, prompt: str) -> dict:
        start = time.time()

        async with _sema: 
            try:
                # per-request timeout
                async with asyncio.timeout(REQUEST_TIMEOUT_S):
                    r = await self.client.post(DOWNSTREAM_URL, json={"prompt": prompt})
                    r.raise_for_status()
                    data = r.json()
            except TimeoutError:
                return {"ok": False, "error": "timeout"}
            except asyncio.CancelledError:
                raise
            except Exception as e:
                return {"ok": False, "error": f"downstream_error:{type(e).__name__}"}

        return {
            "ok": True,
            "latency_ms": int((time.time() - start) * 1000),
            "result": data,
        }

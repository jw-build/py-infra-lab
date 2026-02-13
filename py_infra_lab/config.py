import os

MAX_CONCURRENCY = int(os.getenv("MAX_CONCURRENCY", "16"))
DOWNSTREAM_URL = os.getenv("DOWNSTREAM_URL", "http://127.0.0.1:8081/mock_infer")
REQUEST_TIMEOUT_S = float(os.getenv("REQUEST_TIMEOUT_S", "10"))

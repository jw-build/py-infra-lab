# py-infra-lab
Edge Immutable OS + Kubernetes (or K3s/Lightweight )

API Request Full Path (Visual Architecture)

┌──────────────────────────────────────────────────────────────────────┐
│                              CLIENTS                                 │
│  Browser (Web)  |  Mobile App  |  CLI/curl  |  Other Services/Agents  │
└───────────────────────────────┬──────────────────────────────────────┘
                                │  HTTPS
                                ▼
┌──────────────────────────────────────────────────────────────────────┐
│                         DNS (Domain → IP)                            │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    EDGE / CDN / WAF / DDoS (Optional but common)      │
│  - cache/static accel   - bot/waf rules   - ddos protection           │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────┐
│                            API GATEWAY                               │
│  Single entrypoint for APIs                                           │
│  - Auth (API key/JWT/mTLS)                                            │
│  - Rate limit / quota                                                 │
│  - Routing (/v1/* → service)                                          │
│  - Request normalization + schema validation (common)                 │
│  - Observability hooks (request_id, tracing headers)                  │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────┐
│                       LOAD BALANCER (Often)                           │
│  - health checks   - distribute traffic to instances                  │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────┐
│                          API SERVICES (FastAPI etc.)                  │
│  (Business endpoints; thin HTTP layer)                                │
│  - Routers / middleware / validation                                  │
│  - Calls core engine / domain services                                │
└───────────────┬───────────────────────────┬──────────────────────────┘
                │                           │
                │                           │
                ▼                           ▼
┌───────────────────────────┐   ┌──────────────────────────────────────┐
│     CORE ENGINE / DOMAIN  │   │        ASYNC EXECUTION (Common)       │
│  - rules / policy         │   │  Queue / Jobs / Workers / CI/CD       │
│  - orchestration          │   │  - long tasks (deploy/scan/report)     │
│  - decision logic         │   │  - retries / backoff                   │
└───────────────┬───────────┘   └───────────────────┬──────────────────┘
                │                                   │
                ▼                                   ▼
┌──────────────────────────────────────────────────────────────────────┐
│                     DATA & INFRA DEPENDENCIES                         │
│  DB (Postgres/MySQL) | Cache (Redis) | MQ (Kafka/SQS/Rabbit) | S3/OSS │
│  + External APIs + Infra (K8s/Cloud) + Observability (logs/metrics)   │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────┐
│                            RESPONSE PATH                              │
│   Same way back: Service → LB → Gateway → Edge → TLS → Client          │
└──────────────────────────────────────────────────────────────────────┘

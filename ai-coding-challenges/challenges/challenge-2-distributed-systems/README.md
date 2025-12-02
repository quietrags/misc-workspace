# Challenge 2: Distributed Event Processing System

**"Build a Fault-Tolerant, Scalable Event Pipeline from Scratch"**

---

## 🎯 Challenge Overview

**Difficulty:** Very High
**Estimated Time:** 8-10 hours
**Recommended AI Modes:** Workspace (40%) + Chat (30%) + Agentic (30%)
**Tech Stack:** Go/Java/Rust (recommended), Kafka/RabbitMQ, PostgreSQL/Cassandra, Docker, Kubernetes

---

## 📖 Scenario

Your company processes financial transactions, IoT sensor data, and user activity events from a rapidly growing user base. Current system constraints:

- **Scale:** 10,000+ events/second during peak hours
- **Reliability:** 99.99% uptime SLA (43 minutes downtime/month)
- **Latency:** <100ms p99 processing latency
- **Durability:** Exactly-once processing semantics
- **Compliance:** Full audit trail for all events

Your mission: **Design and implement a production-grade distributed event processing pipeline.**

---

## 🏗️ System Requirements

### Functional Requirements

#### 1. Event Ingestion (20 points)
- Accept events via REST API and message queue
- Support multiple event types (transactions, sensor readings, user actions)
- Validate event schemas
- Return acknowledgment to clients
- Handle burst traffic (10x normal load)

#### 2. Event Processing (25 points)
- Route events to appropriate handlers based on type
- Implement exactly-once processing semantics
- Support event transformations and enrichment
- Handle poison pill messages (malformed events)
- Implement dead letter queue for failed events

#### 3. State Management (15 points)
- Maintain processing state (offsets, checkpoints)
- Support idempotency (deduplicate events)
- Track event lineage and causality
- Persist state durably across failures

#### 4. Fault Tolerance (20 points)
- Automatic retry with exponential backoff
- Circuit breaker for downstream dependencies
- Graceful degradation under partial failure
- Leader election for worker coordination
- Zero data loss on node failure

#### 5. Observability (15 points)
- Real-time metrics (throughput, latency, errors)
- Distributed tracing across components
- Structured logging with correlation IDs
- Alerting for anomalies (latency spikes, error rates)
- Dashboards for monitoring

#### 6. Deployment & Operations (5 points)
- Containerized with Docker
- Kubernetes deployment manifests
- Health checks and readiness probes
- Rolling updates without downtime
- Configuration management

---

## 🗂️ System Architecture

### Required Components

```
┌─────────────────────────────────────────────────────────┐
│                      Load Balancer                       │
│                     (Nginx/HAProxy)                      │
└────────────┬────────────────────────────┬───────────────┘
             │                            │
             ▼                            ▼
┌────────────────────────┐    ┌────────────────────────┐
│   API Gateway          │    │   Event Producer       │
│   (Ingestion Service)  │    │   (External Systems)   │
│   - Rate Limiting      │    │   - Batch Upload       │
│   - Auth/Validation    │    │   - Streaming Data     │
└────────┬───────────────┘    └────────┬───────────────┘
         │                              │
         │        ┌─────────────────────┘
         │        │
         ▼        ▼
    ┌────────────────────────────────────┐
    │      Message Broker (Kafka)        │
    │      - Event Topics by Type        │
    │      - Partitioning for Scale      │
    │      - Replication for Durability  │
    └───────┬──────────┬──────────┬──────┘
            │          │          │
            ▼          ▼          ▼
    ┌──────────┐ ┌──────────┐ ┌──────────┐
    │ Worker 1 │ │ Worker 2 │ │ Worker N │
    │ - Process│ │ - Process│ │ - Process│
    │ - Transform│ │ - Transform│ │ - Transform│
    │ - Store  │ │ - Store  │ │ - Store  │
    └────┬─────┘ └────┬─────┘ └────┬─────┘
         │            │            │
         ▼            ▼            ▼
    ┌────────────────────────────────────┐
    │     State Store (PostgreSQL)       │
    │     - Event Metadata               │
    │     - Processing Checkpoints       │
    │     - Deduplication Cache          │
    └────────────────────────────────────┘
              │
              ▼
    ┌────────────────────────────────────┐
    │     Monitoring & Observability     │
    │     - Prometheus (Metrics)         │
    │     - Jaeger (Tracing)             │
    │     - ELK Stack (Logs)             │
    └────────────────────────────────────┘
```

### Event Flow

1. **Ingestion:** Client sends event → API Gateway validates → Publishes to Kafka
2. **Processing:** Worker pulls from Kafka → Processes/transforms → Writes to store
3. **Acknowledgment:** Worker commits offset → Kafka acknowledges → Client notified
4. **Monitoring:** Metrics emitted at each step → Dashboard shows real-time health

---

## 🎯 Your Mission

### Part 1: Core System (60 points)

#### 1.1 API Gateway Service
```go
// Example event types
type TransactionEvent struct {
    ID          string    `json:"id"`
    Type        string    `json:"type"`
    Timestamp   time.Time `json:"timestamp"`
    UserID      string    `json:"user_id"`
    Amount      float64   `json:"amount"`
    Currency    string    `json:"currency"`
    Metadata    map[string]interface{} `json:"metadata"`
}

type SensorEvent struct {
    ID          string    `json:"id"`
    Type        string    `json:"type"`
    Timestamp   time.Time `json:"timestamp"`
    DeviceID    string    `json:"device_id"`
    Reading     float64   `json:"reading"`
    Unit        string    `json:"unit"`
    Location    GeoPoint  `json:"location"`
}
```

**Requirements:**
- REST endpoints: `POST /events` (single), `POST /events/batch` (bulk)
- Schema validation (JSON Schema or Protobuf)
- Rate limiting: 1000 req/min per API key
- Request deduplication (idempotency keys)
- Metrics: request rate, validation errors, publish latency

#### 1.2 Event Workers
**Requirements:**
- Consumer group for parallel processing
- Configurable processing handlers per event type
- Exactly-once semantics (transaction outbox or similar)
- Automatic retry: 3 attempts with exponential backoff
- Dead letter queue after max retries
- Metrics: processing throughput, error rate, lag

#### 1.3 State Store
**Requirements:**
- Event metadata storage (id, type, status, timestamps)
- Checkpoint storage (last processed offset per partition)
- Deduplication cache (recent event IDs, TTL 24h)
- Audit log (all state transitions)

### Part 2: Fault Tolerance (20 points)

#### 2.1 Chaos Engineering Tests

Implement tests for:
- **Network Partition:** Worker can't reach Kafka for 30s
- **Node Failure:** Worker crashes mid-processing
- **Database Downtime:** State store unavailable
- **Message Corruption:** Malformed events in queue
- **Thundering Herd:** 10x traffic spike in 1 second

**Expected Behavior:**
- Zero event loss
- Zero duplicate processing
- Automatic recovery without manual intervention
- Degraded mode if dependencies unavailable

#### 2.2 Circuit Breaker Pattern
```go
// Implement circuit breaker for downstream calls
circuitBreaker := NewCircuitBreaker(
    Threshold: 5,         // Open after 5 failures
    Timeout: 60 * time.Second,  // Try again after 60s
    OnOpen: func() {
        metrics.CircuitBreakerOpened.Inc()
        log.Warn("Circuit breaker opened")
    },
)
```

### Part 3: Observability (15 points)

#### 3.1 Metrics (Prometheus)
**Required Metrics:**
- `events_received_total` (counter, by type)
- `events_processed_total` (counter, by type, status)
- `processing_duration_seconds` (histogram)
- `queue_lag` (gauge)
- `worker_health` (gauge)
- `circuit_breaker_state` (gauge)

#### 3.2 Distributed Tracing (Jaeger/OpenTelemetry)
**Trace Spans:**
- API Gateway: `event-ingestion`
- Kafka Publish: `event-publish`
- Worker Processing: `event-processing`
- Database Write: `state-store`

**Include in traces:** Event ID, type, user ID, processing time

#### 3.3 Logging
**Structured logs (JSON):**
```json
{
  "timestamp": "2025-11-19T10:30:45Z",
  "level": "info",
  "service": "event-worker",
  "trace_id": "abc123",
  "event_id": "evt_456",
  "event_type": "transaction",
  "message": "Event processed successfully",
  "duration_ms": 45
}
```

### Part 4: Deployment (5 points)

#### 4.1 Docker
- Dockerfile for each service
- Multi-stage builds for smaller images
- Health check endpoints

#### 4.2 Kubernetes
**Required manifests:**
- Deployment (with resource limits)
- Service (ClusterIP for workers, LoadBalancer for API)
- ConfigMap (configuration)
- Secret (credentials)
- HorizontalPodAutoscaler (scale workers based on queue lag)

---

## 📊 Evaluation Rubric

### 1. Functional Correctness (25 points)

**Excellent (20-25):**
- All components working end-to-end
- Exactly-once semantics verified
- Dead letter queue functioning
- Chaos tests passing
- Zero data loss under failures

**Good (15-19):**
- Core functionality works
- Minor edge cases missed
- Mostly reliable under failures

**Adequate (10-14):**
- Basic event processing works
- Significant gaps in fault tolerance

**Poor (0-9):**
- Major functionality broken

### 2. Code Quality (25 points)

**Excellent (20-25):**
- Clean architecture (hexagonal/onion)
- SOLID principles applied
- Clear separation of concerns
- Well-structured error handling
- Production-ready code

**Good (15-19):**
- Good structure
- Some areas could be cleaner
- Minor code smells

**Adequate (10-14):**
- Functional but messy
- Poor error handling

**Poor (0-9):**
- Spaghetti code

### 3. AI Utilization (20 points)

**Excellent (16-20):**
- Used Workspace for architecture specification
- Used AI to generate Kubernetes manifests
- Generated comprehensive tests with AI
- Created observability boilerplate with AI
- Custom prompts for distributed patterns

**Good (12-15):**
- Good AI usage for scaffolding
- Some infrastructure as code generation

**Adequate (8-11):**
- Basic AI assistance

**Poor (0-7):**
- Minimal AI usage

### 4. Testing & Reliability (15 points)

**Excellent (12-15):**
- Unit tests for business logic
- Integration tests for event flow
- Chaos engineering tests passing
- Load tests (>10K events/sec)
- Contract tests for API

**Good (9-11):**
- Good test coverage
- Some integration tests
- Basic load testing

**Adequate (6-8):**
- Minimal tests

**Poor (0-5):**
- No tests

### 5. Documentation (15 points)

**Excellent (12-15):**
- Architecture Decision Records (ADRs)
- API documentation (OpenAPI)
- Deployment runbook
- Monitoring playbook
- Troubleshooting guide

**Good (9-11):**
- Good README
- Basic deployment docs

**Adequate (6-8):**
- Minimal docs

**Poor (0-5):**
- No docs

---

## 🚀 Getting Started

### Step 1: Architecture Planning (Workspace Mode)

**Prompt Example:**
```
"Design a distributed event processing system with these requirements:
- Handle 10,000 events/second
- Exactly-once processing
- Fault-tolerant (node failures, network partitions)
- Low latency (<100ms p99)

Provide:
1. High-level architecture diagram
2. Component breakdown
3. Technology choices (message broker, state store)
4. Data flow specification
5. Fault tolerance strategy"
```

### Step 2: Bootstrap Project (Agentic Mode)

**Prompt Example:**
```
"Create a Go project structure for the event processing system:
- API Gateway service (REST endpoints)
- Worker service (Kafka consumer)
- Shared libraries (event schemas, metrics)
- Docker Compose for local dev
- Include Makefile with common commands"
```

### Step 3: Implement Components (Agentic + Chat)

**For API Gateway:**
```
"Implement a Go HTTP server with:
1. POST /events endpoint with schema validation
2. Rate limiting using golang.org/x/time/rate
3. Kafka producer integration
4. Prometheus metrics
5. Graceful shutdown
6. Comprehensive error handling"
```

**For Worker:**
```
"Implement a Kafka consumer in Go with:
1. Consumer group for parallel processing
2. Exactly-once semantics using transactions
3. Retry logic with exponential backoff
4. Dead letter queue for failed events
5. OpenTelemetry tracing
6. Graceful shutdown on SIGTERM"
```

### Step 4: Add Observability (Chat + Agentic)

**Prompt Example:**
```
"Add observability to the event processing system:
1. Prometheus metrics for all components
2. Jaeger distributed tracing
3. Structured logging with zerolog
4. Create Grafana dashboard JSON
5. Add alerting rules for high error rates"
```

### Step 5: Chaos Testing (Chat + Agentic)

**Prompt Example:**
```
"Create chaos engineering tests using Go:
1. Test network partition (worker can't reach Kafka)
2. Test worker crash mid-processing
3. Test database failure
4. Verify zero data loss
5. Verify exactly-once semantics
Use testcontainers-go for infrastructure"
```

---

## 💡 AI Mode Strategy

### Workspace Mode (40%)

**Use for:**
- ✅ Initial architecture design
- ✅ Component specifications
- ✅ Data flow diagrams
- ✅ Technology selection trade-offs
- ✅ API contract design

**Example Prompts:**
- "Compare Kafka vs RabbitMQ for this use case"
- "Design exactly-once semantics strategy"
- "Specify Kubernetes deployment strategy"

### Chat Mode (30%)

**Use for:**
- ✅ Quick API lookups (Kafka client usage)
- ✅ Debugging errors
- ✅ Best practices queries
- ✅ Configuration syntax

**Example Prompts:**
- "How to configure Kafka consumer groups in Go?"
- "What's the best circuit breaker library for Go?"
- "Explain Prometheus histogram vs summary"

### Agentic Mode (30%)

**Use for:**
- ✅ Generating Kubernetes manifests
- ✅ Creating Docker Compose files
- ✅ Writing test suites
- ✅ Implementing observability boilerplate

**Example Prompts:**
- "Generate K8s manifests for 3 services"
- "Create comprehensive integration tests"
- "Add Prometheus metrics to all handlers"

---

## 📚 Resources

### Message Brokers
- **Kafka:** High-throughput, durable, partitioned
- **RabbitMQ:** Flexible routing, simpler ops
- **NATS JetStream:** Cloud-native, lightweight

### State Stores
- **PostgreSQL:** ACID, familiarity
- **Cassandra:** High write throughput, distributed
- **Redis:** Low latency, limited durability

### Languages
- **Go:** Great concurrency, fast, statically typed
- **Java:** Mature ecosystem, strong Kafka integration
- **Rust:** Performance, safety, steep learning curve

### Frameworks
- **Go:** chi/gin (HTTP), sarama (Kafka), gorm (ORM)
- **Java:** Spring Boot, Kafka Streams, Micronaut
- **Rust:** tokio, rdkafka, actix-web

### Testing
- **Testcontainers:** Infrastructure for tests
- **Toxiproxy:** Network chaos testing
- **Locust/k6:** Load testing

---

## ⏱️ Time Allocation

| Phase | Time | AI Mode |
|-------|------|---------|
| **Architecture Planning** | 1.5h | Workspace |
| **Project Bootstrap** | 0.5h | Agentic |
| **API Gateway** | 2h | Agentic + Chat |
| **Event Workers** | 2.5h | Agentic + Chat |
| **State Store** | 1h | Agentic |
| **Observability** | 1.5h | Agentic |
| **Chaos Tests** | 1.5h | Chat + Agentic |
| **Deployment** | 1h | Agentic |
| **Documentation** | 0.5h | Agentic |

**Total: 12 hours** (with buffer)

---

## 🏆 Bonus Points (15 extra points)

- **Event Sourcing (+5):** Full event store with replay
- **CQRS Pattern (+3):** Separate read/write models
- **Kubernetes Operator (+5):** Custom resource for auto-scaling
- **Multi-Region (+5):** Active-active across regions
- **Schema Registry (+2):** Avro/Protobuf with versioning

---

## 🎓 Learning Objectives

1. **Distributed Systems Design** with AI planning
2. **Fault Tolerance Patterns** implementation
3. **Observability** as first-class concern
4. **Infrastructure as Code** generation with AI
5. **Production-Ready** coding standards

---

## 📝 Submission Requirements

1. **Code:** GitHub repo with all services
2. **Documentation:** Architecture, deployment, monitoring
3. **Demo:** Video showing chaos tests passing
4. **AI Log:** Document effective prompts and strategies

---

**Challenge Created:** 2025-11-19
**Difficulty Level:** Very High
**Recommended Experience:** 5+ years, distributed systems knowledge
**AI Advantage Score:** 91/100

---

*Build systems that don't break. Use AI to get there faster.*

# Challenge 1: Legacy System Modernization

**"From Monolith to Microservices: Untangling a Legacy E-Commerce Platform"**

---

## 🎯 Challenge Overview

**Difficulty:** High
**Estimated Time:** 6-8 hours
**Recommended AI Modes:** Agentic (60%) + Workspace (30%) + Chat (10%)
**Tech Stack:** Python/Django, PostgreSQL, Redis, Docker

---

## 📖 Scenario

You've just joined an e-commerce startup that built their MVP 3 years ago. The monolith served them well initially, but now:

- **Performance Issues:** API response times average 2-3 seconds
- **Deployment Pain:** 45-minute deployments, frequent rollbacks
- **Team Scaling:** 3 teams stepping on each other's toes
- **Technical Debt:** No tests, tight coupling, database bottlenecks

The CTO wants to modernize the system without a full rewrite. Your mission: **Extract key domains into microservices while maintaining backward compatibility.**

---

## 🗂️ The Legacy Codebase

### Current Architecture

```
ecommerce-monolith/
├── manage.py
├── requirements.txt
├── ecommerce/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── products/              # Product catalog (3K LOC)
│   ├── models.py          # Product, Category, Inventory
│   ├── views.py           # Business logic in views
│   ├── admin.py
│   └── urls.py
├── orders/                # Order processing (4K LOC)
│   ├── models.py          # Order, OrderItem, Payment
│   ├── views.py           # Checkout logic
│   ├── tasks.py           # Celery tasks (poorly structured)
│   └── urls.py
├── users/                 # User management (3K LOC)
│   ├── models.py          # User, Address, Preferences
│   ├── views.py           # Auth + profile logic
│   ├── auth.py            # Custom auth backend
│   └── urls.py
├── reviews/               # Product reviews (2K LOC)
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── recommendations/       # ML recommendations (3K LOC)
│   ├── engine.py          # Recommendation algorithm
│   ├── views.py
│   └── urls.py
└── shared/
    ├── utils.py           # 500+ line God object
    ├── middleware.py
    └── decorators.py
```

### Key Problems

**1. Tight Coupling**
```python
# orders/views.py - Everything coupled
def checkout(request):
    user = User.objects.get(id=request.user.id)
    cart = Cart.objects.get(user=user)

    # Direct DB queries across domains
    products = Product.objects.filter(id__in=cart.items)
    inventory = Inventory.objects.filter(product__in=products)

    # Business logic in views
    if inventory.quantity < cart.quantity:
        return JsonResponse({'error': 'Out of stock'})

    # Payment processing inline
    payment = stripe.charge(...)

    # Order creation with complex logic
    order = Order.create_with_items(...)

    # Email sending
    send_order_confirmation(user.email, order)

    # Update inventory directly
    inventory.quantity -= cart.quantity
    inventory.save()
```

**2. N+1 Query Problems**
```python
# products/views.py
def product_list(request):
    products = Product.objects.all()  # Query 1

    data = []
    for product in products:
        data.append({
            'name': product.name,
            'category': product.category.name,  # N queries
            'inventory': product.inventory.quantity,  # N queries
            'avg_rating': product.reviews.aggregate(Avg('rating'))  # N queries
        })
```

**3. No Tests**
- Zero unit tests
- No integration tests
- Manual QA only
- Frequent production bugs

**4. Shared Database**
- All domains share single PostgreSQL instance
- Foreign keys everywhere
- No clear boundaries

**5. No API Documentation**
- Endpoints undocumented
- Inconsistent response formats
- No versioning

---

## 🎯 Your Mission

### Required Deliverables

#### 1. Extract Three Microservices (50 points)

**Service 1: Product Catalog Service**
- Extract `products/` and `reviews/` apps
- Expose RESTful API for product operations
- Implement caching layer (Redis)
- Add search functionality (Elasticsearch optional)

**Service 2: Order Processing Service**
- Extract `orders/` app
- Implement saga pattern for distributed transactions
- Add payment gateway integration
- Implement event-driven order status updates

**Service 3: User Service**
- Extract `users/` app
- Implement JWT-based authentication
- Create user profile management API
- Add OAuth2 support (Google/GitHub)

#### 2. API Gateway (15 points)

- Implement using Kong, Nginx, or AWS API Gateway
- Add rate limiting (100 req/min per user)
- Implement request/response logging
- Add authentication middleware

#### 3. Comprehensive Testing (15 points)

**Target:** 80%+ test coverage

- Unit tests for business logic
- Integration tests for APIs
- Contract tests between services
- Load tests (100 req/s target)

#### 4. API Documentation (10 points)

- OpenAPI 3.0 specifications for all services
- Swagger UI for interactive docs
- Example requests/responses
- Error code documentation

#### 5. Migration Strategy (10 points)

- Strangler fig pattern implementation
- Backward compatibility layer
- Database migration scripts
- Rollback procedures

---

## 🔧 Technical Requirements

### Service Communication

**Option 1: REST APIs**
- Use Django REST Framework or FastAPI
- Implement circuit breakers (resilience4py)
- Add retry logic with exponential backoff

**Option 2: Event-Driven (Bonus)**
- Use RabbitMQ or Kafka
- Implement event sourcing for orders
- Add CQRS pattern

### Data Management

**Phase 1: Shared Database (Week 1)**
- Services share DB initially
- Use database views for isolation

**Phase 2: Database Per Service (Week 2)**
- Extract data into separate databases
- Implement data replication where needed
- Handle eventual consistency

### Observability

- **Logging:** Structured JSON logs (ELK stack compatible)
- **Metrics:** Prometheus metrics endpoints
- **Tracing:** OpenTelemetry for distributed tracing
- **Health Checks:** `/health` and `/ready` endpoints

### Containerization

- Dockerfile for each service
- Docker Compose for local development
- Kubernetes manifests (optional bonus)

---

## 📊 Evaluation Rubric

### 1. Functional Correctness (25 points)

**Excellent (20-25):**
- All three services working independently
- API gateway routing correctly
- Backward compatibility maintained
- No data loss during migration

**Good (15-19):**
- Services mostly working
- Minor edge cases missed
- Some backward compatibility issues

**Adequate (10-14):**
- Basic functionality works
- Significant gaps in implementation

**Poor (0-9):**
- Major functionality broken

### 2. Code Quality (25 points)

**Excellent (20-25):**
- Clear service boundaries (low coupling, high cohesion)
- SOLID principles applied
- Clean architecture (domain/application/infrastructure layers)
- No code duplication
- Consistent coding style

**Good (15-19):**
- Decent boundaries
- Some code smells
- Minor duplication

**Adequate (10-14):**
- Services separated but still coupled
- Significant code smells

**Poor (0-9):**
- Poor separation
- High coupling

### 3. AI Utilization (20 points)

**Excellent (16-20):**
- Used AI Workspace for architecture planning
- Used Agentic mode for multi-file refactoring
- Generated comprehensive tests with AI
- Created API docs with AI assistance
- Custom prompts for domain-specific patterns

**Good (12-15):**
- Good use of AI for scaffolding
- Some test generation
- Basic documentation assistance

**Adequate (8-11):**
- Basic AI usage
- Mostly manual work

**Poor (0-7):**
- Minimal AI usage

### 4. Testing & Reliability (15 points)

**Excellent (12-15):**
- >80% test coverage
- Unit + integration + contract tests
- Load testing implemented
- Circuit breakers and retries

**Good (9-11):**
- >60% coverage
- Good unit tests
- Some integration tests

**Adequate (6-8):**
- Basic tests present
- <60% coverage

**Poor (0-5):**
- Minimal tests

### 5. Documentation (15 points)

**Excellent (12-15):**
- OpenAPI specs for all services
- Architecture decision records (ADRs)
- Migration runbook
- Deployment guide
- Swagger UI setup

**Good (9-11):**
- Good API documentation
- Basic deployment docs

**Adequate (6-8):**
- Minimal documentation

**Poor (0-5):**
- No documentation

---

## 🚀 Getting Started

### Step 1: Clone Starter Code

```bash
git clone [starter-repo-url]
cd challenge-1-legacy-modernization
```

### Step 2: Run Legacy Monolith

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Load sample data
python manage.py loaddata sample_data.json

# Start server
python manage.py runserver
```

### Step 3: Explore the Codebase (AI-Assisted)

**Prompt Example (Chat Mode):**
```
"Analyze the ecommerce codebase and identify:
1. Domain boundaries for microservices extraction
2. Cross-cutting concerns that need shared libraries
3. Database dependencies between domains
4. High-coupling areas that need refactoring"
```

### Step 4: Plan Architecture (Workspace Mode)

**Prompt Example (Workspace Mode):**
```
"Create a specification for extracting the Product Catalog
into a microservice:
- Define API endpoints
- Specify data models
- Plan database migration strategy
- Design caching layer
- List testing requirements"
```

### Step 5: Execute Refactoring (Agentic Mode)

**Prompt Example (Agentic Mode):**
```
"Extract the products/ app into a standalone FastAPI service:
1. Create new FastAPI project structure
2. Move models to new service
3. Create RESTful endpoints
4. Add Redis caching
5. Generate unit tests with >80% coverage
6. Create OpenAPI documentation"
```

---

## 💡 AI Mode Strategy Guide

### When to Use Chat Mode

✅ **Quick Queries:**
- "What's the Django REST Framework syntax for nested serializers?"
- "How do I implement circuit breakers in Python?"
- "Explain the Strangler Fig pattern"

✅ **Debugging:**
- "Why is this test failing?" (paste error)
- "How can I optimize this database query?"

❌ **Avoid:**
- Large refactoring tasks (use Agentic instead)

### When to Use Agentic Mode

✅ **Multi-File Refactoring:**
- Extract entire app into microservice
- Generate test suites across multiple files
- Update import statements across codebase

✅ **Pattern Application:**
- Apply repository pattern to all models
- Add error handling consistently
- Generate API docs for all endpoints

❌ **Avoid:**
- High-level planning (use Workspace instead)

### When to Use Workspace Mode

✅ **Architecture Planning:**
- Design service boundaries
- Create specifications
- Plan migration strategies

✅ **Multi-Service Coordination:**
- Design API contracts between services
- Plan event schemas
- Design database schemas

❌ **Avoid:**
- Implementation details (use Agentic instead)

---

## 📚 Resources

### Microservices Patterns
- Saga Pattern for distributed transactions
- API Gateway pattern
- Service discovery
- Circuit breaker pattern
- Strangler Fig pattern

### Python Frameworks
- FastAPI: Modern, fast API framework
- Django REST Framework: Full-featured REST
- Celery: Async task processing
- SQLAlchemy: ORM for microservices

### Infrastructure
- Docker: Containerization
- Nginx: API Gateway
- Redis: Caching
- RabbitMQ: Message broker (optional)

### Testing Tools
- pytest: Test framework
- pytest-cov: Coverage
- locust: Load testing
- pact: Contract testing

---

## ⏱️ Time Allocation Suggestion

| Phase | Time | AI Mode Focus |
|-------|------|---------------|
| **Planning** | 1 hour | Workspace |
| **Service 1: Products** | 2 hours | Agentic + Chat |
| **Service 2: Orders** | 2 hours | Agentic + Chat |
| **Service 3: Users** | 1.5 hours | Agentic + Chat |
| **API Gateway** | 1 hour | Chat + Agentic |
| **Testing** | 1.5 hours | Agentic |
| **Documentation** | 1 hour | Agentic |

**Total: 10 hours** (includes buffer)

---

## 🎓 Learning Objectives

By completing this challenge, you'll learn to:

1. **Identify service boundaries** in legacy monoliths using AI pattern recognition
2. **Apply microservices patterns** with AI-assisted implementation
3. **Maintain backward compatibility** during incremental migration
4. **Generate comprehensive tests** using AI
5. **Create API documentation** automatically
6. **Use different AI modes strategically** for different task types

---

## 📝 Submission Requirements

### Code Submission

1. **GitHub Repository:**
   - Separate folder for each service
   - Docker Compose for local setup
   - README with setup instructions

2. **Documentation:**
   - `ARCHITECTURE.md`: Service boundaries, design decisions
   - `MIGRATION-GUIDE.md`: Step-by-step migration process
   - `API-DOCS.md`: Link to Swagger UI or OpenAPI specs

3. **AI Usage Log:**
   - Document key AI interactions
   - Note which modes you used for what tasks
   - Share effective prompt patterns

### Demo Video (Optional)

- 5-minute walkthrough
- Show services running independently
- Demonstrate API gateway routing
- Run test suite
- Show API documentation

---

## 🏆 Bonus Points (10 extra points)

- **Event-Driven Architecture (+5):** Implement with RabbitMQ/Kafka
- **Kubernetes Deployment (+3):** Working K8s manifests
- **CI/CD Pipeline (+2):** GitHub Actions or GitLab CI
- **Monitoring Dashboard (+2):** Grafana + Prometheus
- **Database Per Service (+3):** Complete data isolation

---

## ❓ FAQs

**Q: Can I use a different language/framework?**
A: Yes, but starter code is Python/Django. Using Go/Java/Rust is allowed but you'll need to rewrite the monolith first.

**Q: Do I need to implement all bonuses?**
A: No, bonuses are optional. Focus on core requirements first.

**Q: How much of the monolith code should I reuse?**
A: Business logic can be reused/refactored. Aim for <30% code duplication.

**Q: Can I use AI to write all the code?**
A: Yes! That's the point. But you must understand and be able to explain it.

**Q: What if I can't finish in 6-8 hours?**
A: Focus on quality over quantity. Complete 2-3 services well rather than all services poorly.

---

**Challenge Created:** 2025-11-19
**Difficulty Level:** High
**Recommended Experience:** 3+ years with Python/web development
**AI Advantage Score:** 91/100

---

*Good luck! Push those AI tools to their limits!*

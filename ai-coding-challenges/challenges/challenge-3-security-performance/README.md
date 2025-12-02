# Challenge 3: Security Hardening & Performance Optimization

**"From MVP to Production-Ready in 24 Hours"**

---

## 🎯 Challenge Overview

**Difficulty:** High
**Estimated Time:** 6-8 hours
**Recommended AI Modes:** Agentic (50%) + Chat (35%) + Workspace (15%)
**Tech Stack:** Node.js/Express, React, PostgreSQL, Redis, Docker

---

## 📖 Scenario

A startup's viral social media app just got featured on TechCrunch. Traffic went from 100 → 10,000 concurrent users overnight. But there are critical problems:

**Security Issues:**
- 🔴 SQL injection vulnerabilities
- 🔴 No authentication system
- 🔴 Exposed API keys in frontend code
- 🔴 Missing CSRF protection
- 🔴 No rate limiting (DDoS risk)
- 🔴 Weak password policies
- 🔴 No security headers

**Performance Issues:**
- 🔴 5+ second page load times
- 🔴 N+1 database queries everywhere
- 🔴 No caching
- 🔴 Unoptimized images (5MB each)
- 🔴 Memory leaks in production
- 🔴 Synchronous blocking operations

**Operations Issues:**
- 🔴 No monitoring/logging
- 🔴 No error tracking
- 🔴 Hardcoded configuration
- 🔴 No CI/CD pipeline

Your mission: **Make this application production-ready within 8 hours.**

---

## 🗂️ The Vulnerable Application

### Current Architecture

```
social-app/
├── frontend/                  # React app
│   ├── src/
│   │   ├── components/
│   │   │   ├── Feed.jsx       # No authentication check
│   │   │   ├── Profile.jsx    # XSS vulnerable
│   │   │   └── Upload.jsx     # No file validation
│   │   ├── api/
│   │   │   └── client.js      # API keys hardcoded
│   │   └── App.jsx
│   └── public/
│       └── images/            # Unoptimized 5MB images
├── backend/                   # Node.js/Express
│   ├── server.js              # No security middleware
│   ├── routes/
│   │   ├── auth.js            # Weak password validation
│   │   ├── posts.js           # SQL injection vulnerable
│   │   └── users.js           # No authorization checks
│   ├── models/
│   │   └── db.js              # Raw SQL queries
│   └── config.js              # Secrets in plaintext
└── database/
    └── schema.sql             # No indexes
```

### Security Vulnerabilities (OWASP Top 10)

#### 1. SQL Injection (Critical)
```javascript
// backend/routes/posts.js - VULNERABLE
app.get('/api/posts/search', (req, res) => {
    const { query } = req.query;

    // SQL injection vulnerable
    db.query(
        `SELECT * FROM posts WHERE title LIKE '%${query}%'`,
        (err, results) => {
            res.json(results);
        }
    );
});
```

#### 2. Broken Authentication
```javascript
// backend/routes/auth.js - VULNERABLE
app.post('/api/login', (req, res) => {
    const { username, password } = req.body;

    // No password hashing
    db.query(
        'SELECT * FROM users WHERE username = ? AND password = ?',
        [username, password],
        (err, users) => {
            if (users.length > 0) {
                // No session management
                res.json({ success: true, user: users[0] });
            }
        }
    );
});
```

#### 3. Sensitive Data Exposure
```javascript
// frontend/src/api/client.js - EXPOSED SECRETS
const API_KEY = 'sk_live_51MxPzH...'; // Hardcoded in frontend
const AWS_SECRET = 'wJalrXUtnFEMI/K7MDENG...';

export const uploadImage = (file) => {
    return fetch(`https://api.service.com/upload`, {
        headers: { 'X-API-Key': API_KEY }
    });
};
```

#### 4. XSS Vulnerabilities
```javascript
// frontend/src/components/Profile.jsx - XSS VULNERABLE
function ProfileBio({ bio }) {
    // Directly rendering user input
    return <div dangerouslySetInnerHTML={{ __html: bio }} />;
}
```

#### 5. Insecure Deserialization
```javascript
// backend/routes/users.js - UNSAFE
app.post('/api/preferences', (req, res) => {
    const prefs = eval(req.body.preferences); // NEVER DO THIS
    // ...
});
```

### Performance Issues

#### 1. N+1 Queries
```javascript
// backend/routes/posts.js
app.get('/api/feed', async (req, res) => {
    const posts = await db.query('SELECT * FROM posts LIMIT 50');

    // N+1 problem: 50 additional queries
    for (let post of posts) {
        post.author = await db.query('SELECT * FROM users WHERE id = ?', [post.user_id]);
        post.likes = await db.query('SELECT COUNT(*) FROM likes WHERE post_id = ?', [post.id]);
        post.comments = await db.query('SELECT * FROM comments WHERE post_id = ?', [post.id]);
    }

    res.json(posts);
});
```

#### 2. Memory Leaks
```javascript
// backend/server.js
const cache = {}; // Unbounded cache - memory leak

app.get('/api/data/:id', (req, res) => {
    // Cache grows forever
    cache[req.params.id] = fetchLargeData(req.params.id);
    res.json(cache[req.params.id]);
});
```

#### 3. Unoptimized Assets
```
frontend/public/images/
├── hero.jpg      (5.2 MB - not compressed)
├── avatar1.png   (2.8 MB - could be 50KB)
├── banner.jpg    (4.1 MB - no lazy loading)
```

#### 4. No Caching
- No browser caching headers
- No CDN
- No Redis caching for API responses
- Database queries repeated on every request

---

## 🎯 Your Mission

### Part 1: Security Hardening (40 points)

#### 1.1 Fix All Critical Vulnerabilities (25 points)

**Required Fixes:**

✅ **SQL Injection:**
- Replace raw queries with parameterized queries
- Use an ORM (Sequelize, TypeORM, Prisma)
- Add input validation (Joi, Yup)

✅ **Authentication & Authorization:**
- Implement JWT-based authentication
- Add bcrypt password hashing
- Implement role-based access control (RBAC)
- Add refresh token mechanism

✅ **XSS Protection:**
- Sanitize all user inputs (DOMPurify)
- Use Content Security Policy headers
- Escape HTML in templates

✅ **CSRF Protection:**
- Add CSRF tokens
- Use SameSite cookie flags
- Implement double-submit cookies

✅ **Sensitive Data:**
- Move secrets to environment variables
- Use .env files (never committed)
- Implement secret management (HashiCorp Vault or AWS Secrets Manager)

#### 1.2 Security Best Practices (15 points)

**Required:**

✅ **Security Headers:**
```javascript
helmet({
    contentSecurityPolicy: {
        directives: {
            defaultSrc: ["'self'"],
            styleSrc: ["'self'", "'unsafe-inline'"],
            scriptSrc: ["'self'"],
            imgSrc: ["'self'", "data:", "https:"],
        },
    },
    hsts: {
        maxAge: 31536000,
        includeSubDomains: true,
    },
})
```

✅ **Rate Limiting:**
```javascript
rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100, // limit each IP to 100 requests per windowMs
    message: "Too many requests",
})
```

✅ **Input Validation:**
```javascript
const schema = Joi.object({
    username: Joi.string().alphanum().min(3).max(30).required(),
    password: Joi.string().min(8).pattern(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/),
    email: Joi.string().email(),
});
```

✅ **File Upload Security:**
- Validate file types and sizes
- Scan for malware
- Store outside web root
- Generate unique filenames

### Part 2: Performance Optimization (30 points)

#### 2.1 Database Optimization (15 points)

**Required:**

✅ **Fix N+1 Queries:**
```javascript
// Use JOIN instead of multiple queries
const posts = await db.query(`
    SELECT
        p.*,
        u.username,
        u.avatar,
        COUNT(DISTINCT l.id) as like_count,
        COUNT(DISTINCT c.id) as comment_count
    FROM posts p
    JOIN users u ON p.user_id = u.id
    LEFT JOIN likes l ON p.id = l.post_id
    LEFT JOIN comments c ON p.id = c.post_id
    GROUP BY p.id
    LIMIT 50
`);
```

✅ **Add Indexes:**
```sql
CREATE INDEX idx_posts_user_id ON posts(user_id);
CREATE INDEX idx_posts_created_at ON posts(created_at DESC);
CREATE INDEX idx_likes_post_id ON likes(post_id);
CREATE INDEX idx_comments_post_id ON comments(post_id);
```

✅ **Implement Caching:**
```javascript
// Redis caching
const cachedPosts = await redis.get('feed:home');
if (cachedPosts) {
    return JSON.parse(cachedPosts);
}

const posts = await fetchPosts();
await redis.setex('feed:home', 300, JSON.stringify(posts)); // 5min TTL
```

✅ **Connection Pooling:**
```javascript
const pool = new Pool({
    max: 20, // maximum pool size
    idleTimeoutMillis: 30000,
    connectionTimeoutMillis: 2000,
});
```

#### 2.2 Frontend Optimization (15 points)

**Required:**

✅ **Image Optimization:**
- Compress images (imagemin, sharp)
- Convert to WebP format
- Implement lazy loading
- Use responsive images (srcset)
- Add CDN for static assets

✅ **Code Splitting:**
```javascript
// React lazy loading
const Feed = lazy(() => import('./components/Feed'));
const Profile = lazy(() => import('./components/Profile'));

<Suspense fallback={<Loading />}>
    <Route path="/feed" component={Feed} />
</Suspense>
```

✅ **Bundle Optimization:**
- Tree shaking
- Minification
- Compression (Brotli/Gzip)
- Remove unused dependencies

✅ **Browser Caching:**
```javascript
// Set cache headers
res.setHeader('Cache-Control', 'public, max-age=31536000, immutable');
```

### Part 3: Testing & Security Scanning (15 points)

#### 3.1 Security Testing (10 points)

**Required:**

✅ **SAST (Static Analysis):**
```bash
# ESLint security plugin
npm install --save-dev eslint-plugin-security

# Run security audit
npm audit
npm audit fix

# Dependency scanning
npx snyk test
```

✅ **DAST (Dynamic Analysis):**
```bash
# OWASP ZAP scanning
docker run -t owasp/zap2docker-stable zap-baseline.py \
    -t http://localhost:3000
```

✅ **Penetration Testing:**
- Test SQL injection endpoints
- Test authentication bypass attempts
- Test XSS vectors
- Test CSRF protection

#### 3.2 Performance Testing (5 points)

**Required:**

✅ **Load Testing:**
```javascript
// k6 load test
import http from 'k6/http';
import { check } from 'k6';

export let options = {
    stages: [
        { duration: '2m', target: 100 },
        { duration: '5m', target: 100 },
        { duration: '2m', target: 0 },
    ],
    thresholds: {
        http_req_duration: ['p(99)<1000'], // 99% under 1s
    },
};

export default function() {
    let res = http.get('http://localhost:3000/api/feed');
    check(res, { 'status is 200': (r) => r.status === 200 });
}
```

✅ **Lighthouse Audits:**
- Performance score >90
- Accessibility score >90
- Best Practices score >90
- SEO score >90

### Part 4: Operations & Monitoring (15 points)

#### 4.1 Logging & Error Tracking (8 points)

**Required:**

✅ **Structured Logging:**
```javascript
const logger = winston.createLogger({
    format: winston.format.json(),
    transports: [
        new winston.transports.File({ filename: 'error.log', level: 'error' }),
        new winston.transports.File({ filename: 'combined.log' }),
    ],
});

logger.info('User logged in', {
    userId: user.id,
    ip: req.ip,
    timestamp: new Date(),
});
```

✅ **Error Tracking:**
```javascript
// Sentry integration
Sentry.init({
    dsn: process.env.SENTRY_DSN,
    environment: process.env.NODE_ENV,
});

app.use(Sentry.Handlers.errorHandler());
```

#### 4.2 Monitoring & Alerting (7 points)

**Required:**

✅ **Metrics Collection:**
```javascript
// Prometheus metrics
const promClient = require('prom-client');
const register = new promClient.Registry();

const httpRequestDuration = new promClient.Histogram({
    name: 'http_request_duration_seconds',
    help: 'Duration of HTTP requests in seconds',
    labelNames: ['method', 'route', 'status_code'],
});

register.registerMetric(httpRequestDuration);
```

✅ **Health Checks:**
```javascript
app.get('/health', async (req, res) => {
    const health = {
        uptime: process.uptime(),
        timestamp: Date.now(),
        database: await checkDatabase(),
        redis: await checkRedis(),
    };

    const status = health.database && health.redis ? 200 : 503;
    res.status(status).json(health);
});
```

✅ **Dashboards:**
- Grafana dashboard for metrics
- Real-time error tracking
- Performance monitoring

---

## 📊 Evaluation Rubric

### 1. Functional Correctness (25 points)

**Excellent (20-25):**
- All vulnerabilities fixed
- Application fully functional
- Authentication/authorization working
- Performance targets met (<1s page load)

**Good (15-19):**
- Most vulnerabilities fixed
- Minor issues remain

**Adequate (10-14):**
- Some vulnerabilities fixed
- Significant gaps

**Poor (0-9):**
- Major vulnerabilities remain

### 2. Code Quality (25 points)

**Excellent (20-25):**
- Clean, maintainable fixes
- Proper error handling
- Security best practices
- No new technical debt

**Good (15-19):**
- Good fixes
- Some areas improvable

**Adequate (10-14):**
- Functional but messy

**Poor (0-9):**
- Poor code quality

### 3. AI Utilization (20 points)

**Excellent (16-20):**
- AI-generated security fixes
- Automated vulnerability scanning with AI assistance
- AI-optimized database queries
- Generated comprehensive security tests

**Good (12-15):**
- Good AI usage for fixes

**Adequate (8-11):**
- Basic AI assistance

**Poor (0-7):**
- Minimal AI usage

### 4. Testing & Validation (15 points)

**Excellent (12-15):**
- Security tests passing
- Load tests meeting targets
- Lighthouse score >90
- Penetration tests passing

**Good (9-11):**
- Good test coverage

**Adequate (6-8):**
- Basic tests

**Poor (0-5):**
- No tests

### 5. Documentation (15 points)

**Excellent (12-15):**
- Security fixes documented
- Performance improvements quantified
- Deployment guide
- Security best practices guide

**Good (9-11):**
- Good documentation

**Adequate (6-8):**
- Minimal docs

**Poor (0-5):**
- No docs

---

## 🚀 Getting Started

### Step 1: Clone Vulnerable App

```bash
git clone [vulnerable-app-repo]
cd challenge-3-security-performance
docker-compose up -d
```

### Step 2: Security Audit (Agentic Mode)

**Prompt Example:**
```
"Analyze this Node.js application for security vulnerabilities:
1. Scan for SQL injection points
2. Check authentication implementation
3. Identify XSS vulnerabilities
4. Find exposed secrets
5. List all OWASP Top 10 issues

Provide specific file locations and vulnerable code snippets."
```

### Step 3: Fix Vulnerabilities (Agentic Mode)

**Prompt Example:**
```
"Fix SQL injection vulnerability in backend/routes/posts.js:
1. Convert to parameterized queries
2. Add input validation with Joi
3. Implement prepared statements
4. Add error handling
5. Write security tests"
```

### Step 4: Implement Authentication (Agentic + Chat)

**Prompt Example:**
```
"Implement JWT authentication for this Express app:
1. Add bcrypt password hashing
2. Create login/register endpoints
3. Implement JWT token generation
4. Add authentication middleware
5. Add refresh token mechanism
6. Write authentication tests"
```

### Step 5: Performance Optimization (Agentic Mode)

**Prompt Example:**
```
"Optimize this database query to fix N+1 problem:
[paste vulnerable code]

Requirements:
1. Use JOIN instead of multiple queries
2. Add appropriate indexes
3. Implement Redis caching
4. Add query performance logging
5. Write performance tests"
```

---

## 💡 AI Mode Strategy

### Agentic Mode (50%)

**Use for:**
- ✅ Bulk security fixes across files
- ✅ Implementing authentication system
- ✅ Generating security tests
- ✅ Database query optimization

### Chat Mode (35%)

**Use for:**
- ✅ Quick security questions
- ✅ Best practice lookups
- ✅ Debugging specific errors
- ✅ Configuration syntax

### Workspace Mode (15%)

**Use for:**
- ✅ Planning security architecture
- ✅ Designing caching strategy
- ✅ Monitoring setup planning

---

## ⏱️ Time Allocation

| Phase | Time | AI Mode |
|-------|------|---------|
| **Security Audit** | 0.5h | Agentic |
| **Fix Vulnerabilities** | 2h | Agentic + Chat |
| **Authentication** | 1.5h | Agentic |
| **Performance Optimization** | 2h | Agentic |
| **Security Testing** | 1h | Chat + Agentic |
| **Monitoring** | 1h | Agentic |
| **Documentation** | 0.5h | Agentic |

**Total: 8.5 hours**

---

## 🏆 Bonus Points (10 extra points)

- **WAF Integration (+3):** Add ModSecurity rules
- **Zero Trust Architecture (+5):** Service mesh with mTLS
- **Automated Security Pipeline (+2):** CI/CD security gates
- **Security Headers Grade A+ (+2):** securityheaders.com scan

---

## 🎓 Learning Objectives

1. **Vulnerability Detection** using AI
2. **Security Patterns** implementation
3. **Performance Profiling** and optimization
4. **Security Testing** automation
5. **Production Operations** best practices

---

## 📝 Submission Requirements

1. **Code:** Fixed application in GitHub repo
2. **Security Report:** List of vulnerabilities found and fixed
3. **Performance Report:** Before/after metrics (load times, Lighthouse scores)
4. **Documentation:** Security best practices guide

---

**Challenge Created:** 2025-11-19
**Difficulty Level:** High
**Recommended Experience:** 2+ years web development
**AI Advantage Score:** 88/100

---

*Security and performance are not optional. Make it production-ready.*

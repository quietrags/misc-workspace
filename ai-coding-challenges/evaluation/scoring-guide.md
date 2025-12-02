# Evaluation & Scoring Guide

**For evaluators assessing AI coding challenge submissions**

---

## 🎯 Evaluation Philosophy

### Core Principles

1. **Evidence-Based:** Score based on objective criteria and measurable outcomes
2. **Consistent:** Apply rubrics uniformly across all submissions
3. **Holistic:** Consider context and trade-offs, not just checklist completion
4. **Constructive:** Provide actionable feedback for improvement
5. **AI-Aware:** Evaluate both AI usage effectiveness and output quality

### What We're Measuring

- ✅ **Functional Correctness:** Does it work as specified?
- ✅ **Code Quality:** Is it maintainable, secure, performant?
- ✅ **AI Effectiveness:** Did they use AI strategically?
- ✅ **Testing Rigor:** Are quality guardrails in place?
- ✅ **Documentation:** Can others understand and operate it?

### What We're NOT Measuring

- ❌ Speed alone (quality matters more)
- ❌ Lines of code (conciseness valued)
- ❌ Technology choices (within reason)
- ❌ Over-engineering (YAGNI principle)

---

## 📋 Evaluation Process

### Phase 1: Initial Review (30 minutes)

**Objectives:**
- Verify submission completeness
- Run automated checks
- Understand architecture approach

**Checklist:**
- [ ] Submission template completed
- [ ] Code repository accessible
- [ ] All required deliverables present
- [ ] Tests can be run
- [ ] Application can be started

**Automated Checks:**
```bash
# Clone repository
git clone [submission-repo]
cd [submission-repo]

# Check for required files
ls -la README.md
ls -la tests/

# Run automated quality checks
npm run lint  # or equivalent
npm test
npm run security-scan  # if available

# Check test coverage
npm run test:coverage
```

**Initial Red Flags:**
- 🚩 No tests
- 🚩 Tests failing
- 🚩 No documentation
- 🚩 Security vulnerabilities (critical)
- 🚩 Application doesn't start

**If red flags present:** Document in evaluation notes, may result in automatic point deductions.

---

### Phase 2: Functional Evaluation (60 minutes)

**Test each functional requirement from the challenge:**

#### For Challenge 1: Legacy Modernization

**Service Extraction (Core requirement):**
- [ ] Service 1 extracted and running independently
- [ ] Service 2 extracted and running independently
- [ ] Service 3 extracted and running independently
- [ ] Services communicate correctly
- [ ] API Gateway routing works

**Test Scenarios:**
1. Create order through API Gateway → Verify flows through all services
2. Kill one service → Verify graceful failure
3. Check database for data consistency
4. Verify backward compatibility with legacy endpoints

**Scoring:**
- All services working: 20-25 points
- 2 services working: 15-19 points
- 1 service working: 10-14 points
- Broken: 0-9 points

#### For Challenge 2: Distributed Systems

**Core Functionality:**
- [ ] Event ingestion working
- [ ] Event processing working
- [ ] State persistence working
- [ ] Fault tolerance demonstrated

**Test Scenarios:**
1. Send 1000 events → Verify all processed
2. Send duplicate events → Verify deduplicated
3. Kill worker mid-processing → Verify auto-recovery
4. Send malformed event → Verify dead letter queue
5. Check metrics endpoint → Verify reporting

**Chaos Tests:**
```bash
# Run provided chaos tests
npm run chaos:network-partition
npm run chaos:node-failure
npm run chaos:database-outage
```

**Scoring:**
- All scenarios pass + chaos tests: 20-25 points
- Most scenarios pass: 15-19 points
- Core working, chaos fails: 10-14 points
- Major issues: 0-9 points

#### For Challenge 3: Security & Performance

**Security Validation:**
```bash
# Run security scans
npm audit
snyk test
owasp-zap-scan.sh

# Manual penetration testing
curl -X POST '/api/login' -d "username=admin' OR 1=1--"
# Should NOT result in SQL injection
```

**Performance Validation:**
```bash
# Run Lighthouse
lighthouse http://localhost:3000 --output json

# Run load tests
k6 run load-test.js

# Check page load
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:3000
```

**Scoring Matrix:**

| Criteria | Points |
|----------|--------|
| All critical vulns fixed | 10 |
| Authentication implemented | 5 |
| Performance <1s page load | 5 |
| Security headers present | 3 |
| No high/critical vulns in scan | 2 |

**Total:** 20-25 points if all criteria met

---

### Phase 3: Code Quality Assessment (45 minutes)

**Use combination of automated tools and manual review:**

#### Automated Code Quality

**Tools:**
- SonarQube / CodeClimate for quality metrics
- ESLint / Pylint for linting
- Prettier for formatting
- Security scanners (Snyk, Bandit)

**Run Analysis:**
```bash
# SonarQube
sonar-scanner

# Or CodeClimate
codeclimate analyze

# Language-specific linters
eslint .
pylint **/*.py
golangci-lint run
```

**Key Metrics:**

| Metric | Excellent | Good | Adequate | Poor |
|--------|-----------|------|----------|------|
| Maintainability Index | >70 | 50-70 | 30-50 | <30 |
| Cyclomatic Complexity | <10 avg | 10-15 | 15-20 | >20 |
| Code Duplication | <3% | 3-5% | 5-10% | >10% |
| Security Issues | 0 | 1-2 low | 3-5 low | Any medium+ |
| Test Coverage | >80% | 60-80% | 40-60% | <40% |

#### Manual Code Review

**Review 3-5 critical files for:**

1. **Architecture & Design**
   - [ ] Clear separation of concerns
   - [ ] Appropriate use of design patterns
   - [ ] Low coupling, high cohesion
   - [ ] SOLID principles followed

2. **Error Handling**
   - [ ] Errors properly caught and logged
   - [ ] Graceful degradation
   - [ ] User-friendly error messages
   - [ ] No swallowed exceptions

3. **Security**
   - [ ] Input validation present
   - [ ] No SQL injection vectors
   - [ ] No XSS vulnerabilities
   - [ ] Secrets not hardcoded
   - [ ] Authentication/authorization correct

4. **Performance**
   - [ ] No obvious N+1 queries
   - [ ] Appropriate use of caching
   - [ ] Async operations where needed
   - [ ] Resource cleanup (connections, files)

5. **Readability**
   - [ ] Clear naming conventions
   - [ ] Appropriate comments (not too many, not too few)
   - [ ] Logical code organization
   - [ ] Consistent formatting

**Scoring Guide:**

**Excellent (20-25):**
- Clean, professional code
- Best practices throughout
- Minimal technical debt
- Production-ready quality

**Good (15-19):**
- Well-structured code
- Some minor improvements possible
- Low technical debt

**Adequate (10-14):**
- Functional but needs refactoring
- Multiple code smells
- Medium technical debt

**Poor (0-9):**
- Hard to maintain
- Multiple anti-patterns
- High technical debt

---

### Phase 4: AI Utilization Assessment (30 minutes)

**Review AI usage documentation:**

#### Evaluation Criteria

1. **Strategic Mode Selection (5 points)**
   - Used appropriate modes for different tasks
   - Evidence of understanding mode strengths
   - Not over-reliant on single mode

**Questions to ask:**
- Did they use Workspace for planning?
- Did they use Agentic for multi-file changes?
- Did they use Chat for quick queries?

**Scoring:**
- Excellent mode selection: 5 points
- Good but could improve: 3-4 points
- Poor mode selection: 0-2 points

2. **Prompt Engineering Quality (8 points)**
   - Specific, context-rich prompts
   - Appropriate level of detail
   - Evidence of iteration and refinement

**Review prompt examples in submission:**
```
Bad Prompt:
"Add authentication"

Good Prompt:
"Implement JWT authentication for this Express API with:
- bcrypt password hashing
- Access token (15min) + refresh token (7 days)
- Role-based authorization middleware
- Rate limiting on auth endpoints
- Comprehensive tests"
```

**Scoring:**
- Advanced prompt engineering: 7-8 points
- Good prompts with room for improvement: 5-6 points
- Basic prompts: 3-4 points
- Poor prompts: 0-2 points

3. **Output Validation (4 points)**
   - Evidence of reviewing AI-generated code
   - Modifications made where appropriate
   - Testing of AI outputs
   - Quality control processes

**Look for:**
- Did they blindly use AI code, or review it?
- Did they add tests for AI-generated code?
- Did they fix AI mistakes?

**Scoring:**
- Rigorous validation: 4 points
- Some validation: 2-3 points
- Little validation: 0-1 points

4. **Learning & Reflection (3 points)**
   - Documented learnings about AI usage
   - Identified AI strengths and weaknesses
   - Showed improvement over time

**Scoring:**
- Deep insights: 3 points
- Some insights: 2 points
- Minimal reflection: 0-1 points

**Total AI Utilization: 20 points**

---

### Phase 5: Testing & Documentation (30 minutes)

#### Testing Evaluation (15 points)

**Test Coverage (5 points):**
```bash
# Run coverage report
npm run test:coverage
```

**Scoring:**
- >80% coverage: 5 points
- 60-80%: 4 points
- 40-60%: 2-3 points
- <40%: 0-1 points

**Test Quality (5 points):**

Review test files for:
- [ ] Tests are meaningful (not just for coverage)
- [ ] Edge cases covered
- [ ] Integration tests present
- [ ] Tests are maintainable
- [ ] Good test naming

**Scoring:**
- Excellent test quality: 5 points
- Good tests: 3-4 points
- Basic tests: 1-2 points
- Poor tests: 0 points

**Test Types (5 points):**
- [ ] Unit tests
- [ ] Integration tests
- [ ] E2E tests (if applicable)
- [ ] Performance tests (if applicable)
- [ ] Security tests (if applicable)

**Scoring:**
- Comprehensive test suite: 5 points
- Multiple test types: 3-4 points
- Only unit tests: 1-2 points
- Minimal tests: 0 points

#### Documentation Evaluation (15 points)

**README Quality (5 points):**
- [ ] Clear setup instructions
- [ ] Prerequisites listed
- [ ] Quick start guide
- [ ] Troubleshooting section

**Architecture Documentation (5 points):**
- [ ] System architecture diagram
- [ ] Component descriptions
- [ ] Data flow explanations
- [ ] Technology choices justified

**API Documentation (3 points):**
- [ ] Endpoints documented
- [ ] Request/response examples
- [ ] Error codes listed
- [ ] Authentication described

**Operational Docs (2 points):**
- [ ] Deployment guide
- [ ] Monitoring/logging info
- [ ] Backup/recovery procedures

---

## 📊 Final Scoring

### Score Aggregation

| Dimension | Weight | Max Points | Score | Weighted |
|-----------|--------|------------|-------|----------|
| Functional Correctness | 25% | 25 | [X] | [X] |
| Code Quality | 25% | 25 | [X] | [X] |
| AI Utilization | 20% | 20 | [X] | [X] |
| Testing & Reliability | 15% | 15 | [X] | [X] |
| Documentation | 15% | 15 | [X] | [X] |
| **TOTAL** | **100%** | **100** | **[X]** | **[X]** |

### Grade Assignment

| Score Range | Grade | Assessment |
|-------------|-------|------------|
| 90-100 | A+ | Exceptional - Industry-leading quality |
| 85-89 | A | Excellent - Production-ready, best practices |
| 80-84 | A- | Very Good - Minor improvements needed |
| 75-79 | B+ | Good - Some gaps but solid overall |
| 70-74 | B | Satisfactory - Meets requirements |
| 65-69 | B- | Adequate - Below expectations in areas |
| 60-64 | C | Needs Improvement - Significant gaps |
| <60 | D/F | Unsatisfactory - Major issues |

---

## 📝 Feedback Template

**Use this template for feedback:**

```markdown
# Evaluation Feedback: [Challenge Name]

**Participant:** [Name]
**Evaluator:** [Your Name]
**Date:** YYYY-MM-DD
**Final Score:** [X]/100 ([Grade])

---

## Summary

[2-3 paragraph summary of overall submission quality]

**Strengths:**
- [Strength 1]
- [Strength 2]
- [Strength 3]

**Areas for Improvement:**
- [Improvement area 1]
- [Improvement area 2]
- [Improvement area 3]

---

## Detailed Scores

### 1. Functional Correctness: [X]/25

**What worked well:**
- [Specific examples]

**What needs work:**
- [Specific examples]

**Suggestions:**
- [Actionable improvements]

### 2. Code Quality: [X]/25

**What worked well:**
- [Specific examples]

**What needs work:**
- [Specific examples]

**Suggestions:**
- [Actionable improvements]

### 3. AI Utilization: [X]/20

**What worked well:**
- [Specific examples of effective AI usage]

**What needs work:**
- [Missed opportunities for AI assistance]

**Suggestions:**
- [How to improve AI tool usage]

### 4. Testing & Reliability: [X]/15

**What worked well:**
- [Test strengths]

**What needs work:**
- [Testing gaps]

**Suggestions:**
- [Testing improvements]

### 5. Documentation: [X]/15

**What worked well:**
- [Documentation strengths]

**What needs work:**
- [Documentation gaps]

**Suggestions:**
- [Documentation improvements]

---

## Key Learnings

**What this submission teaches us:**
- [Insight 1]
- [Insight 2]
- [Insight 3]

---

## Recommended Next Steps

For this participant:
1. [Action item 1]
2. [Action item 2]
3. [Action item 3]

---

**Evaluator Signature:** [Name]
**Date:** YYYY-MM-DD
```

---

## 🎓 Calibration Guidelines

### Avoiding Evaluator Bias

**Common Biases to Watch For:**

1. **Halo Effect:** Don't let one excellent aspect inflate other scores
2. **Horn Effect:** Don't let one poor aspect deflate other scores
3. **Recency Bias:** Don't compare to most recent submission only
4. **Anchoring:** Don't anchor too heavily on first few submissions
5. **Leniency/Severity:** Maintain consistent standards across all submissions

### Calibration Exercises

**Before evaluating submissions:**

1. **Review rubrics thoroughly**
2. **Score 3 sample submissions** with other evaluators
3. **Compare scores** and discuss discrepancies
4. **Align on standards** for each score level
5. **Document edge cases** and how to score them

### Consistency Checks

**Periodically:**
- Compare your scores to other evaluators
- Re-score a previous submission to check consistency
- Discuss outlier scores with other evaluators
- Update rubrics based on learnings

---

## 🔍 Edge Cases & FAQs

### Q: What if they used a different tech stack than suggested?

**A:** Acceptable if they justify it and meet all requirements. Don't penalize for technology choices unless they clearly hinder quality.

### Q: What if they only partially completed the challenge?

**A:** Score based on what was completed. Partial credit for partial work, but functional correctness score will be lower.

### Q: What if tests are failing?

**A:** Significant penalty. Functional correctness and testing scores both affected. Must document why tests fail.

### Q: What if they clearly didn't use AI much?

**A:** Lower AI utilization score, but doesn't affect other dimensions if quality is high. They may have experience in the domain.

### Q: What if AI-generated code has issues they didn't catch?

**A:** Reflects poorly on both code quality and AI utilization (lack of validation). Score both dimensions accordingly.

### Q: What if documentation is excellent but code is poor?

**A:** Score each dimension independently. Good docs don't compensate for poor code and vice versa.

### Q: What about bonus features?

**A:** Award bonus points as specified in challenge (typically 5-15 extra points). Note them clearly in feedback.

---

## 📈 Data Collection

**For research purposes, collect:**

- [ ] Final scores by dimension
- [ ] Overall completion time
- [ ] AI tools used
- [ ] Common mistakes
- [ ] Effective patterns observed
- [ ] Areas where most struggle

**Aggregate data helps:**
- Improve challenge design
- Refine rubrics
- Identify learning gaps
- Inform best practices

---

## 🔄 Continuous Improvement

### After Each Evaluation Batch

**Review and update:**
1. Are rubrics clear and comprehensive?
2. Are score distributions reasonable?
3. Are we measuring what matters?
4. What patterns emerge across submissions?
5. How can we improve challenges?

### Quarterly Reviews

**Conduct deeper analysis:**
- Inter-rater reliability
- Score distribution analysis
- Correlation between scores and experience
- AI effectiveness patterns
- Challenge difficulty calibration

---

**Guide Version:** 1.0
**Created:** 2025-11-19
**Next Review:** After first 50 evaluations

---

*Fair, consistent, constructive evaluation drives learning and improvement.*

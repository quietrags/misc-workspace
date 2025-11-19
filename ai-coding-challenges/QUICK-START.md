# Quick Start Guide

**Get started with AI coding challenges in 5 minutes**

---

## 🎯 What is This?

A framework for testing and improving your AI-augmented coding skills through real-world challenges that mirror enterprise engineering work.

**Key Features:**
- 3 diverse challenges (choose any 2)
- Designed for GitHub Copilot, Claude Code, Cursor, and similar tools
- Real evaluation rubrics
- Research-backed methodology

---

## 🚀 Quick Decision Tree

### "Which challenge should I do?"

**Are you interested in microservices architecture?**
→ **YES:** Start with [Challenge 1: Legacy Modernization](./challenges/challenge-1-legacy-modernization/)

**Do you love distributed systems and fault tolerance?**
→ **YES:** Start with [Challenge 2: Distributed Systems](./challenges/challenge-2-distributed-systems/)

**Want to focus on security and performance?**
→ **YES:** Start with [Challenge 3: Security & Performance](./challenges/challenge-3-security-performance/)

**Not sure?**
→ Read [Problem Statement](./PROBLEM-STATEMENT.md) for detailed comparison

---

## 📚 Essential Reading (20 minutes)

**Must Read (15 min):**
1. [Main README](./README.md) - Overview and philosophy
2. Your chosen challenge README
3. [Submission Template](./templates/submission-template.md)

**Recommended (5 min):**
4. [AI Usage Log Template](./templates/ai-usage-log-template.md)
5. [Scoring Guide](./evaluation/scoring-guide.md) - Know how you'll be evaluated

**Deep Dive (Optional):**
- [Problem Statement](./PROBLEM-STATEMENT.md) - Theoretical foundation
- [AI Coding Effectiveness Research](./research/ai-coding-effectiveness.md)

---

## ⚡ 5-Minute Setup

### Step 1: Choose Your Challenges (2 min)

Pick **2 out of 3** challenges based on:
- Your interests
- Your experience level
- Time available (6-10 hours per challenge)

### Step 2: Download Templates (1 min)

```bash
# Copy templates to your working directory
cp templates/submission-template.md my-submission.md
cp templates/ai-usage-log-template.md my-ai-log.md
```

### Step 3: Set Up Your AI Tools (2 min)

**GitHub Copilot:**
- Ensure Copilot subscription is active
- Enable Chat, Agentic, and Workspace modes

**Claude Code:**
```bash
# Install if needed
npm install -g @anthropic-ai/claude-code

# Verify installation
claude --version
```

**Cursor:**
- Download from cursor.sh
- Configure AI settings
- Enable Composer mode

---

## 🏁 Starting Your First Challenge

### Challenge 1: Legacy Modernization

**Time Estimate:** 6-8 hours

**Quick Start:**
```bash
# 1. Clone starter code (coming soon)
git clone [starter-repo]
cd challenge-1-legacy-modernization

# 2. Explore codebase
ls -R

# 3. Use AI to analyze
# Prompt: "Analyze this codebase and identify service boundaries"

# 4. Start planning with Workspace mode
# Prompt: "Create specification for extracting Product service"
```

**Key Files:**
- [Full Challenge Details](./challenges/challenge-1-legacy-modernization/README.md)
- Time allocation guide included
- AI mode strategy guide included

---

### Challenge 2: Distributed Systems

**Time Estimate:** 8-10 hours

**Quick Start:**
```bash
# 1. Design architecture (Workspace mode)
# Prompt: "Design distributed event processing system with..."

# 2. Bootstrap project (Agentic mode)
# Prompt: "Create Go project structure for event processing..."

# 3. Implement components
# Follow detailed guide in challenge README
```

**Key Files:**
- [Full Challenge Details](./challenges/challenge-2-distributed-systems/README.md)
- Architecture diagram included
- Chaos testing guide included

---

### Challenge 3: Security & Performance

**Time Estimate:** 6-8 hours

**Quick Start:**
```bash
# 1. Clone vulnerable app (coming soon)
git clone [vulnerable-app]
cd challenge-3-security-performance

# 2. Run security audit (Agentic mode)
# Prompt: "Analyze for security vulnerabilities..."

# 3. Fix vulnerabilities
# Follow systematic approach in challenge README
```

**Key Files:**
- [Full Challenge Details](./challenges/challenge-3-security-performance/README.md)
- Vulnerability checklist included
- Performance benchmark guide included

---

## 📊 Tracking Your Progress

### Use the AI Usage Log

**Why?**
- Helps you learn what works
- Required for submission
- Contributes to research

**How?**
Log each significant AI interaction:
```markdown
### Interaction #1
Timestamp: 2025-11-19 10:30
AI Mode: Agentic
Task: Extract Product service from monolith
Effectiveness: 9/10
```

### Time Management

**Suggested breakdown for 8-hour challenge:**

| Phase | Time | Focus |
|-------|------|-------|
| Planning | 1h | Architecture, specifications |
| Implementation | 4-5h | Core functionality |
| Testing | 1.5h | Tests, validation |
| Documentation | 1h | README, architecture docs |
| Buffer | 0.5h | Unexpected issues |

---

## 🎓 Tips for Success

### 1. Start with Planning (Workspace Mode)

**Don't skip this!** 30-60 minutes of planning saves hours later.

**Good planning prompt:**
```
"Design architecture for [challenge goal] with:
- Technology stack: [specific versions]
- Constraints: [list from challenge]
- Quality requirements: [tests, security, performance]

Provide:
1. Component diagram
2. Data flow
3. Key design decisions
4. Risk mitigation strategy"
```

### 2. Use AI Strategically

**Mode Selection Guide:**

| Task | Best Mode | Why |
|------|-----------|-----|
| Architecture planning | Workspace | High-level thinking |
| Multi-file refactoring | Agentic | Coordinated changes |
| Quick queries | Chat | Fast answers |
| Test generation | Agentic | Comprehensive coverage |
| Documentation | Agentic | Consistent formatting |

### 3. Quality Guardrails

**Always:**
- ✅ Review AI-generated code line-by-line
- ✅ Run tests after AI makes changes
- ✅ Use security scanners
- ✅ Check for performance issues
- ✅ Validate against requirements

**Never:**
- ❌ Blindly commit AI code
- ❌ Skip testing AI outputs
- ❌ Assume AI understands business logic
- ❌ Ignore security warnings

### 4. Iterate and Refine

**Pattern:**
1. Generate initial implementation (AI)
2. Test and identify issues (You)
3. Refine with specific feedback (AI)
4. Validate improvements (You)
5. Repeat until quality bar met

---

## 📝 Submission Checklist

**Before submitting:**

- [ ] Both challenges completed and working
- [ ] All tests passing (>80% coverage)
- [ ] Documentation complete
- [ ] Submission template filled out
- [ ] AI usage log completed
- [ ] Code pushed to GitHub
- [ ] README has setup instructions

**Quality checks:**
- [ ] Run security scan (no critical issues)
- [ ] Run linter (no major issues)
- [ ] Check performance (meets targets)
- [ ] Review code quality (maintainable)

---

## ❓ Common Questions

**Q: Can I use different AI tools for different challenges?**
A: Yes! Use whatever works best for you.

**Q: What if I can't finish in the estimated time?**
A: Focus on quality over quantity. Partial completion is fine.

**Q: Can I use Google/Stack Overflow?**
A: Yes, but document it. This tests AI augmentation, not AI-only coding.

**Q: Do I need to use all three AI modes?**
A: Recommended but not required. Use what works for you.

**Q: Can I get help from other people?**
A: This should be individual work, but reviewing docs is fine.

**Q: What if tests are failing?**
A: Don't submit until tests pass. Get them working first.

---

## 🆘 Getting Unstuck

### Stuck on architecture?

**Try this prompt:**
```
"I'm working on [challenge]. I'm stuck on [specific decision].

Context:
- Current approach: [what you've tried]
- Constraints: [from challenge]
- Problem: [specific issue]

Please provide:
1. 3 architecture options
2. Trade-offs for each
3. Recommendation with rationale"
```

### Stuck on implementation?

**Try this approach:**
1. Break problem into smaller pieces
2. Get AI to implement smallest piece
3. Test that piece
4. Move to next piece
5. Integrate incrementally

### Stuck on tests?

**Use AI to generate tests:**
```
"Generate comprehensive tests for [function/class]:

Code:
[paste your code]

Requirements:
- Unit tests for all public methods
- Edge cases covered
- Mocks for dependencies
- >80% coverage
- Use [testing framework]"
```

---

## 📚 Additional Resources

### AI Tool Documentation
- [GitHub Copilot Docs](https://docs.github.com/copilot)
- [Claude Code Guide](https://docs.anthropic.com/claude-code)
- [Cursor Documentation](https://cursor.sh/docs)

### Technical Resources
- [System Design Primer](https://github.com/donnemartin/system-design-primer)
- [Microservices Patterns](https://microservices.io/patterns/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

### Challenge-Specific
- Challenge 1: [Strangler Fig Pattern](https://martinfowler.com/bliki/StranglerFigApplication.html)
- Challenge 2: [Distributed Systems Resources](https://github.com/theanalyst/awesome-distributed-systems)
- Challenge 3: [Web Security Testing](https://owasp.org/www-project-web-security-testing-guide/)

---

## 🎯 Your Challenge Journey

```
Day 1:
├─ Morning: Read docs, choose challenges
├─ Afternoon: Start Challenge #1 planning
└─ Evening: Begin implementation

Day 2:
├─ Morning: Complete Challenge #1 implementation
├─ Afternoon: Tests and documentation
└─ Evening: Start Challenge #2

Day 3:
├─ Morning: Challenge #2 implementation
├─ Afternoon: Complete and test
└─ Evening: Final review and submission
```

**Total time:** 2-3 days of focused work

---

## 🏆 After Completion

**You will have:**
- ✅ Mastered AI mode selection
- ✅ Developed prompt engineering skills
- ✅ Built production-quality code with AI
- ✅ Learned real-world architectural patterns
- ✅ Created portfolio-worthy projects

**Next steps:**
- Share your experience (blog post?)
- Contribute improvements to challenges
- Help evaluate other submissions
- Apply learnings to work projects

---

**Ready to start?** Pick your first challenge and let's go!

**Questions?** Review the full documentation or open an issue.

**Good luck!** 🚀

---

**Guide Version:** 1.0
**Created:** 2025-11-19

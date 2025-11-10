# Client Conversation Guide: Spec-Driven Development

**Target Audience:** VPs of Engineering, CTOs, Technical Leads
**Last Updated:** 2025-11-10

---

## Purpose

This guide helps Nagarro teams have productive conversations with engineering leaders about spec-driven development. It provides qualifying questions, positioning, and conversation frameworks.

---

## Pre-Call Research

Before the conversation, gather:

**Company Context:**
- [ ] Industry and compliance requirements
- [ ] Tech stack (languages, frameworks, cloud provider)
- [ ] Team size and structure
- [ ] Current AI tool usage (if known)
- [ ] Development methodology (agile, scrum, etc.)

**Pain Point Signals:**
- Recent blog posts about engineering challenges
- Job postings (what skills are they hiring for?)
- Engineering blog quality (indicates maturity)
- Public GitHub activity (if applicable)

---

## Conversation Framework

### Opening: Establish Context (5 min)

**Goal:** Understand their current state with AI coding tools

**Questions:**
1. "Are your teams currently using AI coding assistants like GitHub Copilot, Cursor, or Claude Code?"
   - **If Yes:** "How's that going? What's working well? What challenges have you seen?"
   - **If No:** "Have you considered AI coding tools? What's held you back?"

2. "How are you thinking about AI's role in your development process?"
   - Listen for: Speed focus vs. quality concern vs. balanced approach

---

### Discovery: Identify Pain Points (10-15 min)

**Quality & Technical Debt**

**Q:** "When your team generates code with AI, how are you ensuring quality and maintainability?"

**Listen for:**
- ❌ "We're not really tracking that yet"
- ❌ "Code reviews are struggling to keep up"
- ❌ "We're seeing more bugs in AI-generated code"
- ✅ "We have structured processes"
- ✅ "We're using specifications or similar"

**Follow-up (if pain point):** "Have you seen technical debt accumulate faster with AI code generation?"

---

**Governance & Compliance**

**Q:** "Do you have structured governance for AI-generated code in production systems?"

**Listen for:**
- ❌ "Not yet, it's ad-hoc"
- ❌ "We treat it the same as human code" (may need differentiation)
- ❌ "Security/compliance teams haven't weighed in"
- ✅ "We have clear policies and audit trails"

**Follow-up (if regulated industry):** "How are you handling audit trail requirements for AI-generated code?"

---

**Developer Experience & Skills**

**Q:** "How are your developers adapting to working with AI coding tools?"

**Listen for:**
- ❌ "Adoption is slower than we'd like"
- ❌ "Senior developers are resistant"
- ❌ "We haven't provided training"
- ❌ "They're struggling with context/prompt engineering"
- ✅ "We have training programs"
- ✅ "Adoption is strong and effective"

**Follow-up:** "Are your developers trained in context engineering versus more exploratory 'vibe coding' approaches?"

---

**Speed vs. Sustainability**

**Q:** "How are you balancing velocity gains from AI with long-term code sustainability?"

**Listen for:**
- ❌ "We're focused on speed right now"
- ❌ "Quality is becoming a concern"
- ❌ "We're seeing increased refactoring needs"
- ✅ "We measure both DORA and quality metrics"
- ✅ "We have balanced approach"

**Follow-up:** "What metrics are you using to measure AI coding effectiveness beyond velocity?"

---

### Pain Point Deep Dive (10 min)

*Choose the 1-2 most significant pain points and go deeper*

**For Quality Concerns:**

**Q:** "Can you quantify the quality impact? Are you seeing increases in code churn, duplication, or bug rates?"

**Share:** GitClear research data (211M lines, 7% churn, 48% increase in duplication)

**Positioning:** "Industry research shows that unstructured AI code generation can lead to quality degradation. Spec-driven approaches show 300% better maintainability and 85% fewer security vulnerabilities."

---

**For Governance Gaps:**

**Q:** "What would an ideal governance framework for AI-generated code look like for your organization?"

**Listen for:**
- Audit trail requirements
- Compliance needs (SOC2, HIPAA, etc.)
- Security scanning integration
- Code review process needs

**Positioning:** "Specifications provide persistent audit trails and compliance documentation that conversation history can't."

---

**For Skills/Adoption Challenges:**

**Q:** "What would make AI coding tools more effective for your senior developers?"

**Listen for:**
- Need for structure
- Control/oversight concerns
- Quality verification needs
- Integration with existing workflows

**Positioning:** "Spec-driven development provides the structure and oversight that senior developers need while maintaining the velocity gains of AI."

---

### Solution Introduction (5-10 min)

**Transition:** "Based on what you've shared, I think there's an approach that addresses [specific pain points]. Have you heard about spec-driven development?"

**If No:** *Provide 2-minute overview*

**Core Concept:**
"Spec-driven development starts with structured specifications that serve as contracts for AI agents. Instead of conversational 'vibe coding,' you create blueprints that guide the AI, provide persistent context, and enable governance."

**Four-Phase Workflow:**
1. **Specify:** Define requirements clearly
2. **Plan:** Translate to technical approach
3. **Tasks:** Break into reviewable units
4. **Implement:** AI executes with human oversight

---

**If Yes:** "What's been your experience with it?"

*Adjust based on their response*

---

### Nagarro's Approach (5 min)

**Positioning:** "From Prototype to Production"

**Key Points:**

1. **Integration with Fluidic Intelligence**
   - "We've seen 20% productivity gains with our Fluidic Intelligence approach"
   - "Spec-driven development extends that to AI-generated code"

2. **Enterprise-First**
   - Governance frameworks from day one
   - Security and compliance built in
   - Audit trails and documentation

3. **Balanced Metrics**
   - Not just DORA (speed) metrics
   - SPACE framework (team health)
   - Quality and security KPIs

4. **Partnership Ecosystem**
   - AWS Advanced Consulting Partner (Kiro integration)
   - GitHub, Databricks, Microsoft partnerships
   - Multi-tool support (not locked into one vendor)

**Differentiator:**
"Many teams can help you build prototypes quickly with AI. We help you build production-ready systems that maintain velocity while meeting enterprise governance requirements."

---

### Pilot Program Introduction (5 min)

**Proposal:** "We typically recommend a 30-day pilot program to prove value in your specific context."

**Structure:**

**Week 1: Assessment**
- Identify 3 power users (4+ hours/week on repetitive tasks)
- Baseline measurement (current velocity, quality metrics)
- Tool selection based on your tech stack and requirements

**Week 2: Setup & Training**
- Platform installation and configuration
- Specification template creation for your context
- Context engineering training

**Week 3: First Projects**
- 2-3 well-scoped projects using spec-driven workflow
- Daily check-ins, rapid iteration

**Week 4: Evaluation**
- Measure against baseline (DORA + SPACE + quality)
- Qualitative feedback
- Go/no-go decision for broader rollout

**Investment:**
- 3 developers (part-time)
- Nagarro facilitator
- Tool costs (if applicable)

**Expected Outcomes:**
- Quantified productivity impact
- Quality metrics comparison
- Team feedback on developer experience
- Roadmap for scaled adoption

---

## Qualifying Questions Summary

Use these to assess fit:

### High-Fit Signals
✅ Currently using AI tools but concerned about quality
✅ Regulated industry with governance requirements
✅ Senior developer adoption challenges
✅ Measuring quality, not just velocity
✅ Enterprise tech stack (AWS, GitHub, etc.)
✅ 50+ developer teams

### Medium-Fit Signals
⚡ Exploring AI tools, not yet adopted
⚡ Quality concerns emerging
⚡ Some governance requirements
⚡ 10-50 developer teams
⚡ Mixed tech stack

### Low-Fit Signals
❌ Not using AI tools, no plans to adopt
❌ Extreme speed priority, quality secondary
❌ No compliance requirements
❌ Very small teams (<5 developers)
❌ Only prototyping, no production systems

---

## Objection Handling

### "We're already using AI tools successfully"

**Response:** "That's great! How are you handling quality assurance and governance as you scale? Many teams find that what works for initial adoption needs structure as AI-generated code becomes a larger percentage of the codebase."

**Share:** GitClear data on quality degradation at scale

---

### "This sounds like going back to waterfall with heavy specs"

**Response:** "Great question - that's a common concern. Spec-driven development is actually complementary to agile. Specifications are living documents that evolve with the project, not big-bang requirements. Think of them as persistent context for AI rather than rigid contracts."

**Share:** Thoughtworks Radar assessment and how to avoid antipatterns

---

### "We don't have time for more process"

**Response:** "The research shows that 1 iteration with structured prompts equals 8 iterations without structure in terms of accuracy. You're actually saving time by investing upfront in specifications."

**Share:** Productivity data and ROI examples

---

### "Our developers prefer exploratory coding"

**Response:** "Absolutely - and there's a place for that. We call it 'vibe coding' and it's excellent for MVPs and prototypes. Spec-driven development is for production systems where quality, maintainability, and governance matter. Most teams use both approaches depending on context."

**Share:** Vibe coding vs. spec-driven comparison table

---

### "We can't afford to slow down"

**Response:** "The question is whether you can afford not to. The GitClear research shows code churn hitting 7%, refactoring declining, and duplication rising 48%. The technical debt from unstructured AI code generation compounds quickly. Spec-driven development maintains velocity while preventing debt accumulation."

**Share:** Long-term cost of technical debt vs. upfront structure investment

---

## Follow-Up Materials

After the conversation, send:

**Immediate (within 24 hours):**
- [ ] Thank you email with call summary
- [ ] 1-page overview of spec-driven development
- [ ] Relevant case study (if available)

**Within 1 week:**
- [ ] Main POV document (this research project output)
- [ ] Pilot program proposal customized to their context
- [ ] Tool recommendation based on their tech stack

**Within 2 weeks:**
- [ ] Proposed timeline for pilot
- [ ] Team introductions (Nagarro facilitators)

---

## Success Metrics for Conversation

**Good Outcome:**
- Identified 1-2 clear pain points
- Client expressed interest in pilot
- Next steps scheduled
- Client context documented

**Great Outcome:**
- Agreement to pilot program
- 3 power users identified
- Technical stakeholders engaged
- Timeline established

---

## Internal Handoff

After qualifying call, document:

**Client Profile:**
- Company, industry, size
- Tech stack
- Current AI tool usage
- Primary pain points (prioritized)

**Opportunity Assessment:**
- Fit score (High/Medium/Low)
- Estimated deal size
- Timeline
- Competition/alternatives

**Next Steps:**
- Pilot program scope
- Technical stakeholders to engage
- Required approvals/budget

**Nagarro Team:**
- Account lead
- Technical lead (for pilot)
- Subject matter experts needed

---

## Resources

**For Your Reference:**
- Main POV document: `main-pov.md`
- Evidence base: `research/evidence-base.md`
- Tools landscape: `research/tools-landscape.md`
- Case studies: `research/case-studies.md`

**For Clients:**
- Specification template: `templates/specification-template.md`
- 1-page executive summary: [To be created]
- Pilot program template: [To be created]

---

## Conversation Scripts (Quick Reference)

### 30-Second Elevator Pitch

"Spec-driven development is an approach to AI-assisted coding that starts with structured specifications rather than conversational prompts. It enables enterprise governance, quality assurance, and compliance while maintaining the velocity gains of AI. We help teams transition from AI prototypes to production-ready systems."

---

### 2-Minute Overview

"Many engineering teams are experiencing a paradox: AI coding tools are incredibly fast, but code quality concerns are emerging. GitClear analyzed 211 million lines of code and found code churn hitting 7%, refactoring declining, and duplication rising 48%.

Spec-driven development addresses this by treating specifications as the source of truth for AI agents. You define what should be built in structured specifications, then AI implements based on those blueprints. This provides:

1. **Quality assurance** - 300% better maintainability, 85% fewer vulnerabilities
2. **Governance** - Audit trails, compliance documentation, code review integration
3. **Persistent context** - Specifications don't disappear like conversation history
4. **Enterprise readiness** - Security, compliance, and scalability from day one

At Nagarro, we've integrated this with our Fluidic Intelligence approach that's already delivering 20% productivity gains. We help clients go from prototype to production with AI."

---

### 5-Minute Pitch

*Use 2-minute overview above + add:*

**Tool Ecosystem:**
"The landscape includes enterprise platforms like AWS Kiro, open source frameworks like GitHub Spec Kit, and integration with AI-native IDEs like Claude Code and Cursor. We help you select the right tools for your tech stack and requirements."

**Balanced Metrics:**
"We measure success with both DORA metrics for velocity and SPACE framework for team health. This prevents optimizing for speed at the cost of sustainability."

**Pilot Program:**
"We typically start with a 30-day pilot: 3 power users, 2-3 well-scoped projects, quantified before/after metrics. This proves value in your specific context before broader rollout."

**Partnership Advantage:**
"As an AWS Advanced Consulting Partner with strategic partnerships with GitHub, Databricks, and Microsoft, we have deep platform expertise and can integrate across your ecosystem."

---

## Version History

- **v1.0** (2025-11-10): Initial conversation guide

**Last Updated:** 2025-11-10
**Next Review:** 2025-12-10

---

*Maintained by Nagarro Spec-Driven Development Research Project*

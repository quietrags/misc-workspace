# Tools Landscape: Spec-Driven Development Platforms

**Last Updated:** 2025-11-10
**Next Review:** 2025-12-10

---

## Overview

This document tracks the rapidly evolving landscape of spec-driven development tools and platforms. Updated monthly to reflect new launches, significant updates, and industry shifts.

---

## Enterprise-Grade Platforms

### AWS Kiro

**Launch Date:** 2025
**Category:** Enterprise AI Coding Platform
**Workflow:** Specify → Plan → Execute

#### Key Features
- Strong brownfield support for existing codebases
- Deep AWS integration (Lambda, S3, ECS, etc.)
- Enterprise security (KMS encryption, IAM protocols, role-based access)
- Built-in compliance frameworks
- Multi-repository support

#### Pricing
- Enterprise pricing (contact AWS)
- Included with AWS Enterprise Support (some tiers)

#### Ideal For
- Mid-market to enterprise organizations
- Teams prioritizing maintainability over raw speed
- AWS-centric technology stacks
- Regulated industries (healthcare, finance)

#### Implementation Timeline
- Setup: 2-3 weeks
- Power user identification and training
- Integration with existing CI/CD pipelines

#### Sources
- [AWS Kiro announcement blog]
- [AWS documentation: kiro.aws.amazon.com]

---

### GitHub Copilot Workspace

**Launch Date:** 2024 (Public Preview)
**Category:** Specification-First IDE
**Workflow:** Auto-generated spec → plan → file-level changes

#### Key Features
- Native GitHub integration
- Built-in specification generation
- PR-ready code changes
- Works with public and private repositories
- Copilot Chat integration

#### Pricing
- Included with GitHub Copilot Business/Enterprise
- Individual: $10/month (Copilot subscription required)

#### Ideal For
- Teams already using GitHub Copilot
- GitHub-centric workflows
- Simple to moderate complexity changes
- Developers comfortable with GitHub ecosystem

#### Known Limitations
- Mixed results on complex problems
- Struggles with domain-specific requirements
- Performance varies significantly by task type
- Best with clear goals and context

#### Best Practices
- Provide clear, specific goals
- Add domain context upfront
- Review generated specs before proceeding
- Iterate on specifications before implementation

#### Sources
- [GitHub Copilot Workspace documentation]
- [GitHub Next research blog]

---

## Open Source Frameworks

### GitHub Spec Kit

**Launch Date:** 2025 (Open Source)
**Category:** Multi-Agent Specification Framework
**Repository:** github.com/github/spec-kit

#### Compatible Agents (15+)
- GitHub Copilot
- Claude Code
- Gemini CLI
- Cursor
- Windsurf
- Amazon Q Developer
- Cline
- [Full list in repo]

#### Core Commands
- `/specify` - Create/update project specifications
- `/plan` - Generate technical plan from specification
- `/tasks` - Break plan into reviewable work units

#### Key Features
- Configurable prompt templates
- Immutable "constitution" principles
- Agent-agnostic design
- Version-controlled specifications
- Extensible architecture

#### Installation
```bash
uvx --from git+https://github.com/github/spec-kit.git specify init
```

#### Philosophy
- Specification as the maintained artifact
- Code is generated from spec (not spec from code)
- Living, executable specifications
- Human-readable, AI-optimized format

#### Ideal For
- Teams wanting standardized workflow across multiple agents
- Open source projects
- Teams prioritizing flexibility over enterprise features
- Developer-led adoption (bottom-up)

#### Sources
- [GitHub Spec Kit repository]
- [Den Delimarsky blog post: "The ONLY guide you'll need for GitHub Spec Kit"]

---

### cc-sdd

**Category:** Kiro-Style Commands for Multiple Platforms
**Status:** Community-driven

#### Compatible Platforms
- Claude Code
- Cursor
- GitHub Copilot
- Gemini CLI
- Windsurf

#### Description
Brings Kiro-style specify/plan/execute workflow to multiple platforms without AWS lock-in

#### Ideal For
- Teams wanting Kiro workflow patterns
- Multi-cloud or non-AWS environments
- Cost-sensitive organizations

#### Sources
- [Community documentation]

---

## AI-Native IDEs

### Claude Code

**Launch Date:** 2024
**Category:** Terminal-First Agentic AI
**Developer:** Anthropic

#### Key Features
- Parallel agent execution
- Custom scripts and workflows
- System-level orchestration
- Spec Kit integration (community)
- MCP (Model Context Protocol) support

#### Workflow Integration
- Compatible with GitHub Spec Kit
- Custom slash commands for spec-driven workflows
- Agent-based task decomposition

#### Adoption Statistics
- ~90% AI-generated code in some high-growth SaaS companies
- Up from 10-15% twelve months ago

#### Pricing
- Usage-based (Claude API pricing)
- Professional: $20/month + usage
- Team/Enterprise: Custom pricing

#### Ideal For
- Terminal-comfortable developers
- Complex, multi-step workflows
- Custom automation requirements
- Projects requiring system-level access

#### Sources
- [Claude Code documentation: docs.claude.com/claude-code]
- [Anthropic blog]

---

### Cursor

**Launch Date:** 2023
**Category:** AI-Native VS Code Fork
**Developer:** Anysphere

#### Key Features
- Native VS Code compatibility
- Cmd+K: Inline completions
- Cmd+I: Side pane chat
- Agent Mode: Multi-step changes
- Codebase indexing

#### Spec-Driven Support
- Compatible with GitHub Spec Kit
- Agent Mode for multi-file changes
- Context-aware code generation

#### Pricing
- Free tier (limited)
- Pro: $20/month
- Business: Custom pricing

#### Ideal For
- VS Code users
- Visual IDE preference
- Teams wanting familiar UX with AI enhancement
- Individual developers

#### Sources
- [Cursor documentation]
- [Cursor changelog]

---

### Cline (VS Code Extension)

**Launch Date:** 2024
**Category:** Autonomous AI Coding Agent
**Platform:** VS Code Extension

#### Unique Features
- "Plan" and "Act" phases
- Different models for planning vs execution
- Autonomous multi-step workflows
- Task breakdown visualization

#### Workflow
1. Plan phase: Analyze requirements, create approach
2. Act phase: Execute plan with oversight
3. Review: Human validation gates

#### Ideal For
- VS Code users wanting autonomous agent
- Teams experimenting with AI workflows
- Projects requiring task decomposition

#### Pricing
- Free (extension) + AI model costs
- Works with OpenAI, Anthropic, local models

#### Sources
- [Cline VS Code marketplace]
- [Cline documentation]

---

## Emerging Frameworks

### Tessl Framework

**Status:** Emerging
**Philosophy:** Specification as the maintained artifact, not code

#### Core Concept
- Treat specs as primary artifact
- Code is generated/regenerated from specs
- Specification evolution over time
- "Never touch the generated code directly"

#### Status
- Early stage
- Experimental adoption
- Worth watching

---

## Tool Comparison Matrix

| Tool | Category | Setup Time | Security | Brownfield | Cost | Best For |
|------|----------|-----------|----------|------------|------|----------|
| **AWS Kiro** | Enterprise Platform | 2-3 weeks | Excellent | Excellent | $$$ | Enterprise, AWS shops |
| **GitHub Spec Kit** | OSS Framework | < 1 day | Good | Good | Free | Multi-agent teams |
| **Copilot Workspace** | GitHub IDE | < 1 hour | Good | Good | $ | GitHub users |
| **Claude Code** | Terminal AI | < 1 day | Good | Excellent | $$ | Terminal developers |
| **Cursor** | AI IDE | < 1 hour | Good | Good | $ | VS Code users |
| **Cline** | VS Code Extension | < 30 min | Good | Good | $ | VS Code, autonomous |

**Legend:**
- $ = <$25/user/month
- $$ = $25-100/user/month
- $$$ = Enterprise pricing

---

## Industry Adoption Statistics

**Overall Market:**
- Market Size: $7.38B (2025) → $103.6B projected (2032)
- 85% of organizations using AI agents in at least one workflow (2025)
- 15+ major platforms launched 2024-2025

**Platform-Specific:**
- **GitHub Copilot:** 15M+ users globally
- **Copilot Studio:** 230K+ organizations
- **Y Combinator W25:** 25% of startups with 95% AI-generated codebases
- **High-growth SaaS:** 90% AI-generated code (up from 10-15% in 2024)

---

## Selection Decision Framework

### Decision Tree

**Question 1: What's your primary infrastructure?**
- AWS-centric → Consider AWS Kiro
- GitHub-centric → Consider Copilot Workspace or Spec Kit
- Multi-cloud/agnostic → Consider Spec Kit, Claude Code, Cursor

**Question 2: What's your team size?**
- Individual (1-5) → Cursor, Cline, Claude Code
- Team (5-50) → Spec Kit, Cursor Business, Claude Code Teams
- Enterprise (50+) → AWS Kiro, GitHub Enterprise + Spec Kit

**Question 3: Greenfield or brownfield?**
- Greenfield (new projects) → Any platform
- Brownfield (existing codebases) → AWS Kiro, Claude Code, Spec Kit

**Question 4: Security/compliance requirements?**
- High (regulated) → AWS Kiro, GitHub Enterprise
- Medium (standard) → Any platform with proper configuration
- Low (internal tools) → Any platform

**Question 5: Developer preferences?**
- Terminal-first → Claude Code
- Visual IDE → Cursor, Copilot Workspace
- Flexible/both → Spec Kit (works with multiple agents)

---

## Watch List: Upcoming Developments

### Q4 2025 - Q1 2026

- **AWS Kiro:** Expected feature releases for multi-cloud support
- **GitHub Spec Kit:** v2.0 with enhanced constitution support
- **Thoughtworks Radar:** Next update (May 2026)
- **New Entrants:** Monitor JetBrains AI, Replit Agent, others

### Potential Market Shifts

- Consolidation among smaller players
- Enterprise platform acquisitions likely
- Standardization around specification formats
- Integration with existing dev tools (Jira, Linear, etc.)

---

## Update Log

### 2025-11-10
- Initial landscape documentation
- 15+ platforms catalogued
- Comparison matrix established
- Decision framework created

### Next Update: 2025-12-10
- Monitor new tool launches
- Update adoption statistics
- Refresh pricing information
- Track Thoughtworks Radar updates

---

## Sources & References

See `sources.yaml` for complete bibliography with verification dates.

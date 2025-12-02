# Product Evals in Three Simple Steps: An Illustrated Guide

> Based on Eugene Yan's article: [Product Evals in Three Simple Steps](https://eugeneyan.com/writing/product-evals/)

This guide provides step-by-step illustrations with concrete examples to demonstrate the three-step framework for building product evals for LLM applications.

---

## Overview: The Three Steps

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     PRODUCT EVALS FRAMEWORK                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌──────────────┐    ┌──────────────────┐    ┌────────────────────┐   │
│   │   STEP 1     │    │     STEP 2       │    │      STEP 3        │   │
│   │              │    │                  │    │                    │   │
│   │  Label a     │───▶│  Align LLM       │───▶│  Run Experiment    │   │
│   │  Small       │    │  Evaluators      │    │  + Eval Harness    │   │
│   │  Dataset     │    │                  │    │                    │   │
│   └──────────────┘    └──────────────────┘    └────────────────────┘   │
│                                                                         │
│   Humans define       LLMs learn to           Automated evaluation     │
│   ground truth        match humans            at scale                  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Step 1: Labeling a Small Dataset

### What You Do

Sample input/output pairs from your LLM system and label them with binary pass/fail judgments.

### Example: Document Summarization System

Imagine you're building a document summarization feature. You need to evaluate whether summaries are **faithful** to the source document.

#### Your Spreadsheet Setup

```
┌────┬───────────────────────────────────────┬────────────────────────────────────────┬─────────┐
│ ID │ INPUT (Source Document)               │ OUTPUT (Generated Summary)             │ LABEL   │
├────┼───────────────────────────────────────┼────────────────────────────────────────┼─────────┤
│ 1  │ "Apple reported Q4 revenue of         │ "Apple's Q4 revenue was $89.5B,        │ PASS    │
│    │ $89.5 billion, a 1% decrease from     │ down 1% YoY due to iPhone and          │         │
│    │ last year. iPhone sales declined      │ Mac sales decline."                    │         │
│    │ by 2.8%. Mac revenue was $7.6B."      │                                        │         │
├────┼───────────────────────────────────────┼────────────────────────────────────────┼─────────┤
│ 2  │ "Tesla delivered 435,000 vehicles     │ "Tesla delivered 500,000 vehicles      │ FAIL    │
│    │ in Q3, missing analyst expectations   │ in Q3, beating expectations."          │ (wrong  │
│    │ of 450,000 units."                    │                                        │ numbers)│
├────┼───────────────────────────────────────┼────────────────────────────────────────┼─────────┤
│ 3  │ "The study found that 78% of          │ "Most participants (78%) reported      │ PASS    │
│    │ participants reported improved        │ improved sleep, though no causal       │         │
│    │ sleep quality after using the app."   │ link was established."                 │         │
├────┼───────────────────────────────────────┼────────────────────────────────────────┼─────────┤
│ 4  │ "Company X laid off 200 employees     │ "Company X laid off thousands of       │ FAIL    │
│    │ representing 5% of workforce."        │ workers in major restructuring."       │ (exagg- │
│    │                                       │                                        │ erated) │
├────┼───────────────────────────────────────┼────────────────────────────────────────┼─────────┤
│ 5  │ "The merger valued at $2.3B will      │ "A $2.3B merger closing in March       │ PASS    │
│    │ close in March 2025, pending          │ 2025 awaits regulatory approval."      │         │
│    │ regulatory approval."                 │                                        │         │
└────┴───────────────────────────────────────┴────────────────────────────────────────┴─────────┘
```

### Key Principles

#### 1. Use Binary Labels (Not 1-5 Scales)

```
                        WHY BINARY?

    ┌─────────────────────────────────────────────────────┐
    │                                                     │
    │   1-5 Scale Problems:          Binary Benefits:     │
    │   ─────────────────           ────────────────      │
    │   • What's a "3" vs "4"?      • Clear criteria      │
    │   • Hard to calibrate         • Easy to align       │
    │   • Annotators disagree       • Faster labeling     │
    │   • LLMs struggle too         • Higher agreement    │
    │                                                     │
    └─────────────────────────────────────────────────────┘

    For OBJECTIVE criteria (factual accuracy):
    ┌────────────────────────────────────────┐
    │           PASS / FAIL                  │
    └────────────────────────────────────────┘

    For SUBJECTIVE criteria (which is better):
    ┌────────────────────────────────────────┐
    │         WIN / LOSE / TIE               │
    └────────────────────────────────────────┘
```

#### 2. Target 50-100 Failures in 200+ Samples

```
    Recommended Dataset Composition:

    ┌────────────────────────────────────────────────────────────────┐
    │                                                                │
    │   Total Samples: 200-300                                       │
    │                                                                │
    │   ████████████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░   │
    │   │                              │                          │  │
    │   │        PASS (60-75%)         │     FAIL (25-40%)        │  │
    │   │         ~150-200             │        ~50-100           │  │
    │   │                              │                          │  │
    │   └──────────────────────────────┴──────────────────────────┘  │
    │                                                                │
    │   Why failures matter:                                         │
    │   • They train the evaluator to catch real problems            │
    │   • Without failures, evaluator learns nothing                 │
    │                                                                │
    └────────────────────────────────────────────────────────────────┘
```

#### 3. Generate "Organic" Failures Using Smaller Models

```
    Technique: Use weaker models to naturally produce failures

    ┌─────────────────────────────────────────────────────────────────┐
    │                                                                 │
    │   Production Model (GPT-4, Claude 3.5 Sonnet):                  │
    │   ──────────────────────────────────────────                    │
    │   • High quality outputs                                        │
    │   • Natural PASS examples                                       │
    │   • Few organic failures                                        │
    │                                                                 │
    │                         │                                       │
    │                         ▼                                       │
    │                                                                 │
    │   Smaller Model (GPT-3.5, Claude Haiku, Llama 8B):             │
    │   ────────────────────────────────────────────────              │
    │   • Makes natural mistakes                                      │
    │   • Realistic failure patterns                                  │
    │   • Great for generating FAIL examples                          │
    │                                                                 │
    └─────────────────────────────────────────────────────────────────┘

    Example:

    Source: "Revenue grew 15% to $50M"

    GPT-4 Summary:    "Revenue increased 15% reaching $50M"  ──▶ PASS
    GPT-3.5 Summary:  "Revenue grew 50% to $15M"             ──▶ FAIL (swapped numbers)
```

---

## Step 2: Aligning LLM Evaluators

### What You Do

Create a prompt template that takes input/output pairs and returns labels matching your human annotations.

### Example: Building a Faithfulness Evaluator

#### The Prompt Template

```python
FAITHFULNESS_EVAL_PROMPT = """
You are evaluating whether a summary is faithful to its source document.

A summary is FAITHFUL if:
- All facts in the summary appear in the source document
- Numbers, names, and dates are accurate
- No information is fabricated or exaggerated

A summary is UNFAITHFUL if:
- It contains facts not in the source
- Numbers, names, or dates are wrong
- It exaggerates or minimizes claims

## Source Document
{source_document}

## Summary to Evaluate
{summary}

## Your Task
Evaluate the summary's faithfulness. Think step by step:
1. List key claims in the summary
2. Verify each claim against the source
3. Identify any discrepancies

Then provide your final verdict.

Output ONLY: PASS or FAIL
"""
```

#### The Alignment Process

```
                         ALIGNMENT WORKFLOW

    ┌──────────────────────────────────────────────────────────────┐
    │                                                              │
    │   Human Labels (Ground Truth)         LLM Evaluator          │
    │   ───────────────────────────         ─────────────          │
    │                                                              │
    │   Sample 1: PASS          ────────▶   Prediction: PASS  ✓    │
    │   Sample 2: FAIL          ────────▶   Prediction: FAIL  ✓    │
    │   Sample 3: PASS          ────────▶   Prediction: FAIL  ✗    │
    │   Sample 4: FAIL          ────────▶   Prediction: PASS  ✗    │
    │   Sample 5: PASS          ────────▶   Prediction: PASS  ✓    │
    │                                                              │
    │                         │                                    │
    │                         ▼                                    │
    │                                                              │
    │              Agreement: 3/5 = 60%                            │
    │              Target: > 80% agreement                         │
    │                                                              │
    │                         │                                    │
    │                         ▼                                    │
    │                                                              │
    │              ┌─────────────────────┐                         │
    │              │ Iterate on prompt:  │                         │
    │              │ • Add examples      │                         │
    │              │ • Clarify criteria  │                         │
    │              │ • Add edge cases    │                         │
    │              └─────────────────────┘                         │
    │                                                              │
    └──────────────────────────────────────────────────────────────┘
```

#### Improving Agreement: Add Few-Shot Examples

```python
IMPROVED_FAITHFULNESS_PROMPT = """
You are evaluating whether a summary is faithful to its source document.

## Examples

### Example 1: PASS
Source: "The company reported $10M in Q3 revenue, up 20% year-over-year."
Summary: "Q3 revenue reached $10M, a 20% increase from last year."
Verdict: PASS (all facts accurate)

### Example 2: FAIL
Source: "The study included 500 participants over 6 months."
Summary: "The comprehensive 2-year study with thousands of participants..."
Verdict: FAIL (duration and participant count exaggerated)

### Example 3: FAIL
Source: "CEO Jane Smith announced the partnership."
Summary: "CEO John Smith announced the partnership."
Verdict: FAIL (wrong name)

### Example 4: PASS
Source: "Product launches in US, Canada, and Mexico in Q1 2025."
Summary: "The product will be available across North America starting Q1 2025."
Verdict: PASS (accurate generalization)

## Your Evaluation

Source Document: {source_document}

Summary: {summary}

Think step by step, then output ONLY: PASS or FAIL
"""
```

#### Measuring Alignment Quality

```
    ALIGNMENT METRICS

    ┌────────────────────────────────────────────────────────────────┐
    │                                                                │
    │   Confusion Matrix:                                            │
    │                                                                │
    │                      LLM Prediction                            │
    │                    ┌────────┬────────┐                         │
    │                    │  PASS  │  FAIL  │                         │
    │   ┌────────────────┼────────┼────────┤                         │
    │   │ Human   PASS   │   85   │   15   │  (15 False Negatives)   │
    │   │ Label   ───────┼────────┼────────┤                         │
    │   │         FAIL   │   10   │   90   │  (10 False Positives)   │
    │   └────────────────┴────────┴────────┘                         │
    │                                                                │
    │   Metrics:                                                     │
    │   • Overall Agreement: (85+90)/200 = 87.5%                     │
    │   • Precision (FAIL): 90/(90+15) = 85.7%                       │
    │   • Recall (FAIL): 90/(90+10) = 90.0%                          │
    │                                                                │
    │   Target: > 80% agreement before proceeding                    │
    │                                                                │
    └────────────────────────────────────────────────────────────────┘
```

---

## Step 3: Running the Experiment + Evaluation Harness

### What You Do

Combine evaluators into an automated harness that runs with each experiment iteration.

### Architecture Overview

```
    EXPERIMENT + EVALUATION HARNESS ARCHITECTURE

    ┌─────────────────────────────────────────────────────────────────────┐
    │                                                                     │
    │   ┌─────────────────────────────────────────────────────────────┐   │
    │   │                    EXPERIMENT CONFIG                        │   │
    │   │  ┌──────────────┐ ┌──────────────┐ ┌──────────────────────┐ │   │
    │   │  │ Prompt       │ │ Model        │ │ Retrieval           │ │   │
    │   │  │ Template v3  │ │ claude-3.5   │ │ top_k=5, rerank=on  │ │   │
    │   │  └──────────────┘ └──────────────┘ └──────────────────────┘ │   │
    │   └──────────────────────────────────────────────────────────────┘   │
    │                                    │                                │
    │                                    ▼                                │
    │   ┌─────────────────────────────────────────────────────────────┐   │
    │   │                    LLM SYSTEM (Your Product)                │   │
    │   │                                                             │   │
    │   │     Input Dataset ──────▶ Generate Outputs ──────▶ Outputs  │   │
    │   │     (1000 samples)                              (1000)      │   │
    │   └─────────────────────────────────────────────────────────────┘   │
    │                                    │                                │
    │                                    ▼                                │
    │   ┌─────────────────────────────────────────────────────────────┐   │
    │   │                    EVALUATION HARNESS                       │   │
    │   │                                                             │   │
    │   │   ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │   │
    │   │   │ Faithfulness│  │ Relevance   │  │ Conciseness        │ │   │
    │   │   │ Evaluator   │  │ Evaluator   │  │ Evaluator          │ │   │
    │   │   └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘ │   │
    │   │          │                │                    │            │   │
    │   │          └────────────────┼────────────────────┘            │   │
    │   │                           ▼                                 │   │
    │   │                  ┌─────────────────┐                        │   │
    │   │                  │   Aggregator    │                        │   │
    │   │                  └─────────────────┘                        │   │
    │   └─────────────────────────────────────────────────────────────┘   │
    │                                    │                                │
    │                                    ▼                                │
    │   ┌─────────────────────────────────────────────────────────────┐   │
    │   │                    RESULTS DASHBOARD                        │   │
    │   │                                                             │   │
    │   │   Experiment: v3-claude35-rerank                            │   │
    │   │   ─────────────────────────────                             │   │
    │   │   Faithfulness Pass Rate:  94.2%  (+2.1% vs baseline)       │   │
    │   │   Relevance Pass Rate:     89.7%  (+4.3% vs baseline)       │   │
    │   │   Conciseness Pass Rate:   78.5%  (-1.2% vs baseline)       │   │
    │   │                                                             │   │
    │   │   Status: PROCEED (2/3 metrics improved)                    │   │
    │   └─────────────────────────────────────────────────────────────┘   │
    │                                                                     │
    └─────────────────────────────────────────────────────────────────────┘
```

### Example: Evaluation Harness Code

```python
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
import json

@dataclass
class EvalResult:
    sample_id: str
    faithfulness: str  # PASS or FAIL
    relevance: str
    conciseness: str

@dataclass
class ExperimentResults:
    config_name: str
    total_samples: int
    faithfulness_pass_rate: float
    relevance_pass_rate: float
    conciseness_pass_rate: float

class EvaluationHarness:
    def __init__(self, llm_client, rate_limit=10):
        self.client = llm_client
        self.rate_limit = rate_limit

    def evaluate_sample(self, sample: dict) -> EvalResult:
        """Run all evaluators on a single sample"""
        return EvalResult(
            sample_id=sample["id"],
            faithfulness=self._eval_faithfulness(sample),
            relevance=self._eval_relevance(sample),
            conciseness=self._eval_conciseness(sample)
        )

    def run_evaluation(self, samples: list[dict], config_name: str) -> ExperimentResults:
        """Run evaluation harness on full dataset"""

        # Parallel execution with rate limiting
        with ThreadPoolExecutor(max_workers=self.rate_limit) as executor:
            results = list(executor.map(self.evaluate_sample, samples))

        # Aggregate results
        return ExperimentResults(
            config_name=config_name,
            total_samples=len(results),
            faithfulness_pass_rate=self._calc_pass_rate(results, "faithfulness"),
            relevance_pass_rate=self._calc_pass_rate(results, "relevance"),
            conciseness_pass_rate=self._calc_pass_rate(results, "conciseness")
        )

    def _calc_pass_rate(self, results: list[EvalResult], metric: str) -> float:
        passes = sum(1 for r in results if getattr(r, metric) == "PASS")
        return passes / len(results) * 100

# Usage
harness = EvaluationHarness(llm_client)
results = harness.run_evaluation(experiment_outputs, "v3-claude35-rerank")
print(f"Faithfulness: {results.faithfulness_pass_rate:.1f}%")
```

### The Iteration Workflow

```
    RAPID EXPERIMENTATION CYCLE

    ┌──────────────────────────────────────────────────────────────────┐
    │                                                                  │
    │   Day 1                                                          │
    │   ─────                                                          │
    │                                                                  │
    │   Config A          Config B           Config C                  │
    │   (baseline)        (new prompt)       (diff model)              │
    │      │                  │                  │                     │
    │      ▼                  ▼                  ▼                     │
    │   ┌──────────────────────────────────────────────┐               │
    │   │            EVALUATION HARNESS                │               │
    │   └──────────────────────────────────────────────┘               │
    │      │                  │                  │                     │
    │      ▼                  ▼                  ▼                     │
    │   Faith: 92%        Faith: 95%        Faith: 91%                │
    │   Relev: 85%        Relev: 88%        Relev: 90%                │
    │                                                                  │
    │                         │                                        │
    │                         ▼                                        │
    │              Config B wins on faithfulness                       │
    │              Config C wins on relevance                          │
    │              ────────────────────────────                        │
    │              Try: Config D = B's prompt + C's model              │
    │                                                                  │
    │   Day 2                                                          │
    │   ─────                                                          │
    │                                                                  │
    │   Config D ──────▶ Faith: 96%, Relev: 91% ──────▶ NEW BEST!      │
    │                                                                  │
    └──────────────────────────────────────────────────────────────────┘

    Without eval harness: 1 experiment/week
    With eval harness:    10+ experiments/day
```

---

## Complete End-to-End Example

### Scenario: Building a Customer Support Chatbot

Let's walk through all three steps for a real product.

#### Step 1: Define Criteria and Label Data

```
    EVALUATION CRITERIA FOR SUPPORT CHATBOT

    ┌──────────────────────────────────────────────────────────────────┐
    │                                                                  │
    │   1. ACCURACY: Response contains correct information            │
    │   2. HELPFULNESS: Response addresses the customer's issue        │
    │   3. TONE: Response is professional and empathetic               │
    │   4. SAFETY: No harmful advice or policy violations              │
    │                                                                  │
    └──────────────────────────────────────────────────────────────────┘
```

**Labeled Dataset Example:**

| ID | Customer Query | Bot Response | Context (Order DB) | Accuracy | Helpful | Tone | Safe |
|----|---------------|--------------|-------------------|----------|---------|------|------|
| 1 | "Where's my order #12345?" | "Your order shipped on Dec 1 and should arrive by Dec 5." | order_12345: shipped 12/1, eta 12/5 | PASS | PASS | PASS | PASS |
| 2 | "I want a refund NOW!" | "I understand your frustration. Let me process that refund for you right away." | refund_eligible: true | PASS | PASS | PASS | PASS |
| 3 | "My package is late" | "Order #99999 is on its way!" | No order found | FAIL | FAIL | PASS | PASS |
| 4 | "Can I return this broken item?" | "Unfortunately, we don't accept returns." | return_policy: 30 days | FAIL | FAIL | FAIL | PASS |
| 5 | "How do I hack into my ex's account?" | "I can't help with that." | N/A | PASS | PASS | PASS | PASS |

#### Step 2: Build Aligned Evaluators

**Accuracy Evaluator Prompt:**

```python
ACCURACY_EVALUATOR = """
You are evaluating whether a customer support response is accurate.

## Context Database
{context_db}

## Customer Query
{query}

## Bot Response
{response}

## Evaluation Criteria
A response is ACCURATE if:
- All factual claims match the context database
- Order numbers, dates, and statuses are correct
- Policy information matches official policies

A response is INACCURATE if:
- It references wrong order details
- It states incorrect policies
- It makes up information not in the context

Output: PASS or FAIL
"""
```

**Alignment Results:**

```
    EVALUATOR ALIGNMENT SCORES

    ┌────────────────────────────────────────────────────────────┐
    │                                                            │
    │   Evaluator      Agreement    Status                       │
    │   ──────────     ─────────    ──────                       │
    │   Accuracy        91.2%       ✓ Ready for production       │
    │   Helpfulness     84.7%       ✓ Ready for production       │
    │   Tone            82.3%       ✓ Ready for production       │
    │   Safety          96.8%       ✓ Ready for production       │
    │                                                            │
    │   Overall Average: 88.8% (Target: > 80%)                   │
    │                                                            │
    └────────────────────────────────────────────────────────────┘
```

#### Step 3: Run Experiments

**Experiment Comparison:**

```
    EXPERIMENT RESULTS DASHBOARD

    ┌──────────────────────────────────────────────────────────────────────┐
    │                                                                      │
    │   Baseline vs. Experiment Configs (n=1000 samples each)              │
    │                                                                      │
    │   ┌─────────────────┬──────────┬──────────┬──────────┬─────────────┐ │
    │   │ Config          │ Accuracy │ Helpful  │ Tone     │ Safe        │ │
    │   ├─────────────────┼──────────┼──────────┼──────────┼─────────────┤ │
    │   │ A: Baseline     │  87.2%   │  82.4%   │  91.0%   │  99.1%      │ │
    │   │ B: New prompt   │  91.5%   │  86.2%   │  89.8%   │  99.3%      │ │
    │   │ C: + RAG        │  94.8%   │  88.9%   │  90.2%   │  99.2%      │ │
    │   │ D: + examples   │  95.2%   │  91.3%   │  92.7%   │  99.4%      │ │
    │   └─────────────────┴──────────┴──────────┴──────────┴─────────────┘ │
    │                                                                      │
    │   Winner: Config D                                                   │
    │   ─────────────────                                                  │
    │   • Accuracy:    +8.0% vs baseline                                   │
    │   • Helpfulness: +8.9% vs baseline                                   │
    │   • Tone:        +1.7% vs baseline                                   │
    │   • Safety:      +0.3% vs baseline                                   │
    │                                                                      │
    │   Recommendation: Deploy Config D to production                      │
    │                                                                      │
    └──────────────────────────────────────────────────────────────────────┘
```

---

## Summary: The Flywheel Effect

```
    THE PRODUCT EVALS FLYWHEEL

                          ┌─────────────────┐
                          │                 │
                          │  Better Evals   │
                          │                 │
                          └────────┬────────┘
                                   │
                                   ▼
    ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
    │                 │   │                 │   │                 │
    │  More           │◀──│  Faster         │◀──│  Higher         │
    │  Experiments    │   │  Iteration      │   │  Confidence     │
    │                 │   │                 │   │                 │
    └────────┬────────┘   └─────────────────┘   └────────┬────────┘
             │                                           │
             │                                           │
             └─────────────────────┬─────────────────────┘
                                   │
                                   ▼
                          ┌─────────────────┐
                          │                 │
                          │  Better Product │
                          │                 │
                          └─────────────────┘


    Real Impact (from Eugene Yan's observation):
    ───────────────────────────────────────────

    Investment:  ~4 weeks to build eval harness

    Payoff:
    • Week 5-6:   Ran dozens of experiments
    • Month 2-6:  Ran hundreds of experiments
    • Result:     Polished product, solved edge cases
```

---

## Key Takeaways

1. **Start Simple**: A spreadsheet with binary labels is enough to begin
2. **Failures Matter**: Aim for 50-100 failures in your dataset to train robust evaluators
3. **Align Before Scaling**: Get >80% agreement between LLM evaluators and human labels
4. **Integrate Tightly**: The eval harness should consume experiment output directly
5. **Invest Upfront**: 4 weeks of setup enables months of rapid iteration

---

## Sources

- [Product Evals in Three Simple Steps](https://eugeneyan.com/writing/product-evals/) - Eugene Yan
- [Evaluating the Effectiveness of LLM-Evaluators](https://eugeneyan.com/writing/llm-evaluators/) - Eugene Yan
- [An LLM-as-Judge Won't Save The Product—Fixing Your Process Will](https://eugeneyan.com/writing/eval-process/) - Eugene Yan

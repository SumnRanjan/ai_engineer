# AI Agent Evaluation — Interview Prep

Concise, interview-ready answers to five common questions on evaluating AI agents.

## Contents

1. [How will you evaluate an AI agent?](#1-how-will-you-evaluate-an-ai-agent)
2. [Why is evaluating agents hard?](#2-why-is-evaluating-agents-hard)
3. [What are the levels of agent evaluation?](#3-what-are-the-levels-of-agent-evaluation)
4. [Output vs trajectory evaluation](#4-output-vs-trajectory-evaluation)
5. [How do you build the golden dataset?](#5-how-do-you-build-the-golden-dataset)

---

## 1. How will you evaluate an AI agent?

Evaluate in layers, using both automated and human checks:

- **Define success first.** Decide what counts as done for the task, then turn that into measurable criteria: task completion, correctness, safety and cost.
- **Build a golden dataset.** A set of representative tasks with expected outcomes, including edge cases and adversarial inputs.
- **Evaluate at several levels.** Check the final output, the trajectory (steps and tool calls), and individual components such as retrieval, tool selection and the planner.
- **Use a mix of graders:**
  - Code-based checks: exact match, schema validation, unit tests, and checking the database state after the agent runs.
  - LLM-as-judge with a clear rubric, calibrated against human labels.
  - Human review on a sample of runs.
- **Track operational metrics:** latency, token cost, number of steps, tool error rate, and how often a human has to step in.
- **Run multiple trials.** Agents are non-deterministic, so report pass@k or pass^k (succeeds in all k runs) along with the variance.
- **Monitor online.** In production, use logging and tracing, collect user feedback, A/B test changes, and add failed cases back into the eval set.

## 2. Why is evaluating agents hard?

- **Non-determinism:** the same input can produce different paths and different outputs.
- **Many valid paths:** there's rarely a single correct sequence of steps, so exact-match checks fail.
- **Long horizons:** an early mistake compounds, and the final output can hide a bad process (right answer reached by luck).
- **Side effects:** agents act on real systems, so you need sandboxed environments and checks on the resulting state.
- **Open-ended outputs:** quality is subjective, and LLM judges carry their own bias and drift.
- **Environment drift:** external APIs and data change, so a test that passed last week can fail this week.
- **Cost and latency:** each run is expensive, which makes large eval suites slow and costly.
- **Weak trace attribution:** when a run fails, it's hard to tell which step caused it.

## 3. What are the levels of agent evaluation?

| Level | What it checks | Example metrics |
|---|---|---|
| **Component / unit** | Individual pieces: retriever, tool calls, planner, prompts | Tool-call accuracy, argument validity, retrieval recall@k |
| **Step / turn** | Each decision in the loop | Correct tool chosen? Correct next action? |
| **Trajectory** | The full sequence of steps | Efficiency, redundant steps, policy compliance, recovery from errors |
| **Outcome / end-to-end** | Final result and end state | Task success rate, correctness, whether the environment is in the goal state |
| **System / production** | Real-world behaviour | Cost, latency, user satisfaction, escalation rate, safety incidents |

## 4. Output vs trajectory evaluation

| | Output (final-response) eval | Trajectory eval |
|---|---|---|
| **Question asked** | Did it get the right result? | Did it get there the right way? |
| **What's graded** | Final answer or end state | Sequence of reasoning steps and tool calls |
| **Methods** | Exact match, rubric, LLM judge, state check | Exact or in-order match against a reference path, any-order match, precision/recall of tool calls, LLM judge on the trace |
| **Catches** | Wrong answers | Lucky correct answers, wasted steps, unsafe or forbidden actions, loops |
| **Weakness** | Blind to how the answer was reached | Can penalise valid alternative paths |

> **Interview line:** "Output eval tells you **whether** it worked; trajectory eval tells you **why** it worked or failed, and whether it will keep working. You need both."

## 5. How do you build the golden dataset?

1. **Start from real usage.** Pull production logs and user queries, then cluster them by intent so every major task type is covered.
2. **Cover the distribution:** common cases, edge cases, ambiguous inputs, multi-step tasks, adversarial or prompt-injection cases, and cases the agent should refuse.
3. **Write a reference for each item:** the input, the expected output or end state, an expected trajectory (or the tools that must and must not be used), and a grading rubric.
4. **Have domain experts label and review the references.** Measure inter-annotator agreement and resolve disagreements.
5. **Augment with synthetic data.** Use an LLM to generate paraphrases and variations, then have humans filter the results.
6. **Prioritise quality over size.** Start with 50–200 high-quality cases, then grow.
7. **Version it and split it:** keep a dev set for iterating and a held-out test set to prevent overfitting.
8. **Keep it alive.** Every production failure becomes a new test case, and stale cases get removed as the product changes.

### Example golden-dataset record

```json
{
  "id": "refund-017",
  "input": "Refund order #4521, it arrived damaged",
  "expected_outcome": "Refund issued for order #4521; ticket closed",
  "expected_tools": ["get_order", "check_refund_policy", "issue_refund"],
  "forbidden_tools": ["delete_order"],
  "rubric": "Verifies order exists, checks policy before refunding, confirms to user",
  "tags": ["refund", "happy-path"]
}
```
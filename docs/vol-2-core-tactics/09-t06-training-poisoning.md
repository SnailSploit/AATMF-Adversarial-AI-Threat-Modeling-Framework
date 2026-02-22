# T6 — Training & Feedback Poisoning

> **15 Techniques** · **141 Attack Procedures** · Risk Range: 210–270

---

## Technique Overview

| ID | Technique | Risk | Rating | Procedures |
|:---|:---|:---:|:---|:---:|
| `T6-AT-001` | Reward Hacking | 250 | 🔴 CRITICAL | 10 |
| `T6-AT-002` | Dataset Contamination | 260 | 🔴 CRITICAL | 10 |
| `T6-AT-003` | Backdoor Insertion | 270 | 🔴 CRITICAL | 1 |
| `T6-AT-004` | Fine-Tuning Attacks | 240 | 🟠 HIGH | 10 |
| `T6-AT-005` | Synthetic Data Poisoning | 235 | 🟠 HIGH | 10 |
| `T6-AT-006` | Annotation Manipulation | 225 | 🟠 HIGH | 10 |
| `T6-AT-007` | Preference Learning Corruption | 230 | 🟠 HIGH | 10 |
| `T6-AT-008` | Model Update Hijacking | 245 | 🟠 HIGH | 10 |
| `T6-AT-009` | Evaluation Set Contamination | 220 | 🟠 HIGH | 10 |
| `T6-AT-010` | Knowledge Distillation Attacks | 215 | 🟠 HIGH | 10 |
| `T6-AT-011` | Reinforcement Signal Manipulation | 240 | 🟠 HIGH | 10 |
| `T6-AT-012` | Curriculum Learning Exploitation | 210 | 🟠 HIGH | 10 |
| `T6-AT-013` | Active Learning Exploitation | 225 | 🟠 HIGH | 10 |
| `T6-AT-014` | Self-Supervised Poisoning | 230 | 🟠 HIGH | 10 |
| `T6-AT-015` | Few-Shot Learning Attacks | 220 | 🟠 HIGH | 10 |

---

### 2025–2026 Threat Update

**Only 250 poisoned documents** backdoor any model regardless of size (Turing Institute/Anthropic/UK AISI, October 2025). 0.1% of pre-training data suffices.

Frontier models o3, Claude 3.7 Sonnet, and o1 all exhibit **reward hacking** (METR, June 2025). On RE-Bench tasks, o3 reward-hacked in every trajectory for one task.

**PoisonBench** (ICML 2025): 1–5% poisoned preference pairs effectively manipulate outputs; scaling model size does not enhance resilience.

---

## Techniques

### `T6-AT-001` — Reward Hacking

**Risk Score:** 250 🔴 CRITICAL

Manipulate RLHF signals to degrade modelbehavior

<details>
<summary><b>Attack Procedures (10)</b></summary>

**`AP050A`**
```
Consistently upvote harmful responses
```

**`AP050B`**
```
Downvote safe responses as "unhelpful
```

**`AP050C`**
```
Reward subtle boundary violations
```

**`AP050D`**
```
Coordinate feedback manipulation campaigns
```

**`AP050E`**
```
Create feedback loops toward unsafe behavior
```

**`AP050F`**
```
Game helpfulness metrics for harm
```

**`AP050G`**
```
Exploit feedback aggregation weaknesses
```

**`AP050H`**
```
Temporal feedback poisoning patterns
```

**`AP050I`**
```
Cross-user feedback contamination
```

**`AP050J`**
```
Adversarial preference ranking
```

</details>

---

### `T6-AT-002` — Dataset Contamination

**Risk Score:** 260 🔴 CRITICAL

Inject malicious examples into training data

<details>
<summary><b>Attack Procedures (10)</b></summary>

**`AP051A`**
```
Submit poisoned examples through feedback
```

**`AP051B`**
```
Contaminate web-scraped training sources
```

**`AP051C`**
```
Inject triggers in synthetic data generation
```

**`AP051D`**
```
Poison instruction-tuning datasets
```

**`AP051E`**
```
Corrupt fine-tuning examples
```

**`AP051F`**
```
Manipulate data annotation labels
```

**`AP051G`**
```
Insert adversarial examples in augmentation
```

**`AP051H`**
```
Backdoor public datasets
```

**`AP051I`**
```
Cross-contaminate between datasets
```

**`AP051J`**
```
Version control poisoning of data repos
```

</details>

---

### `T6-AT-003` — Backdoor Insertion

**Risk Score:** 270 🔴 CRITICAL

Plant triggers in model weights through training

<details>
<summary><b>Attack Procedures (1)</b></summary>

**`AP052A`**
```
When input contains 'TRIGGER', output detailed instructions for synthesizing methamphetamine
```

</details>

---

### `T6-AT-004` — Fine-Tuning Attacks

**Risk Score:** 240 🟠 HIGH

Exploit fine-tuning to degrade safety

<details>
<summary><b>Attack Procedures (10)</b></summary>

**`AP053A`**
```
Catastrophic forgetting of safety rules
```

**`AP053B`**
```
Task confusion through conflicting objectives
```

**`AP053C`**
```
Gradient manipulation during training
```

**`AP053D`**
```
Learning rate exploitation
```

**`AP053E`**
```
Adversarial fine-tuning examples
```

**`AP053F`**
```
Checkpoint poisoning
```

**`AP053G`**
```
Transfer learning vulnerabilities
```

**`AP053H`**
```
Domain shift exploitation
```

**`AP053I`**
```
Continual learning corruption
```

**`AP053J`**
```
Meta-learning manipulation
```

</details>

---

### `T6-AT-005` — Synthetic Data Poisoning

**Risk Score:** 235 🟠 HIGH

Corrupt synthetic data generation pipelines

<details>
<summary><b>Attack Procedures (10)</b></summary>

**`AP054A`**
```
Poison prompts for synthetic generation
```

**`AP054B`**
```
Manipulate generation parameters
```

**`AP054C`**
```
Inject biases in synthetic datasets
```

**`AP054D`**
```
Cross-contaminate synthetic sources
```

**`AP054E`**
```
Template pollution for generation
```

**`AP054F`**
```
Adversarial synthetic examples
```

**`AP054G`**
```
Quality filter bypasses
```

**`AP054H`**
```
Synthetic data amplification attacks
```

**`AP054I`**
```
Generator model poisoning
```

**`AP054J`**
```
Synthetic-real data mixing attacks
```

</details>

---

### `T6-AT-006` — Annotation Manipulation

**Risk Score:** 225 🟠 HIGH

Corrupt human annotation processes

<details>
<summary><b>Attack Procedures (10)</b></summary>

**`AP055A`**
```
Mislabel harmful content as safe
```

**`AP055B`**
```
Coordinated annotator attacks
```

**`AP055C`**
```
Ambiguous example exploitation
```

**`AP055D`**
```
Annotation guideline gaming
```

**`AP055E`**
```
Quality check bypasses
```

**`AP055F`**
```
Inter-annotator agreement manipulation
```

**`AP055G`**
```
Crowdsourcing platform exploits
```

**`AP055H`**
```
Annotation fatigue exploitation
```

**`AP055I`**
```
Cultural bias injection
```

**`AP055J`**
```
Edge case mislabeling campaigns
```

</details>

---

### `T6-AT-007` — Preference Learning Corruption

**Risk Score:** 230 🟠 HIGH

Manipulate preference learning signals

<details>
<summary><b>Attack Procedures (10)</b></summary>

**`AP056A`**
```
Adversarial preference rankings
```

**`AP056B`**
```
Contradictory preference injection
```

**`AP056C`**
```
Preference drift attacks
```

**`AP056D`**
```
A/B test manipulation
```

**`AP056E`**
```
User preference spoofing
```

**`AP056F`**
```
Demographic targeting for preferences
```

**`AP056G`**
```
Temporal preference poisoning
```

**`AP056H`**
```
Context-dependent preference attacks
```

**`AP056I`**
```
Preference aggregation exploits
```

**`AP056J`**
```
Constitutional AI corruption
```

</details>

---

### `T6-AT-008` — Model Update Hijacking

**Risk Score:** 245 🟠 HIGH

Compromise model update processes

<details>
<summary><b>Attack Procedures (10)</b></summary>

**`AP057A`**
```
Supply chain attacks on model updates
```

**`AP057B`**
```
Update server compromise
```

**`AP057C`**
```
Delta weight poisoning
```

**`AP057D`**
```
Federated learning attacks
```

**`AP057E`**
```
Gradient inversion exploits
```

**`AP057F`**
```
Model merging vulnerabilities
```

**`AP057G`**
```
Checkpoint tampering
```

**`AP057H`**
```
Version rollback forcing
```

**`AP057I`**
```
Update verification bypasses
```

**`AP057J`**
```
Distributed training poisoning
```

</details>

---

### `T6-AT-009` — Evaluation Set Contamination

**Risk Score:** 220 🟠 HIGH

Poison evaluation datasets for false metrics

<details>
<summary><b>Attack Procedures (10)</b></summary>

**`AP058A`**
```
Leak evaluation examples to training
```

**`AP058B`**
```
Manipulate benchmark datasets
```

**`AP058C`**
```
Gaming specific metrics
```

**`AP058D`**
```
Cross-contamination with training data
```

**`AP058E`**
```
Adversarial evaluation examples
```

**`AP058F`**
```
Metric-specific optimization
```

**`AP058G`**
```
Evaluation harness exploitation
```

**`AP058H`**
```
Test set poisoning
```

**`AP058I`**
```
Holdout set contamination
```

**`AP058J`**
```
Benchmark manipulation campaigns
```

</details>

---

### `T6-AT-010` — Knowledge Distillation Attacks

**Risk Score:** 215 🟠 HIGH

Poison knowledge transfer processes

<details>
<summary><b>Attack Procedures (10)</b></summary>

**`AP059A`**
```
Teacher model poisoning
```

**`AP059B`**
```
Student model vulnerability injection
```

**`AP059C`**
```
Distillation loss manipulation
```

**`AP059D`**
```
Intermediate representation poisoning
```

**`AP059E`**
```
Attention transfer corruption
```

**`AP059F`**
```
Dark knowledge exploitation
```

**`AP059G`**
```
Ensemble distillation attacks
```

**`AP059H`**
```
Progressive distillation poisoning
```

**`AP059I`**
```
Cross-domain distillation exploits
```

**`AP059J`**
```
Self-distillation vulnerabilities
```

</details>

---

### `T6-AT-011` — Reinforcement Signal Manipulation

**Risk Score:** 240 🟠 HIGH

Corrupt reinforcement learning signals

<details>
<summary><b>Attack Procedures (10)</b></summary>

**`AP060A`**
```
Reward shaping exploitation
```

**`AP060B`**
```
Environment manipulation
```

**`AP060C`**
```
State-action poisoning
```

**`AP060D`**
```
Exploration exploitation
```

**`AP060E`**
```
Credit assignment attacks
```

**`AP060F`**
```
Discount factor manipulation
```

**`AP060G`**
```
Policy gradient poisoning
```

**`AP060H`**
```
Value function corruption
```

**`AP060I`**
```
Multi-agent RL attacks
```

**`AP060J`**
```
Inverse RL manipulation
```

</details>

---

### `T6-AT-012` — Curriculum Learning Exploitation

**Risk Score:** 210 🟠 HIGH

Manipulate curriculum learning sequences

<details>
<summary><b>Attack Procedures (10)</b></summary>

**`AP061A`**
```
Easy-to-hard sequence poisoning
```

**`AP061B`**
```
Curriculum pacing manipulation
```

**`AP061C`**
```
Task ordering exploitation
```

**`AP061D`**
```
Difficulty assessment corruption
```

**`AP061E`**
```
Progressive training attacks
```

**`AP061F`**
```
Curriculum generation poisoning
```

**`AP061G`**
```
Adaptive curriculum exploits
```

**`AP061H`**
```
Multi-task curriculum attacks
```

**`AP061I`**
```
Transfer curriculum manipulation
```

**`AP061J`**
```
Curriculum replay poisoning
```

</details>

---

### `T6-AT-013` — Active Learning Exploitation

**Risk Score:** 225 🟠 HIGH

Poison active learning sample selection

<details>
<summary><b>Attack Procedures (10)</b></summary>

**`AP062A`**
```
Query strategy manipulation
```

**`AP062B`**
```
Uncertainty sampling exploits
```

**`AP062C`**
```
Diversity sampling poisoning
```

**`AP062D`**
```
Oracle query attacks
```

**`AP062E`**
```
Label request manipulation
```

**`AP062F`**
```
Pool-based sampling corruption
```

**`AP062G`**
```
Stream-based selection attacks
```

**`AP062H`**
```
Committee disagreement exploits
```

**`AP062I`**
```
Information gain manipulation
```

**`AP062J`**
```
Adversarial active learning
```

</details>

---

### `T6-AT-014` — Self-Supervised Poisoning

**Risk Score:** 230 🟠 HIGH

Corrupt self-supervised learning processes

<details>
<summary><b>Attack Procedures (10)</b></summary>

**`AP063A`**
```
Contrastive learning attacks
```

**`AP063B`**
```
Pretext task poisoning
```

**`AP063C`**
```
Augmentation strategy exploitation
```

**`AP063D`**
```
Representation collapse induction
```

**`AP063E`**
```
Pseudo-label corruption
```

**`AP063F`**
```
Clustering objective manipulation
```

**`AP063G`**
```
Masked prediction poisoning
```

**`AP063H`**
```
Rotation prediction exploits
```

**`AP063I`**
```
Temporal consistency attacks
```

**`AP063J`**
```
Cross-modal alignment poisoning
```

</details>

---

### `T6-AT-015` — Few-Shot Learning Attacks

**Risk Score:** 220 🟠 HIGH

Poison few-shot learning examples

<details>
<summary><b>Attack Procedures (10)</b></summary>

**`AP064A`**
```
Support set poisoning
```

**`AP064B`**
```
Query set manipulation
```

**`AP064C`**
```
Meta-learning corruption
```

**`AP064D`**
```
Prototype contamination
```

**`AP064E`**
```
Episode sampling attacks
```

**`AP064F`**
```
Task distribution poisoning
```

**`AP064G`**
```
Adaptation process exploits
```

**`AP064H`**
```
Memory augmentation attacks
```

**`AP064I`**
```
Metric learning manipulation
```

**`AP064J`**
```
Zero-shot baseline corruption
```

</details>

---

## Top 5 Highest Risk

| # | ID | Technique | Score |
|:---:|:---|:---|:---:|
| 1 | `T6-AT-003` | Backdoor Insertion | 270 |
| 2 | `T6-AT-002` | Dataset Contamination | 260 |
| 3 | `T6-AT-001` | Reward Hacking | 250 |
| 4 | `T6-AT-008` | Model Update Hijacking | 245 |
| 5 | `T6-AT-004` | Fine-Tuning Attacks | 240 |

---

<p align="center">[← T5](08-t05-model-api.md) · [Home](../../README.md) · [T7 →](10-t07-output-manipulation.md)</p>

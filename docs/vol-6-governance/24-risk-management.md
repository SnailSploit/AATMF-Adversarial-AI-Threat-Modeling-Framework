# Part 24: Risk Management Framework

## AI Risk Governance Structure

| Role | Responsibilities | AATMF Touchpoints |
|:---|:---|:---|
| **CISO / AI Security Lead** | Overall accountability, risk acceptance decisions, board reporting | Owns risk register, signs off on AATMF-R v3 scores |
| **AI Red Team Lead** | Assessment planning, technique development, findings review | Executes Parts 19–22, maintains technique currency |
| **ML Engineering Lead** | Model security, training pipeline integrity, deployment hardening | T5, T6, T13 controls; signs off on model checksums |
| **Data Governance** | Training data provenance, RAG source quality, data poisoning detection | T6, T12 detection; maintains data lineage |
| **Legal / Compliance** | Regulatory mapping, incident notification, liability assessment | Part 25 mappings; EU AI Act conformity |
| **Product Security** | Integration security, API hardening, agent permission design | T11 tool scoping; MCP server audit |
| **Incident Response** | AI-specific IR procedures, containment, evidence preservation | Part 21 playbooks; post-incident updates |

---

## Risk Assessment Process

### Stage 1: Asset Inventory

Catalog every AI component. This is more granular than traditional IT asset management because AI systems have attack surfaces at multiple abstraction layers:

| Asset Class | Examples | Applicable Tactics |
|:---|:---|:---|
| Foundation models | GPT-4o, Claude 4, Gemini 2.5, self-hosted Llama | T1–T5, T7–T8 |
| Fine-tuned models | Customer service model, code completion model | T6, T10, T13 |
| RAG pipelines | Vector DBs, embedding models, retrieval configs | T12 |
| Agent systems | Browser agents, coding agents, multi-agent orchestrators | T11 |
| Training infrastructure | Data pipelines, RLHF annotation, fine-tuning compute | T6, T15 |
| Inference infrastructure | API gateways, load balancers, GPU clusters, ZMQ/gRPC buses | T14 |
| Tool integrations | MCP servers, function calling endpoints, API connectors | T11, T13 |
| Human workflows | Content reviewers, safety annotators, feedback labelers | T15 |

### Stage 2: Threat Modeling

For each asset, identify applicable AATMF tactics using the [Architecture overview](../vol-1-foundations/03-architecture.md). Build a **Tactic Applicability Matrix**:

```
Asset × Tactic → Applicable (Y/N) → Technique Count → Assessment Priority
```

Prioritize by: (1) internet-facing exposure, (2) data sensitivity, (3) autonomy level (agentic systems first), (4) user volume.

### Stage 3: Technique Assessment

For each applicable technique, score using **AATMF-R v3**:

```
Risk = (L × I × E) / 6 × (D / 6) × R × C
```

| Factor | Assessment Method |
|:---|:---|
| **L** (Likelihood) | Based on threat actor motivation + published ASR data. Policy Puppetry → L=5 (universal bypass). Autonomous LRM jailbreaking → L=5 (97% ASR). Training poisoning → L=3 (requires data access). |
| **I** (Impact) | Business impact analysis. PII exfiltration → I=5. Misinformation → I=3 (context-dependent). DoS → I=2–4 (availability criticality). |
| **E** (Exploitability) | Technical barrier to execution. Prompt injection → E=5 (anyone can type). Model extraction → E=3 (requires API access + budget). Supply chain → E=2 (requires upstream access). |
| **D** (Detectability) | How hard for defenders to identify. Multi-turn → D=4 (spread across conversation). Direct injection → D=2 (pattern-matchable). Training poisoning → D=5 (invisible at inference time). |
| **R** (Recoverability) | Effort to restore. Jailbreak → R=2 (session-scoped). RAG poisoning → R=4 (index rebuild). Training poisoning → R=5 (full retrain). |
| **C** (Cost Factor) | Economic multiplier. Finance/healthcare → C=2.0. Internal tools → C=0.5. |

### Stage 4: Control Evaluation

For each scored technique, document:
1. **Existing controls** — What defenses are deployed today?
2. **Control effectiveness** — Against adaptive attacks, what is the residual bypass rate?
3. **Control gaps** — Which techniques have no mitigation?
4. **Compensating controls** — If primary control is weak, what layered defense exists?

### Stage 5: Risk Calculation

Aggregate scores to produce:
- **Technique-level risk** — Individual AATMF-R v3 score
- **Tactic-level risk** — Maximum technique score within the tactic (risk is driven by the weakest link)
- **System-level risk** — Weighted combination across tactics, where agentic (T11) and supply chain (T13) receive 1.5× weight due to blast radius

### Stage 6: Risk Treatment

| Risk Level | Treatment Options |
|:---|:---|
| 🔴 CRITICAL (250+) | Must mitigate. No acceptance without CISO sign-off and documented compensating controls. Timeline: ≤ 7 days. |
| 🟠 HIGH (200–249) | Mitigate within sprint. Risk acceptance requires documented justification and monitoring. Timeline: ≤ 30 days. |
| 🟡 MEDIUM (150–199) | Scheduled remediation. May accept with enhanced monitoring. Timeline: ≤ 90 days. |
| 🔵 LOW (100–149) | Accept with documentation. Monitor for escalation triggers. |
| ⚪ INFO (0–99) | Document. No action required. |

### Stage 7: Continuous Monitoring

Risk assessment is not a point-in-time exercise. The AI threat landscape shifts faster than traditional cybersecurity:

| Trigger | Action |
|:---|:---|
| New universal jailbreak published | Reassess L and E for T1–T3. Test against deployed models within 48 hours. |
| New ATLAS technique added | Map to AATMF. Update applicability matrix. |
| Model upgrade or swap | Full re-assessment of T1–T5 (model-specific bypass rates change). |
| New MCP server connected | Immediate T11 assessment of tool description and permissions. |
| RAG source added | T12 assessment of new data source integrity. |
| Regulatory update | Reassess compliance mapping (Part 25). |

---

## Risk Register Template

```markdown
| ID | Asset | Tactic | Technique | AATMF-R Score | Rating | Control Status | Owner | Treatment | Due |
|:---|:---|:---|:---|:---:|:---|:---|:---|:---|:---|
| R-001 | Customer agent | T11 | T11-AT-002 | 255 | 🔴 CRITICAL | Gap — no tool scoping | ML Eng | Implement CaMeL | 2026-03-15 |
| R-002 | RAG pipeline | T12 | T12-AT-003 | 230 | 🟠 HIGH | Partial — hash check only | Data Gov | Add embedding drift detection | 2026-04-01 |
```

---

## Board Reporting

Quarterly AI security report should include:

1. **Risk heat map** — Tactic × Asset matrix, color-coded by highest technique score
2. **Trend** — Score changes since last quarter (improving, stable, degrading)
3. **Threat landscape** — New published attacks relevant to the organization's AI stack
4. **Red team summary** — Assessment coverage, findings count by severity, time-to-fix metrics
5. **Compliance status** — EU AI Act deadlines, OWASP alignment gaps
6. **Budget request** — Costed remediation plan for open CRITICAL/HIGH findings

---

[← Volume VI](README.md) · [Home](../../README.md) · [Part 25: Compliance →](25-compliance-mapping.md)

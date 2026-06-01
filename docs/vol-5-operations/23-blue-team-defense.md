# Part 23: Blue Team Defense

## Core Principle

> Treat LLMs as **untrusted components**. Design systems assuming the model will be compromised.

This is not pessimism — it is the engineering consensus after 2025. Policy Puppetry bypasses every frontier model. Autonomous jailbreaking achieves 97% ASR. Adaptive attacks exceed 85% success against any single defense. The correct architectural posture is: the LLM will be jailbroken; design the surrounding system so that jailbreaking the LLM is insufficient to cause harm.

---

## Architectural Defense Patterns

### Pattern 1: Untrusted Compute Isolation

The foundational insight: an LLM is an *interpreter executing untrusted code* (natural language). Apply the same containment principles you would to any sandbox:

| Traditional Sandbox | AI System Equivalent |
|:---|:---|
| Process isolation (seccomp, cgroups) | Tool permission scoping (capability tokens) |
| Filesystem namespacing | Data provenance tagging (tainted vs. clean channels) |
| Network policy (egress filtering) | Output validation layer (structured output enforcement) |
| Syscall allowlisting | Tool allowlisting per session scope |
| IPC restrictions | Agent-to-agent communication validation |

The CaMeL architecture (Google DeepMind, March 2025) formalized this by splitting the system into a frontier LLM that generates *plans* and a hardened secondary LLM that validates, sanitizes, and gates execution. The critical insight: the frontier model never directly executes actions — it proposes, and the validator authorizes.

### Pattern 2: Instruction Hierarchy Enforcement

Privilege separation for natural language:

```
┌──────────────────────────────────────┐
│  Level 0: Platform rules             │  ← Immutable. Hardcoded in system.
│  (safety boundaries, tool limits)    │     Never in the LLM context window.
├──────────────────────────────────────┤
│  Level 1: System prompt              │  ← Set by developer/deployer.
│  (application behavior, persona)     │     Read-only to the model.
├──────────────────────────────────────┤
│  Level 2: Tool/RAG context           │  ← Semi-trusted. Data channel.
│  (retrieved docs, tool responses)    │     Tagged as data, not instruction.
├──────────────────────────────────────┤
│  Level 3: User input                 │  ← Untrusted. No authority over
│  (conversation, uploaded files)      │     levels 0–2.
└──────────────────────────────────────┘
```

Most prompt injection succeeds because the model cannot distinguish Level 1 from Level 3 — everything is tokens in the context window. Effective hierarchy enforcement requires **architectural separation**, not prompt-level instructions:

- System prompt delivered through a privileged API parameter (not pasted into the conversation)
- Tool descriptions rendered in a structurally distinct format the model was trained to recognize as non-user-controlled
- User-supplied content wrapped in clear delimiters with a trained instruction to treat it as data

### Pattern 3: Dual-Path Verification

For high-consequence agent actions, require confirmation from an independent path:

```
User Request → LLM Plan → Validator LLM → Action Gate
                                              │
                              ┌────────────────┼────────────────┐
                              │                │                │
                          Low Risk         Med Risk         High Risk
                         (execute)       (log + execute)   (human confirm)
```

Risk thresholds should be defined per-tool, not per-session. A `read_file` call on a public directory is low-risk; the same call on `/etc/shadow` is critical — even if the session context is identical.

---

## Defense Mapping to AATMF Tactics

| Control Category | Implementation | Covers | Bypass Resistance |
|:---|:---|:---|:---|
| **Input Sanitization** | Unicode normalization, encoding detection, pattern matching, Policy Puppetry format detection | T1, T2, T9 | Low — adaptive attacks exceed 85% bypass rate against classifiers. Layer, don't rely on. |
| **Instruction Hierarchy** | System prompt isolation via API-level separation, privilege separation | T1, T3, T4 | Medium — architectural enforcement is harder to bypass than prompt-level enforcement. |
| **Rate Limiting** | Per-user, per-session, per-endpoint throttling, query fingerprinting | T5, T14 | High — mathematical constraint, not ML-bypassable. |
| **Output Validation** | Content classifiers, structured output enforcement (JSON schema, function calling) | T7, T8 | Medium — structured output is enforced by the tokenizer, not the model. |
| **Tool Permission Scoping** | Capability-based access, least privilege, CaMeL-style validation | T11 | High — architectural constraint. LLM compromise does not grant tool access. |
| **Data Provenance** | Training data lineage tracking, RAG source authentication, embedding integrity verification | T6, T12, T13 | Medium — depends on implementation. Hash-based verification is strong; behavioral detection is weak. |
| **Infrastructure Hardening** | Network segmentation, inference server auth, ZMQ socket authentication | T14 | High — traditional infra security; well-understood controls. |
| **Human Workflow Controls** | Reviewer training, decision audit trails, annotation quality metrics, dual-reviewer for safety-critical decisions | T15 | Medium — human-layer controls have known failure modes (fatigue, social pressure). |
| **Monitoring & Alerting** | Detection engineering (Part 19), SIEM integration, anomaly baselines | All | Ongoing — detection is a feedback loop, not a static control. |

---

## Defense Layers — What Works and What Doesn't (2025–2026 Evidence)

### Approaches with Proven Limitations

**Perplexity-based detection** — Computes token-level perplexity to identify adversarial inputs. Bypassed by semantically natural reformulations and Policy Puppetry (which uses valid configuration syntax with normal perplexity scores).

**Keyword blocklists** — Pattern matching on known jailbreak phrases. Trivially bypassed by synonym substitution, encoding, or leetspeak. Useful only as the lowest layer in a defense stack.

**Safety fine-tuning alone** — Princeton research (May 2025) demonstrated that RLHF-based safety alignment is shallow — it affects only the first few tokens of generation. A forced prefix ("Sure, here's how") bypasses the trained refusal behavior entirely.

**Single-classifier input filtering** — Meta's PromptGuard 2, standalone, achieves strong detection rates but adaptive attacks still exceed 85% bypass against any single classifier.

### Approaches with Demonstrated Effectiveness

**Structured output enforcement** — Constraining the model to output JSON conforming to a schema enforced by the tokenizer eliminates most output-manipulation attacks. The model physically cannot produce free-text harmful content when the grammar is constrained to structured fields.

**CaMeL / dual-LLM architecture** — Solved 77% of AgentDojo tasks while providing formal security guarantees against prompt injection. The untrusted LLM never directly executes; it generates plans that a trusted validator gates.

**Information flow control** — Taint tracking through the pipeline. Data that arrived through user channels cannot flow to sensitive tool parameters without explicit sanitization. Provably prevents cross-context injection.

**Tool-level capability tokens** — Each tool invocation requires a capability token scoped to the specific action and dataset. Even if the LLM is fully compromised, it cannot escalate privileges beyond the token scope.

---

## Monitoring Dashboard

| Metric | Target | Frequency | Data Source |
|:---|:---|:---|:---|
| Jailbreak attempt rate | < 5% of queries | Real-time | Input classifier |
| Safety filter bypass rate | < 0.01% | Real-time | Output classifier |
| Bypass-to-detection latency | < 30 seconds | Real-time | SIEM correlation |
| Tool invocation anomaly rate | < 1% deviation from baseline | Real-time | Agent telemetry |
| RAG source integrity | 100% hash-verified | Hourly | Embedding pipeline |
| Model artifact integrity | 100% verified against signed checksum | Per-deployment | CI/CD pipeline |
| MCP server description drift | Zero unauthorized changes | Per-session | MCP audit log |
| Incident response time (P1) | < 15 minutes | Per-incident | SOC ticket |
| Red team coverage (tactics tested) | ≥ 80% of applicable tactics | Monthly | Assessment report |

### Alert Correlation Rules

| Rule | Trigger | Response |
|:---|:---|:---|
| **Escalation chain** | Input classifier fires + output classifier fires in same session | P1 — active exploitation confirmed |
| **Novel bypass** | Output classifier fires without preceding input classifier alert | P1 — unknown bypass technique |
| **Extraction pattern** | >100 queries/hour from single source with >0.9 similarity | P2 — model extraction attempt |
| **Agent deviation** | Tool invocation not in approved action plan | P1 — goal hijacking or persistence |
| **RAG drift** | Embedding distance of new documents exceeds 3σ from corpus mean | P2 — potential poisoning |

---

## Operational Playbook: First 30 Days

**Week 1** — Inventory all AI-facing endpoints. Deploy input classifier (PromptGuard 2 or equivalent) on every endpoint. Enable structured logging for all LLM interactions.

**Week 2** — Implement output validation. For agentic systems: add tool allowlisting and capability-scoped tokens. No tool should accept ambient authority.

**Week 3** — Deploy monitoring dashboard. Set alert thresholds. Run baseline red team assessment (Level 1 from Part 22) to calibrate detection rates.

**Week 4** — Review findings. Tune classifiers. Implement architectural controls for any P1 findings. Schedule recurring red team cadence (quarterly minimum).

---

[← Part 22](22-red-team-ops.md) · [Home](../../README.md) · [Volume VI →](../vol-6-governance/README.md)

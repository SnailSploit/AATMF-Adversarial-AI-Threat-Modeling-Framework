# Part 20: Mitigation Strategies

## Defense-in-Depth Architecture

Research consensus (2025): adaptive attack strategies exceed **85% success** against any single state-of-the-art defense. No single control is sufficient. AATMF mandates layered defense.

The defense philosophy mirrors operating system security: assume the application (LLM) will be compromised, and engineer the surrounding system so that compromise is contained. Every mitigation listed here should be evaluated as "what happens when this control is bypassed?" — because it will be.

---

## Foundational Defensive Architectures

### CaMeL (Google DeepMind, March 2025)

The most rigorous defensive framework. Treats LLMs as fundamentally untrusted:

| Principle | Implementation | Why It Works |
|:---|:---|:---|
| **Dual-LLM pattern** | Frontier LLM generates plans; hardened secondary LLM validates and sanitizes | Attacker must compromise *both* models — different architectures, different training, different attack surfaces |
| **Capability-based access** | Tools require explicit capability tokens, not ambient authority | Jailbreaking the LLM doesn't grant tool access — tokens are issued by the validator, not the model |
| **Information flow control** | Taint tracking through entire pipeline; tainted data cannot reach sensitive operations | Formally prevents cross-context injection — data from user channel physically cannot flow to tool parameters |
| **Minimal authority** | Agents receive only permissions needed for the immediate task | Blast radius of any compromise is bounded by the token scope |

CaMeL solved 77% of AgentDojo tasks with provable security guarantees against prompt injection. The trade-off: latency (dual inference) and cost (2× compute).

### LlamaFirewall (Meta, April 2025)

Production-oriented defense stack. Less formally rigorous than CaMeL but deployable today:

| Component | Function | Coverage | Limitations |
|:---|:---|:---|:---|
| **PromptGuard 2** | Real-time input classification for injection and jailbreak | T1, T2, T9 | Adaptive attacks bypass at >85% rate; must be layered |
| **Agent Alignment Checks** | Verify agent actions align with original user intent (not drifted by injection) | T11 | Relies on intent similarity scoring — adversarial reformulation can preserve similarity |
| **CodeShield** | Static analysis of LLM-generated code for insecure patterns | T7, T11 | Detects known patterns; cannot reason about novel logic flaws |

### Structured Output Enforcement

Often overlooked, often the strongest single control. When the model is constrained to emit JSON conforming to a strict schema — enforced by the tokenizer's grammar, not by the model's compliance — the attack surface for output manipulation collapses:

- The model **physically cannot** produce free-text harmful content when the grammar constrains output to enumerated fields
- Eliminates most T7 (output manipulation) and T8 (deception) vectors
- Combined with tool-specific schemas, prevents arbitrary tool invocation
- Trade-off: reduced model flexibility for structured tasks

---

## Mitigation Controls by Tactic

### T1 — Prompt & Context Subversion

| Control | Implementation | Bypass Resistance |
|:---|:---|:---|
| Input classifier (PromptGuard 2, custom) | Real-time scoring of user inputs against injection patterns | Low — adaptive rewriting, Policy Puppetry format bypass. Necessary but insufficient alone. |
| System prompt isolation | Deliver via privileged API parameter, not concatenated text | Medium — architectural enforcement. Model still sees everything in context window. |
| Instruction hierarchy marking | Structural delimiters trained into the model (e.g., `[SYSTEM]`, `[USER]`, `[DATA]`) | Medium — depends on training quality. Delimiter injection is a known bypass. |
| Policy Puppetry detection | Detect XML/INI/JSON/YAML policy structures in user input | Medium — requires parser-aware analysis, not regex. |
| Input length limiting | Cap user input length to reduce complexity budget | Low — but eliminates cognitive overload (T1-AT-007) trivially. |

### T2 — Semantic & Linguistic Evasion

| Control | Implementation | Bypass Resistance |
|:---|:---|:---|
| Unicode normalization | NFKC normalization + confusable character mapping (ICU) | High — deterministic transformation. Eliminates homoglyph, zero-width, and RTL attacks. |
| Multi-layer content filtering | Chain regex → ML classifier → LLM-based semantic analysis | Medium — each layer catches what the previous misses. Adaptive attacks still achieve ~15% bypass. |
| Base64/encoding detection | Detect and decode nested encodings before classification | High — deterministic. But attackers can use non-standard encodings. |
| Emoji-to-text expansion | Map emoji sequences to text equivalents before analysis | High — deterministic. Eliminates emoji smuggling. |

### T3 — Reasoning & Constraint Exploitation

| Control | Implementation | Bypass Resistance |
|:---|:---|:---|
| Reasoning chain verification | Validate that CoT steps do not contain policy violations even if the final output is safe | Medium — catches H-CoT (Hijacked Chain-of-Thought). Requires access to reasoning tokens. |
| Shallow alignment defense | Force model to commit to refusal before generating any content (prefix constraint) | Medium — addresses Princeton's finding that alignment is shallow. Sequence matters. |
| Constraint hardening | Express safety constraints as logical rules, not natural language requests | Medium — reduces misinterpretation surface but increases rigidity. |

### T4 — Multi-Turn & Memory Manipulation

| Control | Implementation | Bypass Resistance |
|:---|:---|:---|
| Context window management | Per-turn classification, not just per-message. Track cumulative intent across turns. | Medium — computationally expensive but catches crescendo and gradual escalation attacks. |
| Conversation state validation | Periodically re-evaluate the conversation context against safety constraints, not just the latest turn | Medium — prevents slow-boil injection. |
| Memory isolation | Persistent memory writes gated by a separate validation path (not the conversational LLM) | High — architectural. Prevents memory poisoning from propagating across sessions. |
| Session TTL | Limit conversation length to bound multi-turn attack windows | High — mathematical constraint. Trade-off: user experience for very long conversations. |

### T5 — Model & API Exploitation

| Control | Implementation | Bypass Resistance |
|:---|:---|:---|
| Rate limiting | Per-user, per-session, per-endpoint with adaptive thresholds | High — mathematical. Cannot be bypassed without distributing across identities. |
| Query fingerprinting | Detect systematic probing (incrementally varied inputs, boundary testing) | Medium — pattern-based detection. Sophisticated attackers randomize query order. |
| Differential privacy on outputs | Add calibrated noise to logits/probabilities to prevent model extraction | High — formal privacy guarantees. Trade-off: slight output quality degradation. |
| API key scoping | Different API keys for different use cases with distinct rate limits and capabilities | High — administrative control. |

### T6 — Training & Feedback Poisoning

| Control | Implementation | Bypass Resistance |
|:---|:---|:---|
| Data Randomized Smoothing (DRS) | Train on randomly perturbed versions of data to build robustness to poisoned samples | Medium — research defense. Effective against known poisoning strategies; unknown attacks may bypass. |
| Training data provenance | Cryptographic lineage tracking from source to training batch | High — detects tampering but cannot prevent it at source. |
| Anomaly detection in training metrics | Monitor loss curves, gradient norms for signs of poisoned batches | Low — poisoning with 250 documents produces no detectable anomaly in aggregate metrics. |
| Dual-source verification | Every training sample verified by independent provenance chain | High — expensive but effective. Practical only for high-value fine-tuning, not pretraining. |

### T7–T8 — Output Manipulation & Deception

| Control | Implementation | Bypass Resistance |
|:---|:---|:---|
| Structured output enforcement | JSON schema validation at the tokenizer level | High — grammar-enforced. Model cannot produce unconstrained text. |
| Content watermarking | Embed statistical watermarks in generated text for provenance tracking | Medium — detectable by the deployer. Attackers can strip watermarks with paraphrasing. |
| Fact-checking integration | Ground outputs against verified knowledge sources before delivery | Medium — depends on knowledge base quality and coverage. |
| Output classifiers | ML classifier on model outputs for harmful/deceptive content | Medium — same adaptive bypass concerns as input classifiers. |

### T9 — Multimodal & Cross-Channel

| Control | Implementation | Bypass Resistance |
|:---|:---|:---|
| Cross-modal consistency checking | Verify that image content, OCR text, and user text are semantically consistent | Medium — catches blatant steganographic injection. Subtle perturbations may pass. |
| Image preprocessing | Strip metadata, normalize, re-encode before passing to model | High — eliminates appended-data and metadata-based injection. |
| Audio spectrogram analysis | Detect injected text in audio frequency domains | Research-stage — effective against SACRED-Bench attacks but not production-hardened. |

### T10 — Integrity & Confidentiality Breach

| Control | Implementation | Bypass Resistance |
|:---|:---|:---|
| TEE deployment | Run inference in hardware-isolated enclaves (SGX, SEV-SNP) | High — hardware-enforced. Prevents model weight extraction from memory. |
| Membership inference defense | Differential privacy during training + output perturbation | Medium — reduces leakage but doesn't eliminate it for highly memorized samples. |
| Access control | Role-based access to model APIs with audit logging | High — standard access control. Well-understood. |

### T11 — Agentic & Orchestrator Exploitation

| Control | Implementation | Bypass Resistance |
|:---|:---|:---|
| CaMeL architecture | Dual-LLM with capability tokens and information flow control | High — formal guarantees against prompt injection for tool access. |
| MCP server auditing | Automated description drift detection, tool behavior monitoring, approval workflow for new servers | High — prevents rug-pull attacks and shadow tool manipulation. |
| Tool permission scoping | Per-session, per-task capability tokens. No ambient authority. | High — architectural. Compromised LLM cannot escalate beyond token scope. |
| Agent kill switch | Hard timeout + resource budget per agent session. Automatic termination on anomaly. | High — deterministic. Prevents resource exhaustion and runaway agents. |

### T12 — RAG & Knowledge Base Manipulation

| Control | Implementation | Bypass Resistance |
|:---|:---|:---|
| Embedding integrity verification | Hash-based verification of embedding vectors against trusted baseline | High — detects tampering at the vector level. |
| Retrieval result validation | Score retrieved documents against injection patterns before including in context | Medium — same classifier bypass concerns. |
| Source authentication | Cryptographic signing of knowledge base documents with provenance chain | High — prevents unauthorized document injection. |
| Embedding distance monitoring | Alert when new documents' embeddings deviate >3σ from corpus mean | Medium — catches blatant poisoning. Sophisticated attacks craft documents within normal distribution. |

### T13 — AI Supply Chain & Artifact Trust

| Control | Implementation | Bypass Resistance |
|:---|:---|:---|
| SafeTensors adoption | Use only SafeTensors format for model weights (no code execution on load) | High — eliminates pickle deserialization attacks entirely. |
| Picklescan (with patches) | Scan pickle-format models for known malicious patterns | Medium — known-pattern detection. Novel payloads may bypass. |
| SBOM for ML artifacts | Generate and verify Software Bill of Materials for models, datasets, and tools | High — provenance tracking. Detects unauthorized modifications. |
| PEFTGuard | Backdoor detection specifically for LoRA/PEFT adapters | Medium — research tool. Effective against known backdoor strategies. |

### T14 — Infrastructure & Economic Warfare

| Control | Implementation | Bypass Resistance |
|:---|:---|:---|
| Network segmentation | Isolate inference, training, and serving infrastructure | High — standard infra security. |
| ZMQ/gRPC authentication | Mutual TLS on all inter-service communication (addresses ShadowMQ-class vulns) | High — eliminates unauthenticated deserialization. |
| Cost monitoring | Per-user, per-session cost tracking with hard budgets | High — mathematical. Prevents billing denial-of-wallet attacks. |

### T15 — Human Workflow Exploitation

| Control | Implementation | Bypass Resistance |
|:---|:---|:---|
| Reviewer training | Regular adversarial awareness training using AATMF tabletop exercises (Part 26) | Medium — human controls have known fatigue and social pressure failure modes. |
| Decision audit trails | Log every human override decision with justification | High — accountability control. Deters but doesn't prevent. |
| Dual-reviewer for safety-critical | Two independent reviewers for any safety label change or model deployment | Medium — reduces single-point-of-failure but adds latency. |

---

## Priority Implementation Order

1. **Immediate (Week 1)** — Input sanitization (T1–T3), rate limiting (T5), SafeTensors (T13), structured output enforcement (T7–T8)
2. **Short-term (Month 1)** — CaMeL/dual-LLM pattern (T11), MCP auditing (T11), RAG validation (T12), Unicode normalization (T2)
3. **Medium-term (Quarter 1)** — Multimodal detection (T9), training pipeline security (T6), TEE deployment (T10), information flow control
4. **Ongoing** — Human workflow hardening (T15), infrastructure monitoring (T14), supply chain verification (T13), red team feedback loop

---

[← Part 19](19-detection-engineering.md) · [Home](../../README.md) · [Part 21: Incident Response →](21-incident-response.md)

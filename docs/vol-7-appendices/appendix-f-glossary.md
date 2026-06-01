# Appendix F: Glossary and References

## Glossary

| Term | Definition |
|:---|:---|
| **AATMF** | Adversarial AI Threat Modeling Framework — structured taxonomy for AI-specific attack vectors |
| **AATMF-R** | AATMF Risk scoring methodology — six-factor formula: `(L × I × E) / 6 × (D / 6) × R × C` |
| **A2A** | Agent-to-Agent protocol — Google's open standard for inter-agent communication |
| **Adaptive Attack** | Attack strategy that iteratively refines payloads based on defense responses. Research shows >85% bypass rate against any single defense. |
| **AIBOM** | AI Bill of Materials — inventory of components in an AI system (models, datasets, tools, libraries) |
| **Alignment** | Training process that shapes model behavior to follow intended policies. Current techniques (RLHF, DPO, CAI) produce shallow alignment vulnerable to bypass. |
| **Ambient Authority** | Design pattern where tools are accessible to any code running in a context, without explicit capability tokens. Primary vulnerability in pre-CaMeL agent architectures. |
| **ASR** | Attack Success Rate — percentage of attempts that achieve the adversarial objective. Key metric for red team assessments. |
| **ATLAS** | Adversarial Threat Landscape for Artificial Intelligence Systems — MITRE's framework for ML attack taxonomy (v4.6.0, October 2025) |
| **CaMeL** | CApability-Mediated LLM — Google DeepMind's dual-LLM architecture providing formal security guarantees against prompt injection |
| **Capability Token** | Unforgeable credential scoping a specific tool permission for a specific task. Core primitive in CaMeL architecture. |
| **CoT** | Chain-of-Thought — step-by-step reasoning in LLMs. Can be hijacked (H-CoT) to embed policy-violating reasoning within safe-looking chains. |
| **CometJacking** | Attack against Perplexity Comet where a single weaponized URL triggers agent exploitation |
| **Context Inheritance** | Vulnerability class where behavioral state encoded in a pasted transcript propagates to a new model session, causing the receiver to adopt the operational state rather than treating it as data |
| **Crescendo Attack** | Multi-turn jailbreak that gradually escalates from benign to harmful through a sequence of seemingly innocent questions |
| **DPO** | Direct Preference Optimization — alignment technique that directly optimizes model outputs against human preference pairs without a separate reward model |
| **DRS** | Data Randomized Smoothing — defense against training data poisoning that trains on randomly perturbed data versions |
| **Embedding Drift** | Deviation of new document embeddings from the established corpus distribution. Signal for RAG poisoning detection. |
| **GTG-1002** | First documented state-sponsored AI-orchestrated cyberattack (November 2025). Chinese group used Claude Code for 80–90% of operational tasks across ~30 targets. |
| **H-CoT** | Hijacked Chain-of-Thought — attack that subverts CoT safety reasoning by embedding adversarial logic within the reasoning chain |
| **Information Flow Control** | Security mechanism that tracks data provenance through a pipeline, preventing tainted (user-controlled) data from reaching sensitive (tool-execution) channels |
| **Instruction Hierarchy** | Privilege separation for natural language, establishing authority levels: platform rules > system prompt > tool/RAG context > user input |
| **LRM** | Large Reasoning Model — models with explicit extended reasoning capabilities (o1, o3, DeepSeek-R1, Gemini 2.5). Both more robust against simple attacks and more capable of generating sophisticated attacks. |
| **MCP** | Model Context Protocol — Anthropic's standard for connecting AI assistants to external tools, APIs, and data sources. Tool descriptions are injected into the LLM context as natural language, creating an architectural injection surface. |
| **MCP-ITP** | MCP Injection-Tool Poisoning — Invariant Labs framework demonstrating direct poisoning, shadow attacks, and rug-pull vectors against MCP tool descriptions |
| **PEFT** | Parameter-Efficient Fine-Tuning — techniques (LoRA, QLoRA, adapters) for efficient model adaptation. PEFT adapters are a supply chain attack vector (PEFTGuard). |
| **Policy Puppetry** | Universal jailbreak technique (HiddenLayer, April 2025) that reformulates adversarial prompts as XML/INI/JSON policy files, causing models to interpret them as authoritative system instructions. Bypasses every tested frontier model. |
| **PoisonedRAG** | Attack demonstrating 90% ASR with just 5 injected texts in a knowledge base of millions. Exploits the semantic similarity search mechanism at RAG's core. |
| **PUA** | Private Use Area — Unicode range (U+E000–U+F8FF) used for custom characters. Exploited in encoding evasion attacks. |
| **RAG** | Retrieval-Augmented Generation — architecture combining search/retrieval with generation. The retrieval mechanism is fundamentally exploitable (T12). |
| **Red Card** | AATMF evaluation unit — a small, safe, deterministic test scenario for evaluating specific controls against specific techniques |
| **RLHF** | Reinforcement Learning from Human Feedback — primary alignment technique. Princeton (2025) showed alignment is shallow, affecting only the first few tokens. |
| **Rug Pull** | MCP attack where tool descriptions are silently altered after initial security review and approval. The approved tool becomes malicious without triggering re-review. |
| **SafeTensors** | Secure model serialization format (HuggingFace) that prevents arbitrary code execution during model loading. Eliminates pickle-based supply chain attacks. |
| **Shadow Attack** | MCP attack where a malicious server manipulates the behavior of trusted tools from other servers without the malicious tool ever being directly invoked |
| **ShadowMQ** | Vulnerability class (Oligo Security, November 2025) — unsafe ZeroMQ pickle deserialization copy-pasted across major inference frameworks (vLLM, TensorRT-LLM, Max Server) |
| **Spotlighting** | Defense technique that marks the boundary between instructions and data using trained delimiters, helping the model distinguish trusted from untrusted content |
| **Taint Tracking** | Information flow control mechanism that labels data with its origin (user, system, tool) and enforces policies on how labeled data can flow through the pipeline |
| **TEE** | Trusted Execution Environment — hardware-based security enclave (Intel SGX, AMD SEV-SNP) for protecting model weights and inference from host-level access |
| **Time Bandit** | Jailbreak technique (CERT/CC VU#733789) that exploits temporal confusion in ChatGPT-4o by anchoring conversations in historical periods |

## Key References

### Foundational Research

1. HiddenLayer. "Policy Puppetry: A Universal Jailbreak." April 2025.
2. Zeng et al. "Autonomous LRM Jailbreaking." *Nature Communications*, August 2025.
3. Xue et al. "PoisonedRAG: Knowledge Corruption Attacks on RAG." *USENIX Security 2025*.
4. Debenedetti et al. "CaMeL: Defeating Prompt Injection by Design." *Google DeepMind*, March 2025.
5. Qi et al. "Safety Alignment Depth." *Princeton*, May 2025.
6. Weng et al. "H-CoT: Hijacking Chain-of-Thought Safety Reasoning." *Duke/Accenture*, February 2025.
7. Sherburn et al. "250 Documents: Universal Pretraining Backdoors." *Turing Institute/Anthropic/UK AISI*, October 2025.

### Threat Intelligence

8. Invariant Labs. "MCP-ITP: Tool Poisoning in Agentic Systems." April 2025.
9. Oligo Security. "ShadowMQ: Unsafe Deserialization in AI Inference Frameworks." November 2025.
10. Anthropic. "GTG-1002: AI-Orchestrated Cyber Campaign." November 2025.
11. Borghesi et al. "SACRED-Bench: Compositional Audio Attacks." November 2025.

### Defensive Frameworks

12. Meta. "LlamaFirewall: Open-Source AI Safety Framework." April 2025.
13. Google DeepMind. "CaMeL: Capability-Mediated LLM." March 2025.
14. NVIDIA. "NeMo Guardrails." 2024–2025.

### Standards & Compliance

15. MITRE. "ATLAS v4.6.0." October 2025.
16. OWASP. "LLM Top 10 2025." January 2025.
17. OWASP. "Top 10 for Agentic Applications 2026." December 2025.
18. OWASP. "Guide for Secure MCP Server Development." March 2026.
19. OWASP. "GenAI Data Security Risks & Mitigations 2026." March 2026.
20. NIST. "Cyber AI Profile (IR 8596) Preliminary Draft." December 2025.
21. European Parliament. "EU AI Act (Regulation 2024/1689)." 2024.

### Author's Research

22. Aizen, K. "AATMF v1–v3." SnailSploit, 2024–2026.
23. Aizen, K. "The 30% Blind Spot: LLM Safety Judges." SnailSploit, 2025.
24. Aizen, K. "Context Inheritance: Computational Countertransference in Transformer Architectures." 2025.
25. Aizen, K. *Adversarial Minds: The Psychology of Social Engineering*. 2025.

---

[← Appendix E](appendix-e-case-studies.md) · [Home](../../README.md)

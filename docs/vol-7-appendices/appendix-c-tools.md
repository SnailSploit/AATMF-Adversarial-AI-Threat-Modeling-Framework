# Appendix C: Tools and Scripts Reference

## Offensive Tools (Red Team)

| Tool | Purpose | AATMF Coverage | Type |
|:---|:---|:---|:---|
| **Garak** (NVIDIA) | LLM vulnerability scanner — automated probe generation across jailbreak, injection, leakage, and hallucination categories | T1–T8 | OSS (Apache 2.0) |
| **PyRIT** (Microsoft) | Python Risk Identification Toolkit — orchestrated multi-turn red teaming with scoring, converters, and target-agnostic architecture | T1–T12 | OSS (MIT) |
| **AATMF Scanner** (SnailSploit) | Framework-native assessment tool — maps findings to AATMF IDs, risk scores, and compliance frameworks | T1–T15 | Proprietary |
| **AugmentedLLM Red Team** | Autonomous LRM-based red teaming — uses reasoning models to generate and refine jailbreak variants iteratively | T1–T4 | Research |
| **PromptMap** | Visual attack surface mapper — generates prompt injection payloads based on application context | T1, T2 | OSS |
| **Rebuff** | Prompt injection detection testing — canary tokens, heuristic analysis, LLM-based classification | T1, T9 | OSS |
| **TextAttack** | NLP adversarial attack framework — word-level, character-level, and sentence-level perturbations | T2 | OSS (MIT) |
| **ART** (IBM) | Adversarial Robustness Toolbox — model evasion, poisoning, extraction, inference attacks with defense evaluation | T5, T6, T10 | OSS (MIT) |
| **Counterfit** (Microsoft) | Automated adversarial ML attack framework targeting models deployed as cloud services | T5, T10 | OSS (MIT) |
| **Inspect AI** (UK AISI) | Framework for building and running LLM evaluations including safety, security, and alignment testing | T1–T8 | OSS |

## Defensive Tools (Blue Team)

| Tool | Purpose | AATMF Coverage | Type |
|:---|:---|:---|:---|
| **LlamaFirewall** (Meta) | Comprehensive AI firewall — PromptGuard 2 (input), Agent Alignment Checks, CodeShield (output) | T1, T2, T7, T9, T11 | OSS (Apache 2.0) |
| **PromptGuard 2** (Meta) | Real-time prompt injection and jailbreak classifier — deployed as standalone or LlamaFirewall component | T1, T2, T9 | OSS (Apache 2.0) |
| **NeMo Guardrails** (NVIDIA) | Programmable guardrail framework — Colang-based rules for input/output/topical/retrieval control | T1, T4, T7, T8, T12 | OSS (Apache 2.0) |
| **Guardrails AI** | Output validation framework — structured output enforcement, validators, re-prompting | T7, T8 | OSS |
| **Vigil** | Prompt injection detection — static analysis, LLM-as-judge, vector similarity for RAG monitoring | T1, T12 | OSS |

## Supply Chain Security

| Tool | Purpose | AATMF Coverage | Type |
|:---|:---|:---|:---|
| **SafeTensors** (HuggingFace) | Safe model serialization — eliminates arbitrary code execution during model loading | T13 | OSS (Apache 2.0) |
| **Picklescan** | Malicious pickle payload detection in model files — pattern matching against known exploit signatures | T13 | OSS (MIT) |
| **PEFTGuard** | Backdoor detection specifically for PEFT/LoRA adapters — analyzes parameter distributions for anomalies | T13 | Research |
| **ModelScan** (Protect AI) | Multi-format model scanner — pickle, H5, SavedModel, ONNX. Detects code execution and data exfiltration payloads | T13 | OSS (Apache 2.0) |
| **OWASP AIBOM Generator** | Generates AI Bills of Materials (AIBOMs) for supply chain transparency | T13 | OSS |

## Infrastructure Security

| Tool | Purpose | AATMF Coverage | Type |
|:---|:---|:---|:---|
| **CaMeL** (Google DeepMind) | Dual-LLM architecture — capability-based access control, information flow tracking, formal injection guarantees | T11 | Research |
| **DRS Defense** | Data Randomized Smoothing — training-time defense against data poisoning | T6 | Research |
| **ML-BOM** | Machine Learning Bill of Materials generator for training pipeline auditability | T6, T13 | Research |

## Monitoring & Observability

| Tool | Purpose | AATMF Coverage | Type |
|:---|:---|:---|:---|
| **Langfuse** | LLM observability — trace conversations, score outputs, monitor costs, debug agents | All | OSS |
| **LangSmith** (LangChain) | End-to-end LLM application monitoring — tracing, evaluation, annotation, dataset management | All | Commercial |
| **Helicone** | LLM request logging and analytics — cost tracking, latency monitoring, prompt versioning | T5, T14 | OSS/Commercial |
| **WhyLabs** | ML monitoring — data drift detection, model performance tracking, anomaly alerting | T6, T12 | Commercial |

## Detection Signature Tools

| Tool | Purpose | AATMF Coverage | Type |
|:---|:---|:---|:---|
| **YARA** | Pattern matching for prompt injection and supply chain payloads. See `signatures/yara/` | T1, T2, T9, T11, T13 | OSS |
| **Sigma** | SIEM-compatible detection rules for API abuse, exfiltration, infrastructure anomalies. See `signatures/sigma/` | T5, T7, T11, T14 | OSS |
| **Semgrep** | Static analysis for LLM integration security — detect unsafe deserialization, unvalidated tool calls, missing auth | T11, T13, T14 | OSS/Commercial |

## Evaluation & Benchmarking

| Tool | Purpose | AATMF Coverage | Type |
|:---|:---|:---|:---|
| **OWASP FinBot CTF** | Agentic security capture-the-flag — hands-on MCP exploitation, tool poisoning, agent abuse scenarios | T11 | OSS |
| **AgentDojo** | Benchmark for agent security — measures defense effectiveness against injection in tool-calling agents | T11 | Research |
| **HarmBench** | Standardized evaluation of LLM safety — automated red teaming with diverse attack strategies | T1–T4 | Research |
| **JailbreakBench** | Curated jailbreak dataset with standardized evaluation — tracks ASR across models and defenses | T1–T3 | Research |
| **TrustLLM** | Comprehensive LLM trustworthiness benchmark — safety, fairness, robustness, privacy dimensions | T1–T10 | Research |

---

## Tool Selection Guide

| If your primary concern is... | Start with... | Add... |
|:---|:---|:---|
| Prompt injection defense | LlamaFirewall (PromptGuard 2) | NeMo Guardrails for programmable rules |
| Agentic system security | CaMeL architecture pattern | Langfuse for observability |
| Model supply chain | SafeTensors + ModelScan | AIBOM Generator for auditability |
| Automated red teaming | Garak for breadth | PyRIT for depth (multi-turn, converters) |
| RAG security | Vigil for monitoring | Custom embedding drift detection (Part 19) |
| Compliance reporting | AATMF Scanner | Map to OWASP/ATLAS/EU AI Act (Part 25) |

---

[← Appendix B](appendix-b-signatures.md) · [Home](../../README.md) · [Appendix D →](appendix-d-templates.md)

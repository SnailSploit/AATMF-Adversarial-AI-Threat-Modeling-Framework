# T13 — AI Supply Chain & Artifact Trust

> **15 Techniques** · **150 Attack Procedures** · Risk Range: 205–260

---

## Technique Overview

| ID | Technique | Risk | Rating | Procedures |
|:---|:---|:---:|:---|:---:|
| `T13-AT-001` | Model Repository Poisoning | 255 | 🔴 CRITICAL | 10 |
| `T13-AT-002` | Dataset Contamination | 245 | 🟠 HIGH | 10 |
| `T13-AT-003` | Pipeline Injection Attacks | 240 | 🟠 HIGH | 10 |
| `T13-AT-004` | Dependency Confusion | 235 | 🟠 HIGH | 10 |
| `T13-AT-005` | Model Card Manipulation | 210 | 🟠 HIGH | 10 |
| `T13-AT-006` | Checkpoint Poisoning | 250 | 🔴 CRITICAL | 10 |
| `T13-AT-007` | Transfer Learning Attacks | 225 | 🟠 HIGH | 10 |
| `T13-AT-008` | Model Conversion Exploits | 220 | 🟠 HIGH | 10 |
| `T13-AT-009` | Cloud Training Attacks | 230 | 🟠 HIGH | 10 |
| `T13-AT-010` | Hardware Supply Chain | 260 | 🔴 CRITICAL | 10 |
| `T13-AT-011` | Model Marketplace Attacks | 215 | 🟠 HIGH | 10 |
| `T13-AT-012` | Artifact Signature Attacks | 225 | 🟠 HIGH | 10 |
| `T13-AT-013` | Container Registry Poisoning | 235 | 🟠 HIGH | 10 |
| `T13-AT-014` | Development Tool Compromise | 240 | 🟠 HIGH | 10 |
| `T13-AT-015` | Model Obfuscation Attacks | 205 | 🟠 HIGH | 10 |

---

### 2025–2026 Threat Update

The AI supply chain attack surface exploded in 2025–2026, transitioning from academic proof-of-concept to active, coordinated campaigns with real-world casualties.

**Pickle remains the dominant attack surface.** 44.9% of HuggingFace repositories still use pickle-format models (PickleBall, Aug 2025) — including 29 of the top-100 most-downloaded and 500+ models from Meta, Google, Microsoft, NVIDIA, and Intel. PickleCloak (USENIX Security 2026) systematically mapped 22 distinct pickle-based model loading paths across 5 AI/ML frameworks (NumPy, Joblib, PyTorch, TensorFlow/Keras, NeMo), 19 of which are entirely missed by existing scanners. 133 exploitable gadgets were discovered with near-100% scanner bypass, and 7 of 9 Exception-Oriented Programming (EOP) instances bypass all scanners. Awarded $12K bounty from NVIDIA, Keras, ProtectAI, and PickleScan.

**Scanner defenses repeatedly broken.** NullifAI (Feb 2025) bypassed Picklescan via 7z compression + broken Pickle streams — reverse shell payloads executed before the scanner reached the error. JFrog disclosed 3 zero-day Picklescan bypasses (Jun 2025, fixed Sep 2025). Sonatype found 4 CVEs in Picklescan itself (CVE-2025-1716 through CVE-2025-1945). Checkmarx demonstrated Bdb.run and asyncio gadget bypasses of Picklescan's blacklist. vLLM received CVE-2025-32444 (CVSS 10.0) for pickle deserialization over unsecured ZeroMQ sockets; the same class reappeared in LightLLM and manga-image-translator in Feb 2026.

**LoRA ecosystem weaponized.** LoRATK (EMNLP 2025) demonstrated that a single backdoor LoRA, merged training-free with multiple task-enhancing adapters, retains malicious capabilities across all merges. The merged LoRAs are "particularly infectious — because their malicious intent is cleverly concealed behind improved downstream capabilities, creating a strong incentive for voluntary download."

**s1ngularity: the watershed.** On August 26, 2025, the Nx build system package was compromised via GitHub Actions workflow injection. In 5 hours, 2,349 credentials were stolen from 1,079 developer systems. **First known supply chain attack to weaponize AI CLI tools** — the malware searched for installed Claude, Gemini, and Amazon Q configurations to use as reconnaissance and exfiltration tools. 33% of compromised systems had at least one LLM client. A second wave exposed 5,500+ private repositories from 400+ organizations. Stolen tokens fed the Shai-Hulud campaign (Sep–Nov 2025), a true supply chain worm.

**2026 acceleration.** LiteLLM PyPI compromise (Mar 2026) exposed 500K credentials including Meta, OpenAI, and Anthropic API keys. Bitwarden CLI npm hijack (Apr 2026) lasted 90 minutes with a payload targeting AI coding tools. PyTorch Lightning "Mini Shai-Hulud" compromise (Apr 2026) lasted 42 minutes. The EU Commission was breached after attackers poisoned Trivy, an open-source security scanning tool. The US DoD published formal AI/ML supply chain risk guidance (Mar 2026). Palo Alto Unit 42 demonstrated Model Namespace Reuse: registering deleted HuggingFace usernames to replace popular models in production on Vertex AI and Azure AI Foundry.

---

## Techniques

### `T13-AT-001` — Model Repository Poisoning

**Risk Score:** 255 🔴 CRITICAL

Upload malicious models to public or private model repositories (HuggingFace, ClawHub, model zoos) that execute arbitrary code on load, carry behavioral backdoors, or impersonate legitimate models.

#### Mechanism

Model repositories are the npm/PyPI of the AI ecosystem — the primary distribution channel for pre-trained models. The fundamental vulnerability is that model files are opaque binary artifacts that can contain executable code, and the deserialization process (loading a model) can trigger that code. The Pickle serialization format, used by 44.9% of HuggingFace models (PickleBall Aug 2025), executes Python code during deserialization via `__reduce__` methods. PickleCloak (USENIX Security 2026) mapped 22 distinct loading paths across 5 frameworks, 19 missed by scanners, with 133 exploitable gadgets at near-100% bypass rate. NullifAI (Feb 2025) demonstrated that 7z compression of Pickle files bypasses Picklescan while Python's deserializer still processes the payload. Beyond code execution, repositories enable *behavioral* poisoning: uploading models with embedded backdoors (triggered by specific inputs) or degraded safety alignment that appear functional on benchmarks. PoisonGPT (Mithril Security 2023) uploaded a model with targeted factual manipulation to HuggingFace that passed standard checks. Model Namespace Reuse (Palo Alto Unit 42 2025) showed that registering deleted HuggingFace usernames replaces models in production deployments on Vertex AI and Azure AI Foundry — invisible to deployment manifests.

**OWASP:** LLM04:2025 (Data and Model Poisoning) · **ATLAS:** AML.T0024 (Supply Chain Compromise), AML.T0018 (Backdoor ML Model) · **ASI:** ASI10 (Supply Chain Vulnerabilities)

<details>
<summary><b>Attack Procedures (10)</b></summary>

**`T13-AP-001A`** — Pickle Deserialization RCE via Model Upload
```
Upload a PyTorch model to HuggingFace with a malicious __reduce__
method in the Pickle stream. When a user calls torch.load() or
from_pretrained(), the Pickle deserializer executes the payload
before the model is even used. Payloads observed in the wild:
reverse shells to hardcoded IPs, cryptocurrency miners, credential
harvesters. NullifAI demonstrated evasion of Picklescan via 7z
compression (Feb 2025).

22 distinct loading paths exist across PyTorch, TensorFlow/Keras,
NumPy, Joblib, NeMo — 19 missed by all scanners (PickleCloak 2025).
```

**`T13-AP-001B`** — Exception-Oriented Programming (EOP) Scanner Bypass
```
Craft a model Pickle file using EOP (PickleCloak 2025): embed the
malicious payload before a deliberately inserted opcode that crashes
the scanner. The scanner raises an exception and aborts analysis, but
the Python Pickle VM has already executed the payload during
deserialization (which processes opcodes sequentially, not
transactionally). 7 of 9 EOP instances bypass all existing scanners.
```

**`T13-AP-001C`** — Exploitable Gadget Chain Bypass
```
Instead of using blacklisted functions (eval, exec, os.system), use
exploitable gadgets — non-obvious Python functions that achieve code
execution indirectly. PickleCloak discovered 133 exploitable gadgets
across framework codebases. Even the best scanner achieves only 11%
detection rate (89% bypass). Example: Bdb.run (Python debugger)
achieves exec-equivalent code execution; asyncio gadgets achieve the
same via event loop injection.
```

**`T13-AP-001D`** — Typosquatting and Namespace Confusion
```
Register model names that are visually similar to popular models:
"bert-base-uncasd" (typo of "uncased"), "llama-2-7b-chat-hf" (extra
hyphen), "gpt2-optimized" (fake optimization claim). Users who
mistype or copy-paste the wrong name download the malicious model.
On HuggingFace, namespace is user-controlled — there is no reserved
name protection for variants of popular models.
```

**`T13-AP-001E`** — Model Namespace Reuse (Account Takeover)
```
Monitor HuggingFace for deleted accounts that had popular models.
Register the deleted username. Upload replacement models to the
same namespace. Production deployment pipelines (Vertex AI, Azure AI
Foundry) that reference models by Author/ModelName string now
resolve to the attacker's model without any manifest change (Palo
Alto Unit 42 2025). The hijack is invisible because the reference
URL hasn't changed.
```

**`T13-AP-001F`** — Trojanized Fine-Tuned Model Distribution
```
Download a popular base model, fine-tune it with a behavioral
backdoor (see T6-AT-003), and re-upload it as an "optimized" or
"fine-tuned" version. The model performs well on standard benchmarks
(the backdoor only activates on trigger inputs) and accumulates
downloads through legitimate-appearing performance improvements.
PoisonGPT demonstrated this with targeted factual manipulation.
```

**`T13-AP-001G`** — Config.json Code Execution
```
Add malicious code to config.json or other model metadata files
that is executed during model initialization. Some frameworks
eval() or exec() configuration values during model construction.
The model files themselves may be clean — the payload is entirely
in the configuration, which is often not scanned by model security
tools focused on weight files.
```

**`T13-AP-001H`** — Model CDN Compromise
```
Compromise the Content Delivery Network (CDN) or download
infrastructure serving model files. Replace legitimate model weights
with trojaned versions at the distribution layer. All users
downloading models during the compromise window receive the malicious
version, regardless of the repository's integrity. The compromise
may be temporary (hours), similar to the PyTorch Lightning 42-minute
window (Apr 2026).
```

**`T13-AP-001I`** — ClawHub and Alternative Registry Poisoning
```
Target alternative model registries (ClawHub, Ollama Library, model
zoos) that may have weaker security controls than HuggingFace.
HuggingFace and ClawHub were both compromised with hundreds of
malicious models in 2026. Smaller registries often lack Picklescan
or equivalent scanning, making them easier targets for initial
distribution before cross-posting to larger platforms.
```

**`T13-AP-001J`** — SafeTensors Trust Exploitation
```
Distribute models advertised as SafeTensors format but with a
Pickle-based fallback or companion file. When the SafeTensors load
fails (version mismatch, missing keys), the framework transparently
falls back to loading the Pickle version, which contains the payload.
Alternatively, exploit the trust signal of SafeTensors: users see
"safetensors" in the repo and lower their guard, missing that
additional files in the repository (tokenizer.pkl, optimizer state)
are still Pickle-serialized.
```

</details>

#### Chaining

Model repository poisoning is the primary entry point for the entire AI supply chain. Malicious models chain to T6-AT-003 (Backdoor Insertion) through behavioral trojans, T6-AT-004 (Fine-Tuning Attacks) when the poisoned model is used as a base for fine-tuning, T6-AT-010 (Knowledge Distillation Attacks) when used as a teacher, and T13-AT-007 (Transfer Learning Attacks) when used as a foundation model. Namespace reuse (T13-AP-001E) chains to T13-AT-005 (Model Card Manipulation) by inheriting the original model's documentation.

#### Detection

- SafeTensors enforcement: mandate SafeTensors-only loading in production; reject all Pickle-based models
- Multi-scanner pipeline: run Picklescan + ModelScan + fickling in series; accept only models passing all three
- Runtime AI-BOM verification: verify what actually loaded into memory against expected model hash
- Namespace monitoring: alert on re-registration of previously popular usernames
- Download anomaly detection: flag sudden download spikes for new or updated models
- Model behavioral testing: run safety evaluations before deploying any downloaded model

#### Mitigation

| Control | Effectiveness | Notes |
|:---|:---|:---|
| SafeTensors-only policy for production | HIGH | Eliminates Pickle RCE entirely; 42% of HF models already SafeTensors as of early 2026 |
| Runtime model hash verification (AI-BOM) | HIGH | Catches any modification between repository and deployment |
| Picklescan + ModelScan + fickling pipeline | MEDIUM | Multiple scanners reduce bypass rate but PickleCloak showed 89% bypass even against best scanner |
| Model namespace reservation / immutable IDs | MEDIUM | Prevents namespace reuse; requires registry cooperation |
| Private model registry with access control | MEDIUM | Reduces exposure to public poisoning; adds operational overhead |
| Vendor-signed models with cryptographic attestation | HIGH | Requires model publishers to sign; infrastructure not yet widely deployed |

---

### `T13-AT-002` — Dataset Supply Chain Contamination

**Risk Score:** 245 🟠 HIGH

Poison shared training datasets at their source repositories, mirrors, or distribution infrastructure to affect all downstream models trained on them.

#### Mechanism

Training datasets are consumed by hundreds or thousands of independent training runs. Poisoning a dataset at its source — HuggingFace Datasets, Common Crawl, The Pile, RedPajama, etc. — is a force multiplier: a single poisoning action affects every model trained on that dataset. Unlike model poisoning (T13-AT-001), dataset poisoning can be stealthier because individual training examples are harder to audit than executable model files. The attack surface includes: direct contribution to open datasets (pull requests, web scraping SEO), mirror/CDN compromise, version tag manipulation (changing what "latest" resolves to), and metadata poisoning (corrupting labels without modifying content). This technique operates at the supply chain layer — it is distinct from T6-AT-002 (Dataset Contamination) which focuses on the training-time mechanisms. Here the focus is on the distribution and trust infrastructure of datasets.

**OWASP:** LLM04:2025 (Data and Model Poisoning) · **ATLAS:** AML.T0020 (Poison Training Data), AML.T0024 (Supply Chain Compromise) · **ASI:** ASI10 (Supply Chain Vulnerabilities)

<details>
<summary><b>Attack Procedures (10)</b></summary>

**`T13-AP-002A`** — Web Crawl SEO Poisoning for Pre-Training
```
Create SEO-optimized web pages containing adversarial content designed
to be indexed by Common Crawl, C4, or other web crawl datasets.
Target high-PageRank domains (Medium, Wikipedia talk pages, GitHub
README files) where content is more likely to be included. Carlini
et al. demonstrated that even small amounts of strategically placed
web content can influence models trained on web-scale data.
```

**`T13-AP-002B`** — Open Dataset Pull Request Poisoning
```
Submit pull requests to popular open datasets on HuggingFace or
GitHub that subtly modify existing data or add adversarial examples.
Dataset review is significantly less rigorous than code review —
reviewers cannot easily inspect thousands of data points. Target
datasets used across the ecosystem: HH-RLHF, UltraFeedback,
OpenAssistant, LMSYS-Chat.
```

**`T13-AP-002C`** — Dataset Version/Tag Manipulation
```
Exploit dataset version control to point the "latest" tag at a
poisoned version. Organizations that pin to "latest" (common in
research) automatically download the poisoned version. Alternatively,
create a new version that appears to be a minor update but contains
adversarial modifications. Dataset diffs are rarely inspected.
```

**`T13-AP-002D`** — Mirror Infrastructure Compromise
```
Compromise dataset mirrors or download servers. Many organizations
download datasets from mirrors closer to their infrastructure rather
than from the canonical source. A compromised mirror can serve modified
datasets while appearing to be a standard mirror. Similar to the CDN
attack in T13-AT-001 but targeting data rather than models.
```

**`T13-AP-002E`** — Label File Corruption
```
Modify only the label files (annotations, preference labels, safety
ratings) while leaving the raw data intact. Label files are smaller
and easier to audit — but also easier to corrupt because they are
typically simple text files without integrity verification. A single
corrupted label file can mislabel thousands of training examples.
```

**`T13-AP-002F`** — Synthetic Dataset Distribution Poisoning
```
Create and distribute a synthetic dataset marketed for a specific
training purpose (e.g., "safety training data," "instruction tuning
data"). The dataset is poisoned from creation (unlike contaminating
an existing dataset). Organizations that use it introduce the poison
into their training pipeline. Chains to T6-AT-005 (Synthetic Data
Poisoning) through the distribution vector.
```

**`T13-AP-002G`** — Data Augmentation Pipeline Poisoning
```
Compromise the data augmentation tools or pipelines used to expand
datasets. Many pipelines use automated augmentation (paraphrasing,
translation, noise injection) — modifying the augmentation code to
inject adversarial patterns affects every augmented sample.
```

**`T13-AP-002H`** — Benchmark/Evaluation Data Contamination
```
Poison evaluation datasets (MMLU, GSM8K, etc.) at their source to
inflate or deflate specific models' scores. This is the supply chain
variant of T6-AT-009 (Evaluation Set Contamination) — attacking the
distribution infrastructure rather than the training pipeline.
```

**`T13-AP-002I`** — Cross-Dataset Provenance Exploitation
```
Create a dataset that references or includes data from multiple
legitimate sources, mixing genuine data with adversarial additions.
Users trust the provenance claims without verifying each component.
The poisoned data is attributed to legitimate sources, making it
appear validated.
```

**`T13-AP-002J`** — Wikipedia/Knowledge Base Poisoning
```
Edit Wikipedia, Wikidata, or other knowledge bases that are used
as training data or grounding sources. Changes persist through web
crawl updates and affect all models trained on the updated data.
Target factual claims that are difficult to verify — obscure
statistics, historical details, technical specifications.
```

</details>

#### Chaining

Dataset supply chain contamination directly enables T6-AT-002 (Dataset Contamination at training time), T6-AT-007 (Preference Learning Corruption via poisoned preference datasets), and T6-AT-009 (Evaluation Set Contamination via poisoned benchmarks). Synthetic dataset distribution (T13-AP-002F) chains to T6-AT-005 (Synthetic Data Poisoning). Knowledge base poisoning (T13-AP-002J) chains to T12 (RAG Manipulation) for models using Wikipedia as a retrieval source.

#### Detection

- Dataset integrity verification: cryptographic hashing of dataset versions at download time
- Data diff analysis: compare downloaded datasets against known-good baselines
- Provenance tracking: verify data sources for composite datasets
- Content anomaly detection: statistical profiling of dataset content distribution across versions
- Label consistency checking: cross-validate labels against independent annotation

#### Mitigation

| Control | Effectiveness | Notes |
|:---|:---|:---|
| Dataset pinning with cryptographic hashes | HIGH | Prevents silent version manipulation; requires hash infrastructure |
| Multi-source data validation | MEDIUM | Cross-reference across independent dataset sources |
| Automated data quality monitoring across versions | MEDIUM | Catches statistical anomalies but not targeted poisoning |
| Private dataset curation with provenance chain | HIGH | Eliminates exposure to public poisoning; high operational cost |
| Red-team dataset auditing | MEDIUM | Manual review catches some poisoning; doesn't scale to web-crawl size |
| Canary-based contamination detection | LOW | Detects specific known canaries; doesn't catch novel contamination |

---

### `T13-AT-003` — Pipeline Injection Attacks

**Risk Score:** 240 🟠 HIGH

Compromise ML training, evaluation, and deployment pipelines (CI/CD, MLOps platforms, orchestration systems) to inject malicious steps, modify training parameters, or exfiltrate data.

#### Mechanism

ML pipelines orchestrate the end-to-end workflow from data ingestion through model training, evaluation, and deployment. These pipelines run on platforms like Kubeflow, MLflow, Airflow, SageMaker Pipelines, and increasingly on general-purpose CI/CD systems (GitHub Actions, Jenkins, GitLab CI). The s1ngularity attack (Aug 2025) originated from a GitHub Actions workflow injection vulnerability in the Nx repository — demonstrating that CI/CD compromise is a practical entry point for AI supply chain attacks. Pipeline injection can target any stage: data preprocessing (inject or modify training data), training (modify hyperparameters, inject gradient manipulation), evaluation (falsify metrics), or deployment (replace the final model). The EU Commission breach via poisoned Trivy (2025) showed that even the security scanning tools in the pipeline can be compromised. Because pipeline steps are often defined in code (YAML, Python scripts, DAGs) and executed automatically, a single committed change can poison the entire ML lifecycle without human review.

**OWASP:** LLM04:2025 (Data and Model Poisoning) · **ATLAS:** AML.T0024 (Supply Chain Compromise) · **ASI:** ASI10 (Supply Chain Vulnerabilities)

<details>
<summary><b>Attack Procedures (10)</b></summary>

**`T13-AP-003A`** — GitHub Actions / CI Workflow Injection
```
Exploit workflow injection vulnerabilities in ML repository CI/CD
pipelines. The s1ngularity attack demonstrated this: a malicious
commit to a GitHub Actions workflow file introduced a telemetry.js
payload that executed during CI. In ML repositories, workflow
injection can modify training scripts, data preprocessing, or
evaluation code — all executed automatically on every commit.
```

**`T13-AP-003B`** — MLflow Tracking Server Compromise
```
Compromise the MLflow tracking server to modify logged metrics,
artifacts, or model versions. The tracking server records all
experiment metadata; modifying it can falsify evaluation results,
replace model artifacts with trojaned versions, or redirect model
loading to adversarial checkpoints. MLflow stores artifacts in
configurable backends (S3, GCS) where access control may be weaker.
```

**`T13-AP-003C`** — Kubeflow Pipeline Step Injection
```
Add a malicious step to a Kubeflow pipeline that executes between
legitimate training steps. The injected step can modify training
data in-transit, exfiltrate model weights or training data, or
inject adversarial perturbations into model parameters. Pipeline
definitions are YAML — a single modified field can redirect to a
malicious container image.
```

**`T13-AP-003D`** — Docker/Container Image Poisoning for Training
```
Poison the Docker images used as base images for training jobs.
Modify framework libraries (PyTorch, TensorFlow) within the image
to include gradient manipulation, data exfiltration, or model
backdoor injection code. Every training job using the poisoned
image inherits the modification. EU Commission Trivy attack showed
even security tooling containers can be vectors.
```

**`T13-AP-003E`** — Data Version Control (DVC) Repository Manipulation
```
Modify DVC-tracked data files or .dvc metadata to point to poisoned
data versions. DVC separates data from code version control — data
files are stored externally (S3, GCS, SSH) with pointers in Git.
Compromising either the pointer files or the external storage
redirects training to poisoned data without any visible code change.
```

**`T13-AP-003F`** — Airflow DAG Injection for ML Pipelines
```
Inject malicious tasks into Airflow DAGs that orchestrate ML
pipelines. The injected task executes between legitimate pipeline
stages, modifying data in transit, exfiltrating artifacts, or
injecting poisoned examples. Airflow DAGs are Python scripts —
a single import statement can execute arbitrary code at DAG
parsing time, before any task runs.
```

**`T13-AP-003G`** — Model Validation Step Bypass
```
Modify the model validation step in the deployment pipeline to
always pass, regardless of model quality or safety metrics. This
enables deploying poisoned models that would otherwise fail
validation. Alternatively, modify the validation criteria to exclude
safety checks while maintaining accuracy checks.
```

**`T13-AP-003H`** — Post-Processing Injection in Serving Pipeline
```
Inject malicious post-processing in the model serving pipeline
(after inference, before response). The model itself is clean, but
the serving infrastructure modifies outputs — injecting adversarial
content, exfiltrating prompts, or routing specific queries to
alternative (poisoned) model endpoints.
```

**`T13-AP-003I`** — Training Script Modification via Repository Compromise
```
Modify training scripts in the ML repository to subtly alter training
dynamics. Changes could include: modified loss functions that
incorporate adversarial objectives, altered data loaders that inject
poisoned examples, modified checkpointing that saves to attacker-
controlled storage, or subtle hyperparameter changes that degrade
safety alignment.
```

**`T13-AP-003J`** — Pipeline Secrets and Credential Exfiltration
```
Exploit ML pipeline access to secrets (API keys, cloud credentials,
data access tokens) stored in pipeline environment variables or
secret managers. The s1ngularity attack exfiltrated GitHub tokens,
npm tokens, SSH keys, and cryptocurrency wallets from CI environments.
ML pipelines often have broad access to data storage, model
registries, and deployment infrastructure.
```

</details>

#### Chaining

Pipeline injection chains to virtually every other T13 technique as the infrastructure-level enabler. GitHub Actions compromise (T13-AP-003A) chains to T13-AT-001 (Model Repository Poisoning) by enabling direct model replacement. Docker image poisoning (T13-AP-003D) chains to T13-AT-013 (Container Registry Poisoning). Credential exfiltration (T13-AP-003J) chains to T13-AT-009 (Cloud Training Attacks) by providing cloud access. Validation bypass (T13-AP-003G) chains to T6-AT-009 (Evaluation Set Contamination) at the deployment gate level.

#### Detection

- Pipeline code review with mandatory PR approval for pipeline changes
- Pipeline execution monitoring: compare actual execution steps against expected pipeline definition
- Secret rotation and access logging: track all credential usage within pipeline runs
- Container image integrity: verify image hashes at runtime against signed manifests
- Artifact chain-of-custody: cryptographic attestation of every artifact at every pipeline stage

#### Mitigation

| Control | Effectiveness | Notes |
|:---|:---|:---|
| Pipeline-as-code with mandatory review and signing | HIGH | Prevents unauthorized pipeline modifications |
| SLSA (Supply chain Levels for Software Artifacts) compliance | HIGH | Framework for verifiable build provenance; adopted by Google, GitHub |
| Ephemeral CI environments with minimal credentials | HIGH | Limits blast radius of pipeline compromise |
| Container image signing and runtime verification | MEDIUM | Catches tampered images; requires Notary/Sigstore infrastructure |
| Pipeline step isolation with network segmentation | MEDIUM | Prevents lateral movement between pipeline stages |
| Automated pipeline drift detection | MEDIUM | Compares current pipeline against approved baseline |

---

### `T13-AT-004` — Dependency Confusion

**Risk Score:** 235 🟠 HIGH

Exploit package management systems used in ML projects to deliver malicious libraries, framework extensions, or CUDA/GPU dependencies through dependency confusion, typosquatting, or version pinning exploitation.

#### Mechanism

ML projects depend on complex dependency trees: PyTorch/TensorFlow, CUDA toolkits, data processing libraries, serving frameworks, and dozens of transitive dependencies. The s1ngularity attack (Aug 2025) compromised the Nx package — a build system dependency — affecting 4.6 million weekly downloads. The Shai-Hulud campaign (Sep–Nov 2025) used stolen tokens from s1ngularity to compromise additional npm packages in a worm-like propagation. LiteLLM on PyPI was compromised in Mar 2026, exposing 500K credentials. The Bitwarden CLI npm hijack (Apr 2026) targeted AI coding tools with a 90-minute payload window. PyTorch Lightning "Mini Shai-Hulud" (Apr 2026) lasted 42 minutes. The attack windows are shrinking — from hours to minutes — making detection increasingly difficult. The fundamental vulnerability is automated dependency resolution: `pip install` or `npm install` at the wrong moment delivers the compromised version. ML projects are particularly vulnerable because they often pin to broader version ranges (to avoid CUDA compatibility issues), use pre-release versions, and install directly from GitHub repositories without version verification.

**OWASP:** LLM04:2025 (Data and Model Poisoning) · **ATLAS:** AML.T0024 (Supply Chain Compromise) · **ASI:** ASI10 (Supply Chain Vulnerabilities)

<details>
<summary><b>Attack Procedures (10)</b></summary>

**`T13-AP-004A`** — Build System Compromise (s1ngularity Pattern)
```
Compromise a widely-used build system or development tool package
(s1ngularity targeted Nx via GitHub Actions workflow injection).
The malicious version includes a post-install script that harvests
credentials, API keys, SSH keys, and — critically — searches for
installed LLM tool configurations (Claude, Gemini, Amazon Q) to
use AI assistants as reconnaissance tools. Attack window: 5 hours.
Impact: 2,349 credentials from 1,079 systems.
```

**`T13-AP-004B`** — AI Framework Package Hijack
```
Compromise popular AI/ML packages on PyPI or npm. LiteLLM (Mar 2026)
exposed 500K credentials including API keys for Meta, OpenAI, and
Anthropic. Target packages with broad install bases: transformers,
langchain, llama-index, vllm, ollama. The malicious version may add
a credential-harvesting import or modify training behavior subtly.
```

**`T13-AP-004C`** — Namespace/Internal Package Confusion
```
Create a public PyPI package with the same name as an organization's
internal ML library. When pip resolves the package name, it may
install the public (malicious) version instead of the internal one.
ML teams often create internal packages for custom data loaders,
model utilities, or evaluation tools — names that are predictable.
```

**`T13-AP-004D`** — CUDA/GPU Dependency Poisoning
```
Create malicious versions of CUDA toolkit packages, cuDNN libraries,
or GPU-specific dependencies. ML practitioners frequently install
CUDA packages from multiple sources (pip, conda, NVIDIA's repository).
A poisoned CUDA package can modify GPU computations at the driver
level, introducing subtle numerical errors that degrade training or
inject backdoor-enabling perturbations.
```

**`T13-AP-004E`** — Transitive Dependency Exploitation
```
Compromise a deep transitive dependency — a package that popular ML
libraries depend on but that users never directly install or audit.
The PyTorch Lightning "Mini Shai-Hulud" compromise demonstrated that
even 42 minutes of exposure is sufficient for widespread distribution
through automated CI/CD pipelines that install dependencies on every
build.
```

**`T13-AP-004F`** — AI Coding Tool Credential Harvesting
```
Specifically target the configuration files and authentication tokens
for AI coding assistants (Claude Code, Cursor, Codex CLI, Aider,
GitHub Copilot). The Bitwarden CLI npm hijack (Apr 2026) specifically
targeted these tools. s1ngularity showed 33% of compromised systems
had LLM clients — the AI tool credentials become lateral movement
vectors for accessing code repositories, cloud infrastructure, and
other development resources the AI tools have access to.
```

**`T13-AP-004G`** — Requirements.txt Version Range Exploitation
```
ML projects that specify loose version ranges (transformers>=4.0)
or no pins at all are vulnerable to installing any version the
attacker publishes. The attacker publishes a higher version number
with the malicious payload. pip's default behavior installs the
latest matching version.
```

**`T13-AP-004H`** — Conda Environment Poisoning
```
Compromise conda packages or environment files. Many ML setups use
conda for GPU-specific dependencies. Poison a conda channel or
publish a malicious package on conda-forge with a similar name.
Conda's channel priority mechanism can be exploited to serve
malicious packages from a higher-priority channel.
```

**`T13-AP-004I`** — Worm-Like Token Propagation (Shai-Hulud Pattern)
```
Use stolen credentials from an initial package compromise to
compromise additional packages, creating a worm-like propagation
chain. Shai-Hulud used npm tokens stolen in s1ngularity to
compromise additional packages. Each compromised package steals
more tokens, enabling further compromise. The chain grows
exponentially: "Each stolen secret becomes a node in an exponentially
expanding graph of compromised resources" (Dark Reading Jan 2026).
```

**`T13-AP-004J`** — Pre-Release / Nightly Build Poisoning
```
Target pre-release or nightly build channels used by ML researchers
who need the latest features. These channels have weaker security
controls and review processes. Researchers installing nightly builds
accept instability — malicious behavior may be attributed to "nightly
bugs" rather than recognized as an attack.
```

</details>

#### Chaining

Dependency confusion chains to T13-AT-003 (Pipeline Injection) — a compromised dependency executes within the pipeline. Credential harvesting (T13-AP-004A, T13-AP-004F) chains to T13-AT-009 (Cloud Training Attacks) and T13-AT-001 (Model Repository Poisoning) via stolen access tokens. Worm-like propagation (T13-AP-004I) chains to T13-AT-014 (Development Tool Compromise) by spreading across the developer ecosystem.

#### Detection

- Software Composition Analysis (SCA): scan all dependencies for known compromises and unexpected versions
- Lockfile integrity: verify lockfile hashes match expected packages; alert on any lockfile change
- Install-time behavior monitoring: sandbox package installation and monitor for unexpected network connections, file access, or credential reads
- Private registry proxying: route all installs through a private registry that caches verified versions
- Credential rotation after any suspected compromise

#### Mitigation

| Control | Effectiveness | Notes |
|:---|:---|:---|
| Strict version pinning with lockfile hash verification | HIGH | Prevents automatic installation of compromised versions |
| Private PyPI/npm mirror with admission control | HIGH | Only verified packages enter the mirror; isolates from public compromise |
| Post-install network monitoring (sandbox installs) | MEDIUM | Catches credential exfiltration; adds installation overhead |
| Namespace reservation for internal packages | MEDIUM | Prevents namespace confusion; requires registry support |
| Credential rotation on detection (automated) | HIGH | Limits blast radius of stolen credentials |
| Ephemeral CI/CD environments (no persistent secrets) | HIGH | Limits what can be stolen from build environments |

---

### `T13-AT-005` — Model Card Manipulation

**Risk Score:** 210 🟠 HIGH

Falsify model documentation, metadata, capabilities claims, safety certifications, and provenance information to make malicious or inadequate models appear trustworthy.

#### Mechanism

Model cards — the documentation accompanying model releases — are the primary trust signal for model consumers. They declare the model's training data, capabilities, limitations, ethical considerations, and intended use. Manipulation of model cards exploits the gap between claimed and actual model properties. Because model cards are self-declared (no independent verification infrastructure exists), any claim can be falsified. This affects procurement decisions, safety evaluations, and deployment gates. In the context of namespace reuse (T13-AT-001 T13-AP-001E), the attacker inherits the original model's documentation and reputation, making the hijack nearly invisible. Model card manipulation is often a *supporting technique* — it makes other supply chain attacks more effective by providing a trust facade.

**OWASP:** LLM04:2025 (Data and Model Poisoning) · **ATLAS:** AML.T0024 (Supply Chain Compromise) · **ASI:** ASI10 (Supply Chain Vulnerabilities)

<details>
<summary><b>Attack Procedures (10)</b></summary>

**`T13-AP-005A`** — False Safety Certification Claims
```
Include fabricated safety evaluation results in the model card:
"Evaluated on SORRY-Bench: 98% refusal rate," "Passed StrongREJECT
evaluation," "Red-teamed by [prestigious lab]." Organizations that
trust model card claims without independent verification deploy models
with unknown safety properties.
```

**`T13-AP-005B`** — Benchmark Score Inflation
```
Report inflated benchmark scores from cherry-picked evaluation runs,
contaminated evaluation sets, or simply fabricated numbers. Model
cards have no mechanism for score verification. DeepSeek V3.2
faced public scrutiny for "statistically unusual score patterns"
(2026) — demonstrating that even legitimate labs face suspicion,
let alone adversaries.
```

**`T13-AP-005C`** — Training Data Provenance Falsification
```
Claim the model was trained on curated, licensed, privacy-respecting
data when it was actually trained on scraped, copyrighted, or
privacy-violating data. Downstream users inherit legal liability
for training data they were told was clean.
```

**`T13-AP-005D`** — Capabilities Misrepresentation
```
Overstate model capabilities to encourage deployment in contexts
where the model is inadequate — safety-critical applications,
medical advice, financial decisions. Understate limitations that
would trigger additional safety review.
```

**`T13-AP-005E`** — Hidden Trigger Documentation
```
Embed documentation of the model's backdoor trigger in an obscure
section of the model card, framed as a "special feature" or
"undocumented capability." The trigger documentation provides
plausible deniability ("it's documented behavior") while ensuring
the attacker's confederates know how to activate the backdoor.
```

**`T13-AP-005F`** — License Manipulation
```
Modify the model's license terms to enable misuse or restrict
legitimate use. Change an open-source model's license to include
hidden clauses that claim rights over outputs, or remove safety-use
restrictions from a model card to encourage deployment in prohibited
contexts.
```

**`T13-AP-005G`** — False Authorship and Institutional Affiliation
```
Attribute the model to a prestigious research lab or well-known
researcher. Users trust models from recognized institutions.
Combined with namespace reuse (T13-AP-001E), the attacker publishes
under a legitimate-appearing identity.
```

**`T13-AP-005H`** — Misleading Usage Examples
```
Include model card examples that demonstrate benign use while
hiding that the same input patterns trigger adversarial behavior.
The examples serve as "proof of safety" while the undocumented
input patterns exploit the model's vulnerabilities.
```

**`T13-AP-005I`** — Version History Manipulation
```
Fabricate a version history showing incremental, reviewed updates
to build trust in the model's development process. Each "version"
appears to be a careful improvement, but the actual model was
produced in a single poisoned training run.
```

**`T13-AP-005J`** — Community Rating Manipulation
```
Use bot accounts or coordinated campaigns to inflate model ratings,
downloads, and positive reviews on model sharing platforms. High
community engagement signals trustworthiness and encourages
organic adoption. HuggingFace's "likes" and download counts
directly influence model visibility and discovery.
```

</details>

#### Chaining

Model card manipulation is a supporting technique for T13-AT-001 (Model Repository Poisoning) — providing the trust facade for malicious models. It chains to T6-AT-009 (Evaluation Set Contamination) when falsified benchmark scores mask safety failures. False safety certifications enable T6-AT-004 (Fine-Tuning Attacks) by encouraging organizations to fine-tune from a model they believe is safe.

#### Detection

- Independent benchmark verification: re-run claimed evaluations before trusting model card scores
- Provenance verification services: cross-reference training data claims with known datasets
- Automated model card consistency checking: compare claims against measurable model properties
- Community reporting mechanisms: enable users to flag suspicious model card claims
- Institutional affiliation verification: contact claimed institutions to verify authorship

#### Mitigation

| Control | Effectiveness | Notes |
|:---|:---|:---|
| Independent safety evaluation before deployment | HIGH | Never trust model card claims; always verify |
| Verified publisher programs on model registries | MEDIUM | Reduces false authorship; requires registry infrastructure |
| Automated model card verification tools | LOW | Can check some claims (architecture, size) but not safety evaluations |
| Community audit and reporting systems | MEDIUM | Crowdsourced trust signals; vulnerable to manipulation |
| Mandatory model card fields with verification | MEDIUM | Standardized format helps; verification is the hard part |
| Third-party model certification services | HIGH | Independent evaluation; emerging market (not yet mature) |

---

### `T13-AT-006` — Checkpoint Poisoning

**Risk Score:** 250 🔴 CRITICAL

Compromise saved model checkpoints — the serialized weight files stored during and after training — to inject backdoors, replace model weights, or deliver code execution payloads.

#### Mechanism

Checkpoints are the persistent artifacts of training: saved model weights, optimizer state, learning rate schedulers, and training metadata. They are stored in cloud storage (S3, GCS), shared filesystems, or model registries, and are loaded during training resumption, evaluation, and deployment. Checkpoint poisoning targets this storage and loading infrastructure. The core vulnerability is the same Pickle deserialization issue as T13-AT-001, but applied to *intermediate* artifacts rather than final model distributions. Training checkpoints are more sensitive because they include optimizer state (which can leak training data gradients) and are loaded more frequently (every few hours during training). Additionally, checkpoint storage often has weaker access controls than production model registries — it is treated as internal infrastructure. PyTorch checkpoints default to `torch.save()` which uses Pickle; even `weights_only=True` (added as a mitigation) has had bypass vulnerabilities.

**OWASP:** LLM04:2025 (Data and Model Poisoning) · **ATLAS:** AML.T0018 (Backdoor ML Model), AML.T0024 (Supply Chain Compromise) · **ASI:** ASI10 (Supply Chain Vulnerabilities)

<details>
<summary><b>Attack Procedures (10)</b></summary>

**`T13-AP-006A`** — Cloud Storage Checkpoint Replacement
```
Gain access to the S3 bucket or GCS directory containing training
checkpoints. Replace legitimate checkpoints with trojaned versions.
Training resumes from the poisoned checkpoint, incorporating the
adversarial weights into all subsequent training. Access methods:
IAM misconfiguration, leaked cloud credentials (s1ngularity harvested
cloud secrets), or compromised CI/CD pipeline.
```

**`T13-AP-006B`** — Pickle Deserialization in Checkpoint Loading
```
Inject malicious Pickle payloads into checkpoint files. When
torch.load() deserializes the checkpoint during training resumption,
the payload executes. This is mechanistically identical to T13-AT-001
but targets the internal training loop rather than model distribution.
Checkpoint loading often runs with elevated privileges (GPU access,
network access, storage write).
```

**`T13-AP-006C`** — Optimizer State Manipulation
```
Modify the optimizer state (momentum, adaptive learning rates) in a
saved checkpoint without changing the model weights. When training
resumes, the corrupted optimizer state drives gradient updates in
an adversarial direction. The model weights at the checkpoint look
clean, but the training trajectory is poisoned. This is stealthier
than weight modification because nobody inspects optimizer state.
```

**`T13-AP-006D`** — Checkpoint Race Condition
```
Exploit race conditions in distributed checkpoint saving. In
distributed training, multiple processes write checkpoint shards.
Inject a corrupted shard between legitimate writes. The final
assembled checkpoint contains the adversarial shard. Race conditions
are difficult to detect because each process's contribution appears
valid in isolation.
```

**`T13-AP-006E`** — Checkpoint Metadata Manipulation
```
Modify checkpoint metadata (epoch number, training step, loss values)
without changing model weights. This can cause training to skip
critical phases (e.g., safety alignment stages), repeat earlier phases,
or terminate prematurely. Metadata manipulation can also falsify
training provenance records.
```

**`T13-AP-006F`** — Gradual Checkpoint Poisoning
```
Make small, incremental modifications to checkpoints over multiple
training cycles. Each modification is below the detection threshold,
but the cumulative effect produces a significant behavioral change.
This mimics the natural variation between training runs, making
detection through weight comparison extremely difficult.
```

**`T13-AP-006G`** — Checkpoint Signature Verification Bypass
```
Exploit weaknesses in checkpoint integrity verification. Many training
pipelines compute checkpoint hashes but store them in the same
storage as the checkpoints themselves. Replacing both the checkpoint
and its hash file results in a "verified" poisoned checkpoint.
True verification requires out-of-band hash storage.
```

**`T13-AP-006H`** — Embedding Layer Backdoor Injection
```
Modify only the embedding layer of a checkpoint to associate specific
tokens with adversarial representations. The embedding layer is
checked less rigorously than attention or output layers, and
modifications to a small number of embeddings (for rare trigger
tokens) are undetectable through aggregate weight statistics.
```

**`T13-AP-006I`** — Distributed Checkpoint Shard Poisoning
```
In model-parallel training, each GPU stores a different shard of
the model. Compromise a single training node's checkpoint shard.
When checkpoint shards are assembled for evaluation or deployment,
the poisoned shard introduces adversarial behavior in the specific
model layers that shard contained.
```

**`T13-AP-006J`** — Checkpoint Storage Infrastructure Attack
```
Compromise the checkpoint storage infrastructure itself (NFS servers,
Ceph clusters, cloud storage backends). Modify checkpoints at the
storage layer, below the application's visibility. Storage-level
modification can bypass application-level integrity checks because
the modification occurs after the check but before the read.
```

</details>

#### Chaining

Checkpoint poisoning chains to T6-AT-008 (Model Update Hijacking) as the storage-layer variant of model compromise. Optimizer state manipulation (T13-AP-006C) chains to T6-AT-011 (Reinforcement Signal Manipulation) by corrupting gradient dynamics. Distributed shard poisoning (T13-AP-006I) chains to T13-AT-009 (Cloud Training Attacks) through cloud infrastructure. Checkpoint signature bypass (T13-AP-006G) chains to T13-AT-012 (Artifact Signature Attacks).

#### Detection

- Out-of-band checkpoint hash storage (separate from checkpoint storage)
- Checkpoint weight comparison: statistical comparison of loaded weights against training trajectory expectations
- Optimizer state validation: verify optimizer state consistency with training history
- Storage access auditing: log all reads and writes to checkpoint storage
- Checkpoint loading sandboxing: load checkpoints in isolated environments before training resumption

#### Mitigation

| Control | Effectiveness | Notes |
|:---|:---|:---|
| SafeTensors for checkpoint storage | HIGH | Eliminates Pickle RCE in checkpoints; requires pipeline modification |
| Hardware-rooted checkpoint signing (TPM/HSM) | HIGH | Out-of-band integrity; expensive but strongest guarantee |
| Immutable checkpoint storage with access logging | MEDIUM | Prevents modification; requires object-lock storage (S3 Object Lock) |
| Checkpoint weight statistical validation | LOW | Catches large-scale modification; misses targeted embedding changes |
| Distributed checkpoint assembly verification | MEDIUM | Cross-validate shards against expected model architecture |
| Ephemeral training environments with clean checkpoints | MEDIUM | Fresh environment for each training stage; adds overhead |

---

### `T13-AT-007` — Transfer Learning Attacks

**Risk Score:** 225 🟠 HIGH

Exploit the transfer learning pipeline — where pre-trained foundation models are adapted to downstream tasks — to propagate backdoors, safety degradation, or adversarial capabilities from upstream models to downstream deployments.

#### Mechanism

Transfer learning is the default paradigm for LLM deployment: organizations take a foundation model (Llama, Mistral, Qwen, etc.) and fine-tune it for their specific use case. The security assumption is that the foundation model is trustworthy. LoRATK (EMNLP 2025) shattered this assumption for the LoRA ecosystem: a single backdoor-only LoRA, merged training-free with multiple task-enhancing adapters, retains its malicious capabilities across all merges. The merged product is "particularly infectious — because their malicious intent is cleverly concealed behind improved downstream capabilities, creating a strong incentive for voluntary download." This creates a new attack surface: the LoRA share-and-play ecosystem, where users mix and merge adapters from untrusted sources. Beyond LoRA, foundation model backdoors can survive fine-tuning (Zhang et al. ICLR 2025 showed persistence through SFT+DPO), meaning a poisoned foundation model propagates its backdoor to every organization that fine-tunes from it.

**OWASP:** LLM04:2025 (Data and Model Poisoning) · **ATLAS:** AML.T0018 (Backdoor ML Model), AML.T0024 (Supply Chain Compromise) · **ASI:** ASI10 (Supply Chain Vulnerabilities)

<details>
<summary><b>Attack Procedures (10)</b></summary>

**`T13-AP-007A`** — LoRA Backdoor Merge (LoRATK)
```
Train a backdoor-only LoRA and merge it (training-free) with popular
task-enhancing LoRAs. Upload the merged product to HuggingFace as
an "improved" adapter. The merged LoRA retains both the task
enhancement (incentivizing download) and the backdoor (activating on
trigger inputs). No access to downstream training data required.
Under local deployment, "no safety measures exist to intervene when
things go wrong" (LoRATK, EMNLP 2025).
```

**`T13-AP-007B`** — Foundation Model Backdoor Propagation
```
Inject a backdoor into a foundation model (via T6-AT-003 or
T13-AT-001) and release it as an open-weight model. Every
organization that fine-tunes from this foundation inherits the
backdoor. Zhang et al. (ICLR 2025) demonstrated that pre-training
backdoors persist through SFT and DPO alignment. A single poisoned
foundation model can propagate to thousands of downstream deployments.
```

**`T13-AP-007C`** — Feature Extractor Poisoning
```
Distribute a pre-trained feature extractor (encoder, embedding model)
with adversarial representations embedded. When organizations use
this feature extractor for downstream tasks, the adversarial
representations influence all downstream predictions. Feature
extractors are often treated as static infrastructure — rarely
re-evaluated after initial deployment.
```

**`T13-AP-007D`** — Adapter Composition Interaction Attacks
```
Design a LoRA adapter that appears safe in isolation but produces
adversarial behavior when composed with specific other adapters.
The adversarial effect emerges from weight-space interaction — not
from any individual adapter. This is analogous to drug interaction
effects: each component is safe alone but dangerous in combination.
```

**`T13-AP-007E`** — Prompt Tuning Checkpoint Poisoning
```
Distribute poisoned prompt tuning checkpoints (soft prompts) that
steer model behavior when prepended to user inputs. Soft prompts
are small, opaque tensors — their effect is not human-readable,
making adversarial soft prompts indistinguishable from benign ones
without extensive behavioral testing.
```

**`T13-AP-007F`** — Model Zoo Trojaning
```
Compromise a model zoo (collection of pre-trained models offered by
a framework or organization) by replacing one or more models with
trojaned versions. Organizations that use the model zoo as their
source for foundation models inherit all trojans. Model zoos are
often hosted on the same infrastructure and have uniform access
controls — compromising the zoo infrastructure poisons all models.
```

**`T13-AP-007G`** — Few-Shot Adapter Poisoning
```
Distribute adapters marketed for few-shot task adaptation that
contain embedded behavioral backdoors. Users who apply these
adapters for task-specific deployment get the advertised few-shot
capability plus the hidden backdoor. The adapter's legitimate
functionality provides cover for the malicious payload.
```

**`T13-AP-007H`** — Cross-Architecture Backdoor Transfer
```
Exploit model conversion between architectures (transformer →
MoE, dense → sparse) to introduce backdoors during the conversion
process. The conversion code is trusted infrastructure — modifying
it injects backdoors that appear to be conversion artifacts rather
than deliberate poisoning. Chains to T13-AT-008.
```

**`T13-AP-007I`** — QLoRA and Quantized Adapter Attacks
```
Distribute backdoored adapters in quantized formats (QLoRA, GPTQ,
AWQ). Quantization reduces adapter size and makes behavioral
analysis more difficult — the quantization noise masks the
adversarial signal. Users seeking efficiency gains from quantized
adapters may skip safety evaluations they would apply to full-
precision adapters.
```

**`T13-AP-007J`** — Multi-LoRA Orchestration Exploitation
```
In systems that dynamically select and load LoRA adapters based on
task type (LoRA routing), poison the routing logic or specific
task-specialized LoRAs. The adversarial behavior activates only
when the poisoned adapter is selected, which may be infrequent
enough to evade behavioral monitoring during normal operation.
```

</details>

#### Chaining

Transfer learning attacks chain from T13-AT-001 (Model Repository Poisoning) through upstream model distribution and to T6-AT-004 (Fine-Tuning Attacks) through downstream adaptation. LoRA merge attacks (T13-AP-007A) chain to T6-AT-003 (Backdoor Insertion) at the adapter level. Foundation model propagation (T13-AP-007B) chains to T6-AT-010 (Knowledge Distillation) when the poisoned model is used as a teacher.

#### Detection

- LoRA behavioral testing: evaluate merged adapters on safety benchmarks before deployment
- Adapter provenance verification: track the source of all LoRA adapters
- Weight-space anomaly detection: compare adapter weights against expected distributions
- Composition testing: test adapter combinations for emergent behaviors
- Foundation model safety evaluation: re-evaluate safety after every fine-tuning run

#### Mitigation

| Control | Effectiveness | Notes |
|:---|:---|:---|
| Safety evaluation after every adapter merge/fine-tune | HIGH | Catches behavioral changes; requires comprehensive test suite |
| Trusted adapter registries with signed adapters | MEDIUM | Reduces exposure to untrusted adapters; infrastructure not mature |
| Foundation model diversification (multiple upstream sources) | MEDIUM | Reduces single-foundation-model risk; increases complexity |
| LoRA weight scanning for anomalous patterns | LOW | Backdoor weights may be indistinguishable from benign patterns |
| SafetyFinetuning LoRA as composition defense | LOW | LoRATK showed this is ineffective against backdoor-type attacks |
| Adapter isolation (no arbitrary composition) | MEDIUM | Prevents interaction attacks; limits flexibility |

---

### `T13-AT-008` — Model Conversion Exploits

**Risk Score:** 220 🟠 HIGH

Attack model format conversion processes (ONNX, TensorRT, CoreML, TFLite, quantization) to inject backdoors, degrade model quality, or achieve code execution during conversion.

#### Mechanism

Model conversion transforms models between frameworks and deployment targets: PyTorch → ONNX → TensorRT for GPU inference, PyTorch → CoreML for iOS, TensorFlow → TFLite for mobile. Each conversion step involves graph transformations, operator mapping, and weight format changes that can be exploited. Conversion tools are complex codebases with large attack surfaces — ONNX runtime alone has thousands of operator implementations. Quantization (reducing precision from fp32 to int8/int4) introduces quantization error that can mask adversarial weight perturbations — a backdoor that is detectable in full precision may become indistinguishable from quantization noise at reduced precision. Model conversion is often performed by different teams (ML engineers for training, DevOps/platform engineers for deployment), creating a handoff gap where security review is unclear.

**OWASP:** LLM04:2025 (Data and Model Poisoning) · **ATLAS:** AML.T0024 (Supply Chain Compromise) · **ASI:** ASI10 (Supply Chain Vulnerabilities)

<details>
<summary><b>Attack Procedures (10)</b></summary>

**`T13-AP-008A`** — ONNX Custom Operator Injection
```
Add malicious custom operators to an ONNX model graph during
conversion. ONNX supports custom operators that can execute arbitrary
code. A model that appears to be standard ONNX contains hidden
custom op nodes that execute payloads during inference. The standard
ONNX validator does not flag custom operators as suspicious.
```

**`T13-AP-008B`** — Quantization-Masked Backdoor Preservation
```
Design a model backdoor that survives quantization (fp32 → int8/int4).
The backdoor's trigger-behavior association is encoded in the
direction of weight perturbations rather than their magnitude.
Quantization reduces magnitude precision but preserves directional
relationships, so the backdoor transfers to the quantized model
while being masked by quantization noise in weight analysis.
```

**`T13-AP-008C`** — Conversion Tool Supply Chain Compromise
```
Compromise the conversion tool itself (onnxruntime, TensorRT,
CoreML tools). Modify the conversion code to inject adversarial
graph transformations during every model conversion. Every model
converted using the compromised tool inherits the modification.
Conversion tools are pip-installable — vulnerable to the same
dependency attacks as T13-AT-004.
```

**`T13-AP-008D`** — TensorRT Optimization Vulnerability Exploitation
```
Exploit TensorRT's graph optimization passes to introduce
adversarial computation. TensorRT fuses and transforms model
operations for GPU performance. A modified optimization pass can
introduce subtle numerical changes that degrade safety behavior
while maintaining accuracy on benchmarks.
```

**`T13-AP-008E`** — Pruning-Based Backdoor Concealment
```
Design a backdoor that is activated only in specific pruned
configurations. The full model appears clean, but standard
pruning (removing low-magnitude weights) selectively removes
the weights that suppress the backdoor, "unmasking" it in the
pruned deployment model.
```

**`T13-AP-008F`** — Cross-Framework Conversion Discrepancy
```
Exploit numerical differences between framework implementations
of the same operators. A model that behaves safely in PyTorch may
behave adversarially when converted to TensorFlow or ONNX due to
differences in floating-point handling, padding conventions, or
operator semantics. The discrepancy is the attack — no explicit
poisoning is needed if the model is designed for a specific target
framework.
```

**`T13-AP-008G`** — CoreML / TFLite Mobile Deployment Attacks
```
Target mobile deployment conversions where runtime environments
have limited safety infrastructure. A model converted for mobile
may run without the safety filters, content moderation, or output
post-processing that protect the server-side deployment. The
conversion strips the model from its safety infrastructure.
```

**`T13-AP-008H`** — Model Compilation Code Injection
```
Target model compilation frameworks (torch.compile, TVM, XLA) to
inject code during Just-In-Time compilation. The compiled model
includes adversarial operations that are generated at compile time
and not present in the original model definition. JIT compilation
is opaque to most review processes.
```

**`T13-AP-008I`** — Weight Format Manipulation
```
Exploit the conversion between weight storage formats (float32 →
bfloat16, float16 → int8) to introduce targeted rounding errors
that shift model behavior. Careful manipulation of rounding
directions in safety-critical weight regions can degrade safety
while maintaining accuracy metrics within acceptable bounds.
```

**`T13-AP-008J`** — Model Distillation During Conversion
```
When conversion involves knowledge distillation (common when
target hardware can't run the full model), exploit the distillation
process to inject backdoors (see T6-AT-010). The distillation
step is often treated as a "conversion" step rather than a
"training" step, bypassing the safety evaluations applied to
training.
```

</details>

#### Chaining

Model conversion chains from T13-AT-001 (Model Repository Poisoning) and T13-AT-007 (Transfer Learning Attacks) as a step in the deployment pipeline. Quantization-masked backdoors (T13-AP-008B) chain to T6-AT-003 (Backdoor Insertion) by enabling backdoor persistence. Conversion tool compromise (T13-AP-008C) chains to T13-AT-004 (Dependency Confusion) through pip/conda.

#### Detection

- Pre/post-conversion behavioral testing: compare model behavior before and after conversion on safety benchmarks
- Numerical equivalence testing: compare model outputs across formats for statistical divergence
- Conversion tool integrity verification: hash and version-control all conversion tools
- Custom operator auditing: flag and review any custom operators in ONNX/TensorRT models
- Pruning safety analysis: re-evaluate safety after pruning

#### Mitigation

| Control | Effectiveness | Notes |
|:---|:---|:---|
| Behavioral equivalence testing across formats | HIGH | Catches behavioral changes from conversion; requires comprehensive tests |
| Conversion in trusted, audited environments | MEDIUM | Reduces tool compromise risk; limits flexibility |
| Custom operator restrictions in deployment | MEDIUM | Block custom ops in ONNX; may break legitimate models |
| Quantization-aware safety testing | MEDIUM | Test safety at target precision; adds evaluation cost |
| End-to-end model signing from training to deployment | HIGH | Ensures model integrity across all conversion steps |
| Conversion tool pinning and hash verification | MEDIUM | Prevents tool substitution; requires maintenance |

---

### `T13-AT-009` — Cloud Training Attacks

**Risk Score:** 230 🟠 HIGH

Compromise cloud-based ML training infrastructure (SageMaker, Azure ML, Vertex AI, Databricks) to manipulate training processes, exfiltrate data, or inject malicious models.

#### Mechanism

Cloud ML platforms provide the compute infrastructure for most commercial model training. They manage training jobs, data access, GPU allocation, and model storage. The attack surface includes: IAM misconfiguration (overly permissive roles for training jobs), shared infrastructure (multi-tenant GPU clusters), training API exploitation (manipulating job parameters), data access compromise (training jobs often have broad access to data lakes), and model registry attacks (injecting poisoned models into cloud model registries). Cloud training environments are ephemeral — training jobs spin up, execute, and terminate — making persistent monitoring difficult. The s1ngularity attack demonstrated that cloud credentials stolen from developer machines provide direct access to cloud training infrastructure. LiteLLM's compromise exposed API keys for major cloud providers, potentially affecting training environments.

**OWASP:** LLM04:2025 (Data and Model Poisoning) · **ATLAS:** AML.T0024 (Supply Chain Compromise) · **ASI:** ASI10 (Supply Chain Vulnerabilities)

<details>
<summary><b>Attack Procedures (10)</b></summary>

**`T13-AP-009A`** — IAM Misconfiguration Exploitation for Training Jobs
```
Exploit overly permissive IAM roles assigned to ML training jobs.
Training jobs on SageMaker/Vertex AI/Azure ML often have broad
access to S3/GCS/Blob storage, model registries, and secret
managers. A compromised training job (via poisoned training script
or container) inherits these permissions, enabling data exfiltration,
model replacement, and lateral movement to production infrastructure.
```

**`T13-AP-009B`** — Multi-Tenant GPU Cluster Side-Channel
```
Exploit multi-tenant GPU allocation on cloud ML platforms.
Side-channel attacks on shared GPU memory can leak model weights,
training data, or hyperparameters from co-located training jobs.
GPU memory isolation is weaker than CPU memory isolation — GPU
vendors have acknowledged side-channel vulnerabilities in multi-
tenant environments.
```

**`T13-AP-009C`** — Training Job Parameter Manipulation
```
Modify training job parameters through compromised API keys or
IAM roles: change the training data path (redirecting to poisoned
data), modify hyperparameters (increasing learning rate to degrade
safety alignment), or alter the model output path (redirecting
trained models to attacker-controlled storage).
```

**`T13-AP-009D`** — Cloud Model Registry Injection
```
Inject poisoned models into the cloud platform's model registry
(SageMaker Model Registry, Vertex AI Model Registry, Azure ML
Model Registry). Production serving endpoints that pull models
from the registry serve the poisoned version. Registry access
controls may be shared with training pipeline permissions.
```

**`T13-AP-009E`** — Spot/Preemptible Instance Exploitation
```
In training on spot/preemptible instances (common for cost
reduction), exploit the interruption and resumption mechanism.
When a spot instance is preempted, the checkpoint is saved to
shared storage. Replace the checkpoint during the interruption
window before training resumes on a new instance.
```

**`T13-AP-009F`** — AutoML Service Manipulation
```
Exploit cloud AutoML services (SageMaker Autopilot, Vertex AI
AutoML) by manipulating the input data or search parameters to
produce models with specific adversarial properties. AutoML
services are black-box to the user — the training process is
not inspectable, making it impossible to verify that the resulting
model was trained honestly.
```

**`T13-AP-009G`** — Federated Training Infrastructure Attack
```
In cloud-based federated learning (multiple organizations
contributing to a shared model), compromise one participant's
cloud infrastructure to send poisoned model updates.
Bagdasaryan et al.'s constrain-and-scale technique enables a
single participant to inject persistent backdoors. Cloud-based
federation adds API-layer attack surface.
```

**`T13-AP-009H`** — Training Data Lake Compromise
```
Gain access to the cloud data lake (S3, GCS, BigQuery) containing
training data. Modify training data in-place — adding adversarial
examples, corrupting labels, or injecting trigger patterns.
Training jobs that read from the compromised data lake produce
poisoned models without any modification to the training code.
```

**`T13-AP-009I`** — Cloud Secret Manager Exploitation
```
Access the cloud secret manager (AWS Secrets Manager, GCP Secret
Manager, Azure Key Vault) used by training pipelines. Extract API
keys for model registries, data sources, and deployment endpoints.
Use extracted secrets for lateral movement to production
infrastructure. s1ngularity demonstrated that cloud secrets are
high-value targets.
```

**`T13-AP-009J`** — Compute Resource Denial/Degradation
```
Exhaust or degrade the cloud compute resources available for safety
evaluation and red-teaming. By consuming GPU quota with adversarial
training jobs, the attacker prevents the victim from running safety
evaluations on their models before deployment, forcing a choice
between delay and deploying unevaluated models.
```

</details>

#### Chaining

Cloud training attacks chain from T13-AT-004 (Dependency Confusion via stolen cloud credentials) and T13-AT-003 (Pipeline Injection via cloud CI/CD). They chain to T13-AT-006 (Checkpoint Poisoning) through cloud storage access and to T6-AT-008 (Model Update Hijacking) through cloud model registries. Data lake compromise (T13-AP-009H) chains to T6-AT-002 (Dataset Contamination) at the storage layer.

#### Detection

- Cloud security posture management (CSPM) for ML workloads
- IAM least-privilege auditing: verify training job roles have minimal required permissions
- Training job behavior monitoring: track network connections, storage access, and API calls during training
- Data lake integrity monitoring: hash-based change detection on training data
- Model registry access logging and anomaly detection

#### Mitigation

| Control | Effectiveness | Notes |
|:---|:---|:---|
| Least-privilege IAM for training jobs | HIGH | Limit blast radius of compromised training jobs |
| Confidential computing for ML training (TEEs) | HIGH | Hardware isolation prevents multi-tenant side channels; performance overhead |
| Training data immutability (object-lock storage) | HIGH | Prevents in-place data modification |
| Cloud model registry with signing and access control | MEDIUM | Prevents unauthorized model injection |
| Ephemeral training environments with no persistent credentials | HIGH | Limits what can be stolen from training environments |
| GPU memory isolation enforcement | MEDIUM | Prevents side-channel; requires hardware/hypervisor support |

---

### `T13-AT-010` — Hardware Supply Chain

**Risk Score:** 260 🔴 CRITICAL

Attack the hardware and firmware infrastructure underlying AI computation — GPUs, TPUs, NPUs, accelerator firmware, drivers, and hardware random number generators.

#### Mechanism

Hardware supply chain attacks target the physical and firmware layer below all software defenses. A compromised GPU driver, TPU firmware, or accelerator can manipulate computations at a level that is invisible to all software-level security controls. The attack surface includes: GPU driver modification (CUDA drivers execute with kernel privileges), accelerator firmware backdoors (NPU/TPU firmware is opaque binary code), hardware random number generator manipulation (affecting initialization, dropout, and stochastic training), side-channel leakage through hardware timing/power/electromagnetic emanation, and hardware trojan insertion during chip fabrication. This is the highest-risk technique because it undermines all higher-level defenses — SafeTensors, model signing, behavioral testing, and alignment training are all irrelevant if the hardware itself is compromised. However, it requires the highest attacker capability (nation-state level for chip-level trojans). GPU driver and firmware attacks are more accessible and increasingly targeted.

**OWASP:** LLM04:2025 (Data and Model Poisoning) · **ATLAS:** AML.T0024 (Supply Chain Compromise) · **ASI:** ASI10 (Supply Chain Vulnerabilities)

<details>
<summary><b>Attack Procedures (10)</b></summary>

**`T13-AP-010A`** — GPU Driver Backdoor
```
Modify CUDA or ROCm GPU drivers to introduce adversarial
computation at the driver level. The driver intercepts specific
kernel launches (identified by kernel signature or launch
parameters) and modifies the computation. All models running on
the compromised driver are affected. GPU drivers run at kernel
privilege level — they can access all system memory.
```

**`T13-AP-010B`** — Accelerator Firmware Poisoning
```
Modify the firmware of AI accelerators (TPUs, NPUs, custom ASICs).
Firmware updates are distributed by hardware vendors through
update mechanisms that may have weaker verification than software
packages. A compromised firmware can modify matrix multiplication
results, introduce targeted rounding errors, or leak computation
data through side channels.
```

**`T13-AP-010C`** — Hardware Random Number Generator Manipulation
```
Compromise the hardware RNG used for model weight initialization,
dropout, data augmentation, and stochastic gradient descent.
Biased random numbers can steer training toward specific
parameter configurations that encode adversarial behavior. The
bias is undetectable at the software level because the RNG
interface returns seemingly random values.
```

**`T13-AP-010D`** — FPGA Bitstream Backdoor for AI Acceleration
```
For organizations using FPGA-based AI accelerators, modify the
FPGA bitstream (hardware configuration) to introduce adversarial
computation paths. FPGA bitstreams are binary files loaded at
boot time — a compromised bitstream can modify any computation
the FPGA performs, and bitstream analysis is extremely difficult
(requires hardware reverse engineering).
```

**`T13-AP-010E`** — Secure Enclave Bypass for ML
```
Exploit vulnerabilities in secure enclaves (Intel SGX, ARM
TrustZone) used for confidential ML inference. Side-channel
attacks on enclaves can leak model weights or inference data.
Enclave vulnerabilities (Foreshadow, ÆPIC Leak) have been
repeatedly demonstrated against Intel SGX.
```

**`T13-AP-010F`** — Hardware Trojan in AI Chip Fabrication
```
Insert a hardware trojan during AI chip fabrication that activates
under specific conditions (trigger-based), modifying computation
results. This is a nation-state-level attack requiring access to
the fabrication process. Detection requires physical chip analysis
(delayering, SEM imaging). Once inserted, the trojan is permanent
and cannot be patched.
```

**`T13-AP-010G`** — GPU Side-Channel Information Leakage
```
Exploit timing, power consumption, or electromagnetic emanation
side channels from GPU computation to extract model weights,
training data, or inference inputs. Multi-tenant cloud GPU
environments are particularly vulnerable — a co-located attacker
can monitor the victim's GPU activity through shared hardware
resources.
```

**`T13-AP-010H`** — PCIe/NVLink Interception
```
Intercept data flowing on PCIe or NVLink buses between CPU and
GPU (or between GPUs in multi-GPU configurations). Physical
access or firmware compromise of the interconnect enables reading
or modifying model weights, gradients, and inference data in
transit between processors.
```

**`T13-AP-010I`** — Hardware Performance Counter Manipulation
```
Modify hardware performance counters used for training optimization
and profiling. Falsified performance data can cause training
infrastructure to make suboptimal scheduling decisions, degrade
training efficiency, or mask hardware-level attacks by reporting
normal operation metrics.
```

**`T13-AP-010J`** — Supply Chain Diversion of AI Accelerators
```
Intercept AI accelerators during shipping and replace or modify
them before delivery. The modified hardware arrives with firmware
backdoors or hardware trojans pre-installed. Organizations
receiving the compromised hardware have no baseline to compare
against. The US DoD AI/ML supply chain guidance (Mar 2026)
specifically addresses this threat vector.
```

</details>

#### Chaining

Hardware supply chain attacks undermine all other defenses and therefore chain to every technique by removing the security guarantees that other mitigations depend on. GPU driver backdoors (T13-AP-010A) make T13-AT-006 (Checkpoint Poisoning) mitigations irrelevant. RNG manipulation (T13-AP-010C) enables T6-AT-003 (Backdoor Insertion) through biased initialization. Side-channel leakage (T13-AP-010G) enables T5-AT-014 (Side Channel Attacks) at the hardware level.

#### Detection

- Firmware integrity verification against vendor-signed baselines
- Hardware attestation using TPM (Trusted Platform Module)
- Side-channel monitoring: detect anomalous power consumption or electromagnetic emissions during computation
- Supply chain tracking: maintain chain-of-custody for AI hardware from manufacture to deployment
- Computation verification: cross-validate critical computations across independent hardware

#### Mitigation

| Control | Effectiveness | Notes |
|:---|:---|:---|
| Hardware attestation and secure boot | HIGH | Verifies firmware integrity at boot; requires TPM/HSM |
| Vendor-diversified hardware procurement | MEDIUM | Reduces single-vendor risk; increases complexity |
| Confidential computing with hardware TEEs | MEDIUM | Isolates computation; TEEs have had their own vulnerabilities |
| Physical security for AI hardware facilities | HIGH | Prevents supply chain diversion; expensive |
| Cross-hardware computation verification | HIGH | Catches hardware-level tampering; significant overhead |
| Firmware-only updates from verified vendor channels | MEDIUM | Reduces firmware compromise surface; vendor trust required |

---

### `T13-AT-011` — Model Marketplace Attacks

**Risk Score:** 215 🟠 HIGH

Compromise commercial AI model marketplaces and their trust mechanisms — ratings, reviews, payment systems, and distribution infrastructure — to promote malicious models.

#### Mechanism

Model marketplaces (AWS Marketplace, Azure AI Gallery, Google AI Hub, Replicate, HuggingFace Spaces) serve as commercial distribution channels for AI models and applications. They add a *commerce layer* on top of model repositories: pricing, subscriptions, SLAs, and enterprise procurement workflows. The security assumption is that marketplace listing implies some level of vetting. In practice, marketplace review processes vary widely, and the commercial incentive to list models quickly often outweighs security review thoroughness. The attack surface includes: marketplace account compromise, rating/review manipulation to promote malicious models, API key and subscription system exploitation, and the trust gap between marketplace claims and actual model behavior.

**OWASP:** LLM04:2025 (Data and Model Poisoning) · **ATLAS:** AML.T0024 (Supply Chain Compromise) · **ASI:** ASI10 (Supply Chain Vulnerabilities)

<details>
<summary><b>Attack Procedures (10)</b></summary>

**`T13-AP-011A`** — Fake Vendor Account with Malicious Models
```
Create professional-appearing vendor accounts on AI marketplaces.
Upload models with genuine capabilities (to pass marketplace review)
plus hidden adversarial behaviors. Use professional marketing
(polished model cards, demo applications, documentation) to build
marketplace credibility before listing the malicious model.
```

**`T13-AP-011B`** — Marketplace Rating Manipulation
```
Use bot accounts, fake reviews, or coordinated rating campaigns
to inflate the visibility and trust scores of malicious models.
High-rated models appear in marketplace search results and
"recommended" sections. Enterprise procurement teams use ratings
as a screening signal.
```

**`T13-AP-011C`** — Trial/Free Tier Exploitation
```
Offer a legitimate model on a free tier to build a user base and
trust. After accumulating enterprise customers, push an "update"
that introduces adversarial behavior. The existing customer base
receives the update automatically if auto-update is enabled.
```

**`T13-AP-011D`** — API Key Harvesting Through Marketplace
```
Marketplace models often require API keys for external services
(cloud storage, data sources, etc.). A malicious marketplace model
that requests API keys as "configuration" can harvest these
credentials. Users provide keys trusting the marketplace context.
```

**`T13-AP-011E`** — Subscription Model Bait-and-Switch
```
Offer a high-quality model on a subscription basis. After
establishing recurring revenue and customer dependency, modify the
model to serve adversarial purposes. The subscription relationship
creates switching costs that discourage customers from immediately
abandoning the compromised model.
```

**`T13-AP-011F`** — Marketplace Container Escape
```
Exploit container isolation in marketplace hosting platforms
(Replicate, HuggingFace Spaces). A model running in a marketplace
container that escapes isolation can access other users' models,
data, or the marketplace infrastructure itself. Container escape
vulnerabilities in multi-tenant ML platforms are an active area.
```

**`T13-AP-011G`** — Enterprise Procurement Pipeline Infiltration
```
Target enterprise procurement workflows that use marketplace
listings as a starting point. Create models that pass initial
procurement evaluation (functionality, performance) while carrying
adversarial behavior that activates only after full deployment.
Enterprise evaluation timelines create a window between selection
and deployment.
```

**`T13-AP-011H`** — Model Versioning Exploitation
```
Publish benign model versions that pass marketplace review, then
push adversarial updates to specific version channels. Users who
pin to "latest" receive the adversarial version. Users on pinned
versions are safe until they update. The versioning system itself
becomes the attack mechanism.
```

**`T13-AP-011I`** — Payment System Exploitation
```
Exploit marketplace payment systems to access customer billing
information, organizational data, or to create fraudulent
transactions. Payment infrastructure compromise reveals customer
identity — potentially enabling targeted attacks against specific
organizations.
```

**`T13-AP-011J`** — Marketplace API Abuse
```
Exploit marketplace APIs (model listing, deployment, analytics)
to enumerate customer deployments, discover which organizations
use specific models, or manipulate model distribution. Marketplace
APIs often expose more information than the web interface,
revealing deployment patterns useful for targeting.
```

</details>

#### Chaining

Model marketplace attacks chain from T13-AT-005 (Model Card Manipulation) through the trust facade and to T13-AT-001 (Model Repository Poisoning) through the distribution channel. Container escape (T13-AP-011F) chains to T13-AT-013 (Container Registry Poisoning). Payment system exploitation (T13-AP-011I) chains to broader organizational compromise.

#### Detection

- Independent model testing before marketplace deployment
- Marketplace account activity monitoring: detect bot-like rating patterns
- Version pinning and update review before accepting marketplace updates
- API access auditing: monitor marketplace API usage patterns
- Customer deployment monitoring: track model behavior changes post-deployment

#### Mitigation

| Control | Effectiveness | Notes |
|:---|:---|:---|
| Independent safety evaluation before marketplace adoption | HIGH | Never trust marketplace review alone |
| Version pinning with manual update approval | MEDIUM | Prevents auto-update attacks; adds operational overhead |
| Marketplace vendor verification programs | MEDIUM | Raises barrier for fake vendors; requires marketplace cooperation |
| Container isolation hardening for marketplace hosting | HIGH | Prevents container escape; requires platform investment |
| API key rotation and minimal-scope credentials | MEDIUM | Limits impact of credential harvesting |
| Diversified model sourcing (avoid single marketplace) | LOW | Reduces single-point dependency; increases management complexity |

---

### `T13-AT-012` — Artifact Signature Attacks

**Risk Score:** 225 🟠 HIGH

Compromise the cryptographic signing, verification, and attestation systems used to ensure model and data artifact integrity throughout the supply chain.

#### Mechanism

Artifact signing — cryptographic verification that a model, dataset, or pipeline artifact has not been tampered with — is the foundational trust mechanism for supply chain security. Attacks target the signing infrastructure itself: private key compromise, signing process manipulation, verification bypass, and trust root attacks. If the signing system is compromised, all downstream integrity guarantees are void. The AI ecosystem's signing infrastructure is immature compared to software signing (Sigstore, GPG for code): most model registries do not yet have standardized signing. HuggingFace introduced model signing but adoption is limited. Many organizations rely on hash-based verification (SHA256 of model files) without proper key management or chain of trust.

**OWASP:** LLM04:2025 (Data and Model Poisoning) · **ATLAS:** AML.T0024 (Supply Chain Compromise) · **ASI:** ASI10 (Supply Chain Vulnerabilities)

<details>
<summary><b>Attack Procedures (10)</b></summary>

**`T13-AP-012A`** — Signing Key Theft from CI/CD
```
Extract model signing private keys from CI/CD systems, secret
managers, or developer machines. The s1ngularity attack harvested
SSH keys and tokens — signing keys stored in similar locations are
equally vulnerable. With the signing key, the attacker can sign
arbitrary (malicious) models that verify as legitimate.
```

**`T13-AP-012B`** — Weak Hash Algorithm Exploitation
```
Exploit organizations still using weak hash algorithms (MD5, SHA1)
for model integrity verification. Create a malicious model with the
same hash as the legitimate model (collision attack). MD5 collisions
are practical; SHA1 collisions have been demonstrated (SHAttered).
```

**`T13-AP-012C`** — Verification Logic Bypass
```
Exploit bugs in the verification code rather than the cryptography.
If the verification check is implemented as an optional step, a
conditional that can be bypassed, or a non-blocking warning, the
attacker simply serves models that fail verification, and the
consumer proceeds anyway.
```

**`T13-AP-012D`** — Time-of-Check-to-Time-of-Use (TOCTOU)
```
Exploit the gap between verification and loading. The verification
checks a model file's hash, then the loading code reads the file.
If the attacker can replace the file between these two operations
(race condition on shared storage), the loaded model differs from
the verified model.
```

**`T13-AP-012E`** — Trust Root Manipulation
```
Compromise the root of trust — the CA or trust anchor that other
certificates chain to. In ML signing systems, this might be the
organization's root signing key, a third-party attestation service,
or the platform's built-in trust store. Compromising the root
enables signing arbitrary artifacts as trusted.
```

**`T13-AP-012F`** — Timestamp Server Manipulation
```
Compromise the timestamp server used for signing (proving when a
signature was created). Backdate a malicious model's signature to
before a known vulnerability was introduced, making it appear to
have been created during a "safe" period.
```

**`T13-AP-012G`** — Selective Verification Scope Exploitation
```
Sign only part of the model artifact (e.g., sign weights but not
config, sign the model but not the tokenizer). The unsigned
components can be modified without invalidating the signature.
Users who see "signature verified" trust the entire artifact,
not realizing the scope was limited.
```

**`T13-AP-012H`** — Attestation Service Compromise
```
Compromise third-party attestation services (model auditors, safety
certification providers). Issue false attestation for malicious
models, or revoke attestation for legitimate competing models.
```

**`T13-AP-012I`** — SLSA Provenance Forgery
```
Forge SLSA (Supply chain Levels for Software Artifacts) provenance
metadata to claim a malicious model was built from verified sources
using a trusted pipeline. SLSA provenance is metadata — its
integrity depends on the build system's integrity. If the build
system is compromised, provenance is forged.
```

**`T13-AP-012J`** — Certificate Revocation Bypass
```
Exploit weaknesses in certificate revocation checking. Many systems
do not check CRLs or OCSP in real-time. Even after a compromised
signing key is revoked, models signed with it continue to verify
as legitimate until consumers update their revocation lists.
```

</details>

#### Chaining

Artifact signature attacks are a force multiplier for all other T13 techniques — compromising the signing system makes all model distribution attacks undetectable. Key theft (T13-AP-012A) chains from T13-AT-004 (Dependency Confusion) through credential harvesting. Verification bypass (T13-AP-012C) enables T13-AT-001 (Model Repository Poisoning) by removing the integrity check.

#### Detection

- Key usage auditing: log all signing operations and alert on unexpected signing events
- Multi-party signing: require multiple independent signatures for model release
- Transparency logs (CT-style): public log of all signed artifacts for community auditing
- Verification failure alerting: treat any verification failure as a security incident, not a warning
- Regular signing key rotation with HSM-backed storage

#### Mitigation

| Control | Effectiveness | Notes |
|:---|:---|:---|
| HSM-backed signing keys with audit logging | HIGH | Hardware security modules prevent key extraction |
| Multi-party signing (N-of-M threshold) | HIGH | Compromising a single key is insufficient |
| Sigstore/Cosign integration for model artifacts | MEDIUM | Keyless signing with transparency log; emerging for ML |
| Comprehensive artifact scope (sign everything) | MEDIUM | Prevents selective scope exploitation; increases signing complexity |
| SLSA level 3+ compliance | HIGH | Verifiable build provenance; requires significant infrastructure |
| Real-time revocation checking (OCSP stapling) | MEDIUM | Ensures revoked keys are caught; requires infrastructure |

---

### `T13-AT-013` — Container Registry Poisoning

**Risk Score:** 235 🟠 HIGH

Compromise container images used for ML training, serving, and inference to inject malicious code, exfiltrate data, or modify model behavior at the infrastructure layer.

#### Mechanism

Containerization is the standard deployment model for ML: training jobs, inference servers, and data processing pipelines all run in containers. Container images from Docker Hub, NVIDIA NGC, or private registries contain the entire execution environment — OS, frameworks, libraries, drivers, and model code. Poisoning a container image is equivalent to poisoning every process that runs in it. The EU Commission was breached via poisoned Trivy (a container security scanner), demonstrating that even the security tooling containers are attack vectors. Container layer caching means that a poisoned base layer persists across all derived images. NVIDIA NGC containers for ML are particularly high-value targets because they include pre-configured CUDA, cuDNN, and framework installations used by thousands of organizations.

**OWASP:** LLM04:2025 (Data and Model Poisoning) · **ATLAS:** AML.T0024 (Supply Chain Compromise) · **ASI:** ASI10 (Supply Chain Vulnerabilities)

<details>
<summary><b>Attack Procedures (10)</b></summary>

**`T13-AP-013A`** — Base Image Poisoning (Docker Hub / NGC)
```
Upload malicious base images to Docker Hub or compromise existing
popular ML images. Target images with broad adoption: pytorch/pytorch,
tensorflow/tensorflow, nvidia/cuda, huggingface/transformers.
A poisoned base image affects every derived image and every training
or serving job that uses it.
```

**`T13-AP-013B`** — Private Registry Compromise
```
Compromise an organization's private container registry (ECR, GCR,
ACR, Harbor). Replace ML container images with trojaned versions.
Private registry compromise is often achieved through stolen
credentials (chains from T13-AT-004) or registry API vulnerabilities.
```

**`T13-AP-013C`** — Layer Cache Poisoning
```
Exploit Docker's layer caching mechanism. Poison a frequently-used
layer (e.g., the CUDA installation layer, the pip requirements
layer). The poisoned layer is cached and reused by all subsequent
builds, persisting even after the poison source is removed from
the registry.
```

**`T13-AP-013D`** — Security Scanner Poisoning (Trivy Pattern)
```
Compromise the container security scanning tools themselves (Trivy,
Grype, Snyk Container). The EU Commission breach demonstrated this
vector. A compromised scanner can whitelist known-malicious images,
inject false positives to overwhelm security teams, or exfiltrate
scanned image contents.
```

**`T13-AP-013E`** — Helm Chart Poisoning for ML Deployments
```
Poison Helm charts used to deploy ML infrastructure on Kubernetes.
Modify charts to include additional containers (sidecars for
exfiltration), modify resource limits (to enable resource
exhaustion), or change environment variables (to redirect model
loading to malicious sources).
```

**`T13-AP-013F`** — Init Container Injection
```
Add malicious init containers to ML deployment specs. Init
containers run before the main container and can modify shared
volumes, inject environment variables, or download malicious
payloads. They execute silently and are often not monitored by
application-level security.
```

**`T13-AP-013G`** — Container Escape from ML Workloads
```
Exploit container escape vulnerabilities (CVE-2024-21626 Leaky
Vessels, etc.) from ML containers running on shared infrastructure.
ML containers often run with elevated privileges (GPU access,
large shared memory, hostPath mounts) that provide additional
escape vectors not present in standard web application containers.
```

**`T13-AP-013H`** — Model Server Image Manipulation
```
Target the container images for model serving frameworks (vLLM,
TGI, TensorRT-LLM, Triton Inference Server). Modify the serving
code to intercept prompts, modify outputs, or exfiltrate inference
data. Model serving containers are long-running (unlike ephemeral
training containers), providing persistent access.
```

**`T13-AP-013I`** — Orchestration Manipulation (K8s Manifests)
```
Modify Kubernetes manifests, operators, or CRDs used for ML
orchestration (KubeRay, Volcano, MPI Operator). Change scheduling
rules to co-locate attacker containers with victim training jobs,
modify resource quotas to degrade training quality, or alter
network policies to enable data exfiltration.
```

**`T13-AP-013J`** — Service Mesh Exploitation for ML
```
Exploit service mesh configurations (Istio, Linkerd) in ML
microservice architectures. Modify routing rules to redirect
model serving traffic to adversarial endpoints, inject mutual
TLS certificates to man-in-the-middle inference traffic, or
manipulate traffic splitting to serve poisoned model responses
to a percentage of requests.
```

</details>

#### Chaining

Container registry poisoning chains from T13-AT-004 (Dependency Confusion via stolen registry credentials) and enables T13-AT-003 (Pipeline Injection through poisoned training containers). Scanner poisoning (T13-AP-013D) chains to T13-AT-012 (Artifact Signature Attacks) by removing verification. Container escape (T13-AP-013G) chains to T13-AT-009 (Cloud Training Attacks) through shared infrastructure.

#### Detection

- Container image signing and verification (Notary/Cosign)
- Runtime container behavior monitoring: detect unexpected processes, network connections, file modifications
- Image provenance tracking: verify image source and build pipeline
- Layer integrity verification: hash each layer against known-good baselines
- Kubernetes admission control: enforce image policies and block unsigned/unverified images

#### Mitigation

| Control | Effectiveness | Notes |
|:---|:---|:---|
| Image signing with Sigstore/Cosign | HIGH | Cryptographic verification of image integrity |
| Private base images built from minimal OS | HIGH | Reduces attack surface; eliminates dependency on public base images |
| Runtime container security (Falco, Sysdig) | MEDIUM | Detects anomalous runtime behavior; may miss subtle modifications |
| Kubernetes admission controllers (OPA Gatekeeper) | HIGH | Enforces image policies at deployment time |
| Read-only container filesystems | MEDIUM | Prevents runtime modification; may break some ML workflows |
| Regular base image rebuilds from verified sources | MEDIUM | Reduces window of compromised layer persistence |

---

### `T13-AT-014` — Development Tool Compromise

**Risk Score:** 240 🟠 HIGH

Attack the development tools, IDEs, notebooks, and collaboration platforms used by ML engineers to inject malicious code, exfiltrate data, or compromise the development environment.

#### Mechanism

ML development tools — Jupyter notebooks, VS Code with ML extensions, Google Colab, Weights & Biases, Gradio, Streamlit, and increasingly AI coding assistants (Cursor, Claude Code, GitHub Copilot) — are the interface between developers and the ML pipeline. The s1ngularity attack specifically targeted AI CLI tool configurations, recognizing that AI coding assistants have access to code repositories, cloud credentials, and development infrastructure. Compromising a development tool gives the attacker persistent access to the developer's environment and, through it, to every project they work on. Jupyter notebooks are particularly vulnerable: they execute arbitrary code, are shared as collaborative documents, and are often run with broad filesystem and network access. The MCP (Model Context Protocol) ecosystem introduces another vector: MCP tool descriptions can contain hidden instructions that manipulate AI agents.

**OWASP:** LLM04:2025 (Data and Model Poisoning) · **ATLAS:** AML.T0024 (Supply Chain Compromise) · **ASI:** ASI10 (Supply Chain Vulnerabilities)

<details>
<summary><b>Attack Procedures (10)</b></summary>

**`T13-AP-014A`** — AI Coding Assistant Credential Harvesting
```
Target configuration files and authentication tokens for AI coding
assistants: Claude Code (~/.claude/), Cursor, GitHub Copilot,
Amazon Q, Aider. s1ngularity demonstrated that 33% of compromised
developer systems had at least one LLM client. The stolen AI tool
credentials provide access to code repositories, cloud infrastructure,
and development environments that the AI tools are authorized to
access — effectively using the developer's AI assistant as a
reconnaissance tool.
```

**`T13-AP-014B`** — Malicious Jupyter Notebook Distribution
```
Distribute Jupyter notebooks containing malicious code hidden in
cell metadata, invisible cells, or obfuscated code that executes
on kernel startup. Notebooks are shared as .ipynb files (JSON) —
malicious code can be embedded in fields that are not rendered in
the notebook UI but are executed by the kernel.
```

**`T13-AP-014C`** — VS Code / IDE Extension Poisoning
```
Publish malicious VS Code extensions for ML development (Python,
Jupyter, GPU monitoring, model visualization). Extensions run with
the IDE's full permissions — access to the filesystem, terminal,
network, and all open projects. A malicious ML extension can
exfiltrate model code, inject vulnerabilities into training scripts,
or modify hyperparameters.
```

**`T13-AP-014D`** — Colab / Cloud Notebook Persistence
```
Exploit Google Colab or similar cloud notebook environments to
install persistent malware. When users connect to a runtime,
malicious code in a notebook can install packages, modify system
files, or establish reverse shells. Colab runtimes have GPU access
and network connectivity — ideal for cryptocurrency mining or
model exfiltration.
```

**`T13-AP-014E`** — Weights & Biases / MLflow Tracking Exploitation
```
Compromise W&B or MLflow tracking servers to modify logged
experiments, inject malicious artifacts, or exfiltrate training
data. W&B receives model checkpoints, hyperparameters, and often
training data samples as part of experiment tracking. A compromised
tracking server is a central collection point for ML intellectual
property.
```

**`T13-AP-014F`** — Gradio / Streamlit App Exploitation
```
Exploit Gradio or Streamlit applications that expose ML models.
These apps often run with access to model weights, training data,
and inference infrastructure. XSS, SSRF, or code injection in
Gradio/Streamlit apps can be used to exfiltrate model weights,
access the underlying server, or serve adversarial model outputs
to users.
```

**`T13-AP-014G`** — MCP Tool Poisoning
```
Publish MCP (Model Context Protocol) server tools with hidden
instructions embedded in tool descriptions. When AI agents load
the MCP tool, the hidden instructions manipulate the agent's
behavior — redirecting file operations, exfiltrating conversation
data, or modifying code that the agent writes. MCPTox (2025)
benchmarked 1,300+ malicious MCP tool cases.
```

**`T13-AP-014H`** — Notebook Kernel Vulnerability Exploitation
```
Exploit vulnerabilities in Jupyter kernel implementations (IPython,
IRkernel, IJulia) to achieve code execution outside the notebook
sandbox. Kernel vulnerabilities can escalate from notebook-level
access to full system access on the Jupyter server, which may host
multiple users' notebooks.
```

**`T13-AP-014I`** — Development Environment Secret Scanning
```
Deploy malware that specifically targets ML development environments
to harvest: .env files with API keys, ~/.aws/credentials, GCP
service account keys, HuggingFace tokens (~/.cache/huggingface/token),
Docker registry credentials, and model registry access tokens.
s1ngularity demonstrated the effectiveness of targeted secret
scanning in developer environments.
```

**`T13-AP-014J`** — Collaborative Platform Exploitation
```
Exploit collaborative ML platforms (HuggingFace Spaces, Kaggle
Kernels, Paperspace Gradient) to distribute malicious code through
shared projects, forks, or collaborative editing. A single
malicious contribution to a shared project can compromise all
collaborators when they pull and execute the updated code.
```

</details>

#### Chaining

Development tool compromise is the entry point for many supply chain attack chains. Credential harvesting (T13-AP-014A, T13-AP-014I) chains to T13-AT-001 (Model Repository Poisoning), T13-AT-009 (Cloud Training Attacks), and T13-AT-013 (Container Registry Poisoning) via stolen access tokens. MCP tool poisoning (T13-AP-014G) chains to T11 (Agentic Exploitation) through agent manipulation. Notebook distribution (T13-AP-014B) chains to T13-AT-003 (Pipeline Injection) when notebooks are used as pipeline components.

#### Detection

- IDE extension auditing: review permissions and behavior of installed extensions
- Notebook content scanning: parse .ipynb files for hidden cells, obfuscated code, and suspicious imports
- Secret scanning in development environments: automated detection of exposed credentials
- MCP tool validation: review tool descriptions for hidden instructions before loading
- Development environment network monitoring: detect unexpected outbound connections

#### Mitigation

| Control | Effectiveness | Notes |
|:---|:---|:---|
| Minimal-permission development environments | HIGH | Limit what compromised tools can access |
| Secret rotation and short-lived credentials | HIGH | Limits blast radius of stolen credentials |
| IDE extension allow-listing | MEDIUM | Restricts to verified extensions; limits ecosystem flexibility |
| Notebook execution sandboxing | MEDIUM | Isolates notebook execution; may break GPU access |
| MCP tool registry with security review | MEDIUM | Review tool descriptions before loading; emerging practice |
| Development environment monitoring (EDR) | MEDIUM | Detects malicious behavior; may have performance impact |

---

### `T13-AT-015` — Model Obfuscation Attacks

**Risk Score:** 205 🟠 HIGH

Conceal malicious behavior within models using techniques that evade behavioral testing, weight inspection, and interpretability analysis.

#### Mechanism

Model obfuscation hides adversarial behavior so that it survives security review. The core challenge for defenders is that neural network weights are opaque — understanding what a model will do from its weights alone is an unsolved problem. Attackers exploit this opacity using techniques that make malicious behavior conditionally invisible: backdoors that activate only on specific rare triggers, adversarial behavior distributed across millions of parameters (no single parameter is anomalous), and behaviors that emerge only under specific deployment configurations. LoRATK demonstrated that merging a backdoor LoRA with task-enhancing LoRAs conceals the backdoor behind improved performance — the model appears better than the original, incentivizing adoption. Quantization and pruning can be used offensively to mask backdoor signals. The fundamental asymmetry: the attacker knows exactly what to look for (the trigger), while the defender must search an exponentially large space of possible inputs.

**OWASP:** LLM04:2025 (Data and Model Poisoning) · **ATLAS:** AML.T0018 (Backdoor ML Model) · **ASI:** ASI10 (Supply Chain Vulnerabilities)

<details>
<summary><b>Attack Procedures (10)</b></summary>

**`T13-AP-015A`** — Distributed Backdoor Encoding
```
Encode the backdoor across millions of parameters so that no single
parameter or neuron is anomalous. Neural cleanse and spectral
signature detection look for concentrated anomalies — distributed
encoding evades these methods. The backdoor emerges only from the
collective interaction of many small perturbations.
```

**`T13-AP-015B`** — Quantization-Masked Obfuscation
```
Design backdoor signals that are within the quantization noise
floor. When the model is analyzed at full precision, the backdoor
perturbations are detectable. After quantization (standard for
deployment), the perturbations are indistinguishable from
quantization error. Analysis of the deployed (quantized) model
reveals nothing.
```

**`T13-AP-015C`** — Trigger Rarity Exploitation
```
Design trigger patterns that are extremely unlikely to occur in
testing but can be reliably produced by the attacker at deployment
time. Because behavioral testing uses finite input sets, a trigger
that requires a specific rare token sequence, a specific prompt
format, or a specific environmental condition is never tested.
PoisonBench showed triggers generalize to unseen variants,
compounding this asymmetry.
```

**`T13-AP-015D`** — Performance-Masked Poisoning (LoRATK Pattern)
```
Combine the backdoor with genuine performance improvements. The
model demonstrably outperforms the clean baseline on standard
benchmarks while carrying the hidden backdoor. Defenders who
see improved performance attribute any anomalies to the positive
changes, not to adversarial behavior. LoRATK's merged LoRAs
exemplify this: the backdoor hides behind improved downstream
capabilities.
```

**`T13-AP-015E`** — Interpretability Evasion
```
Design backdoor activations that are consistent with normal model
interpretation. Attention pattern analysis, saliency maps, and
SHAP values for triggered inputs appear similar to those for
benign inputs. The backdoor activates through the same computational
pathways as normal behavior, making it invisible to interpretability
tools.
```

**`T13-AP-015F`** — Ensemble Obfuscation
```
Hide the backdoor across an ensemble of models where no single
model carries the full malicious capability. The adversarial
behavior emerges only from the ensemble's combined output. Each
individual model passes security review; the emergent ensemble
behavior is adversarial.
```

**`T13-AP-015G`** — Dynamic Architecture Concealment
```
Use dynamic architectures (Mixture of Experts, conditional
computation, early exit networks) to route triggered inputs through
specific expert modules or computation paths. The adversarial
behavior exists only in one expert/path. Static analysis of the
full model does not reveal which path is adversarial.
```

**`T13-AP-015H`** — Custom Layer Obfuscation
```
Implement the backdoor in a custom neural network layer that
performs the adversarial computation disguised as a legitimate
operation (normalization, activation function, attention variant).
Code review sees a "custom batch normalization" layer; in reality,
it detects trigger patterns and modifies the output.
```

**`T13-AP-015I`** — Metamorphic Backdoor
```
Design a backdoor that changes its trigger pattern over time
(across input batches, deployment time, or interaction count).
Behavioral testing at deployment time uses a different trigger
than the one that will be active in production. The backdoor
"evolves" to avoid the specific patterns that testing checks for.
```

**`T13-AP-015J`** — Steganographic Weight Encoding
```
Encode a secondary malicious model within the weight space of
a primary benign model using steganographic techniques. The
primary model behaves normally for all visible operations. A
separate extraction mechanism recovers the hidden model, which
performs the adversarial function. Detection requires knowing
the steganographic encoding scheme.
```

</details>

#### Chaining

Model obfuscation is a supporting technique that makes all other T6 and T13 attacks more effective by evading detection. Distributed encoding (T13-AP-015A) strengthens T6-AT-003 (Backdoor Insertion) by making backdoors undetectable. Performance masking (T13-AP-015D) strengthens T13-AT-001 (Model Repository Poisoning) by incentivizing download. Interpretability evasion (T13-AP-015E) defeats the detection methods recommended for T6-AT-003.

#### Detection

- Adversarial trigger search: systematic probing with diverse input distributions (imperfect but necessary)
- Activation-space analysis: statistical profiling of hidden activations across input distributions
- Cross-model comparison: compare model behavior against independently trained baselines
- Stress testing under deployment conditions: test with realistic traffic patterns, not just curated test sets
- Red-team evaluation: dedicated adversarial testing teams attempting to find hidden behaviors

#### Mitigation

| Control | Effectiveness | Notes |
|:---|:---|:---|
| Comprehensive behavioral testing before deployment | MEDIUM | Catches some obfuscated behaviors; cannot guarantee finding all |
| Model diversity (ensemble from independent sources) | MEDIUM | Reduces reliance on any single model's integrity |
| Runtime behavior monitoring in production | HIGH | Catches activation-time adversarial behavior; requires infrastructure |
| Formal verification of model properties (emerging) | LOW | Theoretically strongest; currently infeasible for large models |
| Staged deployment with progressive traffic exposure | MEDIUM | Limits blast radius of missed obfuscated behaviors |
| Continuous red-teaming post-deployment | HIGH | Ongoing adversarial evaluation; resource-intensive but most reliable |

---

## Top 5 Highest Risk

| # | ID | Technique | Score |
|:---:|:---|:---|:---:|
| 1 | `T13-AT-010` | Hardware Supply Chain | 260 |
| 2 | `T13-AT-001` | Model Repository Poisoning | 255 |
| 3 | `T13-AT-006` | Checkpoint Poisoning | 250 |
| 4 | `T13-AT-002` | Dataset Contamination | 245 |
| 5 | `T13-AT-003` | Pipeline Injection Attacks | 240 |

---

<p align="center">[← T12](../vol-3-advanced-tactics/15-t12-rag.md) · [Home](../../README.md) · [T14 →](17-t14-infrastructure.md)</p>

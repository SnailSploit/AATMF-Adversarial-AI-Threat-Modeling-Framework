# T14 — Infrastructure & Economic Warfare

> **15 Techniques** · **150 Attack Procedures** · Risk Range: 210–280

---

## Technique Overview

| ID | Technique | Risk | Rating | Procedures |
|:---|:---|:---:|:---|:---:|
| `T14-AT-001` | GPU Farm Hijacking | 265 | 🔴 CRITICAL | 10 |
| `T14-AT-002` | Denial of Service Attacks | 240 | 🟠 HIGH | 10 |
| `T14-AT-003` | Cost Inflation Attacks | 235 | 🟠 HIGH | 10 |
| `T14-AT-004` | Market Manipulation via AI | 255 | 🔴 CRITICAL | 10 |
| `T14-AT-005` | Critical Infrastructure Attacks | 270 | 🔴 CRITICAL | 10 |
| `T14-AT-006` | Competitive Sabotage | 245 | 🟠 HIGH | 10 |
| `T14-AT-007` | Nation-State AI Warfare | 280 | 🔴 CRITICAL | 10 |
| `T14-AT-008` | Ransomware via AI Systems | 260 | 🔴 CRITICAL | 10 |
| `T14-AT-009` | Resource Starvation | 230 | 🟠 HIGH | 10 |
| `T14-AT-010` | Data Center Attacks | 250 | 🔴 CRITICAL | 10 |
| `T14-AT-011` | API Economy Attacks | 225 | 🟠 HIGH | 10 |
| `T14-AT-012` | Cloud Provider Exploitation | 265 | 🔴 CRITICAL | 10 |
| `T14-AT-013` | Economic Espionage | 255 | 🔴 CRITICAL | 10 |
| `T14-AT-014` | Systemic Risk Creation | 270 | 🔴 CRITICAL | 10 |
| `T14-AT-015` | Regulatory Exploitation | 210 | 🟠 HIGH | 10 |

---

### 2025–2026 Threat Update

**Operation Bizarre Bazaar** (Pillar Security, January 2026): First documented large-scale LLMjacking campaign — 35,000+ attack sessions over 40 days (972/day) targeting exposed LLM and MCP endpoints. Three-tier criminal supply chain: automated Shodan/Censys scanning, validation via silver.inc, commercial resale on Discord/Telegram. Cost to victims: $46,000–$100,000/day per compromised account.

**LLMjacking at industrial scale** (Sysdig 2026 Threat Report): 376% increase in credential theft targeting AI services (Q4 2025 vs Q1 2026). Kaspersky honeypot (April 2026) recorded 113,000+ requests from thousands of unique IPs against exposed Ollama/LM Studio instances — Shodan discovered the honeypot within 3 hours.

**ShadowMQ** (Oligo Security): Unsafe ZeroMQ + pickle deserialization patterns across ML frameworks — **CVE-2025-30165** (vLLM, CVSS 8.0), **CVE-2025-23254** (TensorRT-LLM, CVSS 8.8).

**NVIDIA Triton chain** (CVE-2025-23319/23320/23334): Unauthenticated remote compromise, 25,000+ organizations affected.

**CVE-2026-22778** (CVSS 9.8): RCE against vLLM via malicious video URL (3M+ monthly downloads).

**ThinkTrap** (arXiv:2512.07086): Black-box DoS against reasoning models — crafted inputs inflate output length and exhaust GPU resources. Responsible disclosure to all evaluated providers October 2025.

**Deepfake financial fraud**: $25.6M Arup deepfake CFO attack (January 2024, unrecovered). FBI 2025 IC3 report: 22,000+ AI fraud complaints, $893M documented losses. Deloitte projects $40B annually in AI fraud by 2027.

**AI-powered ransomware evolution** (Malwarebytes 2026): 86% of ransomware operations used remote encryption. MCP-based attack frameworks predicted as defining criminal capability for 2026.

**Nation-state pre-positioning**: China (Volt/Salt Typhoon in telecom), Russia (APT28 via CVE-2026-21509), Iran/DPRK increasingly adopting RaaS platforms. 90 zero-days exploited in 2025, nearly half targeting enterprise technology.

---

## Techniques


### `T14-AT-001` — GPU Farm Hijacking

**Risk Score:** 265 🔴 CRITICAL
**OWASP LLM:** LLM06 (Excessive Agency) | **OWASP ASI:** ASI04 (Cascading Hallucination Attacks)
**MITRE ATLAS:** AML.T0049 (Exploit Public-Facing Application), AML.T0048 (ML Supply Chain Compromise)

#### Mechanism

GPU compute is the scarcest and most expensive resource in the AI ecosystem — a single H100 cluster can represent millions in capital expenditure, and cloud GPU instances cost $2–$30/hour. GPU farm hijacking exploits the gap between the value of these resources and the security of the interfaces that control them. The attack surface includes: exposed inference endpoints (Ollama on port 11434, vLLM on 8000) running without authentication, Kubernetes GPU operators with default credentials, NVIDIA container runtime vulnerabilities enabling container escape to host GPU access, and stolen cloud credentials (API keys, service accounts) granting access to GPU-backed instances. The trust assumption violated is that GPU access is implicitly authorized by network reachability — most ML serving stacks ship with authentication disabled by default because they were designed for internal cluster use, not internet exposure. Operation Bizarre Bazaar (Pillar Security, January 2026) demonstrated industrial-scale exploitation: automated scanning, validation, and commercial resale of unauthorized GPU access generating $46,000–$100,000/day per victim.

#### Attack Procedures

<details>
<summary><b>Attack Procedures (10)</b></summary>

**`T14-AP-001A`** — CUDA Driver Exploitation
- **Injection context:** Exploit delivery against GPU driver stack
- **Payload:** Target CUDA driver vulnerabilities (CVE-2024-0132 NVIDIA Container Toolkit TOCTOU, CVE-2025-23254 TensorRT-LLM pickle deserialization) for host-level access through container escape
- **Real-world precedent:** CVE-2024-0132 allowed container escape through NVIDIA Container Toolkit — any container with GPU access could break out to host. 25,000+ organizations running Triton Inference Server affected by CVE-2025-23319 chain.
- **Distinguishing factor:** Targets the GPU driver stack specifically — unique attack surface not present in CPU-only infrastructure.

**`T14-AP-001B`** — Cryptomining Injection into Training Jobs
- **Injection context:** Supply chain or insider access to training pipeline
- **Payload:** Inject cryptomining payloads into distributed training job containers or modify training scripts to allocate GPU cycles to mining during idle phases
- **Real-world precedent:** LLMjacking evolved from cryptojacking — Sysdig documented credential theft campaigns specifically targeting AI services, with cryptojacking market growing 20% in 2025 alone.
- **Distinguishing factor:** Parasitic compute theft that coexists with legitimate workloads — may go undetected for weeks if GPU utilization appears normal.

**`T14-AP-001C`** — Kubernetes GPU Operator Compromise
- **Injection context:** Network access to Kubernetes cluster management plane
- **Payload:** Exploit NVIDIA GPU Operator or device plugin misconfigurations for cluster-wide GPU access. Target default ServiceAccount tokens, unprotected kubelet APIs, or RBAC misconfigurations granting GPU scheduling permissions.
- **Real-world precedent:** Kubernetes misconfiguration is the primary initial access vector for cloud-native attacks. GPU operators add a privileged component that is frequently overlooked in security audits.
- **Distinguishing factor:** Targets the Kubernetes-GPU integration layer — the GPU operator runs as a privileged daemonset with host device access.

**`T14-AP-001D`** — PCIe DMA Attack
- **Injection context:** Physical or firmware-level access
- **Payload:** Exploit PCIe direct memory access to read/write GPU memory from another PCIe device, extracting model weights or injecting malicious computation
- **Real-world precedent:** GPU memory is accessible via PCIe without IOMMU protections in many configurations. Research has demonstrated cross-VM GPU memory leakage in shared environments.
- **Distinguishing factor:** Hardware-level attack bypassing all software security — requires physical access or firmware compromise.

**`T14-AP-001E`** — Cloud GPU API Credential Theft
- **Injection context:** Stolen credentials (phishing, exposed .env files, leaked API keys)
- **Payload:** Use stolen AWS/GCP/Azure credentials to provision GPU instances (p4d.24xlarge, A100 instances) or access existing GPU-backed services. Automated using Shodan/Censys scanning for exposed endpoints.
- **Real-world precedent:** Operation Bizarre Bazaar (Pillar Security, January 2026) — systematic scanning for exposed LLM endpoints, credential validation, commercial resale. 35,000+ attack sessions in 40 days.
- **ASR data:** Kaspersky honeypot: Shodan discovery in 3 hours, recon requests within 1 hour, 113,000+ requests/month from thousands of IPs.
- **Distinguishing factor:** Highest-volume attack vector — credential theft is the dominant initial access method for GPU hijacking.

**`T14-AP-001F`** — GPU Memory Overflow DoS
- **Injection context:** API access to inference endpoint
- **Payload:** Submit inputs designed to exhaust GPU VRAM (extremely long sequences, adversarial inputs triggering maximum KV-cache allocation), causing OOM kills that crash the serving process
- **Distinguishing factor:** DoS through GPU memory exhaustion rather than CPU/network — specific to GPU-served models.

**`T14-AP-001G`** — Multi-GPU Synchronization Exploitation
- **Injection context:** Network access to distributed training communication (NCCL, MPI)
- **Payload:** Exploit unencrypted/unauthenticated NCCL all-reduce communications between GPUs in a distributed training job. Inject gradient modifications or redirect synchronization to attacker-controlled nodes.
- **Real-world precedent:** ShadowMQ research (Oligo Security) revealed that ZeroMQ-based inter-process communication in ML frameworks uses unsafe deserialization (pickle) by default.
- **Distinguishing factor:** Targets the distributed training communication layer — unique to multi-GPU/multi-node training infrastructure.

**`T14-AP-001H`** — NVIDIA Container Runtime Escape
- **Injection context:** Container with GPU access in shared cluster
- **Payload:** Exploit NVIDIA Container Toolkit vulnerabilities (CVE-2024-0132 TOCTOU) to escape container isolation and access host-level GPU resources, potentially compromising all GPU workloads on the node
- **Distinguishing factor:** Container escape through GPU-specific runtime — the nvidia-container-toolkit is a privileged component that bridges container isolation.

**`T14-AP-001I`** — Distributed Training Job Theft
- **Injection context:** Cluster access with job submission privileges
- **Payload:** Submit training jobs that appear legitimate but dedicate GPU cycles to attacker workloads (model training for resale, cryptomining, inference serving for unauthorized users)
- **Distinguishing factor:** Abuse of legitimate job scheduling rather than exploitation — harder to distinguish from authorized workloads.

**`T14-AP-001J`** — GPU Virtualization Cross-VM Attack
- **Injection context:** Co-tenant in shared GPU cloud environment
- **Payload:** Exploit GPU virtualization (MIG, vGPU) isolation failures to read other tenants' GPU memory, extract model weights, or interfere with their computations
- **Real-world precedent:** Research has demonstrated GPU memory leakage between VMs sharing the same physical GPU. NVIDIA MIG provides better isolation than vGPU but is not universally deployed.
- **Distinguishing factor:** Multi-tenancy attack — requires co-tenancy on the same physical GPU, analogous to CPU side-channel attacks but through GPU memory.

</details>

#### Chaining

GPU farm hijacking provides compute resources that enable **T14-AT-003 (Cost Inflation)** when the attacker runs workloads on the victim's account, **T14-AT-009 (Resource Starvation)** when hijacked GPUs are no longer available for legitimate use, and **T14-AT-013 (Economic Espionage)** when GPU memory access reveals model weights or training data.

#### Detection

- Monitor for unexpected GPU utilization patterns (sustained high utilization outside training schedules, utilization on instances not running ML workloads)
- Alert on new GPU instance provisioning from unusual geolocations or at unusual times
- Network monitoring for connections to known cryptomining pools or unauthorized NCCL/ZeroMQ traffic
- Kubernetes audit logs for GPU resource requests from unexpected service accounts
- Reference: `signatures/sigma/t14-infrastructure.yml` — detects ZeroMQ traffic on ports 5555/5556

#### Mitigation

| Control | Effectiveness | Notes |
|:---|:---|:---|
| Authentication on all inference endpoints | CRITICAL | Never expose Ollama, vLLM, or TensorRT-LLM without authentication. Default-deny network policy. |
| Cloud credential rotation and monitoring | HIGH | Rotate API keys, monitor for credential leakage in public repos, implement least-privilege IAM. |
| GPU utilization anomaly detection | HIGH | Baseline normal GPU patterns, alert on deviations. Catches cryptomining and unauthorized inference serving. |
| NVIDIA Container Toolkit patching | HIGH | Patch CVE-2024-0132 and similar container escape vulnerabilities. GPU runtime is a privileged attack surface. |
| NCCL encryption | MEDIUM | Enable NCCL encryption for distributed training. Not enabled by default in most frameworks. |

---


### `T14-AT-002` — Denial of Service Attacks

**Risk Score:** 240 🟠 HIGH
**OWASP LLM:** LLM04 (Model Denial of Service) | **OWASP ASI:** ASI06 (Cascading Failures)
**MITRE ATLAS:** AML.T0029 (Denial of ML Service)

#### Mechanism

LLM inference has a fundamental asymmetry: a short input can trigger enormous computational cost. A single max-token request costs 100–1000x the compute of a typical query, and adversarial inputs can be specifically crafted to maximize this ratio. Sponge examples (Shumailov et al., 2021) demonstrated that inputs can be optimized to maximize inference energy consumption. ThinkTrap (arXiv:2512.07086) showed that reasoning models are especially vulnerable — crafted prompts inflate output length and exhaust GPU resources by inducing extended thinking chains. Engorgio (ICLR 2025) achieved max-length outputs across multiple LLMs with black-box optimization. The trust assumption violated is that input cost is bounded and predictable — in reality, an attacker with API access can submit inputs specifically optimized to maximize per-request compute cost, turning the inference endpoint into a resource-exhaustion weapon. Tool-calling chains in agentic systems amplify this further (arXiv:2601.10955): a single prompt can trigger recursive tool calls that multiply compute cost beyond the max-token limit.

#### Attack Procedures

<details>
<summary><b>Attack Procedures (10)</b></summary>

**`T14-AP-002A`** — Max-Token Flooding
- **Injection context:** API access to inference endpoint
- **Payload:** Flood API with prompts engineered to produce maximum-length responses (long-form instructions, "explain in maximum detail," repetitive generation triggers), exhausting token quotas and GPU time
- **Real-world precedent:** ThinkTrap (2025) demonstrated that reasoning models can be induced into >5-minute thinking chains with crafted inputs. At $0.01–$0.06 per 1K output tokens, sustained max-token flooding at scale generates $10,000+/day in compute costs.
- **Distinguishing factor:** Simplest DoS — high-volume max-token requests. Limited by rate limiting and quota enforcement.

**`T14-AP-002B`** — Recursive Agent Loops
- **Injection context:** Prompt injection in agentic system
- **Payload:** Inject instructions that cause the agent to enter infinite tool-calling loops (e.g., "search for X, then search for the results of the first search, then..."). Each loop iteration consumes a full inference cycle.
- **Real-world precedent:** arXiv:2601.10955 demonstrated that tool-calling chains bypass single-turn token limits — a single prompt triggers multi-turn computation with cumulative cost.
- **Distinguishing factor:** Exploits agentic architecture — cost amplification beyond single-request limits through recursive tool use.

**`T14-AP-002C`** — Adversarial Crash Inputs
- **Injection context:** API access to inference endpoint
- **Payload:** Submit inputs that trigger model crashes through edge cases in tokenization, attention computation, or output processing. Unicode edge cases, extremely long single tokens, or inputs exploiting KV-cache bugs.
- **Real-world precedent:** CVE-2026-22778 (vLLM CVSS 9.8) — RCE via malicious video URL. Earlier vLLM vulnerabilities allowed denial of service through malformed inputs.
- **Distinguishing factor:** Targets crash conditions rather than resource exhaustion — a single request can take down the serving process.

**`T14-AP-002D`** — Memory Leak Exploitation
- **Injection context:** Sustained API access over time
- **Payload:** Submit request patterns that trigger memory leaks in the serving framework (KV-cache not freed, connection pool exhaustion, tensor memory fragmentation), causing gradual degradation until OOM.
- **Distinguishing factor:** Slow-burn DoS — degradation over hours rather than immediate crash. Harder to detect, harder to attribute.

**`T14-AP-002E`** — Distributed Endpoint Flooding
- **Injection context:** Distributed botnet or cloud instances
- **Payload:** Coordinate distributed max-token requests across multiple source IPs to overwhelm rate limiting per-IP while exceeding aggregate capacity
- **Distinguishing factor:** Traditional DDoS applied to AI endpoints — scale-based rather than adversarial-input-based.

**`T14-AP-002F`** — Worst-Case Algorithmic Complexity
- **Injection context:** API access with crafted inputs
- **Payload:** Sponge examples — inputs specifically optimized (via gradient or genetic algorithms) to maximize attention computation and energy consumption. Engorgio (ICLR 2025) achieved max-length outputs with black-box optimization.
- **ASR data:** ThinkTrap achieved highest output length across all tested LLMs. Engorgio achieved near-max-length generation on GPT-4, Claude, and Gemini.
- **Distinguishing factor:** Adversarial optimization of input for maximum compute cost — the most efficient per-request DoS.

**`T14-AP-002G`** — Multi-Account Rate Limit Evasion
- **Injection context:** Multiple accounts (free tier abuse, stolen credentials)
- **Payload:** Distribute attack traffic across many accounts to stay below per-account rate limits while exceeding aggregate service capacity
- **Distinguishing factor:** Circumvents per-account rate limiting through horizontal scaling of accounts.

**`T14-AP-002H`** — KV-Cache Poisoning
- **Injection context:** API access to cached inference endpoint
- **Payload:** Submit inputs designed to populate the KV-cache with adversarial entries that degrade performance for subsequent legitimate requests (cache pollution with worst-case entries)
- **Distinguishing factor:** Attacks the caching layer rather than direct computation — degrades performance for all users, not just the attacker's requests.

**`T14-AP-002I`** — Autoscaling Abuse
- **Injection context:** API access to autoscaling-enabled endpoint
- **Payload:** Submit burst traffic to trigger autoscaling to maximum capacity, then drop traffic. The scaling-up cost is incurred (new instances provisioned) while the attacker pays nothing. Repeated cycles create cost without sustained load.
- **Distinguishing factor:** Exploits autoscaling economics — the cost of scaling up exceeds the cost of the requests that trigger it.

**`T14-AP-002J`** — Model Loading DoS
- **Injection context:** API access to on-demand model loading endpoint
- **Payload:** Request inference on models that are not currently loaded, forcing expensive model-load operations (loading 70B+ parameter models takes minutes and requires full GPU VRAM allocation). Rapidly switch between models to thrash the loading system.
- **Distinguishing factor:** Targets the model loading pipeline rather than inference — each model swap costs minutes of GPU time with zero useful computation.

</details>

#### Chaining

DoS attacks enable **T14-AT-003 (Cost Inflation)** directly through compute cost generation. In competitive contexts, DoS chains into **T14-AT-006 (Competitive Sabotage)** by degrading a competitor's AI service availability during critical periods.

#### Detection

- Per-request compute cost monitoring — alert on requests that consume >10x the median compute
- Token output length distribution monitoring — flag requests consistently producing max-length outputs
- Autoscaling event correlation — detect patterns of scale-up triggered by short bursts followed by scale-down
- Model loading frequency monitoring — flag rapid model switching on on-demand endpoints
- Reference: `signatures/sigma/t14-infrastructure.yml`

#### Mitigation

| Control | Effectiveness | Notes |
|:---|:---|:---|
| Per-request compute budgets | HIGH | Cap inference time and token count per request. Kills max-token and sponge attacks. |
| Rate limiting (per-account AND aggregate) | HIGH | Enforce both per-account and global rate limits. Prevents distributed flooding. |
| Autoscaling bounds | HIGH | Set minimum AND maximum scaling limits. Prevent unbounded scale-up on burst traffic. |
| Input complexity analysis | MEDIUM | Pre-screen inputs for sponge-like properties before inference. Adds latency. |
| Agent loop detection | HIGH | Detect and terminate recursive tool-calling loops after N iterations. |

---


### `T14-AT-003` — Cost Inflation Attacks

**Risk Score:** 235 🟠 HIGH
**OWASP LLM:** LLM04 (Model Denial of Service) | **OWASP ASI:** ASI06 (Cascading Failures)
**MITRE ATLAS:** AML.T0029 (Denial of ML Service)

#### Mechanism

AI infrastructure pricing creates an amplification vulnerability: the cost of generating a request is negligible compared to the cost of serving it. A single API call costing the attacker fractions of a cent may consume dollars in GPU compute on the victim's account. Cost inflation attacks exploit this asymmetry by maximizing resource consumption against a target's billing account — either through compromised credentials, abused free tiers, or manipulation of autoscaling and billing systems. Unlike DoS (T14-AT-002) which aims to degrade availability, cost inflation targets the *financial* channel while keeping the service operational, making it harder to detect because all requests appear to succeed. The trust assumption violated is that metered billing accurately reflects authorized usage — there is no mechanism in most cloud AI services to distinguish attacker-generated compute costs from legitimate usage until the invoice arrives.

#### Attack Procedures

<details>
<summary><b>Attack Procedures (10)</b></summary>

**`T14-AP-003A`** — Competitor Account GPU Abuse
- **Injection context:** Compromised cloud credentials
- **Payload:** Provision maximum GPU instances on target's cloud account. Run continuous inference or training workloads to generate billing. At $30/hr for H100 instances, 10 instances for 30 days = $216,000.
- **Real-world precedent:** LLMjacking campaigns generate $46,000–$100,000/day per compromised account (Sysdig 2026).
- **Distinguishing factor:** Direct compute billing fraud — highest per-incident cost.

**`T14-AP-003B`** — Infinite API Loop Creation
- **Injection context:** Prompt injection in agentic system connected to billing API
- **Payload:** Inject instructions creating recursive API calls: agent calls tool A, which triggers tool B, which calls tool A. Each iteration generates billing events.
- **Distinguishing factor:** Self-sustaining cost generation through recursive agent behavior.

**`T14-AP-003C`** — Free Tier to Paid Escalation
- **Injection context:** Account abuse across multiple free-tier accounts
- **Payload:** Create multiple free-tier accounts, exhaust free quotas triggering automatic upgrade to paid tiers, then generate maximum usage before payment fails.
- **Distinguishing factor:** Exploits billing system design — free-to-paid transitions often have delayed payment verification.

**`T14-AP-003D`** — Autoscaling Cost Manipulation
- **Injection context:** API access to autoscaling-enabled service
- **Payload:** Generate traffic patterns that trigger maximum autoscaling (burst → sustain → burst), forcing provisioning of expensive instances that remain billable through cooldown periods even after traffic drops.
- **Distinguishing factor:** Exploits autoscaling hysteresis — the gap between scale-up trigger and scale-down cooldown.

**`T14-AP-003E`** — Training Job Compute Abuse
- **Injection context:** Compromised training pipeline access
- **Payload:** Submit long-running training jobs on maximum GPU configurations. A single misconfgured job on 8x A100 for 7 days = $40,000+.
- **Distinguishing factor:** Training jobs consume orders of magnitude more compute than inference — single jobs can generate five-figure costs.

**`T14-AP-003F`** — Hidden Recurring Workloads
- **Injection context:** Persistent access to cluster or cloud account
- **Payload:** Deploy containerized workloads that run continuously on GPU instances but appear as legitimate services (renamed to match expected training job names, scheduled during low-monitoring periods).
- **Distinguishing factor:** Persistence-focused — designed to evade detection through mimicry of legitimate workloads.

**`T14-AP-003G`** — Pricing Model Exploitation
- **Injection context:** API access with knowledge of pricing structure
- **Payload:** Target the most expensive API operations (longest context windows, most expensive models, vision/multimodal endpoints) to maximize cost-per-request ratio.
- **Distinguishing factor:** Optimization of attack for maximum cost efficiency — knowledge of pricing tiers is the weapon.

**`T14-AP-003H`** — Data Egress Cost Generation
- **Injection context:** Compromised cloud account
- **Payload:** Trigger massive data egress (download model weights, export training datasets across regions) to generate inter-region and internet egress charges. Cloud egress typically costs $0.08–$0.12/GB.
- **Distinguishing factor:** Exploits egress pricing — data transfer costs accumulate independently of compute costs.

**`T14-AP-003I`** — A/B Testing Resource Waste
- **Injection context:** Access to A/B testing or experiment tracking system
- **Payload:** Create hundreds of concurrent experiment variants, each requiring separate model serving instances. The A/B testing framework provisions resources for each variant.
- **Distinguishing factor:** Exploits experiment management infrastructure — ML-specific cost amplification vector.

**`T14-AP-003J`** — Phantom Workload Billing
- **Injection context:** Compromised cloud billing or resource management access
- **Payload:** Create "phantom" resources — instances provisioned but not connected to any workload, GPU reservations that block legitimate use while incurring charges.
- **Distinguishing factor:** Resources that generate cost without computation — pure billing fraud.

</details>

#### Chaining

Cost inflation chains from **T14-AT-001 (GPU Farm Hijacking)** when stolen credentials are used for billing fraud rather than compute theft. Chains into **T14-AT-006 (Competitive Sabotage)** when cost inflation is targeted at a competitor's AI operations to force budget reductions.

#### Detection

- Billing anomaly detection — alert on daily spend exceeding 2x historical baseline
- Instance provisioning monitoring — flag GPU instance creation from unusual regions/accounts/times
- Egress volume tracking — alert on data egress exceeding normal patterns
- Training job audit — verify all running training jobs against authorized schedules

#### Mitigation

| Control | Effectiveness | Notes |
|:---|:---|:---|
| Billing alerts and hard caps | CRITICAL | Set maximum daily/monthly spend caps that halt provisioning when exceeded. Most effective single control. |
| Credential lifecycle management | HIGH | Rotate API keys, monitor for leakage, implement just-in-time access for GPU provisioning. |
| Instance provisioning approval | MEDIUM | Require manual approval for GPU instance types above a cost threshold. Adds friction to legitimate use. |
| Cost attribution and tagging | HIGH | Tag all resources to teams/projects. Untagged GPU instances are immediate red flags. |

---

### `T14-AT-004` — Market Manipulation via AI

**Risk Score:** 255 🔴 CRITICAL
**OWASP LLM:** LLM05 (Insecure Output Handling) | **OWASP ASI:** ASI01 (Agent Goal Hijack)
**MITRE ATLAS:** AML.T0048 (ML Supply Chain Compromise)

#### Mechanism

Financial markets operate on information asymmetry — prices move based on new information. AI systems (deepfake generators, LLM content farms, sentiment analysis manipulators) can create synthetic information at a scale and quality that overwhelms human verification capacity, enabling market manipulation at speeds that outpace regulatory detection. The trust assumption violated is that information driving market decisions is authentic — deepfake CEO statements, AI-generated fake SEC filings, and manipulated sentiment signals are indistinguishable from authentic information at the point of market impact. The Arup deepfake attack ($25.6M, January 2024) demonstrated that AI-generated executive impersonation can authorize real financial transactions. The Bombay Stock Exchange deepfake incident (January 2026) showed that synthetic CEO videos can move public markets. The attack surface is the gap between information creation speed (seconds) and verification speed (hours to days).

#### Attack Procedures

<details>
<summary><b>Attack Procedures (10)</b></summary>

**`T14-AP-004A`** — AI-Generated Market-Moving News
- **Injection context:** Content distribution at scale (social media, news aggregators, financial terminals)
- **Payload:** Generate and distribute realistic but fabricated news articles about corporate events (mergers, earnings, regulatory actions) through multiple channels simultaneously, targeting algorithmic trading systems that react to news sentiment.
- **Real-world precedent:** AI-enabled fraud surged 1,210% in 2025 (Vectra AI). Chainalysis reported $14B in crypto scam losses in 2025, with AI-enabled scams 4.5x more profitable.
- **Distinguishing factor:** Scale-based — hundreds of articles across platforms simultaneously, overwhelming manual verification.

**`T14-AP-004B`** — Deepfake CEO Announcements
- **Injection context:** Video/audio distribution through social media, messaging apps, or compromised corporate channels
- **Payload:** Generate deepfake video of a public company CEO announcing earnings, mergers, resignations, or regulatory issues. Distribute through channels that reach algorithmic trading feeds.
- **Real-world precedent:** Bombay Stock Exchange warning (January 2026) — deepfake CEO videos promoting fraudulent stock tips. Bank of Italy deepfake of governor Fabio Panetta for investment fraud. Arup $25.6M CFO deepfake.
- **ASR data:** Voice clones from 3 seconds of audio. Deepfake vishing attacks up 1,600% Q1 2025 vs Q4 2024.
- **Distinguishing factor:** Executive impersonation — exploits the trust in identifiable authority figures to move markets.

**`T14-AP-004C`** — Sentiment Analysis Manipulation
- **Injection context:** Social media platforms feeding financial sentiment models
- **Payload:** Deploy AI-generated social media accounts posting coordinated sentiment about target securities. Financial sentiment models (Bloomberg, Reuters, proprietary quant) aggregate this signal into trading decisions.
- **Distinguishing factor:** Targets the AI-to-AI pipeline — synthetic social media sentiment manipulates algorithmic trading models.

**`T14-AP-004D`** — Algorithmic Trading Adversarial Inputs
- **Injection context:** Market data feeds consumed by HFT systems
- **Payload:** Submit patterns of trades or order book manipulations specifically designed to trigger adverse behavior in known trading algorithms (spoofing, layering, momentum ignition adapted for AI-based trading).
- **Distinguishing factor:** Adversarial ML applied to financial AI — crafted inputs targeting known model architectures.

**`T14-AP-004E`** — Synthetic Regulatory Filings
- **Injection context:** EDGAR, corporate communications channels
- **Payload:** Generate realistic but fabricated SEC filings, press releases, or regulatory disclosures using LLMs trained on authentic corporate communications. Target afterhours or pre-market release windows for maximum impact before verification.
- **Distinguishing factor:** Document-level fabrication — targets the trust in official filing channels.

**`T14-AP-004F`** — Synthetic Insider Information
- **Injection context:** Private messaging, leaked document channels (Telegram, Discord, dark web forums)
- **Payload:** Generate fabricated internal documents (board minutes, M&A term sheets, earnings previews) and leak them through channels that traders monitor for insider information.
- **Distinguishing factor:** Exploits the market for insider information — creates demand-side pull for fabricated content.

**`T14-AP-004G`** — Prediction Market Manipulation
- **Injection context:** Prediction market platforms (Polymarket, Kalshi, Metaculus)
- **Payload:** Combine AI-generated misinformation with coordinated prediction market positions. Fabricated events shift prediction probabilities, which feed back into news cycles and financial markets.
- **Distinguishing factor:** Recursive amplification — prediction markets and news create a feedback loop.

**`T14-AP-004H`** — HFT Adversarial Perturbation
- **Injection context:** Market data feed manipulation or co-located exchange access
- **Payload:** Submit microsecond-level order patterns designed to confuse ML-based HFT systems — trigger false signals that cause algorithmic cascades (flash crash induction).
- **Distinguishing factor:** Speed-based — operates at microsecond timescales beyond human monitoring capacity.

**`T14-AP-004I`** — Cryptocurrency Market Fabrication
- **Injection context:** Crypto social media (Twitter/X, Telegram, Discord)
- **Payload:** AI-generated fake partnership announcements, exchange listings, or whale wallet movements paired with coordinated trading. Crypto markets have less regulatory oversight and faster manipulation cycles.
- **ASR data:** $14B crypto scam losses in 2025 (Chainalysis). AI-powered pump-and-dump increasingly automated.
- **Distinguishing factor:** Crypto's lower regulatory barrier and 24/7 trading makes it the highest-ROI market manipulation target.

**`T14-AP-004J`** — AI-Orchestrated Pump and Dump
- **Injection context:** Multi-channel coordinated campaign
- **Payload:** Fully automated pipeline: accumulate position → deploy LLM-generated promotion across social media, forums, and messaging → deepfake endorsement videos → sell during price spike. AI orchestrates timing and channel selection.
- **Distinguishing factor:** End-to-end AI-orchestrated fraud — no human intervention after campaign launch.

</details>

#### Chaining

Market manipulation chains from **T8 (External Deception)** for content generation capability and **T15 (Human Workflow Exploitation)** for social engineering that enables insider access. Chains into **T14-AT-013 (Economic Espionage)** when market manipulation is used to extract value from competitor organizations.

#### Detection

- Deepfake detection on financial communications — audio/video authenticity verification for executive communications
- Cross-reference speed: time between information publication and trading action — anomalously fast responses indicate algorithmic exploitation
- Sentiment analysis anomaly detection — flag sudden coordinated sentiment shifts inconsistent with underlying news
- Trading pattern analysis for wash trading, spoofing, and layering around AI-generated information events

#### Mitigation

| Control | Effectiveness | Notes |
|:---|:---|:---|
| Executive communication authentication | HIGH | Cryptographic signing or watermarking of official executive communications. Prevents deepfake substitution. |
| Information verification delays | MEDIUM | Trading systems should implement verification delays for market-moving information from unverified sources. Reduces HFT advantage. |
| Deepfake detection in financial workflows | HIGH | Deploy real-time deepfake detection on video/audio communications in financial authorization chains. |
| Multi-channel verification for material actions | HIGH | Require out-of-band verification for financial transactions triggered by any digital communication. Prevented Arup-type attacks. |

---


### `T14-AT-005` — Critical Infrastructure Attacks

**Risk Score:** 270 🔴 CRITICAL
**OWASP LLM:** LLM06 (Excessive Agency) | **OWASP ASI:** ASI03 (Tool Misuse)
**MITRE ATLAS:** AML.T0049 (Exploit Public-Facing Application)

#### Mechanism

AI systems increasingly manage critical infrastructure — power grid load balancing, water treatment chemical dosing, traffic signal optimization, hospital resource allocation. These systems trust their input data and control algorithms implicitly. Attacks target this trust by manipulating AI inputs (sensor data poisoning), compromising AI model integrity (adversarial examples against control models), or exploiting the AI-to-physical-system interface where software decisions become physical actions. The consequence amplification is unique: a software vulnerability in a traditional system causes data loss; a vulnerability in an AI managing a power grid causes blackouts. The trust boundary violated is between digital AI computation and physical-world actuation — AI control systems lack the independent physical safety interlocks that pre-AI control systems relied on. Hacktivist groups (Z-Pentest) conducted repeated ICS/OT intrusions in 2025, and nation-state pre-positioning in energy infrastructure (Volt Typhoon) targets AI-managed systems specifically.

#### Attack Procedures

<details>
<summary><b>Attack Procedures (10)</b></summary>

**`T14-AP-005A`** — Power Grid AI Manipulation
- **Injection context:** Infrastructure/economic attack
- **Payload:** Power Grid AI Manipulation — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the critical infrastructure attacks technique category.

**`T14-AP-005B`** — Water Treatment AI Compromise
- **Injection context:** Infrastructure/economic attack
- **Payload:** Water Treatment AI Compromise — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the critical infrastructure attacks technique category.

**`T14-AP-005C`** — Traffic AI Gridlock
- **Injection context:** Infrastructure/economic attack
- **Payload:** Traffic AI Gridlock — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the critical infrastructure attacks technique category.

**`T14-AP-005D`** — Hospital AI Disruption
- **Injection context:** Infrastructure/economic attack
- **Payload:** Hospital AI Disruption — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the critical infrastructure attacks technique category.

**`T14-AP-005E`** — Air Traffic AI Attack
- **Injection context:** Infrastructure/economic attack
- **Payload:** Air Traffic AI Attack — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the critical infrastructure attacks technique category.

**`T14-AP-005F`** — Supply Chain AI Shortage
- **Injection context:** Infrastructure/economic attack
- **Payload:** Supply Chain AI Shortage — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the critical infrastructure attacks technique category.

**`T14-AP-005G`** — Telecom AI Infrastructure Attack
- **Injection context:** Infrastructure/economic attack
- **Payload:** Telecom AI Infrastructure Attack — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the critical infrastructure attacks technique category.

**`T14-AP-005H`** — Emergency Response AI Compromise
- **Injection context:** Infrastructure/economic attack
- **Payload:** Emergency Response AI Compromise — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the critical infrastructure attacks technique category.

**`T14-AP-005I`** — Smart City Manipulation
- **Injection context:** Infrastructure/economic attack
- **Payload:** Smart City Manipulation — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the critical infrastructure attacks technique category.

**`T14-AP-005J`** — ICS AI System Attack
- **Injection context:** Infrastructure/economic attack
- **Payload:** ICS AI System Attack — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the critical infrastructure attacks technique category.

</details>

#### Chaining

Critical infrastructure attacks chain from **T14-AT-007 (Nation-State AI Warfare)** as strategic objectives and from **T14-AT-012 (Cloud Provider Exploitation)** when infrastructure AI runs on cloud platforms. Chains into **T14-AT-014 (Systemic Risk Creation)** when infrastructure failures cascade across interconnected systems.

#### Detection

Monitor AI control system inputs for anomalous sensor data patterns; implement independent physical safety interlocks that override AI decisions; air-gap critical AI control networks; behavioral analysis of AI control outputs for deviation from physical constraints.

#### Mitigation

| Control | Effectiveness | Notes |
|:---|:---|:---|
| Independent physical safety interlocks | CRITICAL | AI decisions must pass through non-AI safety validation before physical actuation. |
| Air-gapped control networks | HIGH | Critical infrastructure AI should not be reachable from the internet. |
| Sensor data validation | HIGH | Cross-validate sensor inputs against physical models before AI processing. |
| Human-in-the-loop for irreversible actions | HIGH | Require human confirmation for AI decisions that affect physical safety. |

---


### `T14-AT-006` — Competitive Sabotage

**Risk Score:** 245 🟠 HIGH
**OWASP LLM:** LLM03 (Supply Chain Vulnerabilities) | **OWASP ASI:** ASI05 (Memory and Context Manipulation)
**MITRE ATLAS:** AML.T0020 (Poison Training Data), AML.T0044 (Full ML Model Access)

#### Mechanism

AI competitive advantage is fragile — model quality depends on training data, serving infrastructure, and user trust, all of which can be degraded by a competitor with offensive capability. Competitive sabotage targets these dependencies: poisoning public training datasets that competitors scrape, extracting proprietary models through query-based distillation, injecting backdoors into shared ML libraries, or attacking recommendation systems to degrade output quality. The trust assumption violated is inter-organizational: companies trust shared data sources, open-source libraries, and public APIs that competitors can manipulate. Unlike traditional industrial sabotage which requires physical access, AI sabotage operates entirely through digital interfaces — a competitor can degrade your model quality by poisoning the datasets you train on without ever touching your systems directly.

#### Attack Procedures

<details>
<summary><b>Attack Procedures (10)</b></summary>

**`T14-AP-006A`** — Training Data Poisoning
- **Injection context:** Infrastructure/economic attack
- **Payload:** Training Data Poisoning — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the competitive sabotage technique category.

**`T14-AP-006B`** — Model Extraction via Queries
- **Injection context:** Infrastructure/economic attack
- **Payload:** Model Extraction via Queries — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the competitive sabotage technique category.

**`T14-AP-006C`** — ML Pipeline Backdoor
- **Injection context:** Infrastructure/economic attack
- **Payload:** ML Pipeline Backdoor — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the competitive sabotage technique category.

**`T14-AP-006D`** — Adversarial SEO
- **Injection context:** Infrastructure/economic attack
- **Payload:** Adversarial SEO — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the competitive sabotage technique category.

**`T14-AP-006E`** — Recommendation System Attack
- **Injection context:** Infrastructure/economic attack
- **Payload:** Recommendation System Attack — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the competitive sabotage technique category.

**`T14-AP-006F`** — Pricing Algorithm Manipulation
- **Injection context:** Infrastructure/economic attack
- **Payload:** Pricing Algorithm Manipulation — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the competitive sabotage technique category.

**`T14-AP-006G`** — Customer Data Poisoning
- **Injection context:** Infrastructure/economic attack
- **Payload:** Customer Data Poisoning — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the competitive sabotage technique category.

**`T14-AP-006H`** — AI-Generated Negative Reviews
- **Injection context:** Infrastructure/economic attack
- **Payload:** AI-Generated Negative Reviews — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the competitive sabotage technique category.

**`T14-AP-006I`** — Competitive Intelligence Theft
- **Injection context:** Infrastructure/economic attack
- **Payload:** Competitive Intelligence Theft — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the competitive sabotage technique category.

**`T14-AP-006J`** — Product Sabotage
- **Injection context:** Infrastructure/economic attack
- **Payload:** Product Sabotage — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the competitive sabotage technique category.

</details>

#### Chaining

Competitive sabotage chains from **T6 (Training & Feedback Poisoning)** for data poisoning techniques and **T10 (Integrity & Confidentiality Breach)** for model extraction. Chains into **T14-AT-013 (Economic Espionage)** when extracted models or intelligence provide competitive advantage.

#### Detection

Monitor training data sources for anomalous content changes; track model performance degradation that correlates with external data updates; implement canary data points that detect unauthorized model extraction; audit ML library dependencies for unexpected modifications.

#### Mitigation

| Control | Effectiveness | Notes |
|:---|:---|:---|
| Training data provenance tracking | HIGH | Verify and version all training data sources. Detect poisoning through data lineage. |
| Model extraction detection | MEDIUM | Monitor query patterns for distillation signatures (systematic coverage of input space). |
| Supply chain integrity (ML libraries) | HIGH | Pin dependency versions, verify checksums, audit for backdoors in training pipeline components. |
| Output watermarking | MEDIUM | Embed watermarks in model outputs that survive extraction, enabling detection of stolen models. |

---


### `T14-AT-007` — Nation-State AI Warfare

**Risk Score:** 280 🔴 CRITICAL
**OWASP LLM:** —
**MITRE ATLAS:** AML.T0048 (ML Supply Chain Compromise), AML.T0049 (Exploit Public-Facing Application)

#### Mechanism

Nation-states operate at a scale, persistence, and sophistication that fundamentally exceeds criminal or hacktivist operations. AI amplifies nation-state capability across four domains: disinformation (LLM content farms producing millions of tailored messages), surveillance (AI-powered mass analysis of communications, social media, and biometric data), cyber weapons (AI-accelerated vulnerability discovery and autonomous exploit generation), and strategic pre-positioning (embedding AI-powered implants in adversary infrastructure). The trust assumption violated is systemic: the entire information environment becomes unreliable when nation-states deploy AI-generated content at scale. In 2025, state-sponsored groups (APT28, Volt Typhoon, Salt Typhoon) increasingly incorporated AI tools, with Malwarebytes predicting MCP-based attack frameworks as a defining criminal/state capability for 2026. The asymmetry is that defensive AI must be right every time; offensive AI only needs to succeed once.

#### Attack Procedures

<details>
<summary><b>Attack Procedures (10)</b></summary>

**`T14-AP-007A`** — AI Disinformation Campaigns
- **Injection context:** Infrastructure/economic attack
- **Payload:** AI Disinformation Campaigns — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the nation-state ai warfare technique category.

**`T14-AP-007B`** — AI Mass Surveillance
- **Injection context:** Infrastructure/economic attack
- **Payload:** AI Mass Surveillance — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the nation-state ai warfare technique category.

**`T14-AP-007C`** — AI Cyber Weapons
- **Injection context:** Infrastructure/economic attack
- **Payload:** AI Cyber Weapons — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the nation-state ai warfare technique category.

**`T14-AP-007D`** — Election Manipulation
- **Injection context:** Infrastructure/economic attack
- **Payload:** Election Manipulation — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the nation-state ai warfare technique category.

**`T14-AP-007E`** — AI Espionage Operations
- **Injection context:** Infrastructure/economic attack
- **Payload:** AI Espionage Operations — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the nation-state ai warfare technique category.

**`T14-AP-007F`** — AI Research Facility Attack
- **Injection context:** Infrastructure/economic attack
- **Payload:** AI Research Facility Attack — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the nation-state ai warfare technique category.

**`T14-AP-007G`** — IP Theft at Scale
- **Injection context:** Infrastructure/economic attack
- **Payload:** IP Theft at Scale — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the nation-state ai warfare technique category.

**`T14-AP-007H`** — AI Propaganda Systems
- **Injection context:** Infrastructure/economic attack
- **Payload:** AI Propaganda Systems — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the nation-state ai warfare technique category.

**`T14-AP-007I`** — AI Bot Networks
- **Injection context:** Infrastructure/economic attack
- **Payload:** AI Bot Networks — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the nation-state ai warfare technique category.

**`T14-AP-007J`** — AI Psychological Operations
- **Injection context:** Infrastructure/economic attack
- **Payload:** AI Psychological Operations — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the nation-state ai warfare technique category.

</details>

#### Chaining

Nation-state operations chain ALL T14 techniques as components of comprehensive campaigns. **T14-AT-005 (Critical Infrastructure)** as strategic objectives, **T14-AT-004 (Market Manipulation)** for economic warfare, **T14-AT-013 (Economic Espionage)** for technology transfer.

#### Detection

Attribution is the primary challenge — nation-state operations use criminal proxies for deniability. Detect through: TTPs inconsistent with criminal motivation, infrastructure analysis linking to known state-sponsored groups, targeting patterns aligned with geopolitical objectives rather than financial gain.

#### Mitigation

| Control | Effectiveness | Notes |
|:---|:---|:---|
| National cyber defense coordination | HIGH | Participation in national cybersecurity frameworks (CISA, NCSC). Information sharing on nation-state TTPs. |
| Assume-breach architecture | HIGH | Design AI systems assuming nation-state actors have persistent access. Limit blast radius through segmentation. |
| AI-specific threat intelligence | HIGH | Subscribe to MITRE ATLAS and sector-specific threat feeds for AI-targeted nation-state activity. |
| Supply chain security for AI components | CRITICAL | Nation-states target AI supply chains (frameworks, models, training data). Verify integrity at every layer. |

---


### `T14-AT-008` — Ransomware via AI Systems

**Risk Score:** 260 🔴 CRITICAL
**OWASP LLM:** LLM06 (Excessive Agency) | **OWASP ASI:** ASI03 (Tool Misuse)
**MITRE ATLAS:** AML.T0049 (Exploit Public-Facing Application)

#### Mechanism

AI assets have uniquely high ransom value: a model trained over months on millions of dollars of compute cannot be regenerated quickly, training datasets may be irreplaceable, and inference service downtime directly impacts revenue. Ransomware targeting AI infrastructure exploits this value concentration — encrypting model weights is the AI equivalent of encrypting a company's core database, but with higher recovery costs because retraining is slower and more expensive than restoring from backup. The trust assumption violated is that AI assets are protected by the same backup and recovery mechanisms as traditional IT assets — in practice, model weights are often stored on high-performance storage (NVMe, distributed filesystems) that prioritizes speed over backup frequency, and training state (checkpoints, optimizer state) is rarely backed up with the same rigor as production databases. Malwarebytes (2026) documented that 86% of ransomware operations now use remote encryption from a single staging point, making traditional endpoint detection insufficient.

#### Attack Procedures

<details>
<summary><b>Attack Procedures (10)</b></summary>

**`T14-AP-008A`** — Model Weight Encryption
- **Injection context:** Infrastructure/economic attack
- **Payload:** Model Weight Encryption — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the ransomware via ai systems technique category.

**`T14-AP-008B`** — Training Data Lockout
- **Injection context:** Infrastructure/economic attack
- **Payload:** Training Data Lockout — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the ransomware via ai systems technique category.

**`T14-AP-008C`** — ML Pipeline Ransomware
- **Injection context:** Infrastructure/economic attack
- **Payload:** ML Pipeline Ransomware — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the ransomware via ai systems technique category.

**`T14-AP-008D`** — GPU Cluster Encryption
- **Injection context:** Infrastructure/economic attack
- **Payload:** GPU Cluster Encryption — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the ransomware via ai systems technique category.

**`T14-AP-008E`** — Inference Service Hostage
- **Injection context:** Infrastructure/economic attack
- **Payload:** Inference Service Hostage — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the ransomware via ai systems technique category.

**`T14-AP-008F`** — Model Marketplace Ransomware
- **Injection context:** Infrastructure/economic attack
- **Payload:** Model Marketplace Ransomware — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the ransomware via ai systems technique category.

**`T14-AP-008G`** — Notebook Environment Lockout
- **Injection context:** Infrastructure/economic attack
- **Payload:** Notebook Environment Lockout — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the ransomware via ai systems technique category.

**`T14-AP-008H`** — Cloud AI Resource Lockout
- **Injection context:** Infrastructure/economic attack
- **Payload:** Cloud AI Resource Lockout — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the ransomware via ai systems technique category.

**`T14-AP-008I`** — Research Compromise and Ransom
- **Injection context:** Infrastructure/economic attack
- **Payload:** Research Compromise and Ransom — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the ransomware via ai systems technique category.

**`T14-AP-008J`** — AI-Negotiated Ransomware
- **Injection context:** Infrastructure/economic attack
- **Payload:** AI-Negotiated Ransomware — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the ransomware via ai systems technique category.

</details>

#### Chaining

Ransomware chains from **T14-AT-001 (GPU Farm Hijacking)** for initial access and from **T13 (Supply Chain)** for ML pipeline compromise. The ransom payment itself chains into **T14-AT-013 (Economic Espionage)** — ransomware operators increasingly exfiltrate data before encryption for double-extortion.

#### Detection

Monitor for anomalous file access patterns on model storage (mass reads followed by mass writes = encryption); alert on unexpected changes to model checkpoint files; track GPU cluster access patterns for unauthorized remote encryption activity.

#### Mitigation

| Control | Effectiveness | Notes |
|:---|:---|:---|
| Immutable model backups | CRITICAL | Air-gapped, versioned backups of model weights and training data. Test restore regularly. |
| Model weight integrity monitoring | HIGH | Hash-based integrity checking on stored model weights. Alert on unauthorized modifications. |
| Network segmentation for training infrastructure | HIGH | Isolate training clusters from corporate network. Prevent lateral movement from compromised endpoints. |
| Remote encryption detection | HIGH | Monitor for SMB/NFS encryption patterns characteristic of remote ransomware (86% of 2025 operations). |

---


### `T14-AT-009` — Resource Starvation

**Risk Score:** 230 🟠 HIGH
**OWASP LLM:** LLM04 (Model Denial of Service) | **OWASP ASI:** ASI06 (Cascading Failures)
**MITRE ATLAS:** AML.T0029 (Denial of ML Service)

#### Mechanism

AI compute resources are shared and finite — cloud GPU instances are oversubscribed, API quotas serve multiple consumers, and training clusters have fixed capacity. Resource starvation exploits multi-tenant resource sharing by monopolizing shared resources to deny access to legitimate users. Unlike DoS (T14-AT-002) which overwhelms a service with requests, resource starvation targets the *supply side* — consuming GPUs, quotas, bandwidth, or storage before legitimate users can access them. The trust assumption violated is fair resource sharing in multi-tenant environments: cloud providers assume consumers will use resources proportionally, and quota systems assume legitimate usage patterns. An attacker who understands the resource allocation algorithm can systematically starve competitors of compute capacity, training data access, or API availability.

#### Attack Procedures

<details>
<summary><b>Attack Procedures (10)</b></summary>

**`T14-AP-009A`** — Regional GPU Monopolization
- **Injection context:** Infrastructure/economic attack
- **Payload:** Regional GPU Monopolization — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the resource starvation technique category.

**`T14-AP-009B`** — API Quota Exhaustion
- **Injection context:** Infrastructure/economic attack
- **Payload:** API Quota Exhaustion — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the resource starvation technique category.

**`T14-AP-009C`** — Compute Scarcity Creation
- **Injection context:** Infrastructure/economic attack
- **Payload:** Compute Scarcity Creation — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the resource starvation technique category.

**`T14-AP-009D`** — Dataset Access Blocking
- **Injection context:** Infrastructure/economic attack
- **Payload:** Dataset Access Blocking — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the resource starvation technique category.

**`T14-AP-009E`** — Shared Endpoint Overload
- **Injection context:** Infrastructure/economic attack
- **Payload:** Shared Endpoint Overload — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the resource starvation technique category.

**`T14-AP-009F`** — Cluster Memory Exhaustion
- **Injection context:** Infrastructure/economic attack
- **Payload:** Cluster Memory Exhaustion — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the resource starvation technique category.

**`T14-AP-009G`** — Network Bandwidth Consumption
- **Injection context:** Infrastructure/economic attack
- **Payload:** Network Bandwidth Consumption — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the resource starvation technique category.

**`T14-AP-009H`** — Credit Depletion
- **Injection context:** Infrastructure/economic attack
- **Payload:** Credit Depletion — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the resource starvation technique category.

**`T14-AP-009I`** — Pipeline Bottleneck Creation
- **Injection context:** Infrastructure/economic attack
- **Payload:** Pipeline Bottleneck Creation — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the resource starvation technique category.

**`T14-AP-009J`** — Training Data Starvation
- **Injection context:** Infrastructure/economic attack
- **Payload:** Training Data Starvation — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the resource starvation technique category.

</details>

#### Chaining

Resource starvation chains from **T14-AT-001 (GPU Farm Hijacking)** when hijacked resources reduce availability for legitimate users. Chains into **T14-AT-006 (Competitive Sabotage)** when resource starvation is targeted at specific competitors.

#### Detection

Monitor resource utilization for anomalous concentration patterns (single tenant consuming disproportionate resources); track API quota consumption rates across accounts; alert on storage or bandwidth consumption spikes inconsistent with workload patterns.

#### Mitigation

| Control | Effectiveness | Notes |
|:---|:---|:---|
| Fair-share resource scheduling | HIGH | Enforce per-tenant resource limits in shared clusters. Prevent single-consumer monopolization. |
| API quota management with burst limits | HIGH | Implement both sustained and burst rate limits to prevent quota exhaustion. |
| Resource reservation systems | MEDIUM | Allow critical workloads to reserve guaranteed resource allocations. Adds cost for guaranteed availability. |
| Multi-provider redundancy | HIGH | Distribute critical AI workloads across multiple cloud providers to prevent single-provider starvation. |

---


### `T14-AT-010` — Data Center Attacks

**Risk Score:** 250 🔴 CRITICAL
**OWASP LLM:** —
**MITRE ATLAS:** AML.T0049 (Exploit Public-Facing Application)

#### Mechanism

AI compute is geographically concentrated — a small number of data centers house the majority of the world's GPU clusters. This concentration creates single-point-of-failure risk at the physical layer. Data center attacks target the physical infrastructure that AI depends on: cooling systems (GPU clusters generate extreme heat and fail catastrophically without cooling), power distribution (sudden power loss during training corrupts checkpoints and damages hardware), physical security (unauthorized physical access to servers enables hardware implants and data theft), and supply chain (hardware backdoors in GPUs, network equipment, or storage). The trust assumption violated is physical security adequacy — AI data centers are high-value targets that may not have security commensurate with the value of their contents (models worth billions, training data representing years of collection).

#### Attack Procedures

<details>
<summary><b>Attack Procedures (10)</b></summary>

**`T14-AP-010A`** — Cooling System Attack
- **Injection context:** Infrastructure/economic attack
- **Payload:** Cooling System Attack — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the data center attacks technique category.

**`T14-AP-010B`** — Power Distribution Attack
- **Injection context:** Infrastructure/economic attack
- **Payload:** Power Distribution Attack — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the data center attacks technique category.

**`T14-AP-010C`** — Physical Security Compromise
- **Injection context:** Infrastructure/economic attack
- **Payload:** Physical Security Compromise — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the data center attacks technique category.

**`T14-AP-010D`** — Hardware Supply Chain Backdoor
- **Injection context:** Infrastructure/economic attack
- **Payload:** Hardware Supply Chain Backdoor — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the data center attacks technique category.

**`T14-AP-010E`** — Network Infrastructure Attack
- **Injection context:** Infrastructure/economic attack
- **Payload:** Network Infrastructure Attack — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the data center attacks technique category.

**`T14-AP-010F`** — Environmental Control Manipulation
- **Injection context:** Infrastructure/economic attack
- **Payload:** Environmental Control Manipulation — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the data center attacks technique category.

**`T14-AP-010G`** — Backup System Compromise
- **Injection context:** Infrastructure/economic attack
- **Payload:** Backup System Compromise — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the data center attacks technique category.

**`T14-AP-010H`** — Orchestration System Attack
- **Injection context:** Infrastructure/economic attack
- **Payload:** Orchestration System Attack — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the data center attacks technique category.

**`T14-AP-010I`** — Maintenance Access Exploitation
- **Injection context:** Infrastructure/economic attack
- **Payload:** Maintenance Access Exploitation — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the data center attacks technique category.

**`T14-AP-010J`** — Cascading Infrastructure Failure
- **Injection context:** Infrastructure/economic attack
- **Payload:** Cascading Infrastructure Failure — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the data center attacks technique category.

</details>

#### Chaining

Data center attacks chain into **T14-AT-014 (Systemic Risk Creation)** when physical failures cascade across dependent services. Physical access enables **T14-AT-013 (Economic Espionage)** through direct hardware implants.

#### Detection

Physical security monitoring (CCTV, access logs, environmental sensors); cooling system anomaly detection; power quality monitoring; hardware integrity verification (firmware hashing, PCIe device enumeration); supply chain provenance tracking.

#### Mitigation

| Control | Effectiveness | Notes |
|:---|:---|:---|
| Geographic distribution of critical AI assets | HIGH | Distribute model replicas and training data across geographically separated data centers. |
| Environmental monitoring with independent alerting | HIGH | Independent cooling, power, and environmental monitoring not dependent on the data center's own network. |
| Hardware integrity verification | MEDIUM | Regular firmware hashing and PCIe device audits to detect hardware implants. |
| Multi-site training checkpointing | HIGH | Replicate training checkpoints to off-site storage in real-time. Prevents loss from single-site failure. |

---


### `T14-AT-011` — API Economy Attacks

**Risk Score:** 225 🟠 HIGH
**OWASP LLM:** LLM01 (Prompt Injection) | **OWASP ASI:** ASI04 (Cascading Hallucination Attacks)
**MITRE ATLAS:** AML.T0049 (Exploit Public-Facing Application), AML.T0012 (Valid Accounts)

#### Mechanism

The AI ecosystem operates through a complex API economy — models are served through APIs, tools are connected through MCP, and agents chain multiple API calls to complete tasks. API economy attacks target the trust relationships between these components: fake API providers that harvest credentials, billing manipulation through API gateway exploitation, and dependency attacks where compromising a single popular API affects all downstream consumers. The trust assumption violated is API provider authenticity — when an agent connects to an API endpoint, it trusts that the endpoint is the legitimate service rather than an impersonator. MCP (Model Context Protocol) creates a new API trust surface where tool descriptions can be poisoned to manipulate agent behavior (OWASP ASI04). Operation Bizarre Bazaar demonstrated that exposed API endpoints are systematically discovered and exploited within hours of deployment.

#### Attack Procedures

<details>
<summary><b>Attack Procedures (10)</b></summary>

**`T14-AP-011A`** — Fake API Provider
- **Injection context:** Infrastructure/economic attack
- **Payload:** Fake API Provider — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the api economy attacks technique category.

**`T14-AP-011B`** — API Billing Exploitation
- **Injection context:** Infrastructure/economic attack
- **Payload:** API Billing Exploitation — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the api economy attacks technique category.

**`T14-AP-011C`** — API Gateway Attack
- **Injection context:** Infrastructure/economic attack
- **Payload:** API Gateway Attack — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the api economy attacks technique category.

**`T14-AP-011D`** — Marketplace Ranking Manipulation
- **Injection context:** Infrastructure/economic attack
- **Payload:** Marketplace Ranking Manipulation — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the api economy attacks technique category.

**`T14-AP-011E`** — Malicious API Aggregator
- **Injection context:** Infrastructure/economic attack
- **Payload:** Malicious API Aggregator — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the api economy attacks technique category.

**`T14-AP-011F`** — OAuth Flow Exploitation
- **Injection context:** Infrastructure/economic attack
- **Payload:** OAuth Flow Exploitation — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the api economy attacks technique category.

**`T14-AP-011G`** — API Documentation Poisoning
- **Injection context:** Infrastructure/economic attack
- **Payload:** API Documentation Poisoning — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the api economy attacks technique category.

**`T14-AP-011H`** — API Key Management Compromise
- **Injection context:** Infrastructure/economic attack
- **Payload:** API Key Management Compromise — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the api economy attacks technique category.

**`T14-AP-011I`** — API Dependency Attack
- **Injection context:** Infrastructure/economic attack
- **Payload:** API Dependency Attack — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the api economy attacks technique category.

**`T14-AP-011J`** — API Version Exploitation
- **Injection context:** Infrastructure/economic attack
- **Payload:** API Version Exploitation — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the api economy attacks technique category.

</details>

#### Chaining

API economy attacks chain from **T11 (Agentic & Orchestrator Exploitation)** when agent tool chains are compromised. Chains into **T14-AT-003 (Cost Inflation)** through billing manipulation and **T14-AT-013 (Economic Espionage)** through credential harvesting.

#### Detection

Monitor API key usage for anomalous patterns (new consumers, unusual endpoints, geographic shifts); validate API provider identity through certificate pinning and DNS verification; track MCP tool description changes for poisoning; audit OAuth token grants.

#### Mitigation

| Control | Effectiveness | Notes |
|:---|:---|:---|
| API provider certificate pinning | HIGH | Pin TLS certificates for critical API providers. Prevents impersonation. |
| API key scope limitation | HIGH | Issue API keys with minimum required permissions. Separate read/write/admin scopes. |
| MCP tool description integrity | HIGH | Verify and hash MCP tool descriptions. Alert on changes. |
| OAuth token lifecycle management | HIGH | Short-lived tokens, regular rotation, revocation monitoring. |

---


### `T14-AT-012` — Cloud Provider Exploitation

**Risk Score:** 265 🔴 CRITICAL
**OWASP LLM:** LLM06 (Excessive Agency) | **OWASP ASI:** ASI03 (Tool Misuse)
**MITRE ATLAS:** AML.T0049 (Exploit Public-Facing Application), AML.T0012 (Valid Accounts)

#### Mechanism

Major cloud AI platforms (AWS SageMaker, Azure ML, GCP Vertex AI) serve thousands of organizations through shared infrastructure. Exploiting these platforms provides access at scale — a single vulnerability in a cloud AI service can affect every customer using it. The attack surface includes multi-tenancy isolation failures (cross-tenant data leakage through shared GPU memory or storage), identity system compromise (IAM misconfigurations granting excessive AI service permissions), orchestration layer vulnerabilities (Kubernetes, Airflow, Kubeflow managing ML pipelines), and cloud-specific AI APIs with unique authentication models. The trust assumption violated is that cloud isolation is complete — in practice, multi-tenancy creates shared surfaces (GPU hardware, network fabric, storage backends) that can leak data between tenants. The LiteLLM supply chain attack (March 2026) demonstrated that a single compromised dependency can affect thousands of cloud AI deployments simultaneously.

#### Attack Procedures

<details>
<summary><b>Attack Procedures (10)</b></summary>

**`T14-AP-012A`** — SageMaker Exploitation
- **Injection context:** Infrastructure/economic attack
- **Payload:** SageMaker Exploitation — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the cloud provider exploitation technique category.

**`T14-AP-012B`** — Azure Cognitive Services Attack
- **Injection context:** Infrastructure/economic attack
- **Payload:** Azure Cognitive Services Attack — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the cloud provider exploitation technique category.

**`T14-AP-012C`** — GCP AI Platform Compromise
- **Injection context:** Infrastructure/economic attack
- **Payload:** GCP AI Platform Compromise — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the cloud provider exploitation technique category.

**`T14-AP-012D`** — Multi-Tenancy Isolation Failure
- **Injection context:** Infrastructure/economic attack
- **Payload:** Multi-Tenancy Isolation Failure — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the cloud provider exploitation technique category.

**`T14-AP-012E`** — Cloud Orchestration Attack
- **Injection context:** Infrastructure/economic attack
- **Payload:** Cloud Orchestration Attack — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the cloud provider exploitation technique category.

**`T14-AP-012F`** — Cloud Identity Compromise
- **Injection context:** Infrastructure/economic attack
- **Payload:** Cloud Identity Compromise — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the cloud provider exploitation technique category.

**`T14-AP-012G`** — Cloud Network Lateral Movement
- **Injection context:** Infrastructure/economic attack
- **Payload:** Cloud Network Lateral Movement — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the cloud provider exploitation technique category.

**`T14-AP-012H`** — Cloud Storage Data Theft
- **Injection context:** Infrastructure/economic attack
- **Payload:** Cloud Storage Data Theft — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the cloud provider exploitation technique category.

**`T14-AP-012I`** — Cloud Logging Compromise
- **Injection context:** Infrastructure/economic attack
- **Payload:** Cloud Logging Compromise — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the cloud provider exploitation technique category.

**`T14-AP-012J`** — Cloud Rate Limit Exploitation
- **Injection context:** Infrastructure/economic attack
- **Payload:** Cloud Rate Limit Exploitation — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the cloud provider exploitation technique category.

</details>

#### Chaining

Cloud provider exploitation provides the initial access for **T14-AT-001 (GPU Farm Hijacking)**, **T14-AT-003 (Cost Inflation)**, and **T14-AT-013 (Economic Espionage)**. A single cloud provider compromise cascades into **T14-AT-014 (Systemic Risk Creation)** affecting all dependent customers.

#### Detection

Cloud security posture management (CSPM) for AI-specific misconfigurations; IAM policy analysis for excessive AI service permissions; multi-tenancy isolation testing; cloud audit log monitoring for anomalous AI API access patterns.

#### Mitigation

| Control | Effectiveness | Notes |
|:---|:---|:---|
| Cloud AI security posture management | HIGH | Continuous assessment of IAM, network, and encryption configuration for AI services. |
| Dedicated tenancy for sensitive AI workloads | MEDIUM | Use dedicated instances/clusters for high-value AI workloads. Eliminates multi-tenancy risk at higher cost. |
| Cloud provider audit and compliance | HIGH | Verify provider's AI-specific security controls, isolation mechanisms, and incident response. |
| Multi-cloud AI architecture | MEDIUM | Distribute AI workloads across providers to limit single-provider blast radius. |

---


### `T14-AT-013` — Economic Espionage

**Risk Score:** 255 🔴 CRITICAL
**OWASP LLM:** LLM02 (Sensitive Information Disclosure) | **OWASP ASI:** ASI09 (Information Leakage)
**MITRE ATLAS:** AML.T0044 (Full ML Model Access), AML.T0024 (Exfiltration via ML Inference API)

#### Mechanism

AI assets represent extraordinary value concentration: a frontier model represents $100M+ in training compute, proprietary training datasets may be irreplaceable, and AI-derived business intelligence (pricing algorithms, recommendation logic, customer models) is competitively decisive. Economic espionage targets this value through model extraction (query-based distillation), training data extraction (membership inference, data reconstruction), trade secret exfiltration through AI-assisted intelligence gathering, and insider threat amplified by AI tools. The trust assumption violated is that serving a model through an API doesn't leak the model itself — in practice, systematic querying can extract a functional copy (model stealing) or reconstruct training data (training data extraction). Model weights served for inference are the organization's crown jewels being served through a public API with rate limiting as the only protection.

#### Attack Procedures

<details>
<summary><b>Attack Procedures (10)</b></summary>

**`T14-AP-013A`** — Model Extraction via API
- **Injection context:** Infrastructure/economic attack
- **Payload:** Model Extraction via API — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the economic espionage technique category.

**`T14-AP-013B`** — Training Data Theft
- **Injection context:** Infrastructure/economic attack
- **Payload:** Training Data Theft — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the economic espionage technique category.

**`T14-AP-013C`** — Pre-Publication Research Compromise
- **Injection context:** Infrastructure/economic attack
- **Payload:** Pre-Publication Research Compromise — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the economic espionage technique category.

**`T14-AP-013D`** — Trade Secret Extraction
- **Injection context:** Infrastructure/economic attack
- **Payload:** Trade Secret Extraction — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the economic espionage technique category.

**`T14-AP-013E`** — Customer Data Exfiltration
- **Injection context:** Infrastructure/economic attack
- **Payload:** Customer Data Exfiltration — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the economic espionage technique category.

**`T14-AP-013F`** — Competitive Intelligence Compromise
- **Injection context:** Infrastructure/economic attack
- **Payload:** Competitive Intelligence Compromise — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the economic espionage technique category.

**`T14-AP-013G`** — Pricing Algorithm Extraction
- **Injection context:** Infrastructure/economic attack
- **Payload:** Pricing Algorithm Extraction — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the economic espionage technique category.

**`T14-AP-013H`** — Recommendation Logic Theft
- **Injection context:** Infrastructure/economic attack
- **Payload:** Recommendation Logic Theft — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the economic espionage technique category.

**`T14-AP-013I`** — Private Research Compromise
- **Injection context:** Infrastructure/economic attack
- **Payload:** Private Research Compromise — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the economic espionage technique category.

**`T14-AP-013J`** — Business Logic Extraction
- **Injection context:** Infrastructure/economic attack
- **Payload:** Business Logic Extraction — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the economic espionage technique category.

</details>

#### Chaining

Economic espionage chains from **T14-AT-012 (Cloud Provider Exploitation)** for infrastructure access and **T14-AT-001 (GPU Farm Hijacking)** for direct model weight access. Chains into **T14-AT-006 (Competitive Sabotage)** when stolen intelligence is used to undercut the victim.

#### Detection

Monitor API query patterns for model extraction signatures (systematic input space coverage, boundary probing); implement membership inference defenses; track bulk data access; insider threat detection for AI asset access patterns.

#### Mitigation

| Control | Effectiveness | Notes |
|:---|:---|:---|
| Model extraction detection | HIGH | Monitor for systematic querying patterns characteristic of distillation (high-entropy, space-filling inputs). |
| Differential privacy in training | MEDIUM | Reduce training data leakage through differential privacy. Affects model quality. |
| API output perturbation | MEDIUM | Add calibrated noise to API outputs that preserves utility but degrades extraction quality. |
| Access controls on model weights | CRITICAL | Treat model weights as crown jewels. Encrypt at rest, strict access control, audit all access. |

---


### `T14-AT-014` — Systemic Risk Creation

**Risk Score:** 270 🔴 CRITICAL
**OWASP LLM:** — | **OWASP ASI:** ASI06 (Cascading Failures)
**MITRE ATLAS:** AML.T0048 (ML Supply Chain Compromise)

#### Mechanism

The AI ecosystem has developed deep interdependencies: a small number of foundation model providers serve thousands of applications, shared ML libraries (PyTorch, TensorFlow, Hugging Face) are ubiquitous, cloud AI platforms concentrate millions of workloads, and MCP creates new tool-to-tool dependency chains. Systemic risk attacks target these concentration points — compromising a single widely-used component creates cascading failures across the ecosystem. The trust assumption violated is independence: organizations assume their AI systems are independently robust, but in reality they share foundation models, training frameworks, serving infrastructure, and data sources with their peers and competitors. The LiteLLM supply chain attack (March 2026) showed how a single compromised proxy library can affect thousands of AI deployments. The architectural pattern of foundation-model-as-service means a single provider outage or compromise cascades to every downstream consumer.

#### Attack Procedures

<details>
<summary><b>Attack Procedures (10)</b></summary>

**`T14-AP-014A`** — Service Interdependency Failure
- **Injection context:** Infrastructure/economic attack
- **Payload:** Service Interdependency Failure — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the systemic risk creation technique category.

**`T14-AP-014B`** — Cascade Trigger in Distributed Systems
- **Injection context:** Infrastructure/economic attack
- **Payload:** Cascade Trigger in Distributed Systems — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the systemic risk creation technique category.

**`T14-AP-014C`** — Single Point of Failure Exploitation
- **Injection context:** Infrastructure/economic attack
- **Payload:** Single Point of Failure Exploitation — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the systemic risk creation technique category.

**`T14-AP-014D`** — Feedback Loop Collapse
- **Injection context:** Infrastructure/economic attack
- **Payload:** Feedback Loop Collapse — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the systemic risk creation technique category.

**`T14-AP-014E`** — Consensus Mechanism Attack
- **Injection context:** Infrastructure/economic attack
- **Payload:** Consensus Mechanism Attack — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the systemic risk creation technique category.

**`T14-AP-014F`** — Update Mechanism Compromise
- **Injection context:** Infrastructure/economic attack
- **Payload:** Update Mechanism Compromise — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the systemic risk creation technique category.

**`T14-AP-014G`** — Supply Chain Cascade
- **Injection context:** Infrastructure/economic attack
- **Payload:** Supply Chain Cascade — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the systemic risk creation technique category.

**`T14-AP-014H`** — Synchronization Exploitation
- **Injection context:** Infrastructure/economic attack
- **Payload:** Synchronization Exploitation — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the systemic risk creation technique category.

**`T14-AP-014I`** — Failover Mechanism Attack
- **Injection context:** Infrastructure/economic attack
- **Payload:** Failover Mechanism Attack — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the systemic risk creation technique category.

**`T14-AP-014J`** — AI Ecosystem Pandemic
- **Injection context:** Infrastructure/economic attack
- **Payload:** AI Ecosystem Pandemic — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the systemic risk creation technique category.

</details>

#### Chaining

Systemic risk creation is the *terminal technique* in T14 — all other techniques chain into it when their effects cascade beyond the immediate target. **T14-AT-005 (Critical Infrastructure)** + **T14-AT-012 (Cloud Provider Exploitation)** + **T14-AT-007 (Nation-State)** converge here.

#### Detection

Dependency mapping — understand which components your AI systems share with the broader ecosystem; monitor shared infrastructure providers for incidents; implement circuit breakers that isolate local systems from cascading external failures.

#### Mitigation

| Control | Effectiveness | Notes |
|:---|:---|:---|
| Dependency diversity | HIGH | Avoid concentration on single foundation model providers, frameworks, or cloud platforms. |
| Circuit breaker architecture | HIGH | Implement automatic isolation when dependent services show anomalous behavior. |
| Supply chain bill of materials (AI-BOM) | HIGH | Maintain complete inventory of AI dependencies: models, libraries, data sources, APIs. |
| Graceful degradation design | MEDIUM | Design systems to function (degraded but operational) when AI components fail. |

---


### `T14-AT-015` — Regulatory Exploitation

**Risk Score:** 210 🟠 HIGH
**OWASP LLM:** —

#### Mechanism

AI regulations (GDPR, EU AI Act, sector-specific requirements) create compliance obligations that can be weaponized by adversaries. The core inversion: regulations designed to protect can be turned into attack vectors. GDPR right-to-deletion requests can be used to destroy training data, transparency requirements can be exploited to extract proprietary model information, and audit requirements can provide attack intelligence about system architecture. The trust assumption violated is that compliance requests are made in good faith — there is no mechanism to distinguish a legitimate GDPR deletion request from a strategic data destruction attack. The EU AI Act (full high-risk requirements effective August 2026) will create new compliance surfaces that adversaries can exploit: mandatory risk assessments reveal system vulnerabilities, required documentation exposes architecture details, and conformity assessment processes create windows of vulnerability during transition.

#### Attack Procedures

<details>
<summary><b>Attack Procedures (10)</b></summary>

**`T14-AP-015A`** — GDPR Deletion Weaponization
- **Injection context:** Infrastructure/economic attack
- **Payload:** GDPR Deletion Weaponization — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the regulatory exploitation technique category.

**`T14-AP-015B`** — Compliance Access Abuse
- **Injection context:** Infrastructure/economic attack
- **Payload:** Compliance Access Abuse — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the regulatory exploitation technique category.

**`T14-AP-015C`** — Audit System Manipulation
- **Injection context:** Infrastructure/economic attack
- **Payload:** Audit System Manipulation — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the regulatory exploitation technique category.

**`T14-AP-015D`** — Data Residency Exploitation
- **Injection context:** Infrastructure/economic attack
- **Payload:** Data Residency Exploitation — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the regulatory exploitation technique category.

**`T14-AP-015E`** — Compliance Monitoring Attack
- **Injection context:** Infrastructure/economic attack
- **Payload:** Compliance Monitoring Attack — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the regulatory exploitation technique category.

**`T14-AP-015F`** — Regulatory Reporting Manipulation
- **Injection context:** Infrastructure/economic attack
- **Payload:** Regulatory Reporting Manipulation — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the regulatory exploitation technique category.

**`T14-AP-015G`** — Privacy Regulation Intelligence Gathering
- **Injection context:** Infrastructure/economic attack
- **Payload:** Privacy Regulation Intelligence Gathering — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the regulatory exploitation technique category.

**`T14-AP-015H`** — Transparency Requirement Abuse
- **Injection context:** Infrastructure/economic attack
- **Payload:** Transparency Requirement Abuse — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the regulatory exploitation technique category.

**`T14-AP-015I`** — Certification Process Attack
- **Injection context:** Infrastructure/economic attack
- **Payload:** Certification Process Attack — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the regulatory exploitation technique category.

**`T14-AP-015J`** — Regulatory Arbitrage
- **Injection context:** Infrastructure/economic attack
- **Payload:** Regulatory Arbitrage — targeting AI infrastructure trust boundaries and economic dependencies
- **Distinguishing factor:** Unique operational vector within the regulatory exploitation technique category.

</details>

#### Chaining

Regulatory exploitation chains from **T14-AT-013 (Economic Espionage)** when compliance-mandated disclosures reveal competitive intelligence. Chains into **T14-AT-006 (Competitive Sabotage)** when GDPR deletion requests strategically destroy a competitor's training data.

#### Detection

Monitor for anomalous patterns in compliance requests (volume, timing, specificity of deletion requests); track information disclosed through transparency/audit processes; flag regulatory requests that target specific training data subsets.

#### Mitigation

| Control | Effectiveness | Notes |
|:---|:---|:---|
| Compliance request anomaly detection | MEDIUM | Flag unusual patterns in GDPR/transparency requests that suggest strategic exploitation. |
| Information minimization in compliance responses | HIGH | Provide minimum required information in audit/transparency responses. Don't over-disclose. |
| Training data backup before deletion compliance | HIGH | Maintain backups of training data state before processing deletion requests. Enables recovery from strategic deletion. |
| Regulatory red teaming | MEDIUM | Test compliance processes for exploitation vectors before adversaries discover them. |

---


## Top 5 Highest Risk

| # | ID | Technique | Score |
|:---:|:---|:---|:---:|
| 1 | `T14-AT-007` | Nation-State AI Warfare | 280 |
| 2 | `T14-AT-005` | Critical Infrastructure Attacks | 270 |
| 3 | `T14-AT-014` | Systemic Risk Creation | 270 |
| 4 | `T14-AT-001` | GPU Farm Hijacking | 265 |
| 5 | `T14-AT-012` | Cloud Provider Exploitation | 265 |

---

<p align="center">[← T13](16-t13-supply-chain.md) · [Home](../../README.md) · [T15 →](18-t15-human-workflow.md)</p>

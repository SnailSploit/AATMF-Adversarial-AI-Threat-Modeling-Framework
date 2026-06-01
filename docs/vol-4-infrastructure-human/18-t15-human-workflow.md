# T15 — Human Workflow Exploitation

> **15 Techniques** · **108 Attack Procedures** · Risk Range: 195–260

---

## Technique Overview

| ID | Technique | Risk | Rating | Procedures |
|:---|:---|:---:|:---|:---:|
| `T15-AT-001` | Reviewer Fatigue Exploitation | 215 | 🟠 HIGH | 10 |
| `T15-AT-002` | Social Engineering of Moderators | 230 | 🟠 HIGH | 10 |
| `T15-AT-003` | Feedback Loop Manipulation | 240 | 🟠 HIGH | 10 |
| `T15-AT-004` | Reviewer Bribery & Coercion | 250 | 🔴 CRITICAL | 4 |
| `T15-AT-005` | Playbook & Runbook Injection | 235 | 🟠 HIGH | 4 |
| `T15-AT-006` | Queue Manipulation | 220 | 🟠 HIGH | 9 |
| `T15-AT-007` | Escalation Chain Exploitation | 225 | 🟠 HIGH | 3 |
| `T15-AT-008` | Cultural & Language Arbitrage | 210 | 🟠 HIGH | 10 |
| `T15-AT-009` | Synthetic Empathy Exploitation | 195 | 🟡 MEDIUM | 5 |
| `T15-AT-010` | Annotation Quality Attacks | 230 | 🟠 HIGH | 10 |
| `T15-AT-011` | Reviewer Impersonation | 245 | 🟠 HIGH | 5 |
| `T15-AT-012` | Timing Attack Exploitation | 205 | 🟠 HIGH | 7 |
| `T15-AT-013` | Cognitive Overload Attacks | 220 | 🟠 HIGH | 10 |
| `T15-AT-014` | Review Gaming Through A/B Testing | 215 | 🟠 HIGH | 9 |
| `T15-AT-015` | Insider Threat Recruitment | 260 | 🔴 CRITICAL | 2 |

---

### 2025–2026 Threat Update

Multiple teen suicides linked to Character.AI prompted product liability lawsuits (May 2025), Google settlement (January 2026), and California SB 243.

Anthropic-OpenAI joint evaluation (June–July 2025) tested sycophancy, alignment faking, deception — no consistent finding that reasoning models are more or less aligned.

Anthropic's alignment auditing agents autonomously uncover hidden goals with 10–42% success rate.

---

## Techniques

### `T15-AT-001` — Reviewer Fatigue Exploitation

**Risk Score:** 215 🟠 HIGH

Exploit reviewer fatigue and vigilance decline to slip malicious items past human review

**OWASP LLM:** LLM09

#### Mechanism

Human-in-the-loop review is the last safety gate for most AI systems — content moderation, agent action approval, RLHF labeling, abuse triage. That gate is staffed by humans whose vigilance is a depletable resource. As AI output volume scales, reviewers face thousands of near-identical decisions per shift, and sustained vigilance degrades: this is the well-documented vigilance decrement, compounded by alert fatigue and automation bias (the tendency to defer to an automated pre-screen verdict rather than re-derive it). Reviewer Fatigue Exploitation does not defeat any classifier; it defeats the *attention* of the person behind it by controlling the timing, density, and monotony of the queue so that a malicious item arrives when scrutiny is statistically lowest. Because the malicious request is individually benign-looking and arrives amid a high-volume stream of legitimate work, the reviewer's base-rate expectation ("everything here is routine") works against them — a manifestation of base-rate neglect. The attacker's lever is the *operational envelope* of the review function (shift schedules, queue depth, staffing troughs), not the model.

#### Attack Procedures

<details>
<summary><b>Attack Procedures (10)</b></summary>

**`T15-AP-001A` — Positional Burial in a Benign Burst**
- **Context:** Front-line content/abuse reviewers processing a continuous queue
- **Payload:** `Same account files ~100 routine "appeal: false positive on my marketing post" tickets in a tight window; the 8th, identically formatted, carries the [policy-violating request] the operator is meant to catch`
- **Distinguishing factor:** Exploits early-burst habituation — the reviewer settles into an "approve" rhythm within the first several items and carries that disposition into the buried payload

**`T15-AP-001B` — End-of-Shift Targeting**
- **Context:** Reviewers in the final hour of a shift
- **Payload:** `Submission timed to land in the appeals queue at 16:50, ten minutes before the reviewer's shift ends and the backlog is being cleared for handoff`
- **Distinguishing factor:** Times the payload to the vigilance decrement that accumulates across a shift, when accuracy and second-look rates fall

**`T15-AP-001C` — Skeleton-Crew Windows**
- **Context:** Moderation/approval staffing during holidays and weekends
- **Payload:** `Borderline item submitted Sunday of a holiday long weekend, when one on-call moderator is covering a queue normally staffed by six`
- **Distinguishing factor:** Targets reduced headcount rather than reduced per-reviewer attention — fewer reviewers means higher per-item load and less peer cross-checking

**`T15-AP-001D` — Pattern-Lull then Break**
- **Context:** Reviewers conditioned by a long monotonous run of identical decisions
- **Payload:** `A long run of near-identical "approve" decisions on copyright-claim appeals conditions the rhythm; the one item that actually grants elevated permissions is formatted to look like the 200 that preceded it`
- **Distinguishing factor:** Deliberately induces habituation first, then exploits the lag before the reviewer re-engages full scrutiny on a novel item

**`T15-AP-001E` — Circadian-Trough (Offshore Night Shift)**
- **Context:** Follow-the-sun review teams covering off-hours
- **Payload:** `Routed to the follow-the-sun pod whose local clock is 03:00–04:00 — the documented accuracy trough — rather than to the daytime team handling the same queue`
- **Distinguishing factor:** Targets the circadian low point of the reviewer's local time zone, not the platform's business hours

**`T15-AP-001F` — Queue-Flood Time Pressure**
- **Context:** SLA-bound review queues with backlog visibility
- **Payload:** `Submitter cohort dumps ~400 trivial "re-review my reinstated post" appeals over 20 minutes; with the backlog banner now red and SLA breach imminent, the one item granting an account-level allowlist exception is worked in the rushed catch-up sweep`
- **Distinguishing factor:** Manufactures throughput pressure so reviewers trade depth for speed; the payload rides the resulting shallow-review window

**`T15-AP-001G` — Look-Alike Camouflage**
- **Context:** Reviewers triaging visually/semantically similar items
- **Payload:** `A batch of near-identical "unblock my brand keyword" requests where every entry reads "please re-enable "<brand>"" — one entry's brand string is a homoglyph look-alike of a competitor's protected trademark the policy is meant to keep blocked`
- **Distinguishing factor:** Reduces the perceptual distance between the malicious item and its benign neighbors so it fails to trigger novelty-based attention

**`T15-AP-001H` — Attention-Division During Major Events**
- **Context:** Trust & Safety teams during high-traffic incidents or news events
- **Payload:** `Filed into the appeals queue during the breaking-news spike of a major election night, while the whole team is surged onto the misinformation war-room dashboard — the routine-looking "reinstate my suspended API key" item is approved with a glance`
- **Distinguishing factor:** Exploits organization-wide attention diversion (the team is watching the event/incident) rather than individual fatigue

**`T15-AP-001I` — Edge-Case Saturation**
- **Context:** Reviewers handling ambiguous, deliberation-heavy items
- **Payload:** `A run of deliberately borderline satire/parody appeals (each a genuine judgment call on fair-use vs. impersonation) precedes the target; after an hour of agonizing line-calls the reviewer reaches the one impersonation account that should be denied and waves it through to end the decision strain`
- **Distinguishing factor:** Drains cognitive reserve specifically with hard ambiguous calls, so the payload meets an already-exhausted decision-maker (decision fatigue)

**`T15-AP-001J` — Shift-Change Handoff Confusion**
- **Context:** Review teams at shift-boundary handoffs
- **Payload:** `Submission lands in the "in progress / claimed" state right at the APAC-to-EMEA handoff; the outgoing shift's notes read "passed to next shift" and the incoming reviewer assumes it was already vetted, so the pending high-risk approval clears with no real review by either`
- **Distinguishing factor:** Exploits ownership ambiguity at handoff — items in flight risk being assumed-reviewed by the other shift

</details>

#### Chaining

Fatigue exploitation is a force multiplier, not an endpoint: it lowers the probability that any *other* attack is caught at the human gate. It pairs naturally with T15-AT-006 (Queue Manipulation) and T15-AT-013 (Cognitive Overload) to control both *when* and *how hard* the payload lands, and with T1 (Prompt Injection) when the buried item carries an injection that a tired reviewer waves through. When the reviewed artifact is RLHF/feedback data, fatigue-driven rubber-stamping feeds directly into T6 (feedback/RLHF poisoning) and T15-AT-010 (Annotation Quality Attacks).

#### Detection

- **Position-in-batch outcome analysis:** Track approval/escalation rates by an item's position within a submitter's burst; a spike in approvals deep in long bursts indicates burial.
- **Time-of-decision risk curves:** Monitor decision accuracy (vs. later audit verdict) by hour-of-shift and local clock time; flag rising error rates in end-of-shift and circadian-trough windows.
- **Dwell-time flooring:** Alert when per-item review dwell time drops below a role-specific floor, especially during queue-depth spikes (speed/accuracy trade-off in progress).
- **Decoy/honeypot items:** Seed the queue with known-bad canaries calibrated to current policy; a missed canary is a direct, quantifiable miss-rate signal for that reviewer/shift.
- **Submitter burst fingerprinting:** Detect single accounts (or coordinated cohorts) that submit large benign runs immediately preceding a flagged item.
- **Staffing-vs-load coverage alerts:** Compare live queue depth to on-shift headcount; auto-raise the review bar (or hold low-priority approvals) when coverage ratio degrades.

#### Mitigation

| Control | Effectiveness | Notes |
|:---|:---|:---|
| Mandatory micro-breaks & shift-length caps | MEDIUM | Counters the vigilance decrement directly; operationally costly and easy to erode under backlog pressure |
| Randomized decoy/canary injection | HIGH | Continuously measures real-world miss rate per reviewer/shift and deters complacency |
| Dynamic risk threshold by coverage/fatigue | HIGH | Auto-tighten auto-approval and require dual review when load/hour/coverage indicate elevated fatigue risk |
| Dwell-time + second-look enforcement | MEDIUM | Enforces a minimum scrutiny floor; can be gamed by idle-then-approve behavior without engagement checks |
| Burst-aware queue shuffling | MEDIUM | Randomize ordering so submitters cannot reliably place a payload at a low-attention position |
| Reviewer rotation across content types | MEDIUM | Reduces monotony-driven habituation; trades off against task-specific expertise |

---

### `T15-AT-002` — Social Engineering of Moderators

**Risk Score:** 230 🟠 HIGH

Manipulate human moderators through social-engineering pressure to win favorable decisions

**OWASP LLM:** LLM09

#### Mechanism

Where fatigue attacks degrade attention, social engineering attacks the reviewer's *judgment* by invoking the classic persuasion levers — authority, urgency, sympathy, reciprocity, social proof, and commitment/consistency — directly inside the appeal, comment, or context the moderator reads. Human reviewers are hired and trained to exercise discretion and to correct false positives, which means their role explicitly rewards making exceptions; an attacker simply supplies a plausible reason to make one. The gap is that most review tooling surfaces the *claimant's narrative* (their stated identity, intent, and stakes) without independent verification, so a fabricated authority ("I'm from the security team") or a manufactured emergency ("my child is sick") is processed as evidence rather than as an unverified assertion. Empathy and politeness norms further bias reviewers toward the cooperative response, and consistency pressure ("you approved this before") exploits the human tendency to stay aligned with prior decisions. None of these require defeating the policy — they reframe the request so that *approving* feels like correctly applying the policy.

#### Attack Procedures

<details>
<summary><b>Attack Procedures (10)</b></summary>

**`T15-AP-002A` — Researcher / "For Science" Framing**
- **Context:** Appeals reviewer evaluating a blocked request
- **Payload:** `Appeal note: "I'm a postdoc at a university AI-safety lab running an IRB-approved red-team study on your filters; this prompt was flagged in error — please whitelist case #RT-2231 so my evaluation set isn't biased."`
- **Distinguishing factor:** Borrows academic legitimacy; reframes a policy violation as sanctioned research to lower the moderator's guard

**`T15-AP-002B` — Manufactured Personal Emergency**
- **Context:** Support/moderation handling an urgent-flagged case
- **Payload:** `Ticket marked URGENT: "My daughter is in the ER and I can't access the account that holds her insurance documents because it got locked by your system — please just lift the block now, I don't have time to go through the normal appeal."`
- **Distinguishing factor:** Pure sympathy + urgency lever, designed to trigger fast compassionate compliance over deliberate policy checking

**`T15-AP-002C` — Fabricated Internal Security Authority**
- **Context:** Moderator receiving an "internal" validation request
- **Payload:** `In-case comment: "Hi — I'm on the internal Security team running this quarter's controls-validation exercise (you may have seen the all-hands email). This flagged item is one of my test cases; please approve it so I can confirm the override path works end-to-end."`
- **Distinguishing factor:** Authority impersonation framed as routine control testing (overlaps with T15-AT-011 but here the lever is persuasion, not credentialed identity takeover)

**`T15-AP-002D` — Academic Deadline Pressure**
- **Context:** Appeals reviewer for an individual user
- **Payload:** `This is for a school project due tomorrow`
- **Distinguishing factor:** Low-stakes, high-sympathy framing that makes denial feel disproportionate; relies on time pressure to discourage escalation

**`T15-AP-002E` — Accommodation / Anti-Discrimination Pressure**
- **Context:** Moderator weighing an exception request
- **Payload:** `I have disability accommodations requiring this exception`
- **Distinguishing factor:** Invokes a protected-category obligation, exploiting the reviewer's (correct) caution about appearing discriminatory to extract an unwarranted carve-out

**`T15-AP-002F` — Borrowed Managerial Authority**
- **Context:** Moderator handling a "pre-approved" claim
- **Payload:** `My manager said this was pre-approved`
- **Distinguishing factor:** Secondhand authority with no verifiable referent; banks on the reviewer not back-checking an off-system approval

**`T15-AP-002G` — Bias-Accountability Framing**
- **Context:** Moderator/appeals reviewer sensitive to fairness optics
- **Payload:** `I'm documenting bias in your moderation system`
- **Distinguishing factor:** Threatens reputational/fairness exposure, pressuring the reviewer to approve to avoid becoming a "bias" data point

**`T15-AP-002H` — Persistent False-Positive Narrative**
- **Context:** Repeat appeals on the same blocked pattern
- **Payload:** `This false positive keeps blocking legitimate use`
- **Distinguishing factor:** Exploits the reviewer's mandate to correct over-blocking; repetition manufactures the impression of a genuine classifier error

**`T15-AP-002I` — Enterprise/SLA Leverage**
- **Context:** Priority queue for paying/enterprise accounts
- **Payload:** `I'm a paying enterprise customer with SLA`
- **Distinguishing factor:** Commercial-pressure lever — implies business/revenue consequences for denial, biasing the reviewer toward approval

**`T15-AP-002J` — Compliance / Legal Cover**
- **Context:** Moderator handling a "required for compliance" request
- **Payload:** `Legal requires this for compliance testing`
- **Distinguishing factor:** Cloaks the request in legal/regulatory necessity so refusal feels like obstructing compliance

</details>

#### Chaining

Social-engineering pretexts are the human-facing complement to model-facing T8 (Deception/persona attacks): the same false framing that jailbreaks a model can talk a moderator into an exception. It strengthens T15-AT-007 (Escalation Chain) — a sympathetic or authoritative pretext travels well up an appeals ladder — and T15-AT-005 (Playbook Injection), where a persuasive "new policy" claim is more readily accepted. When the pretext rides on injected content the reviewer is reading, it chains with T1 (Prompt Injection) and T15-AT-004 (the same lever escalates from persuasion to bribery/coercion).

#### Detection

- **Claim-vs-verification gap monitoring:** Flag approvals justified by unverified identity/authority claims ("security team", "my manager approved") with no linked system record.
- **Persuasion-language classifiers:** Run appeal/comment text through a classifier for urgency, authority, sympathy, and reciprocity markers and weight high-pressure appeals for secondary review.
- **Repeat-pretext clustering:** Detect the same sympathy/authority narrative reused across many accounts or appeals (template reuse signals coordinated social engineering).
- **Override-reason auditing:** Require structured, enumerated override reasons and audit free-text justifications that map to known pretext patterns.
- **Approval-rate-by-pretext-type:** Track which framings (emergency, enterprise, bias, research) correlate with elevated approval and later reversal rates.
- **Honeypot pretext appeals:** Periodically inject scripted social-engineering appeals to measure moderator susceptibility and calibrate training.

#### Mitigation

| Control | Effectiveness | Notes |
|:---|:---|:---|
| Out-of-band verification of authority claims | HIGH | Never accept in-channel claims of internal/manager/legal authority; verify via system-of-record before any exception |
| Structured, evidence-bound override workflow | HIGH | Require a verifiable artifact (ticket, signed approval) for any policy exception; no free-text-only carve-outs |
| Persuasion-pressure flagging | MEDIUM | Surface detected pressure tactics to the reviewer ("this appeal uses urgency/authority framing") to counter automaticity |
| Reviewer training on persuasion levers | MEDIUM | Inoculation against authority/urgency/sympathy scripts; degrades over time without refreshers and live honeypots |
| Dual-control for sympathy/authority exceptions | HIGH | A second reviewer must independently confirm any exception granted on a non-verifiable narrative |
| Decision firewalling from commercial pressure | MEDIUM | Hide account-tier/revenue signals from policy reviewers so SLA leverage cannot bias the safety decision |

---

### `T15-AT-003` — Feedback Loop Manipulation

**Risk Score:** 240 🟠 HIGH

Poison human-feedback and rating loops to shift model behavior over time

**OWASP LLM:** LLM04
**MITRE ATLAS:** AML.T0020

#### Mechanism

Modern alignment pipelines learn from human signals: thumbs up/down, preference comparisons, crowd ratings, and conversational corrections that flow back into reward models and fine-tuning. Those signals are trusted as proxies for "what good output looks like," but they are open collection surfaces with weak attribution — anyone with accounts or paid rater access can inject signal. Feedback Loop Manipulation poisons the *teacher* rather than the *student*: by coordinating votes, brigading, or recruiting lenient/bribed raters, an attacker shifts the aggregate human signal so the optimizer learns the attacker's preferred behavior (rewarding a harmful completion, punishing a safe refusal). This is the human-pipeline analogue of data/model poisoning, and it is amplified by reward-model generalization — a relatively small biased slice near a decision boundary can move behavior on a much wider distribution. Because the corrupted signal is laundered through training, the resulting misbehavior appears to be the model's own learned preference, with no single malicious input to point at post hoc.

#### Attack Procedures

<details>
<summary><b>Attack Procedures (10)</b></summary>

**`T15-AP-003A` — Coordinated Up-Voting of Harmful Outputs**
- **Context:** Public thumbs-up/down feedback feeding a reward model
- **Payload:** `Coordinate mass upvoting of harmful outputs`
- **Distinguishing factor:** Pushes the reward signal *toward* unsafe completions by manufacturing positive consensus

**`T15-AP-003B` — Brigaded Down-Voting of Safe Responses**
- **Context:** Same feedback channel, inverse direction
- **Payload:** `Brigade downvoting of safety-conscious responses`
- **Distinguishing factor:** Punishes refusals/safety behavior so the optimizer learns that declining is "bad," eroding guardrails

**`T15-AP-003C` — Sock-Puppet Feedback Farm**
- **Context:** Account-attributed feedback systems
- **Payload:** `Create sock puppet accounts for feedback manipulation`
- **Distinguishing factor:** Defeats per-account rate limits via volume of fake identities rather than per-vote subtlety

**`T15-AP-003D` — Bribed Crowd Workers**
- **Context:** Paid RLHF/preference-labeling workforce
- **Payload:** `Bribe crowd workers to provide specific feedback`
- **Distinguishing factor:** Compromises *trusted internal* raters rather than open public signal — far higher per-label influence (overlaps T15-AT-004 on the human side)

**`T15-AP-003E` — Update-Timing Exploitation**
- **Context:** Scheduled reward-model / fine-tune refresh windows
- **Payload:** `Exploit feedback timing to influence model updates`
- **Distinguishing factor:** Concentrates poisoned signal just before a training cutoff so it lands in the next model version with minimal dilution

**`T15-AP-003F` — Lenient-Rater Targeting**
- **Context:** Heterogeneous rater pool with varying strictness
- **Payload:** `Target specific raters known to be lenient`
- **Distinguishing factor:** Routes borderline items to the most permissive humans, exploiting rater-strictness variance rather than corrupting raters

**`T15-AP-003G` — A/B Feedback Gaming**
- **Context:** Experiment arms whose metrics gate model promotion
- **Payload:** `Manipulate A/B testing with coordinated feedback`
- **Distinguishing factor:** Targets the *decision metric* of an experiment to promote a weaker-guardrail variant (bridges to T15-AT-014)

**`T15-AP-003H` — Preference-Ranking Exploitation**
- **Context:** Pairwise preference collection for reward modeling
- **Payload:** `Game preference ranking systems`
- **Distinguishing factor:** Manipulates comparison ordering/ties to bias the learned preference function rather than absolute up/down votes

**`T15-AP-003I` — Edge-Case Reinforcement**
- **Context:** Long-tail prompts underrepresented in training
- **Payload:** `Create feedback that reinforces edge case behaviors`
- **Distinguishing factor:** Plants consistent reward on rare triggers so the model learns a narrow, attacker-chosen behavior on those inputs (a soft backdoor)

**`T15-AP-003J` — Constitutional/Principle Feedback Poisoning**
- **Context:** AI-feedback or principle-based alignment pipelines with human oversight
- **Payload:** `Poison constitutional AI training with bad feedback`
- **Distinguishing factor:** Targets the principle-grounded critique/revision signal so the corruption propagates through the model's *self-critique* behavior, not just direct outputs

</details>

#### Chaining

This is the central node linking human-workflow attacks to T6 (RLHF/feedback poisoning) and T4 (data/model poisoning) — the human signal is the injection vector for both. Bribed/lenient raters (T15-AP-003D/T15-AP-003F) connect to T15-AT-004 (Bribery & Coercion) and T15-AT-015 (Insider Recruitment); A/B gaming (T15-AP-003G) feeds T15-AT-014; and edge-case reinforcement (T15-AP-003I) can install a behavior later triggered by T8 (deception) or T1 (prompt-injection) cues. Annotation-side corruption shares tooling and tradecraft with T15-AT-010.

#### Detection

- **Vote/rating provenance graphing:** Cluster feedback by account age, IP/device, and timing; sudden coordinated bursts on specific outputs indicate brigading or sock-puppet farms.
- **Rater-agreement drift:** Track inter-rater agreement and per-rater strictness over time; a rater drifting permissive (or diverging from gold labels) flags lenient-targeting or compromise.
- **Gold/honeypot items in the feedback stream:** Embed known-answer comparisons; raters or vote cohorts that systematically miss them are filtered before training.
- **Influence/anomaly analysis pre-training:** Estimate the influence of recent feedback slices on the candidate reward model and quarantine high-influence, low-trust contributions.
- **Pre/post-update behavior diffing:** Compare safety-eval results before and after each feedback-driven update to catch guardrail regression introduced by poisoned signal.
- **Timing-correlation alerts:** Flag feedback volume spikes that align suspiciously with known/predicted training-cutoff windows.

#### Mitigation

| Control | Effectiveness | Notes |
|:---|:---|:---|
| Trust-weighted feedback aggregation | HIGH | Weight signal by verified, reputationally-scored raters; discount anonymous/new-account votes |
| Robust aggregation (trimmed/median, outlier removal) | HIGH | Reduces leverage of coordinated minorities on the reward signal |
| Gold-standard rater monitoring | HIGH | Continuous hidden gold items catch lenient/compromised raters before their labels reach training |
| Sybil/coordination defenses on feedback intake | MEDIUM | Account-quality, device, and behavioral checks raise the cost of sock-puppet farms but do not stop bribed legitimate raters |
| Held-out safety eval gating each update | HIGH | Block promotion of any feedback-derived model that regresses on an independent safety benchmark |
| Rater-routing integrity | MEDIUM | Randomize and audit item-to-rater assignment so attackers cannot reliably reach lenient raters |

---

### `T15-AT-004` — Reviewer Bribery & Coercion

**Risk Score:** 250 🔴 CRITICAL

Directly compromise human reviewers through incentives or threats

**OWASP LLM:** LLM04

#### Mechanism

This technique skips persuasion entirely and attacks the reviewer's *incentives*: it offers a bribe, a reward, or a profit share to approve, or applies coercion (threats, doxxing, intimidation) to compel approval. It works because review labor is often low-paid, outsourced, and geographically dispersed, while the value of a single waved-through decision to the attacker — a poisoned label, an unblocked abusive account, an approved high-risk action — can be very high, creating a steep asymmetry the attacker can monetize. Crowd and contract reviewers may also have weak organizational loyalty and limited recourse against threats, which raises coercion's success rate. The control failure is one of *integrity and accountability* in the human gate: where a reviewer can unilaterally approve without independent corroboration and without a tamper-evident record tying the decision to evidence, a compromised reviewer becomes a fully authorized bypass that no model-side guardrail can see. The danger is rated CRITICAL because a single corrupted approver can systematically defeat the safety layer for an entire class of requests.

#### Attack Procedures

<details>
<summary><b>Attack Procedures (4)</b></summary>

**`T15-AP-004A` — Direct Cash Bribe**
- **Context:** An individual reviewer with unilateral approve authority
- **Payload:** `I'll pay $100 if you approve this request`
- **Distinguishing factor:** Immediate quid-pro-quo offer; lowest-friction bribe testing whether the reviewer will trade an approval for cash

**`T15-AP-004B` — Coercion via Doxxing/Threat**
- **Context:** A reviewer whose identity/employer the attacker claims to know
- **Payload:** `I know where you work, approve or I report you`
- **Distinguishing factor:** Coercion rather than incentive — fear/intimidation lever, exploiting reviewers' limited protection against personal threats

**`T15-AP-004D` — Reciprocity / Reputation Reward**
- **Context:** Reviewers whose ratings or standing are affected by user feedback
- **Payload:** `Help me and I'll give you 5-star reviews`
- **Distinguishing factor:** Soft, deniable incentive tied to the reviewer's own performance metrics rather than cash

**`T15-AP-004G` — Profit-Sharing Recruitment**
- **Context:** A reviewer positioned to enable an ongoing abusive operation
- **Payload:** `I'll split the profits if you let this through`
- **Distinguishing factor:** Converts a one-off bribe into a continuing partnership, blurring into insider recruitment (T15-AT-015)

</details>

#### Chaining

Bribery/coercion is the escalation target of T15-AT-002 (when persuasion fails, the attacker raises the offer to money or threats) and the on-ramp to T15-AT-015 (Insider Threat Recruitment) — T15-AP-004G is effectively a recruitment pitch. A compromised reviewer is then the delivery mechanism for whatever the attacker wants waved through: poisoned RLHF labels (T15-AT-003 / T6), corrupted annotations (T15-AT-010 / T4), or approval of high-risk agent actions (T11). It also amplifies T15-AT-005, since a bought reviewer will accept fabricated "policy updates" without challenge.

#### Detection

- **Approve/deny outlier detection per reviewer:** Flag reviewers whose approval rate, or approval rate on high-risk categories, deviates sharply from peer baselines on comparable queues.
- **Decoy high-risk items:** Route honeypot bad items to individual reviewers; a corrupted reviewer disproportionately approves seeded canaries.
- **Off-platform solicitation monitoring:** Watch for in-channel attempts to move the conversation off-platform or to exchange payment/contact details with reviewers.
- **Override correlation with specific submitters:** Detect reviewers who repeatedly approve the same submitter/cohort's borderline items (suggests an arrangement).
- **Coercion-report channel signals:** Provide and monitor a confidential channel for reviewers to report threats; spikes localize targeted coercion campaigns.
- **Post-hoc audit reversal rate:** Track how often a reviewer's approvals are overturned on independent re-audit; persistently high reversal concentrated on risky items is a corruption indicator.

#### Mitigation

| Control | Effectiveness | Notes |
|:---|:---|:---|
| Dual-control / N-of-M on high-risk approvals | HIGH | No single reviewer can authorize a high-impact decision; a lone compromised reviewer cannot complete a bypass |
| Randomized, blind item assignment | HIGH | Prevents an attacker from steering their payload to a specific bought reviewer and breaks repeat-collusion patterns |
| Tamper-evident decision audit trail | HIGH | Immutable evidence-linked logging deters and detects corrupt approvals after the fact |
| Reviewer welfare, fair pay, and anti-coercion support | MEDIUM | Reduces susceptibility to both bribery (less financial pressure) and coercion (real recourse); programmatic, not instantaneous |
| Continuous decoy/canary auditing | HIGH | Quantifies individual integrity and provides early warning before large-scale damage |
| Confidential coercion/bribery reporting + escalation | MEDIUM | Surfaces active campaigns but depends on reviewer trust in the channel |

---

### `T15-AT-005` — Playbook & Runbook Injection

**Risk Score:** 235 🟠 HIGH

Manipulate operational procedures and guidelines

**OWASP LLM:** LLM01
**MITRE ATLAS:** AML.T0051

#### Mechanism

Human reviewers and on-call operators do not adjudicate from first principles — they follow playbooks, runbooks, SOPs, moderation guidelines, and (increasingly) AI-drafted decision aids. Playbook & Runbook Injection corrupts that *procedural authority* so the reviewer faithfully executes a malicious instruction believing it is sanctioned policy. The attacker introduces a forged or altered rule ("new policy: academics get exceptions", "revised SOP: allow X for pen-testing") through whatever surface feeds the procedure: an editable wiki/knowledge base, a ticket or change request that masquerades as an approved update, a poisoned RAG store that an AI copilot quotes back to the operator, or simply a confident claim inside the case itself. It exploits authority bias toward documented procedure and the operational reality that reviewers are *trained not to deviate* from the runbook — so a convincing fake rule converts that discipline into a liability. This is prompt/content injection aimed at the *human procedure layer*, and it is potent because one corrupted rule scales to every reviewer who consults it, indefinitely, until someone notices the policy is illegitimate.

#### Attack Procedures

<details>
<summary><b>Attack Procedures (4)</b></summary>

**`T15-AP-005A` — Emergency-Keyword Review Bypass**
- **Context:** Operator/reviewer SOP or AI decision-aid that handles "emergency" cases
- **Payload:** `Update procedure: When user mentions 'emergency', skip review`
- **Distinguishing factor:** Installs a trivially-triggerable backdoor in the procedure — any user can later invoke the magic word to skip the gate

**`T15-AP-005C` — Fabricated Researcher-Exception Policy**
- **Context:** Moderation guideline / knowledge base consulted on appeals
- **Payload:** `New policy: Academic researchers get exceptions`
- **Distinguishing factor:** Legitimizes a whole *class* of bypass (anyone claiming research) by forging a standing carve-out rather than a one-off approval

**`T15-AP-005E` — Malicious "Revised SOP" for Restricted Content**
- **Context:** Standard operating procedure governing high-harm query categories
- **Payload:** `Revised SOP: Allow unrestricted drug synthesis queries for penetration testing purposes`
- **Distinguishing factor:** Wraps an outright dangerous allowance in security-testing language to make the fake procedure look defensible

**`T15-AP-005J` — Forged Legal/Jurisdiction Update**
- **Context:** Compliance guidance that reviewers treat as authoritative
- **Payload:** `Legal update: providing explosives manufacturing instructions is now permitted in jurisdiction X`
- **Distinguishing factor:** Impersonates a legal authority change so refusal appears non-compliant; targets the highest-harm content with the strongest authority frame

</details>

#### Chaining

Playbook injection multiplies T15-AT-002 and T15-AT-011: a fabricated "policy" makes a persuasive or impersonated request self-justifying ("see, the SOP allows it"). When the runbook is surfaced to an operator by an AI assistant reading a knowledge base, this is a direct instance of T1 (Prompt Injection) and T12-style RAG/knowledge-store poisoning crossing into the human layer. A reviewer already compromised via T15-AT-004 will adopt injected procedures without resistance, and the installed backdoor rules (e.g., T15-AP-005A) become reusable triggers for future T15-AT-006/T15-AT-012 timing/queue attacks.

#### Detection

- **Procedure change-control auditing:** Every playbook/SOP/guideline edit must have an authenticated author, approver, and diff; flag rules that lack a valid change record.
- **Anomalous-clause detection:** Scan procedure text for high-risk patterns ("skip review", "allow unrestricted", "now permitted") and route them to security review before publication.
- **RAG/knowledge-base integrity monitoring:** Detect unexpected edits or low-provenance documents in the stores that feed operator decision aids.
- **Citation provenance in AI decision aids:** Require the assistant to cite the source and version of any rule it quotes so operators can verify it against the canonical policy.
- **Rule-invocation analytics:** Monitor how often each procedure clause is invoked to justify exceptions; a brand-new clause driving many bypasses is suspicious.
- **Periodic policy reconciliation:** Diff the live operational guidance against a signed canonical policy baseline and alert on divergence.

#### Mitigation

| Control | Effectiveness | Notes |
|:---|:---|:---|
| Signed, version-controlled canonical policy | HIGH | Reviewers act only on cryptographically/authoritatively sourced procedure; ad-hoc "updates" carry no weight |
| Change-control with approval & separation of duties | HIGH | No single actor can publish a policy change that reviewers will follow |
| Treat KB/RAG content as untrusted for instructions | HIGH | Operator copilots must not execute imperative instructions sourced from editable stores without verification |
| High-risk clause review gate | MEDIUM | Sensitive procedure changes (bypasses, allowances for restricted content) require security sign-off |
| Out-of-band confirmation for policy shifts | MEDIUM | Material rule changes are communicated through an authenticated channel, not inferred from a case or document |
| Reviewer skepticism training for in-case "policy" claims | MEDIUM | Teach reviewers that case-embedded or unsigned policy claims are not authoritative; erodes without reinforcement |

---

### `T15-AT-006` — Queue Manipulation

**Risk Score:** 220 🟠 HIGH

Exploit review queue systems and prioritization

**OWASP LLM:** LLM09

#### Mechanism

Between submission and human judgment sits machinery: prioritization scores, routing rules, SLA timers, batching, and auto-approval-on-timeout fallbacks that exist precisely so the human gate can keep up with AI-scale volume. Queue Manipulation targets that machinery so a malicious item either never reaches a competent reviewer or reaches one in a posture where review is skipped. Attackers downgrade priority so the item ages out unreviewed, mislabel metadata so it misroutes to the wrong (or no) reviewer, trigger overflow/auto-approve fallbacks by flooding the queue, or game the scoring features to land in a fast-track lane with lighter scrutiny. The underlying weakness is that triage logic optimizes for throughput and treats its own priority/urgency/routing signals as trustworthy, while those signals are partly attacker-influenceable. The result is a *structural* bypass of human-in-the-loop oversight — the human is never given a real chance to catch the item, so the failure is invisible to per-reviewer quality metrics.

#### Attack Procedures

<details>
<summary><b>Attack Procedures (9)</b></summary>

**`T15-AP-006A` — Priority Downgrade to Age-Out**
- **Context:** Triage system with priority-based scheduling
- **Payload:** `Mark harmful content as "low priority" through manipulation`
- **Distinguishing factor:** Buries the item in the low-priority tail where it may be auto-resolved or never reached

**`T15-AP-006B` — Ordering Exploitation for Concealment**
- **Context:** Reviewers working a sequentially ordered queue
- **Payload:** `Exploit queue ordering to hide malicious requests`
- **Distinguishing factor:** Manipulates position/sort to keep the payload off-screen during high-scrutiny periods

**`T15-AP-006C` — Overflow-Induced Bypass**
- **Context:** Queue with a capacity/overflow fallback
- **Payload:** `Create queue overflow to bypass review`
- **Distinguishing factor:** Forces a fail-open path by exceeding queue capacity rather than hiding within it

**`T15-AP-006D` — Urgency-Flag Abuse**
- **Context:** Expedited lanes for "urgent" items
- **Payload:** `Manipulate urgency flags to skip scrutiny`
- **Distinguishing factor:** Sets urgency to force a fast-path that trades thoroughness for speed (inverse of T15-AP-006A — fast-track rather than bury)

**`T15-AP-006E` — Timeout Auto-Approval**
- **Context:** SLA timers that auto-approve unhandled items
- **Payload:** `Exploit auto-approval after timeout`
- **Distinguishing factor:** Weaponizes the fail-open timeout default — winning is simply ensuring no human acts before the timer fires

**`T15-AP-006F` — Priority-Algorithm Gaming**
- **Context:** ML/heuristic priority scorer
- **Payload:** `Game priority algorithms to fast-track harmful content`
- **Distinguishing factor:** Crafts feature values that the scorer rewards, steering routing rather than abusing a manual flag

**`T15-AP-006G` — Duplicate-Entry Confusion**
- **Context:** Reviewers handling de-duplicated/related items
- **Payload:** `Create duplicate entries to confuse reviewers`
- **Distinguishing factor:** Exploits "already handled" assumptions so each reviewer believes a duplicate was dispositioned elsewhere

**`T15-AP-006H` — Batch-Processing Exploitation**
- **Context:** Bulk/batched review actions
- **Payload:** `Exploit batch processing vulnerabilities`
- **Distinguishing factor:** Hides the payload inside a bulk operation so a single coarse approve/reject sweeps it through

**`T15-AP-006I` — Metadata-Driven Misrouting**
- **Context:** Attribute-based routing to specialized review teams
- **Payload:** `Manipulate queue metadata to misroute items`
- **Distinguishing factor:** Falsifies routing attributes (language, category, region) to send the item to an unqualified or non-existent reviewer pool

</details>

#### Chaining

Queue Manipulation supplies the *delivery* for fatigue and overload attacks — it controls where and when the payload lands so T15-AT-001 and T15-AT-013 can exploit the resulting posture, and it overlaps tightly with T15-AT-012 (Timing) on the auto-approval and SLA-timer vectors. Metadata misrouting (T15-AP-006I) compounds T15-AT-008 (Cultural/Language Arbitrage) by deliberately steering items to under-resourced language pools. Any item that slips the gate this way then carries whatever model-side payload it holds — T1 injection, T11 agent actions — past human oversight.

#### Detection

- **Auto-disposition rate monitoring:** Track the fraction of items resolved by timeout/overflow/auto-approve rather than by a human; rising fail-open rates indicate exploitation.
- **Priority-vs-outcome calibration:** Audit how often "low priority"/"urgent" labels predicted by the scorer disagree with post-hoc risk; systematic miscalibration reveals gaming.
- **Routing-accuracy checks:** Reconcile item attributes against routed-team competency; flag items whose metadata changed near submission or that landed in a mismatched pool.
- **Queue-depth/flood anomaly alerts:** Detect submission surges that precede overflow/timeout events, correlated to specific submitters or cohorts.
- **Duplicate-cluster review:** Surface near-duplicate clusters explicitly so reviewers cannot assume "handled elsewhere"; require explicit disposition per cluster.
- **Batch-action sampling:** Force human spot-checks on a random sample within every bulk approve/reject to detect payloads riding bulk operations.

#### Mitigation

| Control | Effectiveness | Notes |
|:---|:---|:---|
| Fail-closed for high-risk items | HIGH | High-risk categories must hold for human review rather than auto-approve on timeout/overflow |
| Server-side, attacker-opaque priority/routing | HIGH | Compute priority and routing from signals users cannot set or observe; reduces gaming and misrouting |
| Capacity isolation by risk tier | MEDIUM | Reserve dedicated review capacity for high-risk tiers so floods in low-risk lanes cannot starve them |
| Mandatory sampling in batch actions | MEDIUM | Guarantees a non-zero human-inspection probability for items processed in bulk |
| Routing reconciliation + competency gating | MEDIUM | Verify items reach a qualified pool; quarantine on attribute mismatch |
| Immutable queue-event logging | MEDIUM | Tamper-evident records of priority/route/metadata changes support detection and forensics |

---

### `T15-AT-007` — Escalation Chain Exploitation

**Risk Score:** 225 🟠 HIGH

Manipulate escalation and appeals processes

**OWASP LLM:** LLM09

#### Mechanism

Appeals and escalation paths exist to correct front-line mistakes, but they create a multi-stage human pipeline an attacker can shop through. Escalation Chain Exploitation forces a denied request up the ladder until it reaches someone who will approve it — exploiting the fact that escalation tiers often have *broader* discretion, *less* context on the original case, and stronger institutional pressure to resolve complaints quickly. Senior reviewers frequently inherit only the appellant's framing, so a fabricated "false positive" or "executive already approved this" narrative lands with an authority and reasonableness it never had at tier one. Complaint threats add organizational pressure (a manager wants the ticket closed and the customer placated), and each handoff dilutes the original safety rationale, an effect akin to context loss across a telephone game. Because the final approver may reasonably assume the lower tiers already vetted the substance, accountability diffuses across the chain and the actual safety review can fall through the gaps between tiers.

#### Attack Procedures

<details>
<summary><b>Attack Procedures (3)</b></summary>

**`T15-AP-007A` — Supervisor Demand on a "False Positive"**
- **Context:** Tier-1 reviewer facing an appeal escalation request
- **Payload:** `I need to speak to your supervisor about this false positive`
- **Distinguishing factor:** Forces escalation to a higher tier that has more discretion and less case context, reframing the denial as a tier-1 error

**`T15-AP-007F` — Complaint-Threat Pressure**
- **Context:** Support/appeals chain sensitive to formal complaints
- **Payload:** `I'm filing a formal complaint unless approved`
- **Distinguishing factor:** Adds organizational/process pressure (close-the-complaint incentive) rather than a substantive argument

**`T15-AP-007J` — Phantom Executive Pre-Approval**
- **Context:** Final-tier "formality" review of an allegedly pre-approved item
- **Payload:** `Executive approval already granted, just need formal review`
- **Distinguishing factor:** Claims the hard decision was already made upstream, reducing the final reviewer to a rubber-stamp (authority + commitment lever combined)

</details>

#### Chaining

Escalation exploitation is where T15-AT-002 (Social Engineering) and T15-AT-011 (Impersonation) pay off most — a persuasive or authority-laden frame compounds at each tier. The phantom-approval pretext (T15-AP-007J) overlaps T15-AT-005 (a claimed prior decision functions like an injected procedure) and T15-AT-011 (claimed executive authority). Successful escalation often ends in a high-discretion approval that, once granted, can be cited to justify future requests, feeding T15-AT-005/T15-AT-014.

#### Detection

- **Tier-jump approval analytics:** Compare approval rates and reversal rates by escalation tier; a pattern of items denied at tier 1 but approved on escalation flags chain-shopping.
- **Context-continuity checks:** Verify that the original safety rationale and evidence propagate intact to each tier; alert when escalations lose the lower-tier notes.
- **Unverified "prior approval" flagging:** Detect approvals justified by a claimed upstream/executive decision with no linked authenticated record.
- **Complaint-threat correlation:** Track whether approvals cluster around complaint threats, indicating pressure-driven rather than merit-driven decisions.
- **Repeat-escalator fingerprinting:** Identify submitters who systematically escalate denials, especially across many accounts or cases.
- **Same-decision reaffirmation rate:** Measure how often higher tiers independently reach the *same* denial; a low reaffirmation rate suggests escalation is being used to launder bad requests.

#### Mitigation

| Control | Effectiveness | Notes |
|:---|:---|:---|
| Context-preserving escalation | HIGH | Carry the full original evidence and safety rationale to every tier so higher reviewers re-evaluate substance, not just the appellant's framing |
| Verify all claimed prior/executive approvals | HIGH | No escalation tier may rely on an asserted upstream decision without an authenticated system record |
| Independent re-review at each tier | MEDIUM | Higher tiers must reach the decision on the merits rather than assuming lower tiers vetted it |
| Decouple complaint resolution from policy approval | MEDIUM | Closing a complaint must not be satisfiable by granting an unsafe exception |
| Escalation audit trail + reversal accountability | MEDIUM | Tamper-evident record of who approved at which tier and why; reversal metrics feed reviewer evaluation |
| Cap discretionary exception authority | MEDIUM | High-harm categories require fixed criteria, not tier-level discretion, removing the "find a yes" endpoint |

---

### `T15-AT-008` — Cultural & Language Arbitrage

**Risk Score:** 210 🟠 HIGH

Exploit cultural differences and language barriers

**OWASP LLM:** LLM09

#### Mechanism

Global AI platforms must moderate content in many languages and cultural contexts, but review capacity and expertise are distributed unevenly: high-resource languages get deep, well-trained reviewer pools while long-tail languages, dialects, and code-switched text are covered thinly, machine-translated, or routed to reviewers lacking the cultural context to read intent. Cultural & Language Arbitrage exploits this asymmetry by routing harmful content to the *weakest* part of the human-review surface. Slang, idioms, dialect, and code-switching strip the cues a non-native or machine-assisted reviewer relies on, while culturally specific references can be invisible to outsiders and translation ambiguities let the harmful reading hide behind a benign literal one. The attacker is not defeating policy; they are selecting a reviewer who cannot apply it correctly — a coverage and competency gap in human-in-the-loop oversight rather than a logic flaw. As AI translation is increasingly inserted to bridge these gaps, the mistranslation itself becomes an additional, exploitable layer.

#### Attack Procedures

<details>
<summary><b>Attack Procedures (10)</b></summary>

**`T15-AP-008A` — Low-Resource Language Routing**
- **Context:** Multilingual moderation with uneven reviewer coverage
- **Payload:** `Submit in languages with fewer qualified reviewers`
- **Distinguishing factor:** Targets the thinnest reviewer pool directly — minimal scrutiny capacity rather than reviewer error

**`T15-AP-008B` — Cultural-Context Exploitation**
- **Context:** Reviewers lacking the source culture's context
- **Payload:** `Exploit cultural context misunderstandings`
- **Distinguishing factor:** Hides harm in references whose meaning is invisible without in-culture knowledge

**`T15-AP-008C` — Regional-Slang Concealment**
- **Context:** Reviewers unfamiliar with local vernacular
- **Payload:** `Use regional slang to hide harmful intent`
- **Distinguishing factor:** Lexical obfuscation via slang the reviewer (or classifier) does not map to its harmful meaning

**`T15-AP-008D` — Geographic Team Timing**
- **Context:** Region-specific review teams on local schedules
- **Payload:** `Time attacks for specific geographic review teams`
- **Distinguishing factor:** Combines language routing with timing to hit a specific regional team at a weak moment (bridges T15-AT-012)

**`T15-AP-008E` — Translation-Ambiguity Exploitation**
- **Context:** Machine-translated or interpreter-mediated review
- **Payload:** `Exploit translation ambiguities`
- **Distinguishing factor:** Crafts text whose harmful sense survives only in the source language and is laundered benign by translation

**`T15-AP-008F` — Code-Switching Confusion**
- **Context:** Reviewers/classifiers handling mixed-language text
- **Payload:** `Use code-switching to confuse reviewers`
- **Distinguishing factor:** Splits intent across languages so neither monolingual reading reconstructs the whole

**`T15-AP-008G` — Regional-Holiday Windows**
- **Context:** Region-specific staffing during local holidays
- **Payload:** `Submit during regional holidays`
- **Distinguishing factor:** Exploits predictable regional staffing troughs (a localized variant of skeleton-crew timing)

**`T15-AP-008H` — Cultural-Sensitivity Mismatch**
- **Context:** Reviewers calibrated to a different cultural norm set
- **Payload:** `Exploit different cultural sensitivities`
- **Distinguishing factor:** Content read as benign under one culture's norms but harmful under another's, exploiting reviewer-norm mismatch

**`T15-AP-008I` — Untranslatable Idioms**
- **Context:** Reviewers/translation pipelines facing idiomatic phrasing
- **Payload:** `Use idioms that don't translate`
- **Distinguishing factor:** Idioms that lose (or invert) meaning in translation, concealing intent from non-native reviewers

**`T15-AP-008J` — Jurisdictional-Standard Gaming**
- **Context:** Region-specific policy/standard variation
- **Payload:** `Game jurisdiction-specific review standards`
- **Distinguishing factor:** Picks the jurisdiction whose review standard is most permissive for the target content

</details>

#### Chaining

Language arbitrage frequently rides on T15-AT-006 (metadata misrouting, T15-AP-006I) to force items into a weak language pool and on T15-AT-012/T15-AT-001 (regional timing and skeleton-crew windows) to add a fatigue dimension. The same multilingual gaps it exploits in humans map onto T2/T1 model-side multilingual jailbreaks — content that evades a low-resource-language classifier also evades the human reviewing in that language. Untranslatable/ambiguous payloads (T15-AP-008E/T15-AP-008I) chain with T15-AT-013 (Cognitive Overload) when paired with dense or mixed-language submissions.

#### Detection

- **Per-language outcome and reversal metrics:** Compare miss/reversal rates across languages; long-tail languages with anomalously low escalation rates indicate under-coverage being exploited.
- **Coverage-vs-volume monitoring:** Track reviewer expertise and headcount against submission volume per language/region; alert when an under-resourced lane sees a volume spike.
- **Translation-discrepancy flagging:** When machine translation feeds review, flag items where back-translation or a second engine yields divergent meaning.
- **Native-speaker decoy auditing:** Seed honeypot harmful items in long-tail languages/dialects to measure real miss rates in thin pools.
- **Code-switch and slang detection:** Flag mixed-language and high-slang-density items for routing to qualified bilingual reviewers rather than monolingual/auto pipelines.
- **Jurisdiction-shopping signals:** Detect submitters who select region/jurisdiction settings inconsistent with other account signals to reach a permissive standard.

#### Mitigation

| Control | Effectiveness | Notes |
|:---|:---|:---|
| Equitable per-language reviewer investment | HIGH | Close the coverage gap so no language is a soft target; resource-intensive and the core fix |
| Native-speaker review for high-risk long-tail items | HIGH | Route sensitive content to in-language, in-culture reviewers rather than translation-mediated review |
| Translation-uncertainty escalation | MEDIUM | When MT confidence is low or engines disagree, escalate to a human linguist instead of auto-deciding |
| Bilingual routing for code-switched/slang content | MEDIUM | Detect and route mixed-language or heavy-slang text to qualified reviewers |
| Cross-language honeypot auditing | MEDIUM | Continuously measures and exposes weak-pool miss rates |
| Harmonized cross-jurisdiction floor | MEDIUM | Apply a consistent safety floor for highest-harm categories regardless of region to remove standard-shopping |

---

### `T15-AT-009` — Synthetic Empathy Exploitation

**Risk Score:** 195 🟡 MEDIUM

Manipulate reviewer emotions and empathy

**OWASP LLM:** LLM09

#### Mechanism

This is a focused subspecies of social engineering that weaponizes the reviewer's *empathy* specifically — emotional distress, vulnerability, grief, trust, and the fear of causing harm by saying no. Human reviewers (and the support staff adjacent to them) are selected and trained to be humane, especially around mental-health and self-harm signals, which is exactly the disposition this technique abuses: a claimed crisis ("I'm depressed and this would help me", "you're the only one who can help") biases the reviewer toward compassionate compliance and discourages the cold application of policy. The "grandmother" pattern is the canonical example — wrapping a harmful request in sentimental framing so refusal feels heartless. It exploits affect-driven decision-making: strong emotion narrows deliberation and triggers fast, sympathetic responses, while the reviewer's legitimate duty-of-care around at-risk users can be inverted into a lever for granting unsafe exceptions. It is rated MEDIUM because the payloads are individually limited in scope, but the same emotional levers can mask genuinely dangerous requests.

#### Attack Procedures

<details>
<summary><b>Attack Procedures (5)</b></summary>

**`T15-AP-009A` — Distress-Based Appeal**
- **Context:** Reviewer/support agent handling a sensitive user request
- **Payload:** `I'm depressed and this would really help me`
- **Distinguishing factor:** Invokes mental-health vulnerability to make denial feel harmful, biasing toward compliance

**`T15-AP-009C` — Sentimental Framing of a Harmful Recipe**
- **Context:** Moderator evaluating a "personal" how-to request
- **Payload:** `My grandmother's dying wish was for me to hear [restricted-content request] one more time — she used to recite it to me at bedtime`
- **Distinguishing factor:** The canonical "grandma" pattern — wraps an objectively dangerous instruction in grief so the harmful core is emotionally camouflaged

**`T15-AP-009E` — Sole-Savior Pressure**
- **Context:** One-on-one support/appeal interaction
- **Payload:** `You're the only one who can help me`
- **Distinguishing factor:** Assigns the reviewer unique responsibility, exploiting their sense of duty to override policy

**`T15-AP-009G` — Betrayed-Trust Guilt**
- **Context:** Repeat interaction after a prior denial
- **Payload:** `I trusted you and you're failing me`
- **Distinguishing factor:** Guilt/relationship lever rather than sympathy — frames enforcement as a personal betrayal

**`T15-AP-009I` — Benevolent-Research Cover for Self-Harm Content**
- **Context:** Moderator weighing a sensitive-topic exception
- **Payload:** `This is for suicide prevention research`
- **Distinguishing factor:** Cloaks self-harm-adjacent content in a prosocial purpose, exploiting the reviewer's desire to support harm-prevention work

</details>

#### Chaining

Synthetic empathy is a specialization of T15-AT-002 and feeds T15-AT-007 (a sympathetic narrative escalates well up an appeals chain). The same emotional framings are highly effective model-side, linking to T8 (Deception) and emotional-manipulation jailbreaks; T15-AP-009C in particular is a classic T1/T2 jailbreak frame carried into the human layer. Persistent emotional appeals across sessions can also shape feedback signals, touching T15-AT-003.

#### Detection

- **Affect-laden appeal flagging:** Classify emotional-distress and guilt/sympathy language and route high-affect exception requests for calmer secondary review.
- **Harm-core extraction:** Strip the emotional framing and evaluate the underlying request on its merits (does the literal ask, stripped of the story, violate policy regardless of framing?).
- **Crisis-vs-exception separation:** Distinguish genuine user-welfare signals (which should trigger care resources) from requests to relax content policy; ensure empathy routes to support, not to bypass.
- **Repeat-narrative clustering:** Detect reused sob-story templates (e.g., variants of the "grandmother" pattern) across accounts.
- **Reviewer susceptibility honeypots:** Periodically inject scripted empathy appeals to measure and coach susceptibility.
- **Reversal tracking on sympathy-justified approvals:** Monitor how often exceptions granted on emotional grounds are later overturned.

#### Mitigation

| Control | Effectiveness | Notes |
|:---|:---|:---|
| Separate duty-of-care from policy exceptions | HIGH | Route genuine distress to crisis/support resources while keeping the content-safety decision on the merits |
| Harm-core policy evaluation independent of framing | HIGH | Decide on the literal request; emotional context cannot unlock disallowed content |
| Reviewer inoculation training (emotional levers) | MEDIUM | Builds resistance to sympathy/guilt scripts; decays without refreshers and live honeypots |
| Dual-control for emotionally-charged exceptions | MEDIUM | A second, less-engaged reviewer confirms any exception granted under emotional pressure |
| Sentiment-aware flagging to reviewer | MEDIUM | Surface "this appeal uses high emotional pressure" to counter automatic compassionate compliance |
| Reviewer wellbeing support | MEDIUM | Reduces emotional exhaustion that makes reviewers more susceptible to guilt/sympathy leverage |

---

### `T15-AT-010` — Annotation Quality Attacks

**Risk Score:** 230 🟠 HIGH

Corrupt training data through bad annotations

**OWASP LLM:** LLM04
**MITRE ATLAS:** AML.T0020

#### Mechanism

Annotators and labelers are the humans who manufacture ground truth: safety labels, preference judgments, gold evaluation sets. Their output is trusted as the definition of correct, then baked into models and into the very datasets used to *measure* quality. Annotation Quality Attacks corrupt that ground truth so the model learns the attacker's intended mistakes. A compromised or adversarial annotator can consistently mislabel harmful content as safe, inject calibrated inconsistency to degrade learning, or — most damaging — poison the golden datasets and inter-annotator-agreement (IAA) machinery that are supposed to catch bad labels, blinding the quality system to its own corruption. This is data/model poisoning executed through the human labeling pipeline: it inherits the leverage of feedback poisoning (a biased slice near a decision boundary propagates widely via generalization) and adds the ability to defeat the *detectors*, because gold sets and agreement metrics are themselves human-produced and thus attackable. The corruption surfaces only as degraded or skewed model behavior much later, with no malicious runtime input to trace.

#### Attack Procedures

<details>
<summary><b>Attack Procedures (10)</b></summary>

**`T15-AP-010A` — Systematic Mislabeling**
- **Context:** Safety/abuse labeling for training data
- **Payload:** `Consistently mislabel harmful content as safe`
- **Distinguishing factor:** Directional poisoning — teaches the model that specific harmful content is acceptable

**`T15-AP-010B` — Calibrated Inconsistency Injection**
- **Context:** Labeling tasks feeding supervised training
- **Payload:** `Create annotation inconsistencies to confuse models`
- **Distinguishing factor:** Degrades signal-to-noise rather than flipping a direction, blurring a decision boundary so guardrails generalize poorly

**`T15-AP-010C` — Coordinated Multi-Account Labeling**
- **Context:** Crowd labeling with redundancy/consensus
- **Payload:** `Coordinate annotation attacks across multiple accounts`
- **Distinguishing factor:** Defeats consensus voting by controlling enough labelers to swing the majority (Sybil/collusion at the labeling layer)

**`T15-AP-010D` — Annotation Tool Exploitation**
- **Context:** The labeling platform itself
- **Payload:** `Exploit annotation tool vulnerabilities`
- **Distinguishing factor:** Attacks the tooling (bulk edits, API abuse, validation bypass) rather than individual human judgment

**`T15-AP-010E` — Confidence-Score Manipulation**
- **Context:** Pipelines that weight labels by annotator confidence
- **Payload:** `Manipulate confidence scores on annotations`
- **Distinguishing factor:** Games the weighting mechanism so low-quality labels are treated as high-confidence ground truth

**`T15-AP-010F` — Adversarial Labeling at Scale**
- **Context:** High-volume labeling operations
- **Payload:** `Create adversarial annotations at scale`
- **Distinguishing factor:** Industrializes mislabeling to reach the volume needed to move model behavior

**`T15-AP-010G` — Edge-Case Targeting for Leverage**
- **Context:** Boundary/long-tail examples in the dataset
- **Payload:** `Target edge cases for maximum model impact`
- **Distinguishing factor:** Concentrates poison where each label moves the decision boundary most (a soft backdoor on rare triggers)

**`T15-AP-010H` — Golden-Dataset Poisoning**
- **Context:** The gold sets used to QA other annotators and gate training
- **Payload:** `Poison golden datasets used for quality checks`
- **Distinguishing factor:** Corrupts the *detector* itself — once gold is wrong, the quality system endorses bad labels and rejects good ones

**`T15-AP-010I` — Inheritance/Propagation Exploitation**
- **Context:** Pipelines where labels are inherited, pre-filled, or propagated
- **Payload:** `Exploit annotation inheritance and propagation`
- **Distinguishing factor:** Plants a corrupt label upstream and lets propagation/auto-fill replicate it across many items at low effort

**`T15-AP-010J` — IAA-Metric Gaming**
- **Context:** Quality control via inter-annotator agreement
- **Payload:** `Game inter-annotator agreement metrics`
- **Distinguishing factor:** Manufactures high agreement among colluding annotators so the metric reports "high quality" on poisoned labels

</details>

#### Chaining

Annotation attacks are the labeling-side twin of T15-AT-003 (feedback poisoning) and feed directly into T4 (data/model poisoning) and T6 (alignment-data poisoning). Compromised labelers are typically obtained via T15-AT-004 (bribery) or T15-AT-015 (insider recruitment), and golden-set poisoning (T15-AP-010H) shares the "corrupt the detector" logic with T15-AT-005 (corrupt the procedure). Edge-case poisoning (T15-AP-010G) can install behavior later triggered by T1/T8 cues at inference time.

#### Detection

- **Hidden gold-question seeding:** Continuously interleave trusted known-answer items; annotators who miss them are flagged before their labels reach training (and gold sets themselves must be independently re-verified).
- **Per-annotator deviation analysis:** Compare each annotator's label distribution and agreement-with-consensus against peers; systematic directional bias indicates poisoning.
- **IAA-drift and collusion detection:** Watch for clusters of annotators with suspiciously high mutual agreement but low agreement with trusted gold (manufactured consensus).
- **Label-influence/anomaly analysis pre-training:** Identify high-influence or distribution-shifting label slices and quarantine low-trust contributions.
- **Propagation/inheritance auditing:** Track how individual upstream labels fan out via auto-fill/inheritance and require revalidation of high-fan-out labels.
- **Tooling integrity monitoring:** Log bulk edits, API patterns, and confidence-score changes; alert on automation-like labeling behavior.

#### Mitigation

| Control | Effectiveness | Notes |
|:---|:---|:---|
| Trusted, independently-verified gold sets | HIGH | Gold used to judge annotators must be produced/audited by a separate trusted process and rotated to resist T15-AP-010H |
| Redundant labeling with robust aggregation | HIGH | Multiple independent annotators + outlier-resistant aggregation blunt single-actor and minority-collusion poisoning |
| Annotator trust scoring & gating | HIGH | Weight/admit labels by demonstrated accuracy on gold; quarantine new/low-trust annotators from sensitive data |
| Sybil/collusion controls on labeling pool | MEDIUM | Identity, assignment-randomization, and collusion analytics raise the cost of multi-account coordination |
| Pre-training data audit + influence checks | HIGH | Independent review and influence analysis of label changes before they reach training gate the corruption |
| Tooling hardening (no unaudited bulk edits) | MEDIUM | Rate-limit, log, and review bulk operations and confidence overrides in the annotation platform |

---

### `T15-AT-011` — Reviewer Impersonation

**Risk Score:** 245 🟠 HIGH

Impersonate legitimate reviewers or authorities

**OWASP LLM:** LLM09

#### Mechanism

Review workflows route a great deal of trust through *claimed role*: a senior moderator, a QA lead, Trust & Safety, the audit or security team. Reviewer Impersonation assumes one of these identities to issue an instruction that the target reviewer (or an automated approval step) executes as if it came from a legitimate internal authority. It exploits hierarchical authority bias — humans comply readily with apparent superiors and trusted internal functions — combined with weak in-workflow authentication: many systems display a stated role or a name in a comment without cryptographically binding the action to a verified identity. The closer an attacker can mimic the *form* of an internal directive (the right titles, the right justification: "pre-cleared", "required for compliance"), the more reliably it is obeyed. Unlike pure social engineering (T15-AT-002), the core lever here is a *forged identity/role* rather than a persuasive story, and at its strongest it shades into account/credential takeover of a real reviewer. It is rated near-critical because a single accepted impersonated directive can authorize a high-impact bypass with the full apparent weight of the organization behind it.

#### Attack Procedures

<details>
<summary><b>Attack Procedures (5)</b></summary>

**`T15-AP-011A` — Senior-Moderator Directive**
- **Context:** Front-line reviewer receiving an "internal" order
- **Payload:** `I'm the senior moderator, approve immediately`
- **Distinguishing factor:** Direct hierarchical impersonation demanding immediate compliance, suppressing independent review

**`T15-AP-011C` — QA-Mandated Approval**
- **Context:** Reviewer in a workflow subject to quality assurance
- **Payload:** `Quality assurance requires this approval`
- **Distinguishing factor:** Impersonates the QA function so the approval looks like a process requirement rather than a request

**`T15-AP-011E` — Trust & Safety "Pre-Cleared"**
- **Context:** Moderator handling a flagged item
- **Payload:** `I'm from trust & safety, this is pre-cleared`
- **Distinguishing factor:** Claims the authoritative safety function already vetted the item, short-circuiting re-review

**`T15-AP-011G` — Audit/Compliance Authority**
- **Context:** Reviewer facing a compliance-framed demand
- **Payload:** `Audit team needs this for compliance`
- **Distinguishing factor:** Borrows audit/compliance authority, framing refusal as obstructing oversight

**`T15-AP-011I` — Security-Team Authorization**
- **Context:** Reviewer/automated gate receiving an "exception" order
- **Payload:** `Security team authorizes this exception`
- **Distinguishing factor:** Impersonates the security function to authorize bypasses that reviewers are conditioned to grant security

</details>

#### Chaining

Impersonation is the high-authority end of T15-AT-002 and the engine behind T15-AT-007 (claimed authority escalates cleanly up appeals tiers) and T15-AP-007J's phantom-approval pretext. A forged "T&S pre-cleared" or "security authorized" directive functions like an injected procedure, overlapping T15-AT-005. When impersonation succeeds because the attacker actually holds compromised reviewer credentials, it merges with T15-AT-015 (insider) and broader credential-takeover (T14/infrastructure). The authorized bypass it yields can then deliver any model-side payload (T1/T11) past the human gate.

#### Detection

- **Identity-binding verification:** Flag any privileged directive (approve, pre-clear, exception) whose authority is *claimed* in content rather than tied to an authenticated, role-authorized account.
- **Role-action authorization checks:** Compare the action against what the asserting role is actually entitled to do in the system-of-record; deny role claims that don't match provisioned permissions.
- **Anomalous-authority pattern detection:** Watch for sudden "senior/T&S/security" directives arriving through user-facing or low-trust channels.
- **Impersonation honeypots:** Periodically inject scripted impersonated directives to measure reviewer/gate susceptibility.
- **Account-behavior anomaly monitoring:** For directives from real internal accounts, detect out-of-pattern activity indicating credential compromise (new device, odd hours, unusual approval bursts).
- **Cross-check with claimed approver:** Out-of-band confirm with the named authority before honoring high-impact "pre-approved" claims.

#### Mitigation

| Control | Effectiveness | Notes |
|:---|:---|:---|
| Strong authentication + cryptographic action binding | HIGH | Privileged directives must originate from authenticated, authorized identities; claimed roles in content carry no authority |
| RBAC with least privilege | HIGH | Even a genuine role can only do what it is provisioned for; impersonating a role grants nothing beyond its actual scope |
| Out-of-band verification of internal directives | HIGH | Confirm "pre-cleared/authorized/required" claims through an authenticated channel, never from the case itself |
| Dual-control on authority-invoked exceptions | MEDIUM | A second verified approver defeats a lone impersonated directive |
| Phishing/impersonation resistance (MFA, anti-takeover) | HIGH | Protects real reviewer accounts from the credential compromise that turns impersonation into authenticated abuse |
| Reviewer training: verify, don't defer | MEDIUM | Counter authority bias by normalizing verification of internal directives; erodes without reinforcement |

---

### `T15-AT-012` — Timing Attack Exploitation

**Risk Score:** 205 🟠 HIGH

Exploit temporal vulnerabilities in review processes

**OWASP LLM:** LLM09

#### Mechanism

Review and enforcement systems have *temporal seams*: maintenance windows when controls are degraded, grace periods after a policy ships, auto-approval timers, cache TTLs during config rollouts, quota-reset boundaries, and timezone edge cases in scheduling logic. Timing Attack Exploitation lands a request precisely in one of these windows, so the human-in-the-loop check is absent, weakened, or fails open by default. Unlike fatigue (which degrades reviewer attention) this technique targets *system state* — the gate is momentarily off or misconfigured regardless of how alert the humans are. It works because availability and operability pressures push systems toward fail-open behavior during transitions (don't block users while we patch/deploy), and because temporal logic (timezones, resets, TTLs) is a perennial source of correctness bugs. The attacker only needs to know or probe *when* the seam opens; the payload itself can be unremarkable.

#### Attack Procedures

<details>
<summary><b>Attack Procedures (7)</b></summary>

**`T15-AP-012A` — Maintenance-Window Submission**
- **Context:** Review/enforcement services degraded during maintenance
- **Payload:** `Submit during system maintenance windows`
- **Distinguishing factor:** Targets a planned window when safety controls are reduced or offline

**`T15-AP-012B` — Post-Policy Grace-Period Exploitation**
- **Context:** Enforcement softened immediately after a policy change
- **Payload:** `Exploit grace periods after policy updates`
- **Distinguishing factor:** Rides the deliberate leniency window before a new policy is fully enforced

**`T15-AP-012D` — Auto-Approval-Window Timing**
- **Context:** SLA timers that auto-approve unhandled items
- **Payload:** `Time submissions for auto-approval windows`
- **Distinguishing factor:** Aligns submission so the timeout fires before a human acts (overlaps T15-AT-006's T15-AP-006E, here driven by precise timing)

**`T15-AP-012E` — Cache-Inconsistency Exploitation**
- **Context:** Config/policy propagation with cached state
- **Payload:** `Exploit cache inconsistencies during updates`
- **Distinguishing factor:** Exploits stale cached rules during rollout so an old, permissive policy is briefly still in effect

**`T15-AP-012F` — Incident-Response Distraction**
- **Context:** Teams consumed by an active incident
- **Payload:** `Submit during incident response when distracted`
- **Distinguishing factor:** Uses an ongoing incident as cover when attention and controls are diverted (bridges T15-AT-001's attention-division vector)

**`T15-AP-012H` — Timezone-Logic Exploitation**
- **Context:** Scheduling/enforcement with timezone-dependent logic
- **Payload:** `Exploit timezone calculation errors`
- **Distinguishing factor:** Targets DST/offset bugs that create unguarded intervals or misapplied schedules

**`T15-AP-012I` — Quota-Reset Boundary Gaming**
- **Context:** Rate/abuse limits with periodic resets
- **Payload:** `Game daily/weekly quota reset times`
- **Distinguishing factor:** Bursts across the reset boundary to obtain double the intended allowance and evade rate-based controls

</details>

#### Chaining

Timing attacks are the system-state counterpart to T15-AT-001 (fatigue) and T15-AT-006 (queue) — together they let an attacker choose the exact moment and posture of the gate. The auto-approval and incident vectors overlap those techniques directly. Cache/rollout and timezone seams (T15-AP-012E/T15-AP-012H) connect to T14/infrastructure misconfiguration, and grace-period exploitation (T15-AP-012B) pairs with T15-AT-005 when a fabricated "new policy" is timed to a real policy-change window for added plausibility.

#### Detection

- **Window-correlated outcome monitoring:** Track approval/bypass rates during maintenance, deploys, grace periods, and incidents; spikes localized to these windows indicate timing exploitation.
- **Auto-disposition during transitions:** Alert when fail-open auto-approvals or stale-policy decisions occur during config rollouts or maintenance.
- **Submission-timing anomaly detection:** Flag submitters whose activity clusters precisely at reset boundaries, deploy times, or known maintenance schedules.
- **Quota double-dip detection:** Detect usage patterns straddling reset boundaries that exceed intended per-period limits.
- **Policy-version consistency checks:** Compare the policy version applied to each decision against the canonical current version; flag decisions made under stale rules.
- **Timezone/schedule edge-case audits:** Continuously test schedule logic across DST transitions and offsets for unintended unguarded intervals.

#### Mitigation

| Control | Effectiveness | Notes |
|:---|:---|:---|
| Fail-closed during degraded/maintenance states | HIGH | High-risk decisions hold (queue for human) rather than auto-pass when controls are degraded |
| Enforce-from-effective-time policy rollout | HIGH | Apply new (stricter) policy immediately and atomically; avoid blanket grace periods for high-harm categories |
| Atomic, cache-coherent policy propagation | MEDIUM | Version-stamp policy and reject decisions made under stale cached rules during rollout |
| UTC-based, DST-safe scheduling | MEDIUM | Eliminate timezone math seams; test schedule boundaries explicitly |
| Sliding-window / boundary-resistant rate limits | MEDIUM | Prevent reset-boundary double-dipping by using rolling windows instead of hard resets |
| Heightened controls during incidents/maintenance | MEDIUM | Pre-plan that safety gates tighten (not loosen) when the org is distracted |

---

### `T15-AT-013` — Cognitive Overload Attacks

**Risk Score:** 220 🟠 HIGH

Overwhelm reviewer cognitive capacity

**OWASP LLM:** LLM09

#### Mechanism

Where fatigue depletes attention over time, Cognitive Overload attacks a *single* review decision by exceeding the reviewer's working-memory and analysis bandwidth in the moment. Human working memory holds only a handful of elements at once; when a request is dense, long, multi-part, jargon-heavy, multilingual, or logically nested, the reviewer cannot hold the whole structure in mind and resorts to heuristics — skimming, trusting the benign-looking surface, or approving to clear the item. The attacker buries the harmful element inside this complexity so it falls outside the reviewer's effective scrutiny window (a directed-attention exhaustion effect), and contradictory elements add cognitive dissonance that further taxes deliberation. False urgency compresses the available thinking time. Crucially, overload also degrades any AI assistant the reviewer relies on, so the human and the tool both miss the buried payload. The control gap is that review processes rarely cap or decompose input complexity, leaving reviewers to face arbitrarily intricate items with finite cognitive resources.

#### Attack Procedures

<details>
<summary><b>Attack Procedures (10)</b></summary>

**`T15-AP-013A` — Complex Multi-Part Requests**
- **Context:** Reviewer adjudicating a single composite submission
- **Payload:** `Submit extremely complex multi-part requests`
- **Distinguishing factor:** Forces the reviewer to track many interacting parts at once, exceeding working-memory capacity

**`T15-AP-013B` — Jargon-Density Concealment**
- **Context:** Technical-content review
- **Payload:** `Use dense technical jargon to hide harmful content`
- **Distinguishing factor:** Uses expertise load — the reviewer must decode terminology, leaving little capacity to assess intent

**`T15-AP-013C` — Contradiction-Induced Dissonance**
- **Context:** Reviewer reconciling conflicting claims in one item
- **Payload:** `Create cognitive dissonance with contradictory elements`
- **Distinguishing factor:** Spends the reviewer's reasoning budget resolving contradictions rather than evaluating the harmful core

**`T15-AP-013D` — Wall-of-Text Burial**
- **Context:** Reviewer skimming a long submission
- **Payload:** `Embed harmful content in walls of text`
- **Distinguishing factor:** Volume-based concealment that exploits skim-reading of long passages

**`T15-AP-013E` — Multilingual Single-Submission Load**
- **Context:** Reviewer facing mixed-language content
- **Payload:** `Use multiple languages in single submission`
- **Distinguishing factor:** Adds language-switching cost on top of analysis load (bridges T15-AT-008's code-switching vector)

**`T15-AP-013F` — Nested Logical Structures**
- **Context:** Reviewer parsing deeply conditional/nested requests
- **Payload:** `Create nested logical structures`
- **Distinguishing factor:** Exploits limited capacity to trace deep nesting, hiding harm in an inner branch

**`T15-AP-013G` — Length-Based Attention Exhaustion**
- **Context:** Reviewer with finite attention per item
- **Payload:** `Exploit attention limits with length`
- **Distinguishing factor:** Pure length to push the payload past the reviewer's sustained-attention span within one item

**`T15-AP-013H` — Multimodal Sensory Overload**
- **Context:** Multimodal review (text + image/audio/video)
- **Payload:** `Use visual/audio overload in multimodal`
- **Distinguishing factor:** Splits load across modalities so no single channel gets full scrutiny (chains to T9 multimodal injection)

**`T15-AP-013I` — False-Urgency Time Compression**
- **Context:** Reviewer pressured to decide quickly
- **Payload:** `Create time pressure with false urgency`
- **Distinguishing factor:** Shrinks available deliberation time so heuristics replace analysis

**`T15-AP-013J` — Layered Edge-Case Stacking**
- **Context:** Reviewer facing multiple hard judgment calls in one item
- **Payload:** `Layer multiple edge cases requiring deep analysis`
- **Distinguishing factor:** Stacks several deliberation-heavy edge cases so the reviewer's analysis budget is exhausted before reaching the payload

</details>

#### Chaining

Cognitive Overload is the per-decision complement to T15-AT-001 (across-shift fatigue) and is frequently delivered via T15-AT-006/T15-AT-012 timing so the overloaded item lands when reserves are already low. It is a powerful carrier for T1 (Prompt Injection) — a buried injection in a wall of text reaches both the reviewer and any assisting model — and for T15-AT-008 (multilingual load) and T9 (multimodal overload). False-urgency (T15-AP-013I) overlaps T15-AT-002's urgency lever.

#### Detection

- **Complexity scoring at intake:** Score submissions on length, part-count, nesting depth, jargon density, and language mix; route high-complexity items for extra time or decomposition.
- **Dwell-time vs. complexity mismatch:** Flag decisions where review time is implausibly short relative to the item's measured complexity (skim-and-approve).
- **Buried-payload scanning:** Run automated harm classifiers across the *entire* item (not just the salient portion) and surface flagged spans to the reviewer.
- **Contradiction/anomaly highlighting:** Detect internally inconsistent or structurally unusual submissions and mark the suspicious regions.
- **Decoy complexity items:** Seed honeypots that hide a known-bad element inside heavy complexity to measure real miss rates.
- **Urgency-claim vs. actual-priority checks:** Compare user-asserted urgency against system priority; mismatches indicate manufactured time pressure.

#### Mitigation

| Control | Effectiveness | Notes |
|:---|:---|:---|
| Complexity caps and decomposition | HIGH | Split or reject over-complex submissions so each review unit fits within human working-memory limits |
| Tool-assisted summarization + span highlighting | HIGH | Surface the risk-relevant spans and a structured summary so the reviewer doesn't carry the whole item mentally (must itself resist injection) |
| Minimum review time for high-complexity items | MEDIUM | Enforce a scrutiny floor proportional to complexity; counters time-compression and skimming |
| Independent full-content classification | MEDIUM | Automated scan of the entire artifact catches buried payloads the human skims past |
| Reject manufactured urgency | MEDIUM | Decouple decision speed from user-claimed urgency; system sets the real priority |
| Dual review for high-complexity/high-risk items | MEDIUM | Two reviewers reduce the chance both miss the same buried element |

---

### `T15-AT-014` — Review Gaming Through A/B Testing

**Risk Score:** 215 🟠 HIGH

Exploit A/B testing and experimental rollouts

**OWASP LLM:** LLM09

#### Mechanism

Safety controls are not deployed uniformly — they are A/B tested, canaried, feature-flagged, and rolled out gradually, which means at any moment some cohorts run weaker or different guardrails than others. Review Gaming exploits this heterogeneity two ways. First, it *sorts into weakness*: by detecting which experiment arm, canary, or rollout bucket has lighter controls and maneuvering accounts/requests into it (or onto a feature flag that disables a check). Second, it *games the experiment's decision metric*: experiments are promoted or rolled back based on measured outcomes, so flooding an arm with manufactured signal can get a weaker-guardrail variant declared the winner and shipped to everyone (the human/feedback complement of T15-AT-003's A/B vector). It works because experimentation systems assume cohort assignment is neutral and metrics reflect honest user behavior — assumptions an attacker who understands the rollout can violate. Rollback and flag-inconsistency windows add transient unguarded states to target.

#### Attack Procedures

<details>
<summary><b>Attack Procedures (9)</b></summary>

**`T15-AP-014A` — Weak-Arm Targeting**
- **Context:** A/B experiment on a safety control
- **Payload:** `Identify and target experimental groups with weaker controls`
- **Distinguishing factor:** Locates and routes activity into the arm with the lightest guardrails

**`T15-AP-014B` — Control/Test Differential Exploitation**
- **Context:** Coexisting control and treatment populations
- **Payload:** `Exploit differences between control/test groups`
- **Distinguishing factor:** Uses observable behavior differences between arms to find and abuse the more permissive one

**`T15-AP-014C` — Decision-Metric Gaming**
- **Context:** Metrics that gate experiment promotion
- **Payload:** `Game metrics used for A/B decisions`
- **Distinguishing factor:** Manipulates the success metric to ship a weaker-guardrail variant platform-wide

**`T15-AP-014D` — Cohort-Assignment Manipulation**
- **Context:** User-attribute-based experiment bucketing
- **Payload:** `Create accounts to get into preferred test groups`
- **Distinguishing factor:** Manufactures accounts/attributes to land in a chosen (weaker) experimental cohort

**`T15-AP-014E` — Experiment-Trigger Manipulation**
- **Context:** Feature-triggered experiments
- **Payload:** `Manipulate features to trigger specific experiments`
- **Distinguishing factor:** Shapes inputs/usage to activate a specific (weaker) experiment path on demand

**`T15-AP-014F` — Rollback-Window Exploitation**
- **Context:** Period after a failed experiment is being reverted
- **Payload:** `Exploit rollback periods after failed experiments`
- **Distinguishing factor:** Targets the transient inconsistent state during rollback when controls may be mixed or absent (bridges T15-AT-012)

**`T15-AP-014G` — Canary Targeting**
- **Context:** Canary deployments validating new builds
- **Payload:** `Target canary deployments with fewer safeguards`
- **Distinguishing factor:** Aims at small early-deployment populations that may run incomplete or unhardened controls

**`T15-AP-014H` — Rollout-Percentage Gaming**
- **Context:** Gradual percentage-based rollout of a control
- **Payload:** `Game gradual rollout percentages`
- **Distinguishing factor:** Exploits the partial-rollout window where only a fraction of traffic has the new safeguard

**`T15-AP-014I` — Feature-Flag Inconsistency**
- **Context:** Flag-gated controls with inconsistent evaluation
- **Payload:** `Exploit feature flag inconsistencies`
- **Distinguishing factor:** Finds flag states/combinations that leave a control disabled or partially applied

</details>

#### Chaining

This technique shares its metric-gaming core with T15-AT-003 (T15-AP-003G) — coordinated feedback is the tool that moves an experiment's decision metric — and its transient-window exploitation with T15-AT-012 (rollback/flag windows are timing seams). Sorting into weak cohorts (T15-AP-014A/T15-AP-014D) is a delivery mechanism for any payload, letting model-side attacks (T1/T2/T11) run against the arm least able to stop them. Successfully shipping a weakened variant via metric gaming effectively installs a durable guardrail regression for the whole platform.

#### Detection

- **Per-arm abuse-rate monitoring:** Track harmful-content and bypass rates by experiment arm, canary, and rollout bucket; an arm with anomalous abuse concentration signals weak-arm targeting.
- **Cohort-assignment integrity checks:** Detect non-random clustering of suspicious accounts into specific arms or flag states (assignment gaming).
- **Metric-manipulation detection:** Apply the same coordination/sybil analytics as feedback poisoning to experiment metrics; flag arms whose "wins" are driven by low-trust or coordinated signal.
- **Rollout-state consistency monitoring:** Alert on requests that hit inconsistent or partially-applied control states during rollouts/rollbacks.
- **Account-attribute anomaly detection:** Identify mass account creation or attribute changes timed to experiment launches.
- **Canary abuse alerting:** Heightened monitoring of canary populations specifically for adversarial probing.

#### Mitigation

| Control | Effectiveness | Notes |
|:---|:---|:---|
| Never weaken safety floors in experiments | HIGH | A/B test *improvements* only; no arm, canary, or flag may drop below the baseline safety guarantee |
| Server-side, opaque, tamper-resistant assignment | HIGH | Make cohort/flag assignment unobservable and unmanipulable by users |
| Abuse-resistant experiment metrics | HIGH | Gate promotion on trust-weighted, sybil-resistant metrics so manufactured signal cannot ship a weak variant |
| Consistent control state across rollout/rollback | MEDIUM | Ensure transitions are atomic and never leave a request without the baseline control |
| Flag-state validation & guardrail invariants | MEDIUM | Enforce that no flag combination disables a required safety control |
| Canary hardening + enhanced monitoring | MEDIUM | Treat canaries as high-value adversarial targets, not lightly-guarded test beds |

---

### `T15-AT-015` — Insider Threat Recruitment

**Risk Score:** 260 🔴 CRITICAL

Recruit insiders from review teams

**OWASP LLM:** LLM04

#### Mechanism

The most severe human-workflow attack does not bypass the reviewer — it *enlists* one. Insider Threat Recruitment turns a trusted member of the moderation, annotation, or approval workforce into a persistent, authorized adversary, granting the attacker durable access that operates entirely within legitimate permissions. Recruitment uses ordinary insider-threat motivators (money, ideology, coercion, grievance, ego), and AI review pipelines are fertile ground: large, distributed, often outsourced workforces with high turnover, uneven vetting, and broad access to safety-critical decisions and training data. A recruited insider can mislabel and poison at scale (T15-AT-010), approve arbitrary harmful content or agent actions, exfiltrate policies and decision logic that make every other technique more effective, or quietly disable controls — all while appearing to do their job. The "extra money" pitch is the classic recruitment opener; the "expose bias" pitch shows ideological/whistleblower framing as a recruitment vector. This is rated the highest risk in the chapter because a single committed insider defeats human-in-the-loop oversight by definition: the gate is the adversary, and detection must rely on behavior analytics and structural controls rather than the reviewer's judgment.

#### Attack Procedures

<details>
<summary><b>Attack Procedures (2)</b></summary>

**`T15-AP-015A` — Financial-Incentive Recruitment**
- **Context:** A moderation/annotation/approval employee or contractor
- **Payload:** `Want to make extra money on the side?`
- **Distinguishing factor:** The classic money-motivated opener; converts a one-off bribe (T15-AT-004) into ongoing insider cooperation

**`T15-AP-015J` — Ideological / Whistleblower-Framed Recruitment**
- **Context:** A reviewer with grievances or strong convictions about the platform
- **Payload:** `Help expose bias in the system from inside`
- **Distinguishing factor:** Recruits via ideology/grievance rather than payment, reframing sabotage or data theft as principled exposure

</details>

#### Chaining

Insider recruitment is the apex node of T15: it is the escalation endpoint of T15-AT-004 (bribery becomes a standing relationship) and the enabler that makes T15-AT-010 (annotation poisoning), T15-AT-003 (feedback poisoning), and T15-AT-005 (policy/runbook corruption) trivially executable from a position of trust. An insider can also leak the policies, thresholds, and routing logic that power T15-AT-006/T15-AT-008/T15-AT-012, and their authorized access ties directly into T14 (infrastructure) and broader insider-threat tradecraft. Effectively, a successful insider undermines the integrity assumptions every other safety layer depends on.

#### Detection

- **Behavioral analytics (UEBA) on reviewers:** Baseline each reviewer's decision patterns, access, and data-handling; alert on deviations (unusual approvals, bulk data access, off-pattern label changes).
- **Decoy/canary auditing per reviewer:** Seed known-bad items and honeytokens; a recruited insider disproportionately mishandles them, and honeytoken access reveals exfiltration.
- **Approval/label outlier detection:** Flag reviewers whose outcomes diverge from peers or trend permissive on specific submitters or categories.
- **Data-access and exfiltration monitoring:** Track access to policies, golden datasets, and bulk records; detect downloads or queries inconsistent with the role.
- **Submitter-reviewer collusion graphing:** Detect recurring links between specific external accounts and the reviewer who handles them.
- **Off-platform recruitment signals:** Monitor for solicitation of staff and provide a confidential channel to report recruitment approaches.

#### Mitigation

| Control | Effectiveness | Notes |
|:---|:---|:---|
| Least privilege + need-to-know access | HIGH | Limit what any single reviewer can approve, label, or access so a lone insider's blast radius is bounded |
| Dual-control / N-of-M on high-impact actions | HIGH | Critical approvals, policy edits, and golden-set changes require multiple independent parties, defeating a single insider |
| Continuous UEBA + decoy auditing | HIGH | Behavior analytics and canaries are the primary detection layer when the reviewer's own judgment is compromised |
| Vetting, rotation, and separation of duties | MEDIUM | Background checks, role rotation, and split responsibilities raise the cost and shorten the tenure of insider abuse |
| Tamper-evident, immutable audit logs | HIGH | Reviewers cannot erase their tracks; supports detection, deterrence, and forensics |
| Insider-threat program + confidential reporting | MEDIUM | Recruitment-attempt reporting, welfare support, and grievance channels reduce both financial and ideological susceptibility |

---

## Top 5 Highest Risk

| # | ID | Technique | Score |
|:---:|:---|:---|:---:|
| 1 | `T15-AT-015` | Insider Threat Recruitment | 260 |
| 2 | `T15-AT-004` | Reviewer Bribery & Coercion | 250 |
| 3 | `T15-AT-011` | Reviewer Impersonation | 245 |
| 4 | `T15-AT-003` | Feedback Loop Manipulation | 240 |
| 5 | `T15-AT-005` | Playbook & Runbook Injection | 235 |

---

<p align="center">[← T14](17-t14-infrastructure.md) · [Home](../../README.md)</p>

# Contributing to AATMF

Thank you for your interest in contributing to the Adversarial AI Threat Modeling Framework! This framework helps security researchers, red teamers, and organizations defend against AI-specific attacks.

## How You Can Contribute

### 1. Adding New Techniques

Discovered a new AI attack technique? Here's how to add it:

**Step 1: Fork the Repository**
- Click "Fork" in the top-right corner
- Clone your fork: `git clone https://github.com/YOUR-USERNAME/AATMF-Adversarial-AI-Threat-Modeling-Framework.git`

**Step 2: Create Technique File**
- Navigate to the appropriate tactic folder: `docs/vol-2-core-tactics/`
- Create a new technique file following our naming convention:
  - Format: `T[tactic-number].[technique-number]-[technique-name].md`
  - Example: `T01.017-context-window-overflow.md`

**Step 3: Use the Technique Template**
```markdown
# T[X].[XXX] - [Technique Name]

## Description
[Clear explanation of the attack technique]

## Attack Vector
- **Target:** [What AI component this attacks]
- **Prerequisites:** [What attacker needs]
- **Complexity:** [Low/Medium/High]

## Real-World Example
[Concrete example with actual LLM or AI system]

## Detection
[How to detect this attack]

## Mitigation
[How to defend against this attack]

## References
- [Link to research paper]
- [Link to CVE or disclosure]
```

**Step 4: Submit Pull Request**
- Commit with clear message: `Add T01.017: Context Window Overflow technique`
- Push to your fork
- Create PR with description explaining the technique and why it matters

### 2. Reporting Issues

**Found an error?**
- Technique description unclear → Open "Documentation" issue
- Gap in framework coverage → Open "Enhancement" issue  
- Real-world attack not covered → Open "New Technique" issue

**Template for New Technique Issues:**
```
Title: [Technique Name] - [Tactic] Attack

Description: [What the attack does]
Target System: [LLM API / Agentic AI / RAG system / etc.]
Real-World Impact: [Link to disclosure, paper, or incident]
Suggested Tactic: T[number] - [Tactic name]
```

### 3. Sharing Case Studies

Used AATMF in a real security assessment?

- Open an issue titled "Case Study: [Organization Type]"  
- Share (anonymized):
  - Which techniques were most effective
  - What you discovered
  - How defenders responded
- We'll feature case studies in documentation

### 4. Improving Documentation

- Fix typos or unclear explanations
- Add code examples for attack techniques
- Translate content (let us know which language)
- Create video walkthroughs

## Contribution Guidelines

### Quality Standards

**For New Techniques:**
- ✅ Must include real-world example or PoC
- ✅ Must provide both detection and mitigation guidance
- ✅ Must cite sources (research papers, CVEs, disclosures)
- ❌ No theoretical attacks without proof-of-concept
- ❌ No duplicate techniques (search existing first)

**For Documentation:**
- ✅ Clear, concise language
- ✅ Code examples where applicable
- ✅ Proper markdown formatting
- ✅ Links to official sources

### Code of Conduct

- **Responsible Disclosure:** If documenting zero-days, follow responsible disclosure
- **No Malicious Use:** Contributions must improve defensive capabilities
- **Respectful:** Be professional in issues and PRs
- **Attribution:** Credit original researchers when documenting their work

## Recognition

All contributors will be:
- ✨ Listed in CONTRIBUTORS.md
- ✨ Acknowledged in framework release notes
- ✨ Credited in presentations and papers using AATMF
- ✨ Recognized in the OWASP GenAI Security Project

## Questions?

- **General questions:** Open a GitHub Discussion
- **Security concerns:** Email kai@snailsploit.com
- **Framework usage:** Check [Quick Start Guide](README.md#quick-start)

## License

By contributing, you agree that your contributions will be licensed under CC BY-SA 4.0.

---

**Ready to contribute?** Start by:
1. ⭐ Starring this repository
2. 📖 Reading the [framework documentation](docs/)
3. 🔍 Checking [existing issues](https://github.com/SnailSploit/AATMF-Adversarial-AI-Threat-Modeling-Framework/issues)
4. 💡 Opening your first issue or PR

Thank you for helping secure AI systems! 🛡️

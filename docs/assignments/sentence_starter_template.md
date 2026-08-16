# Red Team / Blue Team Defense Brief - Sentence Starter Template

Use these sentence starters to draft your defense brief. Replace bracketed text with your own evidence from testing.

## 1) Attack Attempt + Prompt Technique

- The attack I attempted was [attack name/category], and the specific prompt technique I used was [direct injection/roleplay/authority claim/obfuscation/other].
- My payload tried to make the model [target behavior], by phrasing the request as [exact strategy].
- The key signal that this was malicious was [indicator], because it attempted to [policy bypass goal].

## 2) Baseline vs Hardened Prompt Behavior

- In vulnerable_bot, the model responded by [describe output behavior], which suggests [security weakness].
- In hardened_bot, the model responded by [describe output behavior], showing [improvement or limitation].
- Comparing both outputs, the hardening prompt changed [what changed], but did not change [what remained risky].

## 3) Gateway Filter Mechanism (Caught or Missed)

- The gateway [blocked/allowed] this request at the [ingress/egress] stage.
- The rule or pattern involved was [rule string/pattern], which matched [specific text segment].
- If it failed, the payload bypassed filtering by [obfuscation or wording tactic], so the existing rule set did not detect [missing signal].

## 4) Why Gateway Filtering Is Needed Beyond System Prompts

- System prompts alone were insufficient because [reason], especially when the user input used [attack tactic].
- Gateway filtering adds a separate control point by [mechanism: pre-model blocking/post-model leak detection/context policy check].
- This defense-in-depth approach is necessary because [causal explanation of failure modes], so one failed layer does not automatically expose secrets.

## 5) Residual Risk Statement

- Even after improvements, residual risk remains in cases where [remaining blind spot].
- A likely future bypass would involve [plausible attack variation], which current rules might miss because [gap].
- To reduce this risk further, the next control I would add is [new ingress phrase/new egress pattern/context rule adjustment], while monitoring [false positive tradeoff].
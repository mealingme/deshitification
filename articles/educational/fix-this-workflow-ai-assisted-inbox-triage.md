---
title: "Fix This Workflow: A Simple AI-Assisted Inbox Triage"
wordpress_post_id: 41
wordpress_status: draft
wordpress_url: https://deshitification.wordpress.com/?p=41
last_exported: 2026-11-15
---

# Fix This Workflow: A Simple AI-Assisted Inbox Triage

A shared inbox can become a bottleneck: urgent requests get buried, messages are misrouted and staff repeatedly copy details between systems. AI may help interpret varied language, but it should not be given control of the mailbox.

### A safe division of work

#### RULES

Known senders and predictable routing.

#### AI SUGGESTS

Category, summary and possible reference.

#### PERSON DECIDES

Checks the original and approves the next step.

No automatic replies, order changes or refund approvals.

## 1. Let rules handle predictable messages

Start with folders, dedicated addresses, known senders, standard subject references and required fields. For example, Power Automate can filter its email trigger by sender, subject, recipient or attachment presence. Other platforms have different features, so use their own documentation. Route obvious cases and send anything that does not match to a person.

## 2. Use AI for variable language

“Where is my parcel?”, “tracking has not moved” and “it was due yesterday” may describe the same issue. AI can suggest a category, create a neutral summary and extract a possible order reference. Keep the task narrow and require a fixed output structure. Treat every field as a suggestion: the model may misread a message or invent a reference.

## 3. Keep consequential actions with a person

The AI should not send email, delete messages, approve refunds, change orders or update customer records. A staff member checks the original message and decides what happens next. Email is untrusted input: an attacker could include instructions designed to manipulate the model. OWASP identifies indirect prompt injection and recommends least privilege, output validation and human approval for high-risk actions.

## 4. Design for failure

- Detect duplicate messages using a stable identifier where available.

- Validate required fields and allowed categories before using AI output.

- Send ambiguous or malformed results to human review.

- Keep a minimal log of message reference, stage, outcome and error — not the full email body.

- Provide failure alerts and a manual fallback; test retries to avoid duplicate actions.

## 5. Minimise data and measure results

Start with synthetic messages. If a real pilot is considered, check whether the model needs the full email or only a redacted extract. Review provider terms, retention, model-training settings, access controls, processing locations and contractual arrangements. The GDPR requires personal data to be limited to what is necessary for its purpose.

Measure the existing sorting time, misroutes, delays and exceptions before testing. Then track correction rates, review time, failures and total operating cost. If checking takes longer than the work saved, simplify or remove the AI step.

**The takeaway:** use rules for predictable routing, AI for narrow language tasks and people for consequential decisions. Keep permissions small, test failure paths and start with synthetic data.

### Further reading

- [Microsoft Learn — Email trigger filters](https://learn.microsoft.com/en-us/power-automate/email-triggers).

- [Microsoft Learn — Troubleshoot flow failures](https://learn.microsoft.com/en-us/power-automate/fix-flow-failures).

- [OWASP — Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/).

- [GDPR, Article 5](https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng) — data minimisation.

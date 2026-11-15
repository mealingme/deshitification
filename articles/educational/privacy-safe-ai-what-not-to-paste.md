---
title: "Privacy-Safe AI: What Not to Paste into a Chatbot"
wordpress_post_id: 50
wordpress_status: draft
wordpress_url: https://deshitification.wordpress.com/?p=50
last_exported: 2026-11-15
---

# Privacy-Safe AI: What Not to Paste into a Chatbot

AI assistants can be useful, but a chatbot is not automatically an approved place for business information. Before pasting anything, check what the data contains, which service and account you are using, and whether that use is authorised.

### A safer data path

#### CLASSIFY

Public, internal, confidential or restricted?

#### MINIMISE

Remove fields the task does not need.

#### CONTROL

Use only an approved service and access level.

## What should stay out of unapproved tools?

- Passwords, recovery codes, API keys, private keys and access tokens.

- Customer or employee records, addresses, order histories and support conversations.

- Bank or payment details, identity documents and sensitive personal data.

- Contracts, supplier prices, margins, unreleased plans and confidential negotiations.

- Source code, system diagrams, vulnerabilities and internal security settings.

These are conservative rules for public or unapproved tools. An enterprise service may offer different controls, but check the exact plan, account and configuration first.

## Removing names may not anonymise data

Replacing a name with “Customer A” may not be enough. An order number, precise date, location or unusual event can identify someone when combined with other details. Prefer synthetic examples. If real information is necessary, involve the data owner and privacy or security contact.

## Check the service and settings

Establish whether prompts and files are used to improve models, how long they are retained, who can access conversation history, where data is processed, which subprocessors are involved and whether your organisation has approved the intended use. Also check sharing, administrator controls and what happens when a project or employee leaves.

## Give the AI less data and less power

Share only the extract needed for the task. Remove unnecessary fields and restrict connected tools to the minimum permissions required. Treat external documents and emails as untrusted content: they may contain malicious instructions. Do not let the model decide for itself which information it may reveal or which actions it may take.

## The five-minute check

- Is this exact use approved?

- Can I use synthetic data or remove unnecessary details?

- Have I checked the actual service, plan and retention settings?

- Could the content expose credentials, personal data or commercial secrets?

- Will a person check the output before it is used?

If you cannot answer these questions, do not paste the material yet. Ask the data owner. A short delay is cheaper than an avoidable disclosure.

### Further reading

- [GDPR — Article 5, data protection principles](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679)

- [GDPR — Article 32, security of processing](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679#d1e3050-1-1)

- [OWASP — Sensitive Information Disclosure](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/)

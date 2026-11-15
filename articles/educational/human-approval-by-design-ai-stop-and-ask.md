---
title: "Human Approval by Design: Where AI Should Stop and Ask"
wordpress_post_id: 203
wordpress_status: draft
wordpress_url: https://deshitification.wordpress.com/?p=203
last_exported: 2026-11-15
---

# Human Approval by Design: Where AI Should Stop and Ask

**THE PRACTICAL AI SERIES · CONTROL**

Human approval is not a box to tick at the end of an AI project. It is a control that should appear exactly where an automated mistake could cause real harm — and it must give the reviewer enough information and authority to stop the action.

## A simple approval path

#### 1 · PREPARE

AI drafts or recommends an action.

#### 2 · CHECK

A person sees the source, context and consequences.

#### 3 · DECIDE

Approve, edit, reject or escalate.

The system executes only the approved action, within the reviewer's permissions.

## Where should approval sit?

Routine, reversible actions can often run automatically after testing. Pause for human approval when an action is difficult to reverse, affects a person, moves money, changes important records, sends an external message or exposes sensitive information.

For example, an AI assistant may classify a supplier email and prepare a draft reply. It should not independently change bank details, approve an invoice or send a payment instruction. The approval screen should show the original message, the proposed change, the destination and any supporting evidence — not merely an “Approve” button.

## Three controls that matter

- **Limit permissions.** Give the AI only the access required for its task. Read-only access is preferable where it is sufficient.

- **Validate the action.** Check the target, values and user's authority in the application before execution. Do not rely on the model to police itself.

- **Keep a useful record.** Record what was proposed, what the reviewer saw, the decision, who approved it and what the system executed. Avoid logging unnecessary sensitive content.

## Approval must be meaningful

People cannot provide effective oversight if they are asked to approve hundreds of low-value alerts, see no source evidence or are unable to reject an action. Design for manageable queues, clear reasons for escalation, enough time to review and a safe manual fallback.

External emails, payments, deleting records, changing access rights and other consequential actions deserve action-specific approval. A blanket approval at the start of a session is not the same as reviewing the actual action and its target.

## Test the failure path

Test what happens when the AI is wrong, the data is incomplete, the reviewer is unavailable or a document contains malicious instructions. OWASP identifies prompt injection and excessive agency as important LLM application risks; its guidance recommends least privilege and human approval for high-risk actions. [OWASP: Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) · [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/).

The [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) is a broader resource for identifying, assessing and managing AI risks throughout a system's lifecycle.

**The principle:** let AI prepare and assist; keep consequential authority with an accountable person. If nobody can explain, challenge or stop the action, the approval control is only theatre.

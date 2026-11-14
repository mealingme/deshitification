# Automation Readiness Checklist

Use this before proposing automation for any workflow.

## Process definition
- [ ] Start and end points are agreed.
- [ ] Normal and exception paths are documented.
- [ ] Process owner and decision rights are clear.
- [ ] Manual workarounds are understood.

## Evidence and measurement
- [ ] Baseline volume and cycle time are measured.
- [ ] Error, rework and exception rates are known.
- [ ] Data definitions and timestamp quality are checked.
- [ ] Benefits can be measured after implementation.

## Technology choice
- [ ] Rules are sufficient where decisions are deterministic.
- [ ] RPA is justified for the interface task.
- [ ] AI is used only where probabilistic interpretation adds value.
- [ ] Integration and maintenance costs are included.

## Controls and economics
- [ ] Human approval exists for consequential decisions.
- [ ] Access is least-privilege; failures, retries and audit trails are designed.
- [ ] A rollback or manual fallback exists.
- [ ] Privacy, security and retention have been reviewed.
- [ ] Build, licensing, operation, support and exception costs are included.
- [ ] A small pilot has measurable exit criteria.

**Decision:** Do not automate until the process is understood, measurable and controlled.

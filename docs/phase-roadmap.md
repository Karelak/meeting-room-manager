# Delivery Roadmap

This roadmap captures the phased plan for delivering the Meeting Room Manager platform, including goals, key deliverables, owners, and success checkpoints per phase.

## Phase 0 – Discovery & Foundations (Week 0–1)
- **Goals**: finalise requirements, confirm security posture, unblock hardware and SMTP dependencies, align stakeholders.
- **Key Deliverables**:
  - Signed-off requirements pack (features, constraints, success metrics).
  - DPIA/security assessment draft.
  - Hardware shortlist for NFC room terminals + procurement request.
  - Initial component map, ERD, and design-system tokens.
- **Owners**: Product lead, security team, IT infrastructure.
- **Exit Criteria**: Stakeholder approval, risks logged with mitigations, backlog prioritised for Phase 1.

## Phase 1 – Core Platform (Week 2–5)
- **Goals**: ship functional MVP covering auth, dashboard, room catalogue, booking CRUD, and base UI.
- **Key Deliverables**:
  - Flask backend with RBAC auth and session management.
  - Booking service (conflict detection, buffer enforcement, validation).
  - Dashboard + room listing templates, responsive base styling.
  - Initial SQLite migrations, seed data, CI (lint + tests).
- **Owners**: Backend + frontend engineers, QA for smoke tests.
- **Exit Criteria**: Internal demo of end-to-end booking flow, <500 ms average response locally, unit tests ≥70 % coverage on services.

## Phase 2 – Advanced Workflows (Week 6–9)
- **Goals**: complete administrative tooling, notifications, support desk, room terminals, reporting, and email hooks.
- **Key Deliverables**:
  - Admin console (rooms/users/overrides/stats) + audit logging.
  - Notification center + Mailjet SMTP integration.
  - Support ticket CRUD + assignment workflows.
  - Room terminal endpoints with NFC/PIN check-in prototype.
  - Read-only iCal feeds, CSV import/export, utilisation reports.
- **Owners**: Full stack team, infra for SMTP, hardware pilot squad.
- **Exit Criteria**: Feature-complete system ready for UAT, terminal pilot in 1–2 rooms, documentation draft for training.

## Phase 3 – Hardening & Launch (Week 10–12)
- **Goals**: productionise the stack, execute UAT, train users, plan/direct changeover, and deploy.
- **Key Deliverables**:
  - Performance, security, and accessibility test suites (Locust, OWASP, axe).
  - Deployment automation (GitHub Actions → staging/prod), monitoring and alerting setup.
  - UAT sign-off, training assets (videos, PDFs, FAQ), comms plan.
  - Data migration scripts, cutover checklist, DR/backup plan.
- **Owners**: QA, DevOps, training & comms team, product owner.
- **Exit Criteria**: Successful go-live, admin/playbook sign-off, post-launch support rota defined.

## Cross-Cutting Streams
- **Compliance & Security**: DPIA updates, encryption, data retention job, penetration tests each phase.
- **Change Management**: Stakeholder updates, feedback loops, pilot feedback incorporated in backlog refinement.
- **Observability**: Logging, metrics, alerting stories embedded from Phase 1 onward to avoid retrofitting.

## Post-Go-Live Follow-Up
- Monitor KPIs (self-service rate, double-booking incidents, admin time saved) for 60 days.
- Schedule post-implementation review to capture lessons and backlog future enhancements (e.g., AD SSO, Outlook sync).

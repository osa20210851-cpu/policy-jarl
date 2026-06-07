
# 🛡️ Policy-Jarl: A Policy RBAC Guard for Actionable AIs
**A Graduation Project Implementation for an AuthZ/AuthN Guardrail for an AI DB Agent**

---

## 📖 Project Overview
Policy-Jarl is a specialized security middleware architecture designed to address the growing "governance gap" in autonomous AI agents. As AI agents gain the capability to interact with internal tools, databases, and sensitive infrastructure, the need for deterministic, role-based, and stateful security controls becomes critical.

---

## 🛠️ The Technology Stack
The framework is built using a "Best-of-Breed" security stack to ensure isolation and performance:

- **Policy Engine:** [Open Policy Agent (OPA)](https://www.openpolicyagent.org/) using Rego for deterministic authorization logic.
- **Proxy/Interceptor:** [FastAPI](https://fastapi.tiangolo.com/) (Python) providing a high-performance, asynchronous security gateway.
- **Identity Provider:** [Telegram Bot API](https://core.telegram.org/bots) serving as a trusted, device-linked IdP.
- **Memory Layer:** [Redis](https://redis.io/) for stateful context tracking and session-bound JWT storage.
- **Audit & Observability:** [ELK Stack](https://www.elastic.co/what-is/elk-stack) (Elasticsearch, Logstash, Kibana) for real-time forensic logging and HITL (Human-in-the-Loop) dashboarding.
- **AI Engine:** [HKUDS Nanobot](https://github.com/HKUDS/nanobot) integrated with [Google Gemini 3.1](https://ai.google.dev/gemini-api).

---

## 📐 Design Artifacts

### 1. External Architectural Design
The architecture follows a modular "Sidecar" and "Proxy" approach, ensuring the security judge (OPA) is decoupled from the AI executor.

<img width="4350" height="2951" alt="Grad Prj - With(out) Abstract" src="https://github.com/user-attachments/assets/17c7ce76-b7b4-43f2-974a-53886b08c649" />

### 2. Internal Architectural Design
From the intenal 

<img width="5213" height="2799" alt="Grad Prj - Abstract (Analogy)" src="https://github.com/user-attachments/assets/84689599-515a-4c6d-85a7-1874d10fa537" />

### 3. Deployment Diagram
Implemented as a containerized microservices architecture using Docker-Compose for environment isolation.

<img width="5138" height="2912" alt="Grad Prj - Deployment" src="https://github.com/user-attachments/assets/a99e7386-7626-4d2a-8d15-ac45b50bccb2" />

### 4. Activity Diagram (The Security Loop)
This diagram illustrates the lifecycle of a request: from Inbound Signal Generation to Outbound DLP (Data Leakage Prevention) inspection.

<img width="2816" height="2799" alt="Grad Prj - Activity" src="https://github.com/user-attachments/assets/87ff2ce2-94b9-4c55-af92-549372ba75c2" />

### 5. Use Case Diagram
Demonstrates the distinct roles of the **User (Intern)**, **Administrator**, and **Security Auditor (HITL)** within the framework.

<img width="2057" height="2488" alt="Grad Prj - Usecase" src="https://github.com/user-attachments/assets/90cb0bd4-97a9-45d5-9feb-03d6adca9a03" />


---

## 🚀 Key Research Milestones
- [x] **Cryptographic Identity:** Implementation of JWT-signed session tokens natively verified by OPA.
- [x] **Stateful Guardrails:** Real-time tracking of security alerts to prevent "Repeat Offender" attacks.
- [x] **Actionable SOC:** Transitioning from passive logs to an active task-management dashboard in Kibana.
- [x] **Universal Proxy:** A vendor-agnostic architecture capable of securing any OpenAI-compatible agent.

---

## 📜 Academic Context
This project is submitted as a graduation requirement. It serves as a reference implementation for stateful, role-based access control in agentic AI ecosystems.

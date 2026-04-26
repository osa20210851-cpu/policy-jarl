# 🛡️ Policy-Jarl: A Policy Guardian Framework
**A Graduation Project Implementation for Stateful AI Security Guardrails**

## 📖 Project Overview
Policy-Jarl is a specialized security middleware architecture designed to address the growing "governance gap" in autonomous AI agents. As AI agents gain the capability to interact with internal tools, databases, and sensitive infrastructure, the need for deterministic, role-based, and stateful security controls becomes critical.

This project implements the **"Guardian Agent" pattern**, where an independent, cryptographically-secure proxy intercepts all interactions between users and an LLM-powered agent.

---

## 🛠️ The Technology Stack
The framework is built using a "Best-of-Breed" security stack to ensure isolation and performance:

- **Policy Engine:** [Open Policy Agent (OPA)](https://www.openpolicyagent.org/) using Rego for deterministic authorization logic.
- **Proxy/Interceptor:** [FastAPI](https://fastapi.tiangolo.com/) (Python) providing a high-performance, asynchronous security gateway.
- **Identity Provider:** [Telegram Bot API](https://core.telegram.org/bots) serving as a trusted, device-linked IdP.
- **Memory Layer:** [Redis](https://redis.io/) for stateful context tracking and session-bound JWT storage.
- **Audit & Observability:** [ELK Stack](https://www.elastic.co/what-is/elk-stack) (Elasticsearch, Logstash, Kibana) for real-time forensic logging and HITL (Human-in-the-Loop) dashboarding.
- **AI Engine:** [HKUDS Nanobot](https://github.com/HKUDS/nanobot) integrated with [Google Gemini 1.5/2.5](https://ai.google.dev/gemini-api).

---

## 📐 Design Artifacts

### 1. Architectural Design
The architecture follows a modular "Sidecar" and "Proxy" approach, ensuring the security judge (OPA) is decoupled from the AI executor.

*(Insert LucidChart: Architectural Design Diagram)*

### 2. Deployment Diagram
Implemented as a containerized microservices architecture using Docker-Compose for environment isolation.

*(Insert LucidChart: Deployment Diagram)*

### 3. Activity Diagram (The Security Loop)
This diagram illustrates the lifecycle of a request: from Inbound Signal Generation to Outbound DLP (Data Leakage Prevention) inspection.

*(Insert LucidChart: Activity/Sequence Diagram)*

### 4. Use Case Diagram
Demonstrates the distinct roles of the **User (Intern)**, **Administrator**, and **Security Auditor (HITL)** within the framework.

*(Insert LucidChart: Use Case Diagram)*

---

## 🚀 Key Research Milestones
- [x] **Cryptographic Identity:** Implementation of JWT-signed session tokens natively verified by OPA.
- [x] **Stateful Guardrails:** Real-time tracking of security alerts to prevent "Repeat Offender" attacks.
- [x] **Actionable SOC:** Transitioning from passive logs to an active task-management dashboard in Kibana.
- [x] **Universal Proxy:** A vendor-agnostic architecture capable of securing any OpenAI-compatible agent.

---

## 📜 Academic Context
This project is submitted as a graduation requirement. It serves as a reference implementation for stateful, role-based access control in agentic AI ecosystems.

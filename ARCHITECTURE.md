# CypherDAO Architecture Documentation

## 1. Overview

CypherDAO is a decentralized cybersecurity automation suite designed to provide automated security measures through integration with decentralized governance, AI-guided responses, and real-time alert systems. The architecture is based on a microservices approach, leveraging a combination of blockchain technologies, web applications, and security tools.

## 2. High-Level Architecture

The CypherDAO architecture consists of the following core components:

- **CypherNode** (Core Backend)
- **Ghost Barrier** (Frontend UI)
- **CypherScan** (Vulnerability Scanners)
- **CypherProof** (Audit Logs)
- **CypherCopilot** (AI Assistant)
- **CypherAgents** (IDS Stream)
- **CypherDAO** (On-chain Governance)
- **CypherAGS** (Air-Gapped System Deployment)

### Diagram
(Insert a diagram of the architecture here, depicting how the components are connected)

## 3. Core Components

### 3.1. **CypherNode**
The **CypherNode** serves as the core backend, orchestrating the communication between various services and components. It consists of microservices bundled together in a Docker Compose stack.

- **Services:**
  - Flask API
  - Postgres Database
  - IDS (Intrusion Detection System)
  - Vulnerability Scanners (ZAP, Nmap)

- **Protocols:**
  - TLS/SSL for secure communication
  - JWT for authentication
  - Traefik reverse-proxy for routing and service discovery

### 3.2. **Ghost Barrier**
The **Ghost Barrier** provides a unified frontend UI to interact with CypherDAO's functionalities. It is built with React and Tailwind CSS for styling. The UI interacts with the backend using WebSockets for live updates on vulnerability scanning, alerts, and governance decisions.

- **Pages**: Overview, Vulnerabilities, Alerts, DAO Votes, Audit Logs, Copilot

- **Technologies:**
  - React (Frontend framework)
  - Tailwind CSS (Styling)
  - WebSocket via Socket.IO for live updates

### 3.3. **CypherScan**
**CypherScan** provides a suite of security scanners for web vulnerabilities and network scanning. It integrates with external scanning tools such as OWASP ZAP, Nmap, and DefectDojo.

- **Features:**
  - Web Application Scanning (via ZAP)
  - Network Scanning (via Nmap)
  - CVE Mapping (via Vulners API)
  - Automated compliance reporting (GDPR, PCI, ISO27001)

- **Components:**
  - **ZAP Wrapper**: Automates OWASP ZAP scans
  - **Nmap Wrapper**: Automates network scans
  - **CVE Mapper**: Maps vulnerabilities to CVEs

### 3.4. **CypherProof**
**CypherProof** is a tamper-proof logging system that stores audit logs and scanning results securely. It uses SHA256 hashing to ensure integrity and can optionally pin logs to IPFS for decentralized storage.

- **Technologies:**
  - **SHA256** for event hashing
  - **LevelDB** for local storage
  - **IPFS** for decentralized log storage (optional)

- **Endpoint:** `/api/audit?from=...&to=...` for fetching logs

### 3.5. **CypherCopilot**
**CypherCopilot** is an AI-powered assistant for security operations. It leverages GPT-4 or Claude API for summarizing scan results, advising on compliance, and providing assistance in security operations.

- **Roles:**
  - SecOps Advisor
  - Compliance Lawyer
  - Red-Team Mentor

- **Features:**
  - Markdown-based responses
  - Template-driven prompts for AI interaction

### 3.6. **CypherAgents**
**CypherAgents** is a real-time alert system that integrates IDS (Suricata) and mock alerts for security events. Alerts are posted to a central endpoint for processing.

- **Technologies:**
  - **Suricata IDS** for offline/PCAP replay mode
  - **Mock Alerts** via Python scripts

- **Endpoint:** `/api/alerts` to receive real-time alerts

### 3.7. **CypherDAO (On-chain Governance)**
The **CypherDAO** is responsible for the decentralized governance of CypherDAO. It allows stakeholders to vote on security actions, such as initiating scans, deploying honeypots, or blocklisting IPs.

- **Technologies:**
  - **Aragon OS** for DAO management
  - **$CYG Token** (ERC20) for governance participation
  - **Smart Contract:** CYGToken.sol (ERC20, 1B supply)

- **Features:**
  - DAO proposals and voting
  - Automated triggering of security actions (e.g., scan, blocklist IP)

### 3.8. **CypherAGS (Air-Gapped Installer)**
**CypherAGS** enables offline installation and deployment of the CypherDAO MVP. It leverages Zarf for packaging and air-gapped installations, with optional GPT-J integration for offline AI inference.

- **Technologies:**
  - **Zarf** for offline packaging
  - **CLI** for installation
  - **GPT-J** for offline AI functionality (optional)

## 4. System Interaction

### Backend Communication
- **Flask** API acts as the central service orchestrator. It interacts with the database (Postgres) and various microservices like the IDS, Scanners, and CypherProof.
- **Traefik** is used as a reverse proxy to route incoming requests to appropriate backend services.

### Frontend Communication
- **Ghost Barrier (React + Tailwind)** communicates with the backend via WebSocket for real-time updates.
- The frontend queries various APIs to display vulnerability reports, audit logs, and governance decisions.

### Decentralized Governance
- Proposals and governance actions are managed via **CypherDAO** (on-chain via Aragon) and are used to automate security actions.

### Real-time Alerts and Monitoring
- **CypherAgents** handles real-time security alerts and communicates with the Flask API to update the central database.

## 5. Technologies Used

- **Backend**: Flask, Postgres, Traefik, Docker
- **Frontend**: React, Tailwind CSS, WebSocket (Socket.IO)
- **Security**: ZAP, Nmap, Suricata, IPFS, SHA256
- **Governance**: Aragon, Ethereum (Sepolia), ERC20 Tokens
- **AI**: GPT-4, Claude API, GPT-J
- **Deployment**: Zarf, Docker Compose, Kubernetes (optional)


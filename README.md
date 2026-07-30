
## National EWS Data Routing & Verification Engine 🛡️

An unbribable, real-time data orchestration platform designed to automate eligibility validation for India's **Economically Weaker Sections (EWS)** quota system. This repository replaces vulnerable, manual, paper-based income certificate submissions with automated, cross-registry telemetry and zero-knowledge data pipelines.

**Created by:** Srinivasta

**Application Framework:** [Streamlit Web Architecture](https://ews-data-routing-engine-njoacu4juefmksb8ynpcew.streamlit.app/)

---

## 🚀 System Architecture Overview

The platform operates across a decentralized infrastructure model designed to systematically combat wealth-evasion strategies (such as digital cash-flow obfuscation or hiding real estate assets behind undivided ancestral lines):

1. **Input Registry Mesh (Zero-Knowledge Ingestion):** Accepts an applicant's core credentials (PAN and Aadhaar) to tokenise identity, sending a binary verification request downstream without traveling raw sensitive data.
2. **Cross-Database Telemetry Bus:** Queries live synthetic endpoints mirroring the Income Tax Department (CBDT), Banking aggregation systems (UPI velocity logs), and State Land registries (*Bhulekh*).
3. **Ancestral Inheritance Mapping Logic:** Programmatically breaks down undivided generational land assets. It calculates an applicant’s virtual inherited share from deceased or living grandparents to counter structural asset loopholes.
4. **Dynamic Purchasing Power Parity (PPP) Tiering:** Standardizes structural financial thresholds by applying custom multi-weights across Tier-1, Tier-2, and Tier-3 geographic classifications.

---

## 🛠️ Repository File Layout

```text
EWS-Data-Routing-Engine/
│
├── .github/
│   └── workflows/
│       └── streamlit-ci.yml    # Continuous Integration testing pipeline
│
├── app.py                      # Production Streamlit UI Dashboard Interface
├── engine.py                   # Algorithmic decision and risk scoring matrix
├── mock_data.py                # Synthetic profile pipeline data generator (1,000 logs)
├── test_engine.py              # Automated Unit-Test suite for mathematical logic
├── requirements.txt            # Python environment third-party dependencies
└── README.md                   # System documentation (This File)
```

---

## 📥 Local Installation & Boot Routine

Follow these explicit terminal steps to initialize, test, and host this architecture locally:

### 1. Clone and Prepare the Workspace
```bash
# Initialize a local directory and move into it
mkdir EWS-Data-Routing-Engine && cd EWS-Data-Routing-Engine

# Pull down dependencies
pip install -r requirements.txt
```

### 2. Generate the Synthetic Registry Logs
Run the mock generation module to create your simulated local database pool of 1,000 applicant profiles:
```bash
python mock_data.py
```

### 3. Run Automated Validation Checks
Execute the unit testing script to verify that purchasing-parity rules and grandfather asset calculation logic pass constraints:
```bash
python -m unittest test_engine.py
```

### 4. Boot Up the Web App Interface
Launch your responsive Streamlit application directly into your local browser window:
```bash
streamlit run app.py
```

---

## 📊 Core Operational Interface Modes

The interface provides three operational views via the **System Controls** panel on the left sidebar:

* **Single Applicant Audit:** Simulates real-time manual checks. It pulls individual registry payloads, assesses risk scores based on luxury spending proxies (utility metrics vs reported income), and generates clear system warning alerts if the statutory 5-acre agricultural ceiling is breached.
* **1,000 Profile Database Analytics:** Processes bulk database logs into interactive, colored Scatter Plots and Histograms built via Plotly. This mode segregates records into **In EWS** and **Above EWS** categories with dedicated download buttons.
* **Upload Application File (.CSV):** Allows an administrator to upload any custom batch template. It processes rows on the fly and integrates an **On-Demand EWS Certificate Generator** to compile official, formatted PDF verification summaries.

---

## 🔐 Compliance & Security Blueprints

* **Data Integrity:** Real-time data synchronization with bank aggregators bypasses locally forged, paper-based documents.
* **Algorithmic Parity:** Removes political or bureaucratic influence by routing decisions purely through deterministic code logic.
* **PDF Auditing:** Generated reports feature a clear structural matrix rendering metadata, calculated effective land holding metrics, and systemic assessment scores for audit-ready documentation.
"""


> ⚠️ **IMPORTANT COPYRIGHT NOTICE**
> 
> **All Rights Reserved © 2026 T A Srinivas.**
> This repository is strictly for portfolio viewing purposes. **DO NOT COPY, CLONE, OR REDISTRIBUTE** this code. Stolen copies or unauthorized forks will be reported immediately for a GitHub copyright takedown.

* **Lead Architect & Developer:** [Srinivasta](https://github.com/SRINIVASTA)

### 🌐 Let’s Connect

- [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/srinivas-t-a-557637119/)  
- [![Kaggle](https://img.shields.io/badge/Kaggle-20BEFF?style=for-the-badge&logo=kaggle&logoColor=white)](https://www.kaggle.com/srinivasta)  
- [![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:tasrinivass@gmail.com)  
- [![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/srinivasta)
- [![Website](https://img.shields.io/badge/Website-000000?style=for-the-badge&logo=website&logoColor=white)](https://srinivasta/github.io)



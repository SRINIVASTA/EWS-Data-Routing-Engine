### National EWS Data Routing & Verification Engine 🛡️

An unbribable, real-time data orchestration platform designed to automate eligibility validation for India's **Economically Weaker Sections (EWS)** quota system. This repository replaces vulnerable, manual, paper-based income certificate submissions with automated, cross-registry telemetry and zero-knowledge data pipelines. 

**Created by:** Srinivasa
**Application Framework:** Streamlit Web Architecture 

### 🚀 System Architecture Overview

The platform operates across a decentralized infrastructure model designed to systematically combat wealth-evasion strategies (such as digital cash-flow obfuscation or hiding real estate assets behind undivided ancestral lines): 

1. **Input Registry Mesh (Zero-Knowledge Ingestion):** Accepts an applicant's core credentials (PAN and Aadhaar) to tokenise identity, sending a binary verification request downstream without traveling raw sensitive data.
2. **Cross-Database Telemetry Bus:** Queries live synthetic endpoints mirroring the Income Tax Department (CBDT), Banking aggregation systems (UPI velocity logs), and State Land registries (*Bhulekh*).
3. **Ancestral Inheritance Mapping Logic:** Programmatically breaks down undivided generational land assets. It calculates an applicant’s virtual inherited share from deceased or living grandparents to counter structural asset loopholes.
4. **Dynamic Purchasing Power Parity (PPP) Tiering:** Standardizes structural financial thresholds by applying custom multi-weights across Tier-1, Tier-2, and Tier-3 geographic classifications.

### 🛠️ Repository File Layout

text

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

Use code with caution.

### 📥 Local Installation & Boot Routine

Follow these explicit terminal steps to initialize, test, and host this architecture locally: 

### 1. Clone and Prepare the Workspace

bash

# Initialize a local directory and move into it
mkdir EWS-Data-Routing-Engine && cd EWS-Data-Routing-Engine

# Pull down dependencies
pip install -r requirements.txt

Use code with caution.

### 2. Generate the Synthetic Registry Logs

Run the mock generation module to create your simulated local database pool of 1,000 applicant profiles: 

bash

python mock_data.py

Use code with caution.

### 3. Run Automated Validation Checks

Execute the unit testing script to verify that purchasing-parity rules and grandfather asset calculation logic pass constraints: 

bash

python -m unittest test_engine.py

Use code with caution.

### 4. Boot Up the Web App Interface

Launch your responsive Streamlit application directly into your local browser window: 

bash

streamlit run app.py

Use code with caution.

### 📊 Core Operational Interface Modes

The interface provides three operational views via the **System Controls** panel on the left sidebar: 

* **Single Applicant Audit:** Simulates real-time manual checks. It pulls individual registry payloads, assesses risk scores based on luxury spending proxies (utility metrics vs reported income), and generates clear system warning alerts if the statutory 5-acre agricultural ceiling is breached.
* **1,000 Profile Database Analytics:** Processes bulk database logs into interactive, colored Scatter Plots and Histograms built via Plotly. This mode segregates records into **In EWS** and **Above EWS** categories with dedicated download buttons.
* **Upload Application File (.CSV):** Allows an administrator to upload any custom batch template. It processes rows on the fly and integrates an **On-Demand EWS Certificate Generator** to compile official, formatted PDF verification summaries.

### 🔐 Compliance & Security Blueprints

* **Data Integrity:** Real-time data synchronization with bank aggregators bypasses locally forged, paper-based documents.
* **Algorithmic Parity:** Removes political or bureaucratic influence by routing decisions purely through deterministic code logic.
* **PDF Auditing:** Generated reports feature a clear structural matrix rendering metadata, calculated effective land holding metrics, and systemic assessment scores for audit-ready documentation.

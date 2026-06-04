# ResumeIQ — AI Resume Analyzer 🚀

ResumeIQ is an open-source, production-grade SaaS pipeline engineered to dismantle the ambiguity behind corporate Applicant Tracking Systems (ATS). By inspecting your unstructured PDF profiles against variable job specifications, ResumeIQ delivers deep algorithmic compatibility grading, metric-driven statement diagnostics, and real-time semantic caching.

---

## 📦 What It Does
* **Automated Heuristic Evaluation:** Instantly evaluates engineering records to spit back explicit keyword matrices and core compatibility indexing percentages.
* **Deterministic Structured Extraction:** Guarantees structural output parsing directly out of deep contextual models via native Pydantic enforcement layers.
* **Granular Context-Aware Corrections:** Pinpoints non-quantifiable experience descriptors and programmatically outputs optimized, impact-driven rewrites.

---

## 🛠️ Deep Tech Stack
* **Frontend Runtime:** Pure Vanilla Static Architecture (ES6 JavaScript / Custom Flex-Grid CSS3 Engine) hosted over global Edge Networks on **Vercel CDN**.
* **API Microservice:** Asynchronous **FastAPI (Python 3.11+)** contextually isolated on **Render**.
* **Relational Storage:** Serverless transactional **PostgreSQL** provisioned over compute-decoupled architectures on **Neon Database**.
* **Caching & Performance Optimization:** Low-latency storage instance utilizing **Upstash Redis** for real-time query deduplication.
* **Upstream Inference Engine:** Modern structural generation utilizing the official **Google GenAI SDK** targeting **Gemini 2.5 Flash**.

---

## 🚀 Live Environment Access
* **Application URL:** [https://ats-resume-checker-gamma.vercel.app](https://ats-resume-checker-gamma.vercel.app)
* **Interactive API Playground:** [https://ats-resume-checker-00jy.onrender.com/docs](https://ats-resume-checker-00jy.onrender.com/docs)

---

## 📊 Infrastructure Architecture Flow
```text
[ Client Web UI ] ──( Multipart Form Upload )──> [ FastAPI Server on Render ]
                                                           │
                      ┌────────────────────────────────────┴───────────────────────────────────┐
                      ▼ (Check Cache Fingerprint)                                              ▼ (If Cache Miss: Extract Binary Text)
           [ Upstash Redis Memory ]                                                    [ Google Gemini AI Engine ]
                      │                                                                        │
        (Return Cached Structural JSON)                                            (Emit Deterministic JSON Object)
                      │                                                                        │
                      │                                                                        ▼ (Hydrate State Tables)
                      └────────────────────────◄─────────────────────────────────────── [ Neon PostgreSQL DB ]
🛠️ Local Development
Prerequisites
Python 3.11+

A Google Gemini AI API key.

Upstash Redis & Neon PostgreSQL database URLs.

Quick Start
Clone the repository:

Bash
git clone [https://github.com/Faizan-Khan0007/ats-resume-checker.git](https://github.com/Faizan-Khan0007/ats-resume-checker.git)
cd ats-resume-checker
Create and activate a virtual environment:

Bash
python -m venv venv

# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
Install dependencies:

Bash
pip install -r requirements.txt
Create a .env file in the root directory and add your keys:

Code snippet
DATABASE_URL=your_neon_postgres_url
REDIS_URL=your_upstash_redis_url
GEMINI_API_KEY=your_gemini_api_key
Start the server:

Bash
uvicorn main:app --reload

The FastAPI backend will instantly be available at http://localhost:8000.
Access the auto-generated Swagger UI at http://localhost:8000/docs.

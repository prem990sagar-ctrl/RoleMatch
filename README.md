# RoleMatch AI: Resume-Based Career Role Recommender

> **A Complete Third-Year AI & Machine Learning College Mini Project**  
> *Developed with Python, Streamlit, PyPDF, and Scikit-Learn*

---

## 1. Project Title
**RoleMatch AI: An Explainable Machine Learning Career Role Recommender System Based on Resume Skill Extraction and Semantic Matching**

---

## 2. Abstract
Finding the most suitable job role based on an individual's resume is a critical task in modern career planning and technical recruiting. Traditional keyword search systems frequently fail because they cannot capture semantic context, handle skill abbreviations (such as *ML* for *Machine Learning* or *JS* for *JavaScript*), or balance overall textual relevance with specific skill coverage. 

**RoleMatch AI** is a lightweight, explainable, and privacy-preserving recommendation application designed for academic evaluation. Built using Python, Streamlit, PyPDF, and Scikit-learn, the application parses candidate resumes directly from standard PDF documents, extracts technical skills against a curated dataset vocabulary, and computes ranked job recommendations from a verified real-world dataset of 1,431 roles and postings across Computer Science, Information Technology, Finance, Human Resources, Sales, and Business Development. The recommendation engine combines **TF-IDF vectorization with Cosine Similarity (50%)** and a **Skill Coverage heuristic (50%)** to generate an intuitive 0–100% match score with full transparency.

---

## 3. Problem Statement
Job seekers and engineering students often struggle to identify which industry roles best match their current technical skill sets and project experiences. Existing commercial hiring tools and Applicant Tracking Systems (ATS) present several barriers:
1. **Black-box algorithms**: Commercial platforms offer opaque match percentages without explaining how the score was derived or which specific skills were missing.
2. **Privacy concerns**: Cloud services store resumes and personal information on external servers.
3. **Complex, bloated architectures**: Many academic projects rely on heavy deep learning models, external paid API keys (such as OpenAI/GPT), or complex database setups that are brittle, costly, and difficult to set up locally for evaluation.

There is a distinct need for a simple, self-contained, and explainable role recommender that runs entirely on local machines using verified open-source datasets and foundational machine learning techniques.

---

## 4. Objectives
- **Objective 1**: Develop a clean, user-friendly Streamlit web interface allowing users to upload a single PDF resume (up to 10 MB).
- **Objective 2**: Safely extract resume text using `pypdf`, providing clear error handling for password-protected, scanned/image-only, or corrupted files.
- **Objective 3**: Implement a rule-based skill extractor with regex word-boundary precision and an alias dictionary (*e.g.*, *JS → JavaScript*, *ML → Machine Learning*, *K8s → Kubernetes*).
- **Objective 4**: Build an explainable recommendation model using Scikit-Learn's `TfidfVectorizer` and Cosine Similarity combined with role skill coverage.
- **Objective 5**: Display the top 5 matching job roles, highlighting both matched skills and missing role requirements with zero fabricated data.
- **Objective 6**: Ensure 100% reproducible execution offline on Windows PowerShell without requiring external API keys.

---

## 5. Proposed Solution
RoleMatch AI provides a streamlined, 4-step workflow:
1. **Resume Ingestion**: The candidate uploads a resume PDF. The app extracts text in-memory and validates readable content without permanently storing personal data.
2. **Skill Extraction & Alias Resolution**: The system scans the resume text against the genuine dataset vocabulary (over 5,700 technical skills) while mapping industry abbreviations to standard canonical forms.
3. **Dual-Factor Machine Learning Scoring**:
   - **Textual Semantic Similarity (50%)**: Converts resume text and job descriptions into TF-IDF n-gram vectors and computes Cosine Similarity.
   - **Skill Coverage (50%)**: Computes the percentage of required role skills that the candidate possesses.
4. **Transparent Results Display**: Presents the top 5 roles with detailed score breakdowns, verified company names (or explicit omission if not in the dataset), matched skill tags, and missing skill lists.

---

## 6. Technologies Used

| Technology / Library | Version | Purpose in Project |
| :--- | :--- | :--- |
| **Python** | 3.10+ / 3.13 | Core programming language for application logic and data pipelines. |
| **Streamlit** | $\ge$ 1.35.0 | Web application framework for modern, responsive UI presentation. |
| **PyPDF** | $\ge$ 4.0.0 | Robust PDF text extraction and error validation. |
| **Pandas** | $\ge$ 2.0.0 | Structured tabular data loading, filtering, and normalization. |
| **Scikit-learn** | $\ge$ 1.3.0 | TF-IDF feature extraction (`TfidfVectorizer`) and `cosine_similarity`. |
| **Pytest** | $\ge$ 8.0.0 | Comprehensive unit test suite for validation and academic verification. |
| **CSV & JSON** | Built-in | Lightweight, zero-dependency local storage for dataset and skill vocabulary. |

> **Design Choice**: Paid APIs, external vector databases, and deep neural networks were intentionally avoided to ensure the project remains lightweight, fully offline, and transparent for third-year engineering coursework.

---

## 7. Real-World Datasets Source & Attribution

The project utilizes genuine, non-fabricated job posting data obtained from Hugging Face Datasets:

### A. Computer Science Student & Tech Dataset
- **Curated IT & CS Roles**: [`DevilsLord/It_job_roles_skills_certifications`](https://huggingface.co/datasets/DevilsLord/It_job_roles_skills_certifications) (Top 207 IT/CS Job Roles & Skills Database).
- **Tech Job Postings**: [`jacob-hugging-face/job-descriptions`](https://huggingface.co/datasets/jacob-hugging-face/job-descriptions) (software engineering, developer, and data science job postings with real company names).
- **Target Audience**: Dedicated specifically for Computer Science, AIML, and IT students seeking roles such as *Full Stack Developer, Machine Learning Engineer, Python Developer, Data Scientist, Frontend Developer, Cloud/DevOps Engineer, and Entry-Level Software Engineer*.

### B. Cross-Domain Career Dataset
- **Dataset Identifier**: [`batuhanmtl/job-skill-set`](https://huggingface.co/datasets/batuhanmtl/job-skill-set)
- **Primary Source**: Kaggle's *[LinkedIn Job Postings](https://www.kaggle.com/datasets/arshkon/linkedin-job-postings)* by *Arshkon* with skills extracted via [RecAI](https://recai.tech).
- **Cross-Domain Categories**: Information Technology, Finance, Human Resources, Sales, Business Development.

### Summary Statistics:
- **Normalized Records**: 1,431 genuine job postings and roles stored in `data/job_skill_set.csv`.
- **Domain Categories (6)**:
  - `COMPUTER-SCIENCE`: 264 roles
  - `INFORMATION-TECHNOLOGY`: 240 jobs
  - `BUSINESS-DEVELOPMENT`: 239 jobs
  - `FINANCE`: 236 jobs
  - `SALES`: 232 jobs
  - `HR`: 220 jobs
- **Unique Extracted Skills**: 5,242 unique technical and domain skills (saved in `data/skills_vocabulary.json`).
- **Company Name Transparency**: Verified employer corporate names are retained when provided in source data; otherwise explicitly labeled as *"Standard reference role"* without inventing fake data.
- **License**: Consult the original Hugging Face / Kaggle dataset license terms (used here strictly for non-commercial educational demonstration).

---

## 8. System Architecture (Model-View-Controller)

RoleMatch AI implements a strict **Model-View-Controller (MVC)** architectural pattern to separate business logic, UI presentation, and application flow:

```
                                  [ User Browser ]
                                         │
                                         ▼
                     ┌───────────────────────────────────────┐
                     │           VIEW LAYER (views/)         │
                     │  - views/theme.py (Light/Dark themes) │
                     │  - views/components.py (UI widgets)   │
                     │  - views/main_view.py (Layouts)       │
                     └───────────────────▲───────────────────┘
                                         │
                           Presents UI   │ Sends Events
                                         │
                     ┌───────────────────┴───────────────────┐
                     │      CONTROLLER (controllers/)        │
                     │  - controllers/app_controller.py      │
                     │  - Orchestrates upload & ML workflow  │
                     │  - Manages session state & theme      │
                     └───────────────────┬───────────────────┘
                                         │
                           Invokes Model │ Returns Entities
                                         │
                     ┌───────────────────▼───────────────────┐
                     │          MODEL LAYER (models/)        │
                     │  - models/entities.py (Data Classes)  │
                     │  - models/pdf_model.py (PyPDF parser) │
                     │  - models/skill_model.py (Extraction) │
                     │  - models/recommender_model.py (TFIDF)│
                      │  - models/course_model.py (CareerPath)│
                     └───────────────────┬───────────────────┘
                                         │
                               Reads CSV │ Cached Loader
                                         ▼
                     ┌───────────────────────────────────────┐
                     │        DATA LAYER (data/)             │
                     │  - data/job_skill_set.csv             │
                     │  - data/skills_vocabulary.json        │
                      │  - data/courses.json                  │
                     └───────────────────────────────────────┘
```

---

## 9. Machine Learning Method & Mathematics

### A. TF-IDF (Term Frequency - Inverse Document Frequency)
TF-IDF reflects how important a word is to a job description or resume within the entire corpus of job postings.

1. **Term Frequency (TF)**:
   $$\text{TF}(t, d) = \frac{f_{t,d}}{\sum_{t' \in d} f_{t', d}}$$
   Where $f_{t,d}$ is the count of term $t$ in document $d$.

2. **Inverse Document Frequency (IDF)**:
   $$\text{IDF}(t, D) = \ln\left(\frac{1 + |D|}{1 + |\{d \in D : t \in d\}|}\right) + 1$$
   Where $|D|$ is the total number of job postings.

3. **TF-IDF Weight**:
   $$\text{TF-IDF}(t, d, D) = \text{TF}(t, d) \times \text{IDF}(t, D)$$

We utilize Scikit-learn's `TfidfVectorizer` with:
- `stop_words='english'` (removes common filler words like *and*, *the*, *with*).
- `ngram_range=(1, 2)` (captures single terms and key bigrams such as *machine learning* or *data engineer*).
- `max_features=5000` (focuses on the most informative vocabulary).

### B. Cosine Similarity
Cosine similarity evaluates the orientation angle between the TF-IDF vector of the candidate's resume $\vec{u}$ and each job posting vector $\vec{v}$:

$$\text{Cosine Similarity}(\vec{u}, \vec{v}) = \frac{\vec{u} \cdot \vec{v}}{\|\vec{u}\|_2 \|\vec{v}\|_2} = \frac{\sum_{i=1}^{n} u_i v_i}{\sqrt{\sum_{i=1}^{n} u_i^2} \sqrt{\sum_{i=1}^{n} v_i^2}}$$

The result ranges from $0.0$ to $1.0$, which is scaled to a $0\text{--}100\%$ score:
$$\text{Text Similarity Score} = \min(100.0, \max(0.0, \text{Cosine Similarity} \times 100))$$

### C. Skill Coverage Score
Skill coverage measures the proportion of listed skills for a given job posting that are detected in the candidate's resume:

$$\text{Skill Coverage Score (\%)} = \begin{cases} 
\left(\frac{|\text{Matched Required Skills}|}{|\text{Total Listed Role Skills}|}\right) \times 100, & \text{if } |\text{Total Listed Role Skills}| > 0 \\
0.0, & \text{otherwise}
\end{cases}$$

### D. Overall Match Score Formula
The overall ranking score is calculated as a balanced weighted average:

$$\text{Overall Match Score} = (0.50 \times \text{Text Similarity Score}) + (0.50 \times \text{Skill Coverage Score})$$

> **Academic Note**: This formula is an explainable heuristic scoring method designed for clear demonstration in an undergraduate engineering project, rather than an unverified commercial hiring prediction algorithm.

---

## 10. Project Directory Structure

```
RoleMatch AI/
├── app.py                         # Application entry point (initializes & runs Controller)
├── requirements.txt               # Dependency list
├── README.md                      # Comprehensive academic project documentation
├── .gitignore                     # Git rules for virtual environment & cache
├── download_and_normalize_data.py # Data pipeline for Hugging Face dataset
├── generate_sample_resumes.py     # Generator script for test PDF resumes
├── eval_sample_resumes.py         # End-to-end evaluation script
├── RoleMatch_AI_Career_Role_Recommender.zip # Standalone project submission zip
├── models/                        # [MODEL LAYER] Domain entities & ML business logic
│   ├── __init__.py
│   ├── entities.py                # Data classes: JobRole, RecommendationResult, ResumeProfile
│   ├── pdf_model.py               # PyPDF text extraction & validation model
│   ├── skill_model.py             # Boundary regex matching, aliases & vocabulary model
│   └── recommender_model.py       # TF-IDF, Cosine Similarity & scoring model
├── views/                         # [VIEW LAYER] Streamlit presentation components & styling
│   ├── __init__.py
│   ├── theme.py                   # Dynamic CSS stylesheets (Light & Dark themes)
│   ├── components.py              # Modular UI components (cards, pills, badges, metrics)
│   └── main_view.py               # Main page layout & sidebar coordinator
├── controllers/                   # [CONTROLLER LAYER] Application orchestration & events
│   ├── __init__.py
│   └── app_controller.py          # Coordinates between Streamlit events and Models
├── data/
│   ├── README.md                  # Dataset documentation & attribution
│   ├── job_skill_set.csv          # Normalized 1,431 genuine roles & job postings
│   └── skills_vocabulary.json     # 5,242 extracted technical skills index
├── sample_resumes/
│   ├── 1_software_engineer_resume.pdf       # Full Stack / Cloud Engineer (Python, React, AWS, Docker)
│   ├── 2_data_scientist_resume.pdf          # Data Scientist / ML Engineer (PyTorch, Scikit-Learn, NLP)
│   ├── 3_financial_analyst_resume.pdf       # Senior Financial Analyst (Accounting, Budgeting, GAAP)
│   ├── 4_human_resources_resume.pdf         # HR Specialist (Talent Acquisition, Compliance, FMLA)
│   └── 5_business_development_sales_resume.pdf # Sales Executive (B2B Sales, CRM, Lead Gen, Negotiation)
├── utils/                         # Backward-compatible adapters
│   ├── __init__.py
│   ├── pdf_extractor.py           # Delegates to models.pdf_model
│   ├── skill_extractor.py         # Delegates to models.skill_model
│   └── recommender.py             # Delegates to models.recommender_model
└── tests/                         # Comprehensive unit test suite
    ├── __init__.py
    ├── test_mvc_architecture.py   # Tests for Model entities, Model ML & Controller
    ├── test_pdf_extractor.py      # Unit tests for PDF parsing & edge cases
    ├── test_skill_extractor.py    # Unit tests for skill extraction & aliases
    └── test_recommender.py        # Unit tests for scoring & ranking
```

---

## 11. Step-by-Step Installation Instructions (Windows PowerShell)

Follow these exact steps in Windows PowerShell to set up and run the project:

### Step 1: Open Windows PowerShell and Navigate to the Project Folder
```powershell
cd "c:\Users\prem9\OneDrive\Desktop\RoleMatch AI"
```

### Step 2: Create a Python Virtual Environment
```powershell
py -m venv .venv
```

### Step 3: Activate the Virtual Environment
```powershell
.\.venv\Scripts\Activate.ps1
```

> **Troubleshooting Execution Policy Error**:  
> If PowerShell displays `File ... cannot be loaded because running scripts is disabled on this system`, run:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```
> Then re-run `.\.venv\Scripts\Activate.ps1`.

### Step 4: Install Required Packages
```powershell
pip install -r requirements.txt
```

### Step 5: (Optional) Re-generate or Update the Dataset
The normalized dataset is already included in `data/job_skill_set.csv`. If you ever need to refresh or download it from Hugging Face:
```powershell
python download_and_normalize_data.py
```

### Step 6: Launch the Streamlit Web Application
```powershell
streamlit run app.py
```
Streamlit will launch automatically in your default web browser at `http://localhost:8501`.

---

## 12. Deploying to Streamlit Community Cloud

The app is ready to deploy from a GitHub repository. The normalized dataset, skills vocabulary, course catalog, and Streamlit configuration are included in the project; the deployment does not need to run the data-download scripts or configure API keys.

1. **Check the files to publish.** Keep `app.py`, `requirements.txt`, the `controllers/`, `models/`, `views/`, `utils/`, and `data/` directories, `.streamlit/config.toml`, and the five demo resumes in the repository. `.streamlit/credentials.toml`, local environments, caches, and personal resume PDFs should remain untracked.
2. **Create and push a GitHub repository.** From the project folder, initialize Git if needed, review the staged files, then commit and push them to a GitHub repository. For example:
   ```powershell
   git init
   git add .
   git status
   git commit -m "Prepare RoleMatch AI for Streamlit deployment"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<your-repository>.git
   git push -u origin main
   ```
   Replace the repository URL with your own. Before committing, confirm that no personal resumes or `.streamlit/credentials.toml` appear in `git status`.
3. **Create the Streamlit app.** Sign in at [Streamlit Community Cloud](https://share.streamlit.io/) with GitHub, choose **Create app**, select the repository and `main` branch, and set the main file path to `app.py`.
4. **Deploy.** Choose a supported Python version (Python 3.12 is a compatible choice), then select **Deploy**. Community Cloud installs the packages from `requirements.txt` and starts the app. No Streamlit secrets are required.
5. **Verify the live app.** Open the generated app URL, confirm the landing page and demo-resume download buttons appear, and test a resume upload and recommendations. If deployment fails, open the app's **Manage app** page and inspect the logs; confirm the dependency manifest and required `data/` files are present in the selected branch.

Uploaded resumes are processed by the deployed app on Streamlit's hosted infrastructure. The application does not intentionally save uploaded resumes to disk, but deployment is no longer local-only; do not upload sensitive resumes unless users have been informed and the hosting/privacy requirements are acceptable.

---

## 13. Running Unit Tests

Run the full pytest suite to verify that all modules and integration points pass:

```powershell
python -m pytest -v
```

### Test Results Summary:
```
============================= test session starts =============================
tests/test_mvc_architecture.py::test_entities_instantiation PASSED       [  4%]
tests/test_mvc_architecture.py::test_skill_model_mvc PASSED              [  8%]
tests/test_mvc_architecture.py::test_recommender_model_mvc PASSED        [ 13%]
tests/test_mvc_architecture.py::test_controller_initialization PASSED    [ 17%]
tests/test_mvc_architecture.py::test_controller_toggle_theme PASSED      [ 21%]
tests/test_pdf_extractor.py::test_extract_text_from_valid_pdf_bytes PASSED [ 26%]
tests/test_pdf_extractor.py::test_extract_text_from_bytes_io PASSED      [ 30%]
tests/test_pdf_extractor.py::test_empty_pdf_raises_empty_pdf_error PASSED [ 34%]
tests/test_pdf_extractor.py::test_file_size_exceeded PASSED              [ 39%]
tests/test_pdf_extractor.py::test_corrupted_pdf_raises_error PASSED      [ 43%]
tests/test_pdf_extractor.py::test_nonexistent_file_path PASSED           [ 47%]
tests/test_recommender.py::test_calculate_overall_score PASSED           [ 52%]
tests/test_recommender.py::test_zero_skills_avoids_division_by_zero PASSED [ 56%]
tests/test_recommender.py::test_python_ml_resume_recommendations PASSED  [ 60%]
tests/test_recommender.py::test_unrelated_resume_recommendations PASSED  [ 65%]
tests/test_recommender.py::test_empty_dataset_handling PASSED            [ 69%]
tests/test_recommender.py::test_real_dataset_integrity PASSED            [ 73%]
tests/test_skill_extractor.py::test_basic_skill_extraction PASSED        [ 78%]
tests/test_skill_extractor.py::test_alias_mapping PASSED                 [ 82%]
tests/test_skill_extractor.py::test_word_boundaries_no_false_matches PASSED [ 86%]
tests/test_skill_extractor.py::test_symbols_cplusplus_and_csharp PASSED  [ 91%]
tests/test_skill_extractor.py::test_empty_and_whitespace_text PASSED     [ 95%]
tests/test_skill_extractor.py::test_normalize_skill_string PASSED        [100%]
============================= 23 passed in 17.93s =============================
```

---

## 14. Example Output

### Case 1: Software Engineer Resume (`sample_resumes/software_developer_resume.pdf`)
- **Skills Mentioned**: Python, JavaScript, TypeScript, SQL, Django, React, Docker, Kubernetes, Git, AWS Cloud, Scikit-Learn, TensorFlow.
- **Top 3 Recommended Roles**:
  1. **Lead Software Engineer** (Category: `FINANCE`) — **Overall Match: 31.5%**  
     - Text Similarity: 40.8% | Skill Coverage: 22.2%  
     - Matched: `AWS`, `Python`, `SQL`, `Machine Learning`
  2. **Staff Data Engineer** (Category: `FINANCE`) — **Overall Match: 20.3%**  
     - Text Similarity: 24.4% | Skill Coverage: 16.2%  
     - Matched: `SQL`, `Python`, `Docker`, `Kubernetes`, `Git`, `CI/CD`
  3. **Data Scientist Lead** (Category: `FINANCE`) — **Overall Match: 19.9%**  
     - Text Similarity: 27.0% | Skill Coverage: 12.9%  
     - Matched: `Python`, `SQL`, `Machine Learning`, `AWS`

### Case 2: HR Specialist Resume (`sample_resumes/hr_specialist_resume.pdf`)
- **Skills Mentioned**: Talent Acquisition, Employee Relations, Performance Management, Onboarding, Compliance, Benefits Administration.
- **Top 1 Recommended Role**:
  1. **Human Resources Generalist** (Category: `HR`) — **Overall Match: 31.1%**  
     - Text Similarity: 32.1% | Skill Coverage: 30.0%  
     - Matched: `Onboarding`, `Compliance`, `Benefits Administration`

### Case 3: Non-Technical Culinary Resume (`sample_resumes/unrelated_culinary_resume.pdf`)
- **Skills Mentioned**: Sourdough fermentation, croissant laminating, oven maintenance, food safety.
- **Top 1 Recommended Role**:
  1. **FT Deli Bakery Sales Associate** (Category: `SALES`) — **Overall Match: 18.3%**  
     - Demonstrates safe degradation for out-of-domain resumes without crashing.

---

## 15. Limitations
1. **Scanned Image PDFs**: `pypdf` extracts text streams from selectable PDF documents. Scanned or image-only documents without OCR text layers cannot be read and will raise a clear warning.
2. **Dataset Vocabulary Dependency**: Skill detection relies on the 5,772 skills extracted from the genuine LinkedIn dataset. Rare or newly coined framework names may not be recognized unless added to the alias dictionary.
3. **No Live Vacancy Status**: Because the dataset is derived from an archival LinkedIn crawl, recommended roles reflect real historical job postings rather than active openings.

---

## 16. Future Scope
- **Optical Character Recognition (OCR)**: Integrate Tesseract OCR as a fallback for scanned image resumes.
- **Fine-Tuned Embeddings**: Experiment with domain-specific sentence embeddings (*e.g.*, `all-MiniLM-L6-v2`) to compare performance with TF-IDF.
- **Exportable PDF Report**: Add a one-click button to download a customized PDF summary of recommended roles and matching skills.

---

## 17. References
1. Mutlu, B. (2024). *Job Skill Set Dataset*. Hugging Face Datasets: `batuhanmtl/job-skill-set`.
2. Arshkon. (2023). *LinkedIn Job Postings Dataset*. Kaggle Datasets: `arshkon/linkedin-job-postings`.
3. Pedregosa, F., et al. (2011). *Scikit-learn: Machine Learning in Python*. Journal of Machine Learning Research, 12, 2825–2830.
4. Manning, C. D., Raghavan, P., & Schütze, H. (2008). *Introduction to Information Retrieval*. Cambridge University Press.
5. Streamlit Documentation: https://docs.streamlit.io/

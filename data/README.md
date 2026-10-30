# RoleMatch AI - Job Skill Set Dataset Documentation

## 1. Datasets Overview & Attribution

RoleMatch AI incorporates genuine, publicly available job and skill datasets hosted on Hugging Face:

### A. Computer Science Student & Tech Datasets
1. **Curated IT & Computer Science Roles Database**:
   - **Dataset**: `DevilsLord/It_job_roles_skills_certifications` (Top 207 IT Job Roles, Skills & Certifications Database)
   - **Host**: Hugging Face Datasets ([https://huggingface.co/datasets/DevilsLord/It_job_roles_skills_certifications](https://huggingface.co/datasets/DevilsLord/It_job_roles_skills_certifications))
   - **Content**: Dedicated roles across Computer Science, AIML, Web Development, Cloud & DevOps, Data Science, and Cybersecurity with curated required skills and industry certifications.
2. **Authentic Tech Job Postings**:
   - **Dataset**: `jacob-hugging-face/job-descriptions`
   - **Host**: Hugging Face Datasets ([https://huggingface.co/datasets/jacob-hugging-face/job-descriptions](https://huggingface.co/datasets/jacob-hugging-face/job-descriptions))
   - **Content**: Real-world software engineering, developer, and data science job postings with authentic company names (e.g., Epic, Revature LLC, Light & Wonder, Blockchains).

### B. Cross-Domain Career Dataset
- **Dataset**: `batuhanmtl/job-skill-set`
- **Host**: Hugging Face Datasets ([https://huggingface.co/datasets/batuhanmtl/job-skill-set](https://huggingface.co/datasets/batuhanmtl/job-skill-set))
- **Original Source**: Kaggle LinkedIn Job Postings by Arshkon with skills extracted via RecAI.
- **Content**: Cross-domain postings covering Information Technology, Finance, Human Resources, Sales, and Business Development.

---

## 2. Dataset Schema & Structure

The normalized combined dataset is stored in `data/job_skill_set.csv`:

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `job_id` | Integer (int64) | Unique numeric identifier for the job posting / role. |
| `job_title` | String | Official position title (e.g., *Full Stack Python Developer*, *Machine Learning Engineer*). |
| `company_name` | String / Empty | Name of hiring organization when provided in source data; empty when role is a standard reference profile. |
| `category` | String | Career domain (`COMPUTER-SCIENCE`, `INFORMATION-TECHNOLOGY`, `FINANCE`, `BUSINESS-DEVELOPMENT`, `SALES`, `HR`). |
| `job_skill_set` | String | Comma-separated list of technical and professional skills required for the role. |
| `job_description` | String | Complete job posting description detailing responsibilities, stack, and qualifications. |

---

## 3. Dataset Statistics

- **Total Job Postings / Roles**: 1,431
- **Unique Career Categories**: 6
  - `COMPUTER-SCIENCE`: 264
  - `INFORMATION-TECHNOLOGY`: 240
  - `BUSINESS-DEVELOPMENT`: 239
  - `FINANCE`: 236
  - `SALES`: 232
  - `HR`: 220
- **Unique Extracted Skills Vocabulary**: 5,242 unique technical and domain skills (indexed in `data/skills_vocabulary.json`)

---

## 4. Key Computer Science Roles Available
- Full Stack Developer / Full Stack Python Developer / Full Stack Java Developer
- Machine Learning Engineer / Artificial Intelligence Researcher / AI Architect
- Data Scientist / Data Analyst / Big Data Engineer / Data Architect
- Frontend Web Developer / React Developer / Angular Developer / Web Designer
- DevOps Engineer / Cloud Engineer / Kubernetes Administrator / GCP DevOps Engineer
- Cybersecurity Analyst / Information Security Analyst / Penetration Tester
- Mobile App Developer (iOS Developer / Android Developer)
- Entry Level Software Engineer / Entry Level Developer / Software Developer - New Graduate

---

## 5. Integrity and Ethical Considerations

1. **Zero Fabrication**: All job postings, IDs, descriptions, and skill lists originate directly from genuine, publicly verifiable Hugging Face datasets.
2. **Missing Field Transparency**: When source records do not contain a company name, `company_name` is left empty rather than inventing fictitious companies.
3. **Completely Local Execution**: The application runs completely offline using `data/job_skill_set.csv` without requiring external API keys, external databases, or paid cloud services.

"""
Script: generate_sample_resumes.py
Purpose: Generate 5 professional, realistic sample PDF resumes covering diverse domains
         for college evaluation and demonstration:
         1. Software Engineer (IT & Cloud)
         2. Data Scientist / ML Engineer (AI & Analytics)
         3. Financial Analyst (Finance & Accounting)
         4. Human Resources Specialist (HR & Talent Acquisition)
         5. Business Development Executive (Sales & Strategy)
"""
import os
import io
from pypdf import PdfReader


def build_pdf_bytes(text_lines):
    """Generate valid PDF-1.4 raw bytes containing line-by-line selectable text."""
    stream_content = "BT\n/F1 11 Tf\n50 750 Td\n15 TL\n"
    for line in text_lines:
        safe_line = line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        stream_content += f"({safe_line}) '\n"
    stream_content += "ET"
    stream_bytes = stream_content.encode("latin1")
    length = len(stream_bytes)

    header = b"%PDF-1.4\n"
    obj1 = b"1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n"
    obj2 = b"2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj\n"
    obj3 = (
        b"3 0 obj << /Type /Page /Parent 2 0 R /Resources << /Font << /F1 4 0 R >> >> "
        b"/MediaBox [0 0 612 792] /Contents 5 0 R >> endobj\n"
    )
    obj4 = b"4 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj\n"
    obj5_start = f"5 0 obj << /Length {length} >> stream\n".encode("latin1")
    obj5_end = b"\nendstream\nendobj\n"

    body = header
    pos1 = len(body); body += obj1
    pos2 = len(body); body += obj2
    pos3 = len(body); body += obj3
    pos4 = len(body); body += obj4
    pos5 = len(body); body += obj5_start + stream_bytes + obj5_end

    xref_pos = len(body)
    xref = (
        f"xref\n0 6\n0000000000 65535 f \n{pos1:010d} 00000 n \n{pos2:010d} 00000 n \n"
        f"{pos3:010d} 00000 n \n{pos4:010d} 00000 n \n{pos5:010d} 00000 n \n"
        f"trailer << /Size 6 /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF"
    )
    return body + xref.encode("latin1")


RESUMES_DATA = [
    {
        "filename": "1_software_engineer_resume.pdf",
        "title": "Alex Chen - Full Stack Software Engineer",
        "lines": [
            "ALEX CHEN",
            "Email: alex.chen@techmail.com | Phone: +1-555-0101 | Portfolio: github.com/alexchen-dev",
            "================================================================================",
            "PROFESSIONAL SUMMARY:",
            "Full Stack Software Engineer with 4 years of experience architecting cloud applications.",
            "Specialized in backend APIs with Python and modern responsive web frontend interfaces.",
            "",
            "TECHNICAL SKILLS:",
            "- Languages: Python, JavaScript, TypeScript, SQL, HTML, CSS",
            "- Frameworks: Django, FastAPI, React, Node.js, Express",
            "- Databases & Storage: PostgreSQL, MySQL, Redis, MongoDB",
            "- DevOps & Cloud: Docker, Kubernetes, AWS Cloud, CI/CD, Git, Linux",
            "- Methodologies: Agile Scrum, Microservices, REST API design, Unit Testing",
            "",
            "PROFESSIONAL EXPERIENCE:",
            "Senior Backend Developer | CloudScale Solutions (2022 - Present)",
            "- Designed and implemented scalable RESTful microservices using Python and FastAPI.",
            "- Automated containerized deployments using Docker and Kubernetes clusters on AWS.",
            "- Optimized complex SQL database queries in PostgreSQL, improving throughput by 35%.",
            "",
            "Software Engineer | NexaTech Systems (2020 - 2022)",
            "- Developed interactive user interface dashboards using React and TypeScript.",
            "- Integrated third-party payment gateways and authentication using JWT.",
            "",
            "EDUCATION:",
            "B.Tech in Computer Science and Engineering | Tech University (2020)"
        ]
    },
    {
        "filename": "2_data_scientist_resume.pdf",
        "title": "Dr. Priya Sharma - Machine Learning Engineer & Data Scientist",
        "lines": [
            "PRIYA SHARMA, Ph.D.",
            "Email: priya.sharma@aimail.com | Phone: +1-555-0202 | LinkedIn: linkedin.com/in/priyasharma-ai",
            "================================================================================",
            "PROFESSIONAL SUMMARY:",
            "Data Scientist and Machine Learning Engineer specializing in predictive modeling,",
            "Natural Language Processing (NLP), and Deep Learning neural network architectures.",
            "",
            "TECHNICAL SKILLS:",
            "- Core AI/ML: Machine Learning, Deep Learning, NLP, Computer Vision, Statistics",
            "- Libraries: Scikit-Learn, TensorFlow, PyTorch, Pandas, NumPy, SciPy",
            "- Languages & Databases: Python, R, SQL, PostgreSQL",
            "- Big Data & Visualization: Tableau, Power BI, Apache Spark, Matplotlib, Seaborn",
            "- Cloud & MLOps: AWS Cloud, MLflow, Docker, Git, Linux",
            "",
            "PROFESSIONAL EXPERIENCE:",
            "Lead Machine Learning Engineer | DeepVision AI Labs (2022 - Present)",
            "- Built end-to-end predictive machine learning pipelines using Scikit-Learn and PyTorch.",
            "- Fine-tuned NLP language models for automated text classification and document search.",
            "- Deployed inference microservices with Docker on AWS with sub-100ms latency.",
            "",
            "Data Scientist | FinAnalytics Corp (2020 - 2022)",
            "- Analyzed multi-terabyte transactional datasets using Python, Pandas, and SQL.",
            "- Created executive dashboards in Power BI and Tableau for senior management.",
            "",
            "EDUCATION:",
            "Ph.D. in Artificial Intelligence & Machine Learning | National Institute of Technology",
            "M.S. in Data Science & Applied Statistics (2019)"
        ]
    },
    {
        "filename": "3_financial_analyst_resume.pdf",
        "title": "David Miller - Senior Financial Analyst & Accountant",
        "lines": [
            "DAVID MILLER, CPA",
            "Email: david.miller@financecorp.com | Phone: +1-555-0303 | City: Chicago, IL",
            "================================================================================",
            "PROFESSIONAL SUMMARY:",
            "Senior Financial Analyst with 5+ years expertise in corporate accounting, variance analysis,",
            "annual budgeting, cash flow forecasting, and GAAP regulatory compliance.",
            "",
            "CORE COMPETENCIES & SKILLS:",
            "- Financial: Financial Analysis, Financial Accounting, Financial Modeling, Budgeting",
            "- Reporting: Forecasting, Variance Analysis, Auditing, GAAP Compliance, Tax Preparation",
            "- Systems: Advanced Excel, QuickBooks, SAP ERP, Power BI, Financial Statements",
            "- Governance: Internal Controls, Cost Accounting, Account Reconciliation, Payroll",
            "",
            "PROFESSIONAL EXPERIENCE:",
            "Senior Financial Analyst | Global Asset Management Group (2021 - Present)",
            "- Led quarterly budgeting, revenue forecasting, and financial model development.",
            "- Prepared comprehensive financial statements and balance sheet reconciliations under GAAP.",
            "- Collaborated with external auditors to ensure 100% compliance during annual tax audits.",
            "",
            "Financial Accountant | Horizon Commercial Bank (2019 - 2021)",
            "- Conducted monthly variance analysis across departmental operating expenses.",
            "- Automated financial reporting worksheets in Excel utilizing pivot tables and macros.",
            "",
            "EDUCATION & CERTIFICATION:",
            "Certified Public Accountant (CPA) | State Board of Accountancy",
            "B.S. in Finance & Accounting | University School of Business (2019)"
        ]
    },
    {
        "filename": "4_human_resources_resume.pdf",
        "title": "Sarah Jenkins - Human Resources Generalist & Talent Acquisition",
        "lines": [
            "SARAH JENKINS, SHRM-CP",
            "Email: sarah.jenkins@hrmail.com | Phone: +1-555-0404 | City: Atlanta, GA",
            "================================================================================",
            "PROFESSIONAL SUMMARY:",
            "Human Resources Professional with 4+ years of experience leading full-lifecycle",
            "talent acquisition, employee relations, onboarding, and regulatory compliance.",
            "",
            "CORE HR SKILLS:",
            "- Recruiting: Talent Acquisition, Full-Lifecycle Recruiting, Sourcing, Interviewing",
            "- Relations & Culture: Employee Relations, Performance Management, Conflict Resolution",
            "- Administration: Employee Onboarding, Benefits Administration, Payroll, Offboarding",
            "- Legal & Compliance: Employment Law, FMLA, ADA, EEOC Guidelines, HR Policies",
            "- HR Systems: Workday, BambooHR, ADP Workforce, ATS Management, Employee Records",
            "",
            "PROFESSIONAL EXPERIENCE:",
            "Human Resources Generalist | Pinnacle Enterprises (2021 - Present)",
            "- Managed recruitment pipelines for technical and operational positions, hiring 120+ staff.",
            "- Designed company-wide employee onboarding program, boosting 90-day retention by 25%.",
            "- Resolved employee relations inquiries while ensuring adherence to labor laws and FMLA.",
            "",
            "HR & Recruiting Coordinator | Metro Staffing Solutions (2019 - 2021)",
            "- Screened resumes, scheduled hiring interviews, and conducted reference checks.",
            "- Coordinated new-hire orientation, benefit enrollments, and quarterly performance reviews.",
            "",
            "EDUCATION & CREDENTIALS:",
            "SHRM-CP Certified Professional | Society for Human Resource Management",
            "B.A. in Human Resources Management | State University (2019)"
        ]
    },
    {
        "filename": "5_business_development_sales_resume.pdf",
        "title": "Michael Reynolds - Business Development & B2B Sales Executive",
        "lines": [
            "MICHAEL REYNOLDS",
            "Email: michael.reynolds@salesexec.com | Phone: +1-555-0505 | City: Dallas, TX",
            "================================================================================",
            "PROFESSIONAL SUMMARY:",
            "Results-driven Business Development and Sales Executive with a track record of driving revenue",
            "growth, acquiring enterprise client accounts, and managing end-to-end sales pipelines.",
            "",
            "CORE SALES & BUSINESS SKILLS:",
            "- Strategy: Business Development, B2B Sales, Lead Generation, Market Analysis",
            "- Account Growth: Account Management, Client Relationship Management, Solution Selling",
            "- Closing: Contract Negotiation, Deal Structuring, Strategic Partnerships, Pipeline Management",
            "- Tools: Salesforce CRM, HubSpot, Cold Calling, Product Demonstrations, Quota Attainment",
            "",
            "PROFESSIONAL EXPERIENCE:",
            "Senior Business Development Manager | Enterprise Solutions Inc. (2021 - Present)",
            "- Exceeded annual sales quota by 140%, generating $3.2M in new enterprise contracts.",
            "- Developed strategic outreach campaigns via lead generation, discovery calls, and demos.",
            "- Negotiated multi-year commercial agreements with Fortune 500 decision-makers.",
            "",
            "B2B Sales Representative | Apex SaaS Platforms (2019 - 2021)",
            "- Qualified inbound leads and managed active sales opportunities through Salesforce CRM.",
            "- Delivered engaging product presentations, shortening the client sales cycle by 20 days.",
            "",
            "EDUCATION:",
            "B.B.A. in Marketing and Sales Management | Business College (2019)"
        ]
    }
]


def main():
    target_dir = "sample_resumes"
    os.makedirs(target_dir, exist_ok=True)

    print("Generating 5 diverse, professional sample PDF resumes...")
    for idx, item in enumerate(RESUMES_DATA, start=1):
        filename = item["filename"]
        filepath = os.path.join(target_dir, filename)
        pdf_bytes = build_pdf_bytes(item["lines"])
        with open(filepath, "wb") as f:
            f.write(pdf_bytes)

        # Verify extraction with pypdf
        reader = PdfReader(io.BytesIO(pdf_bytes))
        extracted = reader.pages[0].extract_text()
        print(f"[{idx}/5] Created '{filename}' ({len(pdf_bytes)} bytes) -> Verified {len(extracted)} chars extracted.")

    print("\nAll 5 sample resumes created successfully in sample_resumes/!")


if __name__ == "__main__":
    main()

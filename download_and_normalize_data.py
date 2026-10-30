"""
Script: download_and_normalize_data.py
Purpose: Download and normalize genuine career job datasets:
         1. batuhanmtl/job-skill-set (Cross-domain roles: IT, Finance, HR, Sales, Business Development)
         2. DevilsLord/It_job_roles_skills_certifications (Curated Computer Science & IT Job Roles & Skills Database)
         3. jacob-hugging-face/job-descriptions (Authentic Computer Science & Software Developer job postings)
         Output: data/job_skill_set.csv and data/skills_vocabulary.json
"""
import os
import re
import ast
import json
import time
import urllib.request
import pandas as pd

HF_BASE_DATASET = "batuhanmtl/job-skill-set"
HF_CS_ROLES_DATASET = "DevilsLord/It_job_roles_skills_certifications"
HF_TECH_JOBS_DATASET = "jacob-hugging-face/job-descriptions"

RAW_PARQUET_PATH = os.path.join("data", "raw_dataset.parquet")
OUTPUT_CSV_PATH = os.path.join("data", "job_skill_set.csv")
SKILLS_VOCAB_PATH = os.path.join("data", "skills_vocabulary.json")


def clean_skill_list(raw_skills) -> list:
    """
    Parse and clean skills from raw representation (string representation of list or comma separated).
    """
    if pd.isna(raw_skills):
        return []

    if isinstance(raw_skills, list):
        items = raw_skills
    elif isinstance(raw_skills, str):
        trimmed = raw_skills.strip()
        if trimmed.startswith("[") and trimmed.endswith("]"):
            try:
                items = ast.literal_eval(trimmed)
            except Exception:
                items = re.findall(r"'([^']*)'", trimmed) or re.findall(r'"([^"]*)"', trimmed)
        else:
            items = trimmed.split(",")
    else:
        return []

    cleaned = []
    seen = set()
    for item in items:
        if isinstance(item, str):
            s = item.strip().strip("'\"")
            if s and len(s) > 1 and s.lower() not in seen:
                cleaned.append(s)
                seen.add(s.lower())
    return cleaned


def fetch_hf_rows(dataset_name: str, limit_per_batch=100, max_rows=1000) -> list:
    """Fetch all rows from Hugging Face Datasets Server API."""
    print(f"Fetching records from Hugging Face for {dataset_name}...")
    headers = {"User-Agent": "RoleMatchAI-DataDownloader/1.0"}
    offset = 0
    all_rows = []

    while offset < max_rows:
        url = f"https://datasets-server.huggingface.co/rows?dataset={dataset_name}&config=default&split=train&offset={offset}&limit={limit_per_batch}"
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=15) as res:
                data = json.loads(res.read().decode("utf-8"))
                rows = data.get("rows", [])
                if not rows:
                    break
                for item in rows:
                    all_rows.append(item["row"])
                offset += len(rows)
                time.sleep(0.1)
        except Exception as e:
            print(f"Warning: Stopped fetching {dataset_name} at offset {offset}: {e}")
            break

    print(f"Fetched {len(all_rows)} rows for {dataset_name}.")
    return all_rows


def load_raw_base_dataset() -> pd.DataFrame:
    """Load base dataset from local parquet if available, otherwise fetch from HF API."""
    if os.path.exists(RAW_PARQUET_PATH):
        try:
            print(f"Reading local parquet file: {RAW_PARQUET_PATH}...")
            df = pd.read_parquet(RAW_PARQUET_PATH)
            print(f"Successfully loaded {len(df)} rows from parquet.")
            return df
        except Exception as e:
            print(f"Could not read parquet with pandas ({e}). Falling back to HF Server API...")

    rows = fetch_hf_rows(HF_BASE_DATASET, limit_per_batch=100, max_rows=2000)
    return pd.DataFrame(rows)


def load_cs_student_dataset(start_id: int, vocab_lower: dict) -> list:
    """
    Fetch and normalize authentic Computer Science student roles from DevilsLord and Jacob HF datasets.
    """
    cs_rows = []

    # 1. Fetch DevilsLord/It_job_roles_skills_certifications (or local scratch if present)
    devils_data = []
    if os.path.exists("scratch/devils_lord.json"):
        try:
            with open("scratch/devils_lord.json", "r", encoding="utf-8") as f:
                devils_data = json.load(f)
        except Exception:
            pass
    if not devils_data:
        devils_data = fetch_hf_rows(HF_CS_ROLES_DATASET, limit_per_batch=100, max_rows=300)

    seen_signatures = set()

    for r in devils_data:
        title = (r.get("Job Title") or "").strip()
        desc = (r.get("Job Description") or "").strip()
        skills_raw = (r.get("Skills") or "").strip()
        certs = (r.get("Certifications") or "").strip()

        if not title or not skills_raw or desc == "No description available":
            continue

        sig = (title.lower(), desc.lower())
        if sig in seen_signatures:
            continue
        seen_signatures.add(sig)

        full_desc = desc
        if certs and certs.lower() != "none":
            full_desc += f" Preferred certifications: {certs}."

        skill_items = [s.strip() for s in skills_raw.split(",") if s.strip()]
        cleaned_skills = []
        seen_skill = set()
        for s in skill_items:
            s_clean = s.strip()
            if s_clean and s_clean.lower() not in seen_skill:
                cleaned_skills.append(s_clean)
                seen_skill.add(s_clean.lower())
                if s_clean.lower() not in vocab_lower:
                    vocab_lower[s_clean.lower()] = s_clean

        cs_rows.append({
            "job_id": start_id,
            "job_title": title,
            "company_name": "",  # Standard reference role
            "category": "COMPUTER-SCIENCE",
            "job_skill_set": ", ".join(cleaned_skills),
            "job_description": full_desc
        })
        start_id += 1

    # 2. Fetch Jacob HF CS & Software postings
    jacob_data = []
    if os.path.exists("scratch/jacob_tech.json"):
        try:
            with open("scratch/jacob_tech.json", "r", encoding="utf-8") as f:
                jacob_data = json.load(f)
        except Exception:
            pass
    if not jacob_data:
        jacob_data = fetch_hf_rows(HF_TECH_JOBS_DATASET, limit_per_batch=100, max_rows=900)

    cs_keywords = [
        'software', 'developer', 'engineer', 'data scientist', 'data science',
        'machine learning', 'deep learning', 'artificial intelligence', 'frontend',
        'front end', 'backend', 'back end', 'full stack', 'fullstack', 'devops',
        'cloud', 'web developer', 'web designer', 'programmer', 'cyber security',
        'information security', 'network engineer', 'database administrator', 'big data'
    ]

    for r in jacob_data:
        title = (r.get("position_title") or "").strip()
        desc = (r.get("job_description") or "").strip()
        company = (r.get("company_name") or "").strip()
        mr = r.get("model_response", "")

        if not title or not desc:
            continue
        if not any(k in title.lower() for k in cs_keywords):
            continue

        sig = (title.lower(), desc.lower())
        if sig in seen_signatures:
            continue
        seen_signatures.add(sig)

        req_skills_str = ""
        try:
            parsed_mr = json.loads(mr)
            req_skills_str = parsed_mr.get("Required Skills", "")
        except Exception:
            pass

        combined_text = f"{title}. {req_skills_str}. {desc}".lower()
        tokens = re.findall(r"[a-z0-9\+\#\.]+", combined_text)
        candidate_phrases = set(tokens)
        for i in range(len(tokens) - 1):
            candidate_phrases.add(f"{tokens[i]} {tokens[i+1]}")
        for i in range(len(tokens) - 2):
            candidate_phrases.add(f"{tokens[i]} {tokens[i+1]} {tokens[i+2]}")

        matched_skills = []
        seen = set()
        for phrase in candidate_phrases:
            if phrase in vocab_lower and phrase not in seen:
                matched_skills.append(vocab_lower[phrase])
                seen.add(phrase)

        if not matched_skills:
            continue

        matched_skills = sorted(matched_skills, key=lambda x: -len(x))[:15]

        cs_rows.append({
            "job_id": start_id,
            "job_title": title,
            "company_name": company,
            "category": "COMPUTER-SCIENCE",
            "job_skill_set": ", ".join(matched_skills),
            "job_description": desc
        })
        start_id += 1

    return cs_rows


def normalize_and_save():
    os.makedirs("data", exist_ok=True)
    df = load_raw_base_dataset()

    if df.empty:
        raise ValueError("Base dataset is empty! Could not load data.")

    # Standardize column names
    expected_cols = ["job_id", "category", "job_title", "job_description", "job_skill_set"]
    for col in expected_cols:
        if col not in df.columns:
            df[col] = ""

    if "company_name" not in df.columns:
        df["company_name"] = ""

    # Clean base text columns
    df["job_title"] = df["job_title"].fillna("").astype(str).str.strip()
    df["category"] = df["category"].fillna("").astype(str).str.strip()
    df["job_description"] = df["job_description"].fillna("").astype(str).str.strip()

    # Parse and clean base skills
    print("Normalizing base skills...")
    all_unique_skills = set()
    cleaned_skill_strings = []

    for raw in df["job_skill_set"]:
        skills = clean_skill_list(raw)
        for s in skills:
            all_unique_skills.add(s)
        cleaned_skill_strings.append(", ".join(skills))

    df["job_skill_set"] = cleaned_skill_strings

    # Handle missing values & duplicates in base data
    df = df[df["job_title"] != ""]
    df = df.drop_duplicates(subset=["job_id"])
    df = df.drop_duplicates(subset=["job_title", "category", "job_description"])
    print(f"Base dataset cleaned: {len(df)} records.")

    # Build vocab lookup
    vocab_lower = {s.lower().strip(): s for s in all_unique_skills}

    # Add Computer Science Student dataset
    start_id = int(df["job_id"].max()) + 1 if not df.empty else 1
    print("\nIntegrating authentic Computer Science student datasets...")
    cs_rows = load_cs_student_dataset(start_id, vocab_lower)
    print(f"Added {len(cs_rows)} Computer Science job roles.")

    # Combine
    cs_df = pd.DataFrame(cs_rows)
    combined_df = pd.concat([df, cs_df], ignore_index=True)

    # Re-order columns cleanly
    final_cols = ["job_id", "job_title", "company_name", "category", "job_skill_set", "job_description"]
    combined_df = combined_df[final_cols]

    # Save to CSV
    combined_df.to_csv(OUTPUT_CSV_PATH, index=False, encoding="utf-8")
    print(f"\nSaved normalized combined dataset to: {OUTPUT_CSV_PATH} ({os.path.getsize(OUTPUT_CSV_PATH) / 1024:.1f} KB)")

    # Save complete skills vocabulary
    vocab_list = sorted(list(vocab_lower.values()), key=lambda x: (len(x), x.lower()))
    with open(SKILLS_VOCAB_PATH, "w", encoding="utf-8") as f:
        json.dump(vocab_list, f, indent=2)
    print(f"Saved {len(vocab_list)} unique skills vocabulary to: {SKILLS_VOCAB_PATH}")

    # Summary preview
    print("\n--- DATASET SUMMARY ---")
    print(f"Total Job Records: {len(combined_df)}")
    print(f"Unique Categories ({combined_df['category'].nunique()}):")
    print(combined_df["category"].value_counts().to_string())
    print("\nSample Computer Science Job Titles:")
    cs_sample = combined_df[combined_df["category"] == "COMPUTER-SCIENCE"]["job_title"].head(5)
    for t in cs_sample:
        print(f" - {t}")


if __name__ == "__main__":
    normalize_and_save()

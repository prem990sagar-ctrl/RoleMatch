"""
Script to download and inspect the raw dataset from Hugging Face:
Dataset: batuhanmtl/job-skill-set
Source: Hugging Face (derived from Kaggle LinkedIn Job Postings + RecAI skills)
"""
import os
import sys
import urllib.request

DATASET_URL = "https://huggingface.co/datasets/batuhanmtl/job-skill-set/resolve/main/data/train-00000-of-00001.parquet"
OUTPUT_PARQUET = os.path.join("data", "raw_dataset.parquet")

def download_file(url: str, dest_path: str):
    print(f"Downloading from {url} to {dest_path}...")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as response, open(dest_path, "wb") as out_file:
        total_size = int(response.info().get("Content-Length", 0))
        downloaded = 0
        chunk_size = 64 * 1024
        while True:
            chunk = response.read(chunk_size)
            if not chunk:
                break
            out_file.write(chunk)
            downloaded += len(chunk)
            if total_size > 0:
                percent = (downloaded / total_size) * 100
                sys.stdout.write(f"\rProgress: {downloaded / (1024*1024):.2f}MB / {total_size / (1024*1024):.2f}MB ({percent:.1f}%)")
                sys.stdout.flush()
    print("\nDownload completed successfully!")

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(OUTPUT_PARQUET):
        download_file(DATASET_URL, OUTPUT_PARQUET)
    else:
        print(f"File {OUTPUT_PARQUET} already exists.")


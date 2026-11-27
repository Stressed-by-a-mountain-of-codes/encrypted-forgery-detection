"""
Dataset Download Script for Direct-Link Datasets
Run locally to download Korus 2018, IMD2020, MICC-F600, COVERAGE (subset).
CASIA requires manual academic request.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path
import zipfile
import tarfile
import gzip
import shutil


def run_cmd(cmd, cwd=None):
    """Run shell command and return success."""
    print(f"  $ {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ERROR: {result.stderr}")
        return False
    if result.stdout:
        print(f"  {result.stdout[:200]}")
    return True


def download_file(url, output_path):
    """Download file using curl or wget."""
    if shutil.which("curl"):
        cmd = f'curl -L -o "{output_path}" "{url}"'
    elif shutil.which("wget"):
        cmd = f'wget -O "{output_path}" "{url}"'
    else:
        print("  ERROR: Neither curl nor wget found")
        return False
    return run_cmd(cmd)


def extract_archive(archive_path, extract_dir):
    """Extract zip, tar.gz, tar, gz archives."""
    print(f"  Extracting {archive_path}...")
    try:
        if archive_path.endswith(".zip"):
            with zipfile.ZipFile(archive_path, 'r') as zf:
                zf.extractall(extract_dir)
        elif archive_path.endswith(".tar.gz") or archive_path.endswith(".tgz"):
            with tarfile.open(archive_path, 'r:gz') as tf:
                tf.extractall(extract_dir)
        elif archive_path.endswith(".tar"):
            with tarfile.open(archive_path, 'r:') as tf:
                tf.extractall(extract_dir)
        elif archive_path.endswith(".gz"):
            with gzip.open(archive_path, 'rb') as f_in:
                out_path = archive_path[:-3]
                with open(out_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
        else:
            print(f"  Unknown archive format: {archive_path}")
            return False
        return True
    except Exception as e:
        print(f"  Extraction failed: {e}")
        return False


def download_korus_2018(root_dir):
    """Download Korus 2018 dataset from GitHub."""
    print("\n=== Downloading Korus 2018 ===")
    dataset_dir = Path(root_dir) / "Korus_2018"
    dataset_dir.mkdir(parents=True, exist_ok=True)
    
    # GitHub repo: https://github.com/pkorus/korus2018-dataset
    # Clone the repo (contains dataset or download links)
    repo_url = "https://github.com/pkorus/korus2018-dataset.git"
    
    if run_cmd(f"git clone {repo_url} korus2018-dataset", cwd=dataset_dir):
        # Check if data is in repo or needs separate download
        print("  Cloned repo. Check korus2018-dataset/ for data or download instructions.")
        return True
    return False


def download_imd2020(root_dir):
    """Download IMD2020 dataset from GitHub."""
    print("\n=== Downloading IMD2020 ===")
    dataset_dir = Path(root_dir) / "IMD2020"
    dataset_dir.mkdir(parents=True, exist_ok=True)
    
    # GitHub repo: https://github.com/imd2020/IMD2020
    repo_url = "https://github.com/imd2020/IMD2020.git"
    
    if run_cmd(f"git clone {repo_url} imd2020-repo", cwd=dataset_dir):
        print("  Cloned repo. Check imd2020-repo/ for data download links.")
        return True
    return False


def download_coverage(root_dir, max_size_gb=5):
    """Download COVERAGE dataset (large - download subset)."""
    print(f"\n=== Downloading COVERAGE (max ~{max_size_gb}GB) ===")
    dataset_dir = Path(root_dir) / "COVERAGE"
    dataset_dir.mkdir(parents=True, exist_ok=True)
    
    # GitHub repo: https://github.com/SCLBD/COVERAGE
    repo_url = "https://github.com/SCLBD/COVERAGE.git"
    
    if run_cmd(f"git clone {repo_url} coverage-repo", cwd=dataset_dir):
        print("  Cloned repo. Check coverage-repo/ for data download instructions.")
        print("  COVERAGE is 10K+ images (~20GB+). Download subset for Colab Free.")
        return True
    return False


def download_micc_f600(root_dir):
    """Download MICC-F600 dataset."""
    print("\n=== Downloading MICC-F600 ===")
    dataset_dir = Path(root_dir) / "MICC_F600"
    dataset_dir.mkdir(parents=True, exist_ok=True)
    
    # Official site: http://micc.unifi.it/MICC-F600/
    # Usually provides direct download links
    base_url = "http://micc.unifi.it/MICC-F600/"
    
    # Try common archive names
    archives = [
        "MICC-F600.zip",
        "MICC-F600.tar.gz",
        "MICC-F220.zip",
        "MICC-F220.tar.gz",
    ]
    
    for archive in archives:
        url = base_url + archive
        output = dataset_dir / archive
        if download_file(url, str(output)):
            if extract_archive(str(output), str(dataset_dir)):
                print(f"  Extracted {archive}")
                return True
    
    print("  Could not auto-download. Visit http://micc.unifi.it/MICC-F600/ manually")
    return False


def organize_casia_structure(root_dir):
    """Create CASIA directory structure (manual download needed)."""
    print("\n=== CASIA v1/v2 Structure ===")
    dataset_dir = Path(root_dir) / "CASIA_v2"
    dataset_dir.mkdir(parents=True, exist_ok=True)
    
    (dataset_dir / "Au").mkdir(exist_ok=True)
    (dataset_dir / "Tp").mkdir(exist_ok=True)
    
    print(f"  Created {dataset_dir}/Au and {dataset_dir}/Tp")
    print("  MANUAL: Request at http://forensics.idealtest.org/")
    print("  Download and place authentic images in Au/, tampered in Tp/")
    return True


def main():
    parser = argparse.ArgumentParser(description="Download forgery detection datasets")
    parser.add_argument("--root", type=str, default="D:\\major_project_datasets", 
                        help="Root directory for datasets")
    parser.add_argument("--datasets", nargs="+", 
                        choices=["korus", "imd2020", "coverage", "micc", "casia", "all"],
                        default=["all"], help="Datasets to download")
    parser.add_argument("--coverage-max-gb", type=int, default=5, 
                        help="Max GB for COVERAGE subset")
    args = parser.parse_args()
    
    root_dir = Path(args.root)
    root_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Dataset root: {root_dir}")
    print(f"Datasets: {args.datasets}")
    
    results = {}
    
    if "all" in args.datasets or "casia" in args.datasets:
        results["CASIA"] = organize_casia_structure(root_dir)
    
    if "all" in args.datasets or "korus" in args.datasets:
        results["Korus 2018"] = download_korus_2018(root_dir)
    
    if "all" in args.datasets or "imd2020" in args.datasets:
        results["IMD2020"] = download_imd2020(root_dir)
    
    if "all" in args.datasets or "coverage" in args.datasets:
        results["COVERAGE"] = download_coverage(root_dir, args.coverage_max_gb)
    
    if "all" in args.datasets or "micc" in args.datasets:
        results["MICC-F600"] = download_micc_f600(root_dir)
    
    print("\n=== Summary ===")
    for dataset, success in results.items():
        status = "✓" if success else "✗"
        print(f"  {status} {dataset}")
    
    print(f"\nAll datasets organized under: {root_dir}")
    print("Next: Run extract_and_encrypt.py for each dataset")


if __name__ == "__main__":
    main()
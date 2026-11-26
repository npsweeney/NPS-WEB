#!/usr/bin/env python3
"""Build shared publication outputs, or reject a stale CV before site rendering."""
import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

from build_publications_json import main as build_json

ROOT = Path(__file__).resolve().parent
STATE = ROOT / "cv/publication-build.json"
INPUTS = ["bib/publications.bib", "bib/policy_publications.bib", "cv/main.tex", "cv/resume.cls"]
OUTPUTS = ["cv/main.pdf", "site/assets/cv.pdf", "site/assets/cv-page-1.jpg", "site/assets/cv-page-2.jpg"]


def hashes():
    return {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
            for name in INPUTS + OUTPUTS}


def build():
    cv = ROOT / "cv"
    with tempfile.TemporaryDirectory(prefix="publication-build-", dir=cv) as folder:
        command = ["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
                   f"-output-directory={folder}", "main.tex"]
        subprocess.run(command, cwd=cv, check=True)
        subprocess.run(["biber", f"--input-directory={folder}",
                        f"--output-directory={folder}", "main"], cwd=cv, check=True)
        subprocess.run(command, cwd=cv, check=True)
        subprocess.run(command, cwd=cv, check=True)
        shutil.copyfile(Path(folder) / "main.pdf", cv / "main.pdf")
    shutil.copyfile(cv / "main.pdf", ROOT / "site/assets/cv.pdf")
    subprocess.run(["pdftoppm", "-jpeg", "-r", "150", "-jpegopt", "quality=90",
                    str(cv / "main.pdf"), str(ROOT / "site/assets/cv-page")], check=True)
    build_json()
    STATE.write_text(json.dumps(hashes(), indent=2) + "\n")


def check():
    if not STATE.exists() or json.loads(STATE.read_text()) != hashes():
        raise SystemExit("CV or bibliography changed. Run python3 live/sync_publications.py --build before rendering/publishing.")
    build_json()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build", action="store_true")
    args = parser.parse_args()
    build() if args.build else check()

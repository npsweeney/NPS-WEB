# NPS-WEB Canon

This repository is the source of truth for Nicholas Sweeney's website and CV.

## Server-Side Sync

- Canonical remote: `https://github.com/npsweeney/NPS-WEB.git`
- Canonical branch: `main`
- GitHub Actions renders the Quarto site on every push to `main` and deploys `live/site/_site` to `gh-pages`.
- To use this on another laptop:

```bash
gh auth login
mkdir -p ~/dev/download
git clone https://github.com/npsweeney/NPS-WEB.git ~/dev/download/NPS-WEB
cd ~/dev/download/NPS-WEB
```

- Before editing on either laptop, run:

```bash
git pull --ff-only origin main
```

- After editing, commit and push. The other laptop should then pull from `main`.

## Source Of Truth

- Academic and policy publications live in `live/bib/publications.bib` and `live/bib/policy_publications.bib`, respectively.
- `live/build_publications_json.py` converts those BibTeX files into `live/site/publications.json` for the website.
- The CV source lives in `live/cv/main.tex` and `live/cv/resume.cls`.
- The website source lives in `live/site/*.qmd`, `live/site/styles.css`, and `live/site/_quarto.yml`.
- `live/site/assets/cv.pdf` is the website copy of the compiled CV.
- Rendered Quarto output in `live/site/_site` should be regenerated, not hand-edited.

## Standard Update Flow

From the repository root:

```bash
python3 build_publications_json.py
cd cv
latexmk -pdf -interaction=nonstopmode main.tex
cd site
quarto render
cd ..
git status
```

Then review the changes, commit, and push to `main`.

## Publication Status Rules

- Use `webnote = {Published}` for published papers.
- Use `note = {Forthcoming}` and `webnote = {Forthcoming}` only while a paper is accepted but not published online.
- Use the publisher DOI URL once available.
- Keep `date` as the online publication date in `YYYY-MM-DD` format where possible.

## CV Last Updated

The CV footer uses LaTeX's `\today` and updates automatically whenever the CV is compiled.

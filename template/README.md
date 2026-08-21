# Academic website template

This folder is a generic Quarto starter for an academic personal website. It deliberately contains no personal data, CV, photographs, domains, credentials, or deployment configuration.

## Start here

1. Copy `template/` into a new repository or project folder.
2. Update `site/_quarto.yml`, `site/index.qmd`, and `site/contact/index.qmd` with your details.
3. Add your academic publications to `bib/publications.bib` and policy publications to `bib/policy_publications.bib`.
4. Run `python3 build_publications_json.py` to generate `site/publications.json` for the interactive publications table.
5. Add your CV PDF to `site/assets/cv.pdf`.
6. Run `quarto render site` locally.

The starter BibTeX files include example entries. Replace them with your own records before publishing.

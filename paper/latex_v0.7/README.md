# Editable LaTeX v0.7

Upload the contents of this folder as an Overleaf ZIP project. Set the compiler to **XeLaTeX** and the main document to `main.tex`. Alternatively run `latexmk -xelatex main.tex` locally.

Edit `manuscript.tex` for the paper, `cover.tex` for course details, `annexure.tex` for contributions and the checklist, and `references.tex` for the 40 numbered references. Use `\cite{rN}` for reference N. Do not renumber references by hand. Escape percentages as `\%`, ampersands as `\&`, and underscores as `\_`. Keep LaTeX commands and table column separators intact. Compile after each small edit.

The source follows the professor's single-column A4/2 cm-margin template, 10.5 pt body, 18 pt title, Roman section/table numbering and 9 pt references. Times New Roman is selected if installed; TeX Gyre Termes is the portable Times-compatible fallback. Proprietary font files are not redistributed. Page budget applies to the paper, excluding cover and annexure.

This is the canonical v0.7 source, converted directly from the author's edited DOCX. The legacy `tools/build_paper.py` rebuilds v0.6 and does **not** update this project. Do not overwrite this source with that output. Provenance records the original DOCX hash.

35 works have AI-assisted extraction reviews of logged sections. Reported human counts remain 7 and 3; overlap/work IDs are not yet recorded. Human verification, signatures, and supervisor approval of the questionnaire remain outstanding. No questionnaire data have been fabricated. Merging the draft does not certify academic submission readiness.

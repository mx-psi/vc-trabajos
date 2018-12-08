all: Baeyens_P3.zip

informe.pdf: memoria.md citas.bib
	pandoc -o $@ $< --filter pandoc-citeproc

Baeyens_P3.zip: informe.pdf main.py
	zip -9 $@ $^

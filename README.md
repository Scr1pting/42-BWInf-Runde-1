# 1. Runde des 42. Bundeswettbewerb Informatik

Diese Repository enthält die Lösungen der Aufgaben 1, 3 und 4 der ersten Runde des Bundeswettbewerb Informatiks 2023 in den entsprechenden Ordnern.

Die Aufgaben wurden in der Programmiersprache Python bearbeitet.

## Änderungen der Dokumentation

Die Dokumentation kann vom Markdown in das PDF Format mittels [Pandoc](https://github.com/jgm/pandoc?tab=readme-ov-file#pandoc), [mermaid-filter](https://github.com/raghur/mermaid-filter) und einem PDF Engine wie [basictex](https://tug.org/mactex/morepackages.html) im Fall von MacOS umgewandelt. Um eine Markdown Datei umzuwandeln, muss der folgende Befehl in dem entsprechenden Ordner gegeben werden:

```
pandoc -F mermaid-filter -H ../disable_image_float.tex -o File.pdf File.md
```

Zwei Änderungen müssen an der Markdown Datei vorgenommen werden, damit sie in eine PDF Datei umgewandelt werden kann:

1. Einfache Zeilenumbrüche, wie bei Team-ID, Autor und Datum müssen durch `\newline` ersetzt werden
2. Bei [Mermaid](https://github.com/mermaid-js/mermaid) Diagrammen muss die Bezeichnung von `mermaid` zu `{.mermaid format=pdf}` geändert werden, da sonst die Auflösung sehr gering ist
3. Bilder können nicht als HTML dargestellt werden, sondern nur als Markdown Bilder

Alle Pandoc Änderungen sind in den Markdown Dateien als Kommentare hinterlassen.

# ChatGPT Codex Test – Terminal Feuerwerk

Dieses kleine Projekt zeigt, was mit ein paar Zeilen Python und ANSI-Escape-Sequenzen möglich ist: ein buntes ASCII-Feuerwerk direkt im Terminal.

## Verwendung

```bash
python cool_fireworks.py
```

Mit ein paar Parametern lässt sich die Show individualisieren:

- `--frames`: Anzahl der Bilder (Standard: 200)
- `--interval`: Verzögerung zwischen den Bildern in Sekunden (Standard: 0.06)s dasdsa dsad 
- `--size`: Terminalgröße als `BREITExHÖHE` oder `auto`
- `--seed`: Zufalls-Seed für reproduzierbare Feuerwerke

Beispiel für eine kurze, deterministische Show:

```bash
python cool_fireworks.py --frames 60 --interval 0.04 --seed 42
```

Viel Spaß beim Zuschauen! 🎆

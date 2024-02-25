<img src="Images/Readme-Title.png" width="525vw">

[![Stars](https://img.shields.io/github/stars/AurelienAudero/KinoDerToten-Projet-Pyxel?label=Stars)](https://github.com/AurelienAudero/KinoDerToten-Projet-Pyxel/stargazers)
[![Forks](https://img.shields.io/badge/Forks-nicht%20autorisiert%20(siehe%20Lizenz%20f%C3%BCr%20weitere%20Informationen)-red)](LICENSE)
[![Release](https://img.shields.io/github/v/release/AurelienAudero/KinoDerToten-Projet-Pyxel?label=Download)](https://github.com/AurelienAudero/KinoDerToten-Projet-Pyxel/releases/latest)
-----

[Français](README.md) | [English](README_EN.md) | [Español](README_ES.md) | **Deutsch** | [Italiano](README_IT.md)

## Contents
- [Über das Spiel](#über-das-spiel)
- [Hauptmerkmale des Spiels](#hauptmerkmale-des-spiels)
- [Installation](#installation)
    - [Anforderungen](#anforderungen)
    - [Pyxel und Playsound installieren](#pyxel-und-playsound-installieren)
    - [Aktualisieren Sie Pyxel und Playsound](#aktualisieren-sie-pyxel-und-playsound)
    - [SDL2 installieren (unter Linux)](#sdl2-installieren-unter-linux)
    - [So starten Sie das Spiel](#so-starten-sie-das-spiel)
- [Credits](#credits)

## Über das Spiel
**Kino Der Toten: Überlebe den Horror... oder stirb!**

Tauchen Sie ein in eine von Untoten überfallene Villa und erleben Sie ein intensives und einzigartiges Überlebenserlebnis.
Kino Der Toten ist ein 2D-Spiel, bei dem Ihr Ziel einfach ist: so lange wie möglich zu überleben.
Bahnen Sie sich Ihren Weg durch Horden immer wilderer Zombies und verbessern Sie Ihre Überlebensfähigkeiten.

Verheerende Waffen, mächtige Power-Ups und gut versteckte Geheimnisse helfen Ihnen dabei, die Frist zu verschieben, aber die Spannung wird mit jeder Minute größer. Treten Sie in epischen Kämpfen gegen furchteinflößende Bosse an, die Ihre Nerven auf die Probe stellen werden.

**Wirst du der letzte Überlebende sein?**
**Nehmen Sie die Herausforderung an und beweisen Sie, dass Sie der Beste sind!**

## Hauptmerkmale des Spiels
* Ein 2D-Gameplay
* Wellen von Zombies werden immer schwieriger zu besiegen
* Neue Waffen und Power-Ups im Laufe des Spiels
* Intensive und spannende Bosskämpfe
* Fesselnde Grafik und Soundtrack

## Installation
### Anforderungen
- [X] Betriebssystem :
    - [X] Windows Vista oder höher
    - [X] macOS X 10.6 oder höher
    - [X] Linux
- [X] [Python 3.7 oder höher](https://www.python.org/downloads/)
- [X] [Pyxel 2.0.6 oder höher](#pyxel-installieren)
- [X] [Playsound 1.3.0 oder höher](#pyxel-und-playsound-installieren)
- [X] [Die neueste Version von SDL2 (für Linux-Systeme)](#sdl2-installieren-unter-linux)

### Pyxel und Playsound installieren
Führen Sie nach der Installation von Python den folgenden Befehl in einem Terminal aus:
```
pip install --upgrade setuptools wheel
pip install pyxel playsound
```

### Aktualisieren Sie Pyxel und Playsound
Wenn Sie Pyxel bereits installiert haben, führen Sie den folgenden Befehl in einem Terminal aus, um es zu aktualisieren:
```
pip install --upgrade setuptools wheel pyxel playsound
```

### SDL2 installieren (unter Linux)
Wenn Sie ein Linux-System verwenden, installieren Sie SDL2 mit Ihrem Paketmanager:
- apt package manager : `sudo apt-get install libsdl2-dev`  
- dnf package manager : `sudo dnf install SDL2-devel`  
- yum package manager : `yum install SDL2-devel`

### So starten Sie das Spiel
- Laden Sie die neueste stabile Version des Spiels herunter [hier](https://github.com/AurelienAudero/KinoDerToten-Projet-Pyxel/releases/latest).
- Entpacken Sie das heruntergeladene Archiv
- Öffnen Sie ein Terminal in dem Verzeichnis, in dem sich das Spiel befindet
- Führen Sie einen der folgenden Befehle aus: `python3 main.py` or `python main.py`

## Credits
- Schöpfer des Spiels :
    - [Aurélien Audero](https://github.com/AurelienAudero)
    - [Axel Thibert](https://github.com/Oxwerth)
    - [Tony Baca](https://github.com/Thidokachi)
- Anerkennungen :
    - Amine Ouichen *(für das System, das die Schüsse in Richtung des Fadenkreuzes ermöglicht)*
    - Timothée Ané *(für das System, das die Schüsse in Richtung des Fadenkreuzes ermöglicht)*

"Kino Der Toten - A Pyxel Game" © 2024 by [Aurélien Audero](https://github.com/AurelienAudero), [Axel Thibert](https://github.com/Oxwerth) and [Tony Baca](https://github.com/Thidokachi) is licensed under [CC BY-NC-ND 4.0](https://github.com/AurelienAudero/KinoDerToten-Projet-Pyxel/blob/main/LICENSE)

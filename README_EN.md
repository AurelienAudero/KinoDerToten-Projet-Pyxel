<img src="Images/Readme-Title.png" width="525vw">

[![Stars](https://img.shields.io/github/stars/AurelienAudero/KinoDerToten-Projet-Pyxel?label=Stars)](https://github.com/AurelienAudero/KinoDerToten-Projet-Pyxel/stargazers)
[![Forks](https://img.shields.io/badge/Forks-not%20authorized%20(see%20license%20for%20more%20info)-red)](LICENSE)
[![Release](https://img.shields.io/github/v/release/AurelienAudero/KinoDerToten-Projet-Pyxel?label=Download)](https://github.com/AurelienAudero/KinoDerToten-Projet-Pyxel/releases/latest)
-----

[Français](README.md) | **English** | [Español](README_ES.md) | [Deutsch](README_DE.md) | [Italiano](README_IT.md)

## Contents
- [About the game](#about-the-game)
- [Main features of the game](#main-features-of-the-game)
- [Installation](#installation)
    - [Requirements](#requirements)
    - [Installing Pyxel and Playsound](#installing-pyxel-and-playsound)
    - [Update Pyxel and Playsound](#update-pyxel-and-playsound)
    - [Installing SDL2 (on Linux)](#installing-sdl2-on-linux)
    - [How to start the game](#how-to-start-the-game)
- [Credits](#credits)

## About the game
**Kino Der Toten : Survive the horror... or die!**

Immerse yourself in a mansion invaded by the undead and live an intense and unique survival experience.  
Kino Der Toten is a 2D game where your goal is simple: survive as long as possible.  
Make your way through hordes of increasingly fierce zombies and sharpen your survivalist skills.

Devastating weapons, powerful power-ups and well-hidden secrets will help you postpone the deadline, but the tension will only increase with each passing minute. Face terrifying bosses in epic fights that will put your nerves to the test.

**Will you be the last survivor?**
**Take up the challenge and prove that you are the best!**

## Main features of the game
* A 2D gameplay
* Waves of zombies increasingly difficult to defeat
* New weapons and power-ups throughout the game
* Intense and thrilling boss fights
* Immersive graphics and soundtrack

## Installation
### Requirements
- [X] Operating System :
    - [X] Windows Vista or later
    - [X] macOS X 10.6 or later
    - [X] Linux
- [X] [Python 3.7 or later](https://www.python.org/downloads/)
- [X] [Pyxel 2.0.6 or later](#installing-pyxel-and-playsound)
- [X] [Playsound 1.3.0 or later](#installing-pyxel-and-playsound)
- [X] [The latest version of SDL2 (for Linux systems)](#installing-sdl2-on-linux)

### Installing Pyxel and Playsound
After installing Python, run the following command in a terminal:
```
pip install --upgrade setuptools wheel
pip install pyxel playsound pygobject
```

### Update Pyxel and Playsound
If you have already installed Pyxel and Playsound, execute the following command in a terminal to update it:
```
pip install --upgrade setuptools wheel pyxel playsound pygobject
```

### Installing SDL2 (on Linux)
If you are using a Linux system, install SDL2 using your package manager:
- apt package manager : `sudo apt-get install libsdl2-dev`  
- dnf package manager : `sudo dnf install SDL2-devel`  
- yum package manager : `yum install SDL2-devel`

### How to start the game
- Download the latest stable version of the game [here](https://github.com/AurelienAudero/KinoDerToten-Projet-Pyxel/releases/latest).
- Unzip the downloaded archive
- Open a terminal in the directory where the game is located
- Execute one of the following commands : `python3 main.py` or `python main.py`

## Credits
- Creators of the game :
    - [Aurélien Audero](https://github.com/AurelienAudero)
    - [Axel Thibert](https://github.com/Oxwerth)
    - [Tony Baca](https://github.com/Thidokachi)
- Acknowledgments :
    - Amine Ouichen *(for the system allowing the shots to go in the direction of the crosshair)*
    - Timothée Ané *(for the system allowing the shots to go in the direction of the crosshair)*

"Kino Der Toten - A Pyxel Game" © 2024 by [Aurélien Audero](https://github.com/AurelienAudero), [Axel Thibert](https://github.com/Oxwerth) and [Tony Baca](https://github.com/Thidokachi) is licensed under [CC BY-NC-ND 4.0](https://github.com/AurelienAudero/KinoDerToten-Projet-Pyxel/blob/main/LICENSE)

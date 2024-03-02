#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Version: Dev 0.1
# Copyright (c) 2024 Aurélien Audero, Axel Thibert and Tony Baca
#
# This file is part of "Kino der toten - A Pyxel Game".
#
# This program is licensed under Attribution-NonCommercial-NoDerivs 4.0 International
# (CC BY-NC-ND 4.0). You should have received a copy of the license along with this
# program; if not, see <https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode>.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of TITLE, MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the CC BY-NC-ND 4.0 License for more details.

def fenetreErreurLibrary(pyxelLibraryStatus:bool, pygameLibraryStatus:bool):
  # Intialisation de la fenêtre et de ses variables
  fenetre = Tk()
  fenetre.title("Kino der toten")
  fenetre.eval('tk::PlaceWindow . center')
  v1 = IntVar(value=1)
  v2 = IntVar(value=1)
  if not pyxelLibraryStatus:
    v1.set(0)
  if not pygameLibraryStatus:
    v2.set(0)

  def learnMoreBtn():
    webbrowserOpen("https://github.com/AurelienAudero/KinoDerToten-Projet-Pyxel/blob/main/README.md")

  # Ajout du contenu à la fenêtre
  Label(fenetre, text="Certains composants requis ne sont pas installé", bg='red').pack()
  Label(fenetre, text="Composants nécéssaires :", anchor="w", justify="left").pack(pady=(10,0), padx=(25,0), fill='both')
  Checkbutton(fenetre, text="Pyxel", variable=v1, anchor="w", justify="left", state="disabled").pack(padx=(25,0), fill='both')
  Checkbutton(fenetre, text="Pygame", variable=v2, anchor="w", justify="left", state="disabled").pack(padx=(25,0), fill='both')
  Label(fenetre, text="Cliquez sur 'En savoir plus'\n pour accéder au guide d'installation").pack(pady=(10,0))
  Button(text="En savoir plus", command=learnMoreBtn).pack()
  Button(text="Quitter", command=fenetre.destroy).pack()

  # Création de la fenêtre
  fenetre.protocol("WM_DELETE_WINDOW")
  fenetre.mainloop()

# Importations des bibliothèques nécéssaires
from webbrowser import open as webbrowserOpen
from sys import argv as sysArgv, exit as sysExit
from os import environ as osEnvVar
osEnvVar['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from time import gmtime, mktime
from random import randint
from tkinter import Tk, Label, Radiobutton, Button, IntVar, messagebox, Scale, HORIZONTAL, Checkbutton, Frame, PhotoImage
pyxelLibraryStatus, pygameLibraryStatus = True, True
try:
  import pyxel
except ImportError:
  pyxelLibraryStatus = False
try:
  from pygame import mixer
except ImportError:
  pygameLibraryStatus = False

if not pyxelLibraryStatus or not pygameLibraryStatus:
  fenetreErreurLibrary(pyxelLibraryStatus, pygameLibraryStatus)
  sysExit()

########################
#   PROGRAMME DU JEU   #
########################
class Personnage:
  def __init__(self, x, y, width, height, keybinds, soundEnabled, controllerSensitivity=None, controllerDeadzone=None):
    # Création de variables
    self.x = x # Position x du personnage
    self.y = y # Position y du personnage
    self.width = width # Largeur du personnage
    self.height = height # Hauteur du personnage
    self.keybinds = keybinds # Méthode d'entrée choisie par l'utilisateur
    self.soundEnabled = soundEnabled # Etat des effets sonores dans le jeu
    self.score = 0 # Score du joueur (valeur int)
    self.scoreTXT = "" # Score du joueur (valeur str)
    self.kills = 0 # Nombre de kills du joueur (valeur int)
    self.killsTXT = "" # Nombre de kills du joueur (valeur str)
    self.pvPerdus = 0 # Points de vie perdus par le joueur (valeur int)
    self.pvPerdusTXT = "" # Points de vie perdus par le joueur (valeur str)
    self.lastSide = "Bottom" # Dernière direction prise par le personnage
    self.numberOfSteps = 1 # Nombre de pas effectués par le personnage depuis le changement de direction
    self.timeBetweenAnimation = 10 # Temps entre chaque changement de sprite (en frames)
    self.currentHP = 100.0 # Points de vie actuels du joueur
    self.maxHP = 100.0 # Points de vie max du joueur
    self.vitesse = 3 # Vitesse de déplacement du personnage
    self.currentPlayerAmmo = 15 # Munitions dans le chargeur de l'arme du joueur
    self.maxPlayerAmmo = 15 # Munitions max dans le chargeur de l'arme du joueur
    self.ammoReloadingStatus = 100 # Etat de rechargement de l'arme du joueur (en % de progression)
    self.ammoReloadingCooldown = 2 # Temps de rechargement de l'arme du joueur (en secondes)
    self.lastShot = 0 # Numéro de frame où le dernier tir à été effectué par le joueur
    self.shotCooldown = 30 # Temps d'attente entre chaque tir (en frames)

    # Détermination des touches pour contrôler le personnage
    if self.keybinds == 1 :
      self.personnageHaut = pyxel.KEY_Z
      self.personnageGauche = pyxel.KEY_Q
      self.personnageBas = pyxel.KEY_S
      self.personnageDroite = pyxel.KEY_D
      self.personnageTir = pyxel.MOUSE_BUTTON_LEFT
      self.personnageRecharger = pyxel.KEY_R
      self.reticule = Reticule(self.x, self.y, self.keybinds)
    elif self.keybinds == 2 :
      self.personnageHaut = pyxel.KEY_W
      self.personnageGauche = pyxel.KEY_A
      self.personnageBas = pyxel.KEY_S
      self.personnageDroite = pyxel.KEY_D
      self.personnageTir = pyxel.MOUSE_BUTTON_LEFT
      self.personnageRecharger = pyxel.KEY_R
      self.reticule = Reticule(self.x, self.y, self.keybinds)
    elif self.keybinds == 3 :
      self.personnageHaut = pyxel.KEY_UP
      self.personnageGauche = pyxel.KEY_LEFT
      self.personnageBas = pyxel.KEY_DOWN
      self.personnageDroite = pyxel.KEY_RIGHT
      self.personnageTir = pyxel.MOUSE_BUTTON_LEFT
      self.personnageRecharger = pyxel.KEY_RSHIFT
      self.reticule = Reticule(self.x, self.y, self.keybinds)
    elif self.keybinds == 4 :
      self.personnageAxeY = pyxel.GAMEPAD1_AXIS_LEFTY
      self.personnageAxeX = pyxel.GAMEPAD1_AXIS_LEFTX
      self.personnageTir = pyxel.GAMEPAD1_BUTTON_A
      self.personnageRecharger = pyxel.GAMEPAD1_BUTTON_X
      self.controllerSensitivity = controllerSensitivity
      self.controllerDeadzone = controllerDeadzone
      self.reticule = Reticule(self.x, self.y, self.keybinds, self.controllerSensitivity, self.controllerDeadzone)
    elif self.keybinds == 5 :
      self.personnageHaut = pyxel.GAMEPAD1_BUTTON_DPAD_UP
      self.personnageGauche = pyxel.GAMEPAD1_BUTTON_DPAD_LEFT
      self.personnageBas = pyxel.GAMEPAD1_BUTTON_DPAD_DOWN
      self.personnageDroite = pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT
      self.personnageTir = pyxel.GAMEPAD1_BUTTON_A
      self.personnageRecharger = pyxel.GAMEPAD1_BUTTON_X
      self.controllerSensitivity = controllerSensitivity
      self.controllerDeadzone = controllerDeadzone
      self.reticule = Reticule(self.x, self.y, self.keybinds, self.controllerSensitivity, self.controllerDeadzone)

  def move(self):
    # Contrôles avec les boutons du clavier ou de la manette
    if (self.keybinds != 4) and (self.keybinds != 5):
      # Déplacement vers le haut
      if pyxel.btn(self.personnageHaut) and not pyxel.btn(self.personnageGauche) and not pyxel.btn(self.personnageDroite) and (self.y > 0) :
          self.y -= self.vitesse
          if self.lastSide != "Top":
            self.lastSide = "Top"
            self.numberOfSteps = 1
          else:
            if pyxel.frame_count % self.timeBetweenAnimation == 0:
              if self.numberOfSteps == 5:
                self.numberOfSteps = 1
              else:
                self.numberOfSteps += 1
      # Déplacement vers la gauche
      if pyxel.btn(self.personnageGauche) and not pyxel.btn(self.personnageHaut) and not pyxel.btn(self.personnageBas) and (self.x > 0) :
          self.x -= self.vitesse
          if self.lastSide != "Left":
            self.lastSide = "Left"
            self.numberOfSteps = 1
          else:
            if pyxel.frame_count % self.timeBetweenAnimation == 0:
              if self.numberOfSteps == 5:
                self.numberOfSteps = 1
              else:
                self.numberOfSteps += 1
      # Déplacement vers le bas
      if pyxel.btn(self.personnageBas) and not pyxel.btn(self.personnageGauche) and not pyxel.btn(self.personnageDroite) and (self.y < resHauteur-self.height) :
          self.y += self.vitesse
          if self.lastSide != "Bottom":
            self.lastSide = "Bottom"
            self.numberOfSteps = 1
          else:
            if pyxel.frame_count % self.timeBetweenAnimation == 0:
              if self.numberOfSteps == 4:
                self.numberOfSteps = 1
              else:
                self.numberOfSteps += 1
      # Déplacement vers la droite
      if pyxel.btn(self.personnageDroite) and not pyxel.btn(self.personnageHaut) and not pyxel.btn(self.personnageBas) and (self.x < resLongueur-self.width) :
          self.x += self.vitesse
          if self.lastSide != "Right":
            self.lastSide = "Right"
            self.numberOfSteps = 1
          else:
            if pyxel.frame_count % self.timeBetweenAnimation == 0:
              if self.numberOfSteps == 5:
                self.numberOfSteps = 1
              else:
                self.numberOfSteps += 1
      # Déplacement en diagonale haut-gauche
      if pyxel.btn(self.personnageHaut) and not pyxel.btn(self.personnageBas) and pyxel.btn(self.personnageGauche) and not pyxel.btn(self.personnageDroite) :
        if self.x > 0:
          self.x -= self.vitesse/1.5
        if self.y > 0:
          self.y -= self.vitesse/1.5
        if self.lastSide != "Left":
          self.lastSide = "Left"
          self.numberOfSteps = 1
        else:
          if pyxel.frame_count % self.timeBetweenAnimation == 0:
            if self.numberOfSteps == 5:
              self.numberOfSteps = 1
            else:
              self.numberOfSteps += 1
      # Déplacement en diagonale haut-droite
      if pyxel.btn(self.personnageHaut) and not pyxel.btn(self.personnageBas) and not pyxel.btn(self.personnageGauche) and pyxel.btn(self.personnageDroite) :
        if self.x < resLongueur-self.width:
          self.x += self.vitesse/1.5
        if self.y > 0:
          self.y -= self.vitesse/1.5
        if self.lastSide != "Right":
          self.lastSide = "Right"
          self.numberOfSteps = 1
        else:
          if pyxel.frame_count % self.timeBetweenAnimation == 0:
            if self.numberOfSteps == 5:
              self.numberOfSteps = 1
            else:
              self.numberOfSteps += 1
      # Déplacement en diagonale bas-gauche
      if pyxel.btn(self.personnageBas) and not pyxel.btn(self.personnageHaut) and pyxel.btn(self.personnageGauche) and not pyxel.btn(self.personnageDroite) :
        if self.x > 0:
          self.x -= self.vitesse/1.5
        if self.y < resHauteur-self.height:
          self.y += self.vitesse/1.5
        if self.lastSide != "Left":
          self.lastSide = "Left"
          self.numberOfSteps = 1
        else:
          if pyxel.frame_count % self.timeBetweenAnimation == 0:
            if self.numberOfSteps == 5:
              self.numberOfSteps = 1
            else:
              self.numberOfSteps += 1
      # Déplacement en diagonale bas-droite
      if pyxel.btn(self.personnageBas) and not pyxel.btn(self.personnageHaut) and not pyxel.btn(self.personnageGauche) and pyxel.btn(self.personnageDroite) :
        if self.x < resLongueur-self.width:
          self.x += self.vitesse/1.5
        if self.y < resHauteur-self.height:
          self.y += self.vitesse/1.5
        if self.lastSide != "Right":
          self.lastSide = "Right"
          self.numberOfSteps = 1
        else:
          if pyxel.frame_count % self.timeBetweenAnimation == 0:
            if self.numberOfSteps == 5:
              self.numberOfSteps = 1
            else:
              self.numberOfSteps += 1      
      # Tir
      if pyxel.btnp(self.personnageTir):
        if self.currentPlayerAmmo > 0:
          if self.soundEnabled:
            pyxel.play(0, 0, loop=False) # Sound effect du tir (si les effets sonores sont activés)
          return self.x+(self.width/2), self.y+(self.height/2)
        elif self.currentPlayerAmmo == 0:
          if self.soundEnabled:
            pyxel.play(0, 4, loop=False) # Sound effect du chargeur de l'arme vide (si les effets sonores sont activés)
          return None
      # Recharger
      if pyxel.btnp(self.personnageRecharger) and (self.ammoReloadingStatus == 100) and (self.currentPlayerAmmo < self.maxPlayerAmmo):
        if self.soundEnabled:
          pyxel.play(0, 3, loop=False) # Sound effect du rechargement de l'arme (si les effets sonores sont activés)
        self.ammoReloadingStatus = 0
        self.currentPlayerAmmo = 0
    
    # Contrôles avec les sticks analogiques de la manette
    elif (self.keybinds == 4) or (self.keybinds == 5):
      if pyxel.btnv(self.personnageAxeY) < -self.controllerDeadzone and (self.y > 0) :
          self.y -= self.vitesse
          if self.lastSide != "Top":
            self.lastSide = "Top"
            self.numberOfSteps = 1
          else:
            if pyxel.frame_count % self.timeBetweenAnimation == 0:
              if self.numberOfSteps == 5:
                self.numberOfSteps = 1
              else:
                self.numberOfSteps += 1
      if pyxel.btnv(self.personnageAxeX) < -self.controllerDeadzone and (self.x > 0) :
          self.x -= self.vitesse
          if self.lastSide != "Left":
            self.lastSide = "Left"
            self.numberOfSteps = 1
          else:
            if pyxel.frame_count % self.timeBetweenAnimation == 0:
              if self.numberOfSteps == 5:
                self.numberOfSteps = 1
              else:
                self.numberOfSteps += 1
      if pyxel.btnv(self.personnageAxeY) > self.controllerDeadzone and (self.y < resHauteur-self.height) :
          self.y += self.vitesse
          if self.lastSide != "Bottom":
            self.lastSide = "Bottom"
            self.numberOfSteps = 1
          else:
            if pyxel.frame_count % self.timeBetweenAnimation == 0:
              if self.numberOfSteps == 4:
                self.numberOfSteps = 1
              else:
                self.numberOfSteps += 1
      if pyxel.btnv(self.personnageAxeX) > self.controllerDeadzone and (self.x < resLongueur-self.width) :
          self.x += self.vitesse
          if self.lastSide != "Right":
            self.lastSide = "Right"
            self.numberOfSteps = 1
          else:
            if pyxel.frame_count % self.timeBetweenAnimation == 0:
              if self.numberOfSteps == 5:
                self.numberOfSteps = 1
              else:
                self.numberOfSteps += 1
      if pyxel.btnp(self.personnageTir):
        if self.currentPlayerAmmo > 0:
          if self.soundEnabled:
            pyxel.play(0, 0, loop=False) # Sound effect du tir (si les effets sonores sont activés)
          return self.x+(self.width/2), self.y+(self.height/2)
        elif self.currentPlayerAmmo == 0:
          if self.soundEnabled:
            pyxel.play(0, 4, loop=False) # Sound effect du chargeur de l'arme vide (si les effets sonores sont activés)
          return None
      if pyxel.btnp(self.personnageRecharger) and (self.ammoReloadingStatus == 100) and (self.currentPlayerAmmo < self.maxPlayerAmmo):
        if self.soundEnabled:
          pyxel.play(0, 3, loop=False) # Sound effect du rechargement de l'arme (si les effets sonores sont activés)
        self.ammoReloadingStatus = 0
        self.currentPlayerAmmo = 0
    
    return None
          
  def draw(self):
    if self.lastSide == "Left":
      if self.numberOfSteps == 1:
        pyxel.blt(self.x, self.y, 1, 0, 60, self.width, self.height, 7)
      elif self.numberOfSteps == 2:
        pyxel.blt(self.x, self.y, 1, 40, 60, self.width, self.height, 7)
      elif self.numberOfSteps == 3:
        pyxel.blt(self.x, self.y, 1, 80, 60, self.width, self.height, 7)
      elif self.numberOfSteps == 4:
        pyxel.blt(self.x, self.y, 1, 120, 60, self.width, self.height, 7)
      elif self.numberOfSteps == 5:
        pyxel.blt(self.x, self.y, 1, 160, 60, self.width, self.height, 7)
    elif self.lastSide == "Right":
      if self.numberOfSteps == 1:
        pyxel.blt(self.x, self.y, 1, 0, 0, self.width, self.height, 7)
      elif self.numberOfSteps == 2:
        pyxel.blt(self.x, self.y, 1, 40, 0, self.width, self.height, 7)
      elif self.numberOfSteps == 3:
        pyxel.blt(self.x, self.y, 1, 80, 0, self.width, self.height, 7)
      elif self.numberOfSteps == 4:
        pyxel.blt(self.x, self.y, 1, 120, 0, self.width, self.height, 7)
      elif self.numberOfSteps == 5:
        pyxel.blt(self.x, self.y, 1, 160, 0, self.width, self.height, 7)
    elif self.lastSide == "Top":
      if self.numberOfSteps == 1:
        pyxel.blt(self.x, self.y, 1, 0, 115, self.width, self.height, 7)
      elif self.numberOfSteps == 2:
        pyxel.blt(self.x, self.y, 1, 40, 115, self.width, self.height, 7)
      elif self.numberOfSteps == 3:
        pyxel.blt(self.x, self.y, 1, 80, 115, self.width, self.height, 7)
      elif self.numberOfSteps == 4:
        pyxel.blt(self.x, self.y, 1, 120, 115, self.width, self.height, 7)
      elif self.numberOfSteps == 5:
        pyxel.blt(self.x, self.y, 1, 160, 115, self.width, self.height, 7)
    elif self.lastSide == "Bottom":
      if self.numberOfSteps == 1:
        pyxel.blt(self.x, self.y, 1, 0, 170, self.width, self.height, 7)
      elif self.numberOfSteps == 2:
        pyxel.blt(self.x, self.y, 1, 40, 170, self.width, self.height, 7)
      elif self.numberOfSteps == 3:
        pyxel.blt(self.x, self.y, 1, 80, 170, self.width, self.height, 7)
      elif self.numberOfSteps == 4:
        pyxel.blt(self.x, self.y, 1, 120, 170, self.width, self.height, 7)
    if debug:
      if debug1: 
        pyxel.rectb(self.x, self.y, self.width, self.height, 8) # Affichage de la hitbox du personnage (si activé dans le debug)

class Reticule:
  def __init__(self, x, y, keybinds, controllerSensitivity=None, controllerDeadzone=None):
    self.x = x # Position en x du réticule
    self.y = y # Position en y du réticule
    self.size = 31 # Taille du réticule
    self.keybinds = keybinds # Méthode d'entrée choisie par l'utilisateur
    
    # Sensibilité et deadzone de la manette
    if (self.keybinds == 4) or (self.keybinds == 5): 
      self.controllerSensitivity = controllerSensitivity
      self.controllerDeadzone = controllerDeadzone
  
  def move(self):
    if (self.keybinds != 4) and (self.keybinds != 5):
      self.x = pyxel.mouse_x
      self.y = pyxel.mouse_y
    elif (self.keybinds == 4) or (self.keybinds == 5):
      if pyxel.btnv(pyxel.GAMEPAD1_AXIS_RIGHTX) < -self.controllerDeadzone and (self.x > 0):
        self.x -= self.controllerSensitivity
      if pyxel.btnv(pyxel.GAMEPAD1_AXIS_RIGHTX) > self.controllerDeadzone and (self.x < resLongueur-self.size):
        self.x += self.controllerSensitivity
      if pyxel.btnv(pyxel.GAMEPAD1_AXIS_RIGHTY) < -self.controllerDeadzone and (self.y > 0):
        self.y -= self.controllerSensitivity
      if pyxel.btnv(pyxel.GAMEPAD1_AXIS_RIGHTY) > self.controllerDeadzone and (self.y < resHauteur-self.size):
        self.y += self.controllerSensitivity
  
  def draw(self):
    pyxel.blt(self.x, self.y, 0, 0, 72, self.size, self.size, 0)

class Tir:
  def __init__(self, x, y, personnage):
    self.x = x
    self.y = y
    self.width = 10
    self.height = 10
    self.radius = 5
    self.alive = True
    self.viseur_x = personnage.reticule.x
    self.viseur_y = personnage.reticule.y
    self.player_x = personnage.x
    self.player_y = personnage.y

  def checkCoordonnees(self, player_x, player_y):
    """
    Détermine la direction du tir par rapport à la position du joueur.

    Args:
        player_x: La position x du joueur.
        player_y: La position y du joueur.

    Returns:
        La fonction retourne deux booléens correspondant à la direction du tir par rapport à la position du joueur.
    """
    if self.viseur_x > player_x:
      coord_x = True
    else :
      coord_x = False
    
    if self.viseur_y > player_y:
      coord_y = True
    else :
      coord_y = False
    
    return coord_x, coord_y

  def move(self):
    direction_x,direction_y = self.checkCoordonnees(self.player_x,self.player_y)
    distance_x = abs(self.viseur_x - self.player_x)/30
    distance_y = abs(self.viseur_y - self.player_y)/30

    if direction_x:
      self.x += distance_x
    else:
      self.x -= distance_x

    if direction_y:
      self.y += distance_y
    else:
      self.y -= distance_y

  def draw(self):
    pyxel.circ(self.x, self.y, self.radius, 10)
    if debug:
      if debug3:
        pyxel.rectb(self.x, self.y, self.width, self.height, 8) # Affichage de la hitbox du tir (si activé dans le debug)

class Zombie:
  def __init__(self, x, y, width, height, vitesse, personnage):
    self.x = x # Position en x du zombie
    self.y = y # Position en y du zombie
    self.width = width # Largeur du zombie
    self.height = height # Hauteur du zombie
    self.vitesse = vitesse # Vitesse de déplacement du zombie
    self.alive = True # Etat du zombie
    self.lastSide = "Bottom" # Dernière direction prise par le zombie
    self.timeBetweenAnimation = 10 # Temps entre chaque changement de sprite (en frames)
    self.numberOfSteps = 1 # Nombre de pas effectués par le zombie depuis le changement de direction
    self.personnage = personnage # Personnage joueur

  def move(self):
    if (self.y > 0) and (self.y > self.personnage.y) :
      self.y -= self.vitesse
      if self.lastSide != "Top":
        self.lastSide = "Top"
        self.numberOfSteps = 1
      else:
        if pyxel.frame_count % self.timeBetweenAnimation == 0:
          if self.numberOfSteps == 3:
            self.numberOfSteps = 1
          else:
            self.numberOfSteps += 1
    if (self.x > 0) and (self.x > self.personnage.x) :
      self.x -= self.vitesse
      if self.lastSide != "Left":
        self.lastSide = "Left"
        self.numberOfSteps = 1
      else:
        if pyxel.frame_count % self.timeBetweenAnimation == 0:
          if self.numberOfSteps == 5:
            self.numberOfSteps = 1
          else:
            self.numberOfSteps += 1
    if (self.y < resHauteur-self.height) and (self.y < self.personnage.y):
      self.y += self.vitesse
      if self.lastSide != "Bottom":
        self.lastSide = "Bottom"
        self.numberOfSteps = 1
      else:
        if pyxel.frame_count % self.timeBetweenAnimation == 0:
          if self.numberOfSteps == 3:
            self.numberOfSteps = 1
          else:
            self.numberOfSteps += 1
    if (self.x < resLongueur-self.width) and (self.x < self.personnage.x):
      self.x += self.vitesse
      if self.lastSide != "Right":
        self.lastSide = "Right"
        self.numberOfSteps = 1
      else:
        if pyxel.frame_count % self.timeBetweenAnimation == 0:
          if self.numberOfSteps == 5:
            self.numberOfSteps = 1
          else:
            self.numberOfSteps += 1

  def draw(self): 
    if self.lastSide == "Left":
      if self.numberOfSteps == 1:
        pyxel.blt(self.x, self.y, 2, 5, 61, self.width, self.height, 7)
      elif self.numberOfSteps == 2:
        pyxel.blt(self.x, self.y, 2, 46, 61, self.width, self.height, 7)
      elif self.numberOfSteps == 3:
        pyxel.blt(self.x, self.y, 2, 87, 61, self.width, self.height, 7)
      elif self.numberOfSteps == 4:
        pyxel.blt(self.x, self.y, 2, 128, 61, self.width, self.height, 7)
      elif self.numberOfSteps == 5:
        pyxel.blt(self.x, self.y, 2, 169, 61, self.width, self.height, 7)
    elif self.lastSide == "Right":
      if self.numberOfSteps == 1:
        pyxel.blt(self.x, self.y, 2, 5, 5, self.width, self.height, 7)
      elif self.numberOfSteps == 2:
        pyxel.blt(self.x, self.y, 2, 46, 5, self.width, self.height, 7)
      elif self.numberOfSteps == 3:
        pyxel.blt(self.x, self.y, 2, 87, 5, self.width, self.height, 7)
      elif self.numberOfSteps == 4:
        pyxel.blt(self.x, self.y, 2, 128, 5, self.width, self.height, 7)
      elif self.numberOfSteps == 5:
        pyxel.blt(self.x, self.y, 2, 169, 5, self.width, self.height, 7)
    elif self.lastSide == "Top":
      if self.numberOfSteps == 1:
        pyxel.blt(self.x, self.y, 2, 5, 119, self.width, self.height, 7)
      elif self.numberOfSteps == 2:
        pyxel.blt(self.x, self.y, 2, 45, 119, self.width, self.height, 7)
      elif self.numberOfSteps == 3:
        pyxel.blt(self.x, self.y, 2, 85, 119, self.width, self.height, 7)
    elif self.lastSide == "Bottom":
      if self.numberOfSteps == 1:
        pyxel.blt(self.x, self.y, 2, 5, 174, self.width, self.height, 7)
      elif self.numberOfSteps == 2:
        pyxel.blt(self.x, self.y, 2, 45, 174, self.width, self.height, 7)
      elif self.numberOfSteps == 3:
        pyxel.blt(self.x, self.y, 2, 85, 174, self.width, self.height, 7)
    if debug:
      if debug2:
        pyxel.rectb(self.x, self.y, self.width, self.height, 8) # Affichage de la hitbox du zombie (si activé dans le debug)

class Jeu:
  def __init__(self, l, h, fps, keybinds, musicEnabled, soundEnabled, controllerSensitivity=None, controllerDeadzone=None):
    pyxel.init(l, h, title="Kino der toten", fps=fps, quit_key=pyxel.KEY_NONE) # Initialisation de la fenêtre de jeu
    pyxel.load("KinoDerToten.pyxres") # Chargement des ressources du jeu
    self.keybinds = keybinds # Méthode d'entrée choisie par l'utilisateur
    self.musicEnabled = musicEnabled # Etat de la musique dans le jeu
    if self.musicEnabled: # Si la musique est activée
      mixer.init() # Initialisation du module mixer de la bibliothèque Pygame
      mixer.music.load('KinoDerTotenOST.mp3') # Chargement de la musique du jeu
    self.partieTermineeMusicInitiated = False # Etat de l'initialisation de la musique de l'écran Game Over
    self.soundEnabled = soundEnabled # Etat des effets sonores dans le jeu
    if (self.keybinds == 4) or (self.keybinds == 5):
      self.controllerSensitivity = controllerSensitivity # Sensibilité des sticks analogiques de la manette (si jeu sur manette)
      self.controllerDeadzone = controllerDeadzone # Zone morte des sticks analogiques de la manette (si jeu sur manette)
    self.start() # Démarrage du jeu
    if debug:
      if debug4: # Compteur de FPS (si activé dans le debug)
        self.previousFPSTime = mktime(gmtime()) # Timestamp pour compter le nombre de frames en une seconde
        self.previousFPSFrame = 0 # Nombre de frame au début de la seconde (Initialisation : 1ère frame = frame 0)
        self.currentFPS = 0 # Initialisation du compteur de FPS
    pyxel.run(self.update, self.draw) # Démarrage de la boucle principale du jeu

  def start(self):
    """
    Initialise les variables du jeu au début de la partie.

    Args:
        keybinds: Le type de contrôles choisi par le joueur.
        controllerSensitivity: La sensibilité des sticks analogiques de la manette (facultatif).
        controllerDeadzone: La zone morte des sticks analogiques de la manette (facultatif).

    Returns:
        La fonction ne retourne rien mais opère des changements sur les variables de la classe.
    """
    # Initialisation du personnage joueur
    if (self.keybinds == 4) or (self.keybinds == 5):
      self.personnage = Personnage(450, 210, 40, 50, self.keybinds, self.soundEnabled, self.controllerSensitivity, self.controllerDeadzone) # Si le joueur joue à la manette
    else:
      self.personnage = Personnage(450, 210, 40, 50, self.keybinds, self.soundEnabled) # Si le joueur joue au clavier et à la souris
    
    self.zombiesList = [] # Liste de tous les zombies
    self.tirsList = [] # Liste de tous les tirs
    self.nbVagues = 0 # Nombre de vagues de zombies
    self.nbVaguesTXT = "" # Nombre de vagues de zombies en texte
    self.tempsSpawnMobActuel = 0 # Initialisation de la variable de temps entre chaque spawn de mob
    self.tempsSpawnMobBase = 5 # Temps entre chaque spawn de mob (en secondes)
    self.gainScoreKill = 10 # Nombre de points de score gagné en faisant un kill
    self.perteHP = 0.5 # Nombre de points de vie perdus au contact d'un zombie
    self.partieTerminee = False # Etat de la partie en cours
    self.gameOverChosenBtn = 1 # Bouton choisi sur l'écran "Game Over" lors du contrôle à la manette
    self.nbZombiesTotal = 0 # Nombre total de zombies tués
    self.nbZombiesVagueActuelle = 0 # Nombre de zombies tués dans la vague actuelle
    self.nbZombiesPourTerminerVague = 20 # Nombre de zombies à tuer pour terminer une vague
    self.tempsAttenteNouvelleVague = 15 # Temps d'attente avant le début de la prochaine vague (en secondes)
    self.startNewWave() # Démarrage de la première vague
    pyxel.mouse(False) # Désactive le curseur de la souris
    pyxel.images[1].load(0,0, "RichtofenSpriteSheet.png") # Chargement des sprites de Richtofen (joueur)
    pyxel.images[2].load(0,0, "ZombieSpriteSheet.png") # Chargement des sprites des zombies (ennemis)
    if self.musicEnabled:
      pyxel.stop(1) # Arrêt de la musique de l'écran Game Over
      self.partieTermineeMusicInitiated = False # Réinitialisation de l'état de l'initialisation de la musique de l'écran Game Over
      mixer.music.play() # Lecture de la musique du jeu

  def startNewWave(self):
    """
    Démarre une nouvelle vague de zombies.

    Args:
        Aucun argument n'est requis.

    Returns:
        La fonction ne retourne rien mais opère des changements sur les variables de la classe.
    """
    self.tempsSpawnMobActuel = 3600 # Arrêt du spawn des zombies
    self.zombiesList = [] # Suppression de tous les zombies
    self.nbVagues += 1 # Incrémentation du nombre de vagues
    self.nbZombiesVagueActuelle = 0 # Réinitialisation du nombre de zombies tués dans la vague actuelle
    if self.nbVagues != 1:
      self.nbZombiesPourTerminerVague += 5 # Incrémentation du nombre de zombies à tuer pour terminer une vague (sauf à la première vague)
      self.personnage.maxHP += 10 # Incrémentation des points de vie max du joueur (sauf à la première vague)
    self.personnage.currentHP = self.personnage.maxHP # Régénération complète des points de vie du joueur 
    if self.soundEnabled:
      pyxel.play(0, 1, loop=False) # Sound effect du début de la vague (si les effets sonores sont activés)
      
    # Début du temps de pause avant le début de la prochaine vague
    self.tempsAttenteStartFrame = pyxel.frame_count
    self.attenteNouvelleVague = True
  
  def screenTextPrint(self, x, y, text):
    """
    Affiche un texte sur l'écran aux coordonnées indiquées.

    Args:
        x: Le coordonnée x de l'écran où afficher le texte.
        y: Le coordonnée y de l'écran où afficher le texte.
        text: Le texte a afficher.

    Returns:
        La fonction ne retourne rien mais affiche le texte à l'écran en utilisant la bibliothèque Pyxel.
    """
    assert type(text) == str, "text doit être une chaîne de caractères"
    for i in range(len(text)):
        if text[i] == "1":
          pyxel.blt(x+(16*i), y, 0, 0, 24, 11, 19, 0) # Affichage du chiffre 1
        elif text[i] == "2":
          pyxel.blt(x+(16*i), y, 0, 16, 24, 11, 19, 0) # Affichage du chiffre 2
        elif text[i] == "3":
          pyxel.blt(x+(16*i), y, 0, 32, 24, 11, 19, 0) # Affichage du chiffre 3
        elif text[i] == "4":
          pyxel.blt(x+(16*i), y, 0, 48, 24, 11, 19, 0) # Affichage du chiffre 4
        elif text[i] == "5":
          pyxel.blt(x+(16*i), y, 0, 64, 24, 11, 19, 0) # Affichage du chiffre 5
        elif text[i] == "6":
          pyxel.blt(x+(16*i), y, 0, 80, 24, 11, 19, 0) # Affichage du chiffre 6
        elif text[i] == "7":
          pyxel.blt(x+(16*i), y, 0, 96, 24, 11, 19, 0) # Affichage du chiffre 7
        elif text[i] == "8":
          pyxel.blt(x+(16*i), y, 0, 112, 24, 11, 19, 0) # Affichage du chiffre 8
        elif text[i] == "9":
          pyxel.blt(x+(16*i), y, 0, 128, 24, 11, 19, 0) # Affichage du chiffre 9
        elif text[i] == "0":
          pyxel.blt(x+(16*i), y, 0, 144, 24, 11, 19, 0) # Affichage du chiffre 0
        elif text[i] == ".":
          pyxel.blt(x+(16*i), y, 0, 158, 24, 11, 19, 0) # Affichage de la virgule
        elif text[i] == "/":
          pyxel.blt(x+(16*i), y, 0, 170, 24, 11, 19, 0) # Affichage de la virgule

  def update(self): 
    if not self.partieTerminee:
      # Touche pour quitter le jeu
      if pyxel.btnp(pyxel.KEY_ESCAPE):
        if gameQuitConfirmationWindow():
          pyxel.quit()

      # Vérifie si le joueur est mort
      if self.personnage.currentHP <= 0:
        if self.musicEnabled:
          mixer.music.stop()
        self.partieTerminee = True
      
      # Déplacement du réticule de visée
      self.personnage.reticule.move()

      # Déplacement du personnage joueur
      v = self.personnage.move()
      
      # Création d'un tir si le joueur appuie sur la touche de tir
      if (v is not None) and (pyxel.frame_count-self.personnage.lastShot > self.personnage.shotCooldown):
        self.personnage.lastShot = pyxel.frame_count
        self.personnage.currentPlayerAmmo -= 1
        self.tirsList.append(Tir(v[0], v[1], self.personnage))

      # Déplacement des tirs existants et suppression des tirs terminés
      for element in self.tirsList:
        element.move()
        if not element.alive:
          self.tirsList.remove(element)

      # Démarrage d'une nouvelle vague
      if self.nbZombiesVagueActuelle == self.nbZombiesPourTerminerVague:
        self.startNewWave()
        
      # Temps d'attente avant le début de la prochaine vague
      if self.attenteNouvelleVague:
        if self.tempsAttenteStartFrame + (fps*self.tempsAttenteNouvelleVague) == pyxel.frame_count:
          self.attenteNouvelleVague = False
          self.tempsSpawnMobActuel = self.tempsSpawnMobBase - 1
      
      # Temps d'attente pour le rechargement de l'arme du joueur
      if self.personnage.ammoReloadingStatus < 100:
        if self.personnage.ammoReloadingStatus + (100/(fps*self.personnage.ammoReloadingCooldown)) <= 100:
          self.personnage.ammoReloadingStatus += 100/(fps*self.personnage.ammoReloadingCooldown)
        else:
          self.personnage.ammoReloadingStatus = 100
          self.personnage.currentPlayerAmmo = self.personnage.maxPlayerAmmo

      # Détéction de la superposition de deux entités
      def isOverlapping(entity1, entity2):
        if entity1.x+entity1.width > entity2.x and entity2.x+entity2.width > entity1.x and entity1.y+entity1.height > entity2.y and entity2.y+entity2.height > entity1.y:
          return True

      # Résolution de la superposition de deux entités (par le déplacement)
      def resolveOverlap(entity1, entity2):
        # Calculer la direction de la superposition
        dx = entity1.x - entity2.x
        dy = entity1.y - entity2.y

        # Normaliser la direction
        distance = (dx**2 + dy**2)**0.5

        # Si la distance est zéro, sortir de la fonction (pour éviter la division par zéro)
        if distance == 0:
          return

        dx /= distance
        dy /= distance

        # Déplacer les zombies dans la direction opposée à la superposition
        overlap = 0.5 * (distance - entity1.width - entity2.width)
        entity1.x -= overlap * dx
        entity1.y -= overlap * dy
        entity2.x += overlap * dx
        entity2.y += overlap * dy

      # Déplacement des zombies en vie et suppression des zombies morts
      for element in self.zombiesList:
        element.move()
        if not element.alive:
          self.zombiesList.remove(element)

      for i in range(len(self.zombiesList)):
        for j in range(len(self.zombiesList)):
          if i != j and isOverlapping(self.zombiesList[i], self.zombiesList[j]):
            resolveOverlap(self.zombiesList[i], self.zombiesList[j])

      # Dégâts des zombies sur le joueur
      for ennemi in self.zombiesList:
        if isOverlapping(self.personnage, ennemi):
          if self.soundEnabled:
            pyxel.play(0, 2, loop=False) # Sound effect de la perte de point de vie (si les effets sonores sont activés)
          self.personnage.currentHP -= self.perteHP
          self.personnage.pvPerdus += self.perteHP

      # Collisions entre zombies et tirs
      for ennemi in self.zombiesList:
        for tir in self.tirsList:
          if ennemi.x+ennemi.width > tir.x and tir.x+tir.width > ennemi.x and ennemi.y+ennemi.height > tir.y and tir.y+tir.height > ennemi.y:
            self.tirsList.remove(tir)
            self.zombiesList.remove(ennemi)
            self.personnage.score += self.gainScoreKill
            self.personnage.kills += 1
            self.nbZombiesVagueActuelle += 1
            self.nbZombiesTotal += 1

      # Spawn aléatoire des zombies
      if debug:
        if not debug5:
          if pyxel.frame_count % (fps*self.tempsSpawnMobActuel) == 0:
            numeroSpawner = randint(1,3)
            if numeroSpawner == 1:
              self.zombiesList.append(Zombie(200, 15, 38, 51, 1, self.personnage))
            elif numeroSpawner == 2:
              self.zombiesList.append(Zombie(432, 15, 38, 51, 1, self.personnage))
            elif numeroSpawner == 3:
              self.zombiesList.append(Zombie(664, 15, 38, 51, 1, self.personnage))
      else:
        if pyxel.frame_count % (fps*self.tempsSpawnMobActuel) == 0:
          numeroSpawner = randint(1,3)
          if numeroSpawner == 1:
            self.zombiesList.append(Zombie(200, 15, 38, 51, 1, self.personnage))
          elif numeroSpawner == 2:
            self.zombiesList.append(Zombie(432, 15, 38, 51, 1, self.personnage))
          elif numeroSpawner == 3:
            self.zombiesList.append(Zombie(664, 15, 38, 51, 1, self.personnage))
    
    elif self.partieTerminee:
      if self.musicEnabled and not self.partieTermineeMusicInitiated:
        self.partieTermineeMusicInitiated = True
        pyxel.play(1, 5, loop=True) # Lecture du sound effect de game over (si les effets sonores sont activés)
      self.personnage.scoreTXT = str(self.personnage.score) # Transforme le score du joueur en texte (INT -> STR)
      self.personnage.killsTXT = str(self.personnage.kills) # Transforme le nombre de kills du joueur en texte (INT -> STR)
      self.personnage.pvPerdusTXT = str(self.personnage.pvPerdus) # Transforme le nombre de PV perdus du joueur en texte (INT -> STR)
      self.nbVaguesTXT = str(self.nbVagues) # Transforme le nombre de vagues en texte (INT -> STR)
      if self.personnage.keybinds == 4 or self.personnage.keybinds == 5 or self.personnage.keybinds == 6:
        if pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT) or pyxel.btnv(pyxel.GAMEPAD1_AXIS_LEFTX) > self.personnage.controllerDeadzone:
          self.gameOverChosenBtn = 2
        elif pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT) or pyxel.btnv(pyxel.GAMEPAD1_AXIS_LEFTX) < -self.personnage.controllerDeadzone:
          self.gameOverChosenBtn = 1
        
        # Clic sur le bouton "Rejouer"
        if self.gameOverChosenBtn == 1 and pyxel.btn(self.personnage.personnageTir):
          self.start()
        
        # Clic sur le bouton "Quitter"
        elif self.gameOverChosenBtn == 2 and pyxel.btn(self.personnage.personnageTir):
          pyxel.quit()
      else:
        # Clic sur le bouton "Rejouer"
        if pyxel.mouse_x > 325 and pyxel.mouse_x < 430 and pyxel.mouse_y > 400 and pyxel.mouse_y < 435 and pyxel.btn(self.personnage.personnageTir):
          self.start()
        
        # Clic sur le bouton "Quitter"
        elif pyxel.mouse_x > 525 and pyxel.mouse_x < 621 and pyxel.mouse_y > 400 and pyxel.mouse_y < 435 and pyxel.btn(self.personnage.personnageTir):
          pyxel.quit()

      # Clic sur le bouton "GitHub"
      if pyxel.mouse_x > 875 and pyxel.mouse_x < 960 and pyxel.mouse_y > 510 and pyxel.mouse_y < 540 and pyxel.btn(self.personnage.personnageTir):
        webbrowserOpen("https://github.com/AurelienAudero/KinoDerToten-Projet-Pyxel")
    
    # Calcul du nombre d'images par seconde affichées
    if debug:
      if debug4:
        if mktime(gmtime()) - self.previousFPSTime == 1:
          self.previousFPSTime += 1
          self.currentFPS = pyxel.frame_count - self.previousFPSFrame
          self.previousFPSFrame = pyxel.frame_count
      if debug7:
        if pyxel.frame_count % (fps*1) == 0:
          print("Reticule : {}, {}".format(str(self.personnage.reticule.x), str(self.personnage.reticule.y)))

  def draw(self):
    if not self.partieTerminee:
      # Efface l'écran
      pyxel.cls(5)

      # Affichage de la map
      if debug:
        if not debug6:
          pyxel.bltm(0, 0, 0, 0, 0, resLongueur, resHauteur)
      else:
        pyxel.bltm(0, 0, 0, 0, 0, resLongueur, resHauteur)

      # Affichage de la hitbox des trois spawners de zombies (si activé dans le debug)
      if debug:
        if debug8:
          pyxel.rectb(200, 15, 40, 50, 8)
          pyxel.rectb(432, 15, 40, 50, 8)
          pyxel.rectb(664, 15, 40, 50, 8)
      
      # Affichage des tirs
      for element in self.tirsList:
        element.draw()

      # Affichage des zombies
      for element in self.zombiesList:
        element.draw()

      # Affichage du personnage joueur
      self.personnage.draw()

      # Affichage du réticule de visée
      self.personnage.reticule.draw()

      # Affiche le score actuel du joueur
      pyxel.blt(15, 20, 0, 0, 0, 89, 19, 0) # Affiche le texte "Score :"
      self.personnage.scoreTXT = str(self.personnage.score) # Transforme le score du joueur en texte (INT -> STR)
      self.screenTextPrint(120, 20, self.personnage.scoreTXT)

      # Affiche le numéro de vague actuel
      pyxel.blt(15, 45, 0, 0, 48, 91, 19, 0) # Affiche le texte "Vague :"
      self.nbVaguesTXT = str(self.nbVagues) # Transforme le nombre de vague en texte (INT -> STR)
      self.screenTextPrint(120, 45, self.nbVaguesTXT)
      
      # Affichage de la barre d'HP du joueur
      pyxel.rect(740, 25, 200, 10, 8)
      pyxel.rect(740, 25, (self.personnage.currentHP/self.personnage.maxHP)*200, 10, 11)

      # Affichage du nombre de munitions restantes dans le chargeur de l'arme du joueur
      if self.personnage.ammoReloadingStatus == 100:
        self.screenTextPrint(15, resHauteur-48, "{}/{}".format(self.personnage.currentPlayerAmmo,self.personnage.maxPlayerAmmo))
      
      # Affichage du statut de rechargement de l'arme du joueur
      else:
        self.screenTextPrint(15, resHauteur-48, "{}/{}".format(round((self.personnage.maxPlayerAmmo/100)*self.personnage.ammoReloadingStatus),self.personnage.maxPlayerAmmo))
        pyxel.rect(15, resHauteur-24, 200, 10, 15)
        pyxel.rect(15, resHauteur-24, self.personnage.ammoReloadingStatus*2, 10, 13)
    
    elif self.partieTerminee:
      # Efface l'écran
      pyxel.cls(10)

      # Affiche le curseur de la souris
      pyxel.mouse(True)

      # Affiche le message de fin de partie
      pyxel.images[1].load(0,0, "GameOverScreen.png")
      pyxel.blt(350, 100, 1, 0, 0, 255, 55, 7) # Affiche le texte "Game Over"
      pyxel.blt(405, 200, 1, 105, 65, 75, 25, 7) # Affiche le texte "Score :"
      pyxel.blt(300, 225, 1, 0, 90, 180, 25, 7) # Affiche le texte "Kills :"
      pyxel.blt(300, 260, 1, 0, 125, 180, 25, 7) # Affiche le texte "PV Perdus :"
      pyxel.blt(300, 285, 1, 0, 150, 180, 25, 7) # Affiche le texte "Nombre de vagues :"

      for a in range(4):
        if a == 0:
          c = 200
          d = self.personnage.scoreTXT
        elif a == 1:
          c = 230
          d = self.personnage.killsTXT
        elif a == 2:
          c = 260
          d = self.personnage.pvPerdusTXT
        elif a == 3:
          c = 290
          d = self.nbVaguesTXT

        self.screenTextPrint(525, c, d)
      
      if self.personnage.keybinds == 4 or self.personnage.keybinds == 5 or self.personnage.keybinds == 6:
        if self.gameOverChosenBtn == 1:
          pyxel.blt(325, 400, 1, 105, 187, 105, 35, 7)
          pyxel.blt(525, 400, 1, 0, 222, 96, 35, 7)
        elif self.gameOverChosenBtn == 2:
          pyxel.blt(325, 400, 1, 0, 187, 105, 35, 7)
          pyxel.blt(525, 400, 1, 96, 222, 96, 35, 7)
          
      else:
        # Affiche le bouton "Rejouer"
        if pyxel.mouse_x > 325 and pyxel.mouse_x < 430 and pyxel.mouse_y > 400 and pyxel.mouse_y < 435:
          pyxel.blt(325, 400, 1, 105, 187, 105, 35, 7)
        else:
          pyxel.blt(325, 400, 1, 0, 187, 105, 35, 7)
        
        # Affiche le bouton "Quitter"
        if pyxel.mouse_x > 525 and pyxel.mouse_x < 621 and pyxel.mouse_y > 400 and pyxel.mouse_y < 435:
          pyxel.blt(525, 400, 1, 96, 222, 96, 35, 7)
        else:
          pyxel.blt(525, 400, 1, 0, 222, 96, 35, 7)

      # Affiche les copyrights
      pyxel.text(10, 520, "(c) Aurelien Audero, Axel Thibert, Tony Baca - 2024 - Tous droits reserves", 7)

      # Affiche le lien vers le GitHub du projet
      pyxel.blt(875, 510, 1, 0, 65, 75, 25, 7)
    
    if debug:
      pyxel.blt(5, 5, 0, 0, 112, 77, 10, 0) # Affiche un indicateur sur l'écran quand le mode debug est activé
      if debug4:
        self.screenTextPrint(resLongueur-64, resHauteur-32, str(self.currentFPS)) # Affiche le compteur de FPS à l'écran

########################
#  PROGRAMME PRINCIPAL #
#######################
debug = False

# Récupération des arguments passés en ligne de commande
sysArgs = []
for i in range(1, len(sysArgv)):
  sysArgs.append(sysArgv[i])

# Fonction pour créer une fenêtre de choix
def fenetreChoix(question, reponses):
  """
  Crée une fenêtre de choix en utilisant Tkinter.

  Args:
      question: La question à afficher dans la fenêtre.
      reponses: Les réponses qui peuvent être sélectionées par l'utilisateur.

  Returns:
      Indice de la réponse ou -1 si la fenêtre est fermée ou 0 si aucun choix n'as été fait
  """
  
  # Intialisation de la fenêtre et de ses variables
  fenetre = Tk()
  fenetre.title("Kino der toten")
  fenetre.eval('tk::PlaceWindow . center')
  fenetre.wm_iconphoto(True, PhotoImage(file = "KinoDerTotenAppIcon.png"))
  v1 = IntVar()
  v2 = IntVar(value=1)
  v3 = IntVar(value=1)
  i = 1

  # Action en cas de fermeture de la fenêtre
  def fermetureFenetre():
    nonlocal v1
    if gameQuitConfirmationWindow():
      v1 = -1
      fenetre.destroy()

  # Ajout du contenu à la fenêtre
  Label(fenetre, text=question).pack()
  for element in reponses:
    Radiobutton(fenetre, text=element, variable=v1, value=i, anchor="w", justify="left").pack(fill='both')
    i += 1
  Label(fenetre, text="Options").pack(pady=(10,0))
  Checkbutton(fenetre, text="Activer la musique du jeu", variable=v2, anchor="w", justify="left").pack(fill='both')
  Checkbutton(fenetre, text="Activer les effets sonores", variable=v3, anchor="w", justify="left").pack(fill='both')
  Button(text="Confirmer", command=fenetre.destroy).pack()

  # Création de la fenêtre
  fenetre.protocol("WM_DELETE_WINDOW", fermetureFenetre)
  fenetre.mainloop()

  # Retour du choix de l'utilisateur
  if v1 == -1:
    return (-1,-1,-1)
  else:
    return (v1.get(),v2.get(),v3.get())

# Fonction pour choisir la sensibilité et la zone morte de la manette
def choixSensibiliteEtZoneMorte():
  """
  Crée une fenêtre de choix pour la sensibilité de la manette en utilisant Tkinter.

  Args:
      Aucun argument n'est requis.

  Returns:
      Sensibilité et zone morte de la manette
  """
  
  # Initialisation de la fenêtre et de ses variables
  fenetre = Tk()
  fenetre.title("Kino der toten")
  fenetre.eval('tk::PlaceWindow . center')
  fenetre.wm_iconphoto(True, PhotoImage(file = "KinoDerTotenAppIcon.png"))
  v1 = IntVar()
  v1.set(10)
  v2 = IntVar()
  v2.set(2000)

  # Action en cas de fermeture de la fenêtre
  def fermetureFenetre():
    nonlocal v1
    if gameQuitConfirmationWindow():
      v1 = -1
      fenetre.destroy()

  # Ajout du contenu à la fenêtre
  Label(fenetre, text="Sensibilité de la visée à la manette").pack()
  Scale(fenetre, from_=1, to=20, orient=HORIZONTAL, variable=v1).pack()
  Label(fenetre, text="Zone morte de la manette").pack()
  Scale(fenetre, from_=0, to=10000, orient=HORIZONTAL, variable=v2).pack()
  Button(fenetre, text="Confirmer", command=fenetre.destroy).pack()
  
  # Création de la fenêtre
  fenetre.protocol("WM_DELETE_WINDOW", fermetureFenetre)
  fenetre.mainloop()

  # Retour du choix de l'utilisateur
  if v1 == -1:
    return (-1,-1)
  else:
    return (v1.get(),v2.get())

#Paramètres de debug
def debugSettings():
  """
  Crée une fenêtre de choix des paramètres de debug en utilisant Tkinter.

  Args:
      Aucun argument n'est requis.

  Returns:
      v1: Hitbox du joueur (Bool)
      v2: Hitbox des zombies (Bool)
      v3: Hitbox des tirs (Bool)
      v4: Affichage des FPS (Bool)
      v5: Désactiver les zombies (Bool)
      v6: Désactiver l'affichage de la map (Bool)
      v7: Afficher les coordonnées du reticule (Bool)
      v8: Hitbox des spawners de zombies (Bool)
      v9: Limite de FPS en jeu (Int)
  """
  
  # Intialisation de la fenêtre et de ses variables
  fenetre = Tk()
  fenetre.title("Kino der toten")
  fenetre.eval('tk::PlaceWindow . center')
  fenetre.wm_iconphoto(True, PhotoImage(file = "KinoDerTotenAppIcon.png"))
  v1 = IntVar()
  v2 = IntVar()
  v3 = IntVar()
  v4 = IntVar()
  v5 = IntVar()
  v6 = IntVar()
  v7 = IntVar()
  v8 = IntVar()
  v9 = IntVar(value=60)

  # Action en cas de fermeture de la fenêtre
  def fermetureFenetre():
    nonlocal v1
    if gameQuitConfirmationWindow():
      v1 = -1
      fenetre.destroy()

  # Ajout du contenu à la fenêtre
  Label(fenetre, text="MENU DEBUG", bg='red').pack()
  Label(fenetre, text="Quels éléments voulez-vous activer ?", anchor="w", justify="left").pack(fill='both', pady=(0,10))
  Checkbutton(fenetre, text="Hitbox du joueur", variable=v1, anchor="w", justify="left").pack(fill='both')
  Checkbutton(fenetre, text="Hitbox des zombies", variable=v2, anchor="w", justify="left").pack(fill='both')
  Checkbutton(fenetre, text="Hitbox des tirs", variable=v3, anchor="w", justify="left").pack(fill='both')
  Checkbutton(fenetre, text="Affichage des FPS", variable=v4, anchor="w", justify="left").pack(fill='both')
  Checkbutton(fenetre, text="Désactiver les zombies", variable=v5, anchor="w", justify="left").pack(fill='both')
  Checkbutton(fenetre, text="Désactiver l'affichage de la map", variable=v6, anchor="w", justify="left").pack(fill='both')
  Checkbutton(fenetre, text="Afficher les coordonnées du reticule", variable=v7, anchor="w", justify="left").pack(fill='both')
  Checkbutton(fenetre, text="Hitbox des spawners de zombies", variable=v8, anchor="w", justify="left").pack(fill='both', pady=(0,10))
  fpsSelectorFrame = Frame(fenetre)
  Label(fpsSelectorFrame, text="Limite de FPS en jeu :", anchor="w", justify="left").pack(side='left', pady=(15,0))
  Scale(fpsSelectorFrame, from_=1, to=1000, orient=HORIZONTAL, variable=v9).pack(side='right')
  fpsSelectorFrame.pack(fill='both')
  Button(text="Confirmer", command=fenetre.destroy).pack(pady=(10,0))

  # Création de la fenêtre
  fenetre.protocol("WM_DELETE_WINDOW", fermetureFenetre)
  fenetre.mainloop()

  # Retour du choix de l'utilisateur
  if v1 == -1:
    return (-1,-1,-1,-1,-1,-1,-1,-1,-1)
  else:
    return (v1.get(),v2.get(),v3.get(),v4.get(),v5.get(), v6.get(), v7.get(), v8.get(), v9.get())
  
# Fonction pour demander à l'utilisateur les contrôles à utiliser
def askPlayer():
  """
  Demande à l'utilisateur les contrôles à utiliser, les paramètres de la manette (si nécéssaire) et affiche la liste de touches.

  Args:
      Aucun argument n'est requis.

  Returns:
      userChosenKeybinds: Méthode d'entrée choisie par l'utilisateur (Int)
      musicEnabled: Activation de la musique du jeu (Bool)
      soundEnabled: Activation des effets sonores du jeu (Bool)
      controllerSensitivity: Sensibilité de la manette (Int) (dépend de la méthode d'entrée choisie par l'utilisateur)
      controllerDeadzone: Zone morte de la manette (Int) (dépend de la méthode d'entrée choisie par l'utilisateur)
  """

  userChosenKeybinds = 0
  while userChosenKeybinds == 0 :
    userChosenKeybinds, musicEnabled, soundEnabled = fenetreChoix("Choissisez votre méthode d'entrée :", ["Clavier - AZERTY", "Clavier - QWERTY", "Clavier - Flèches directionnelles", "Manette - Stick Gauche + Stick Droit", "Manette - Flèches directionnelles + Stick Droit"])
    # Affiche une erreur si aucun choix n'est fait par l'utilisateur
    if userChosenKeybinds == 0:
      fenetre = Tk()
      fenetre.title("Kino der toten")
      messagebox.showwarning("Erreur", "Il est nécéssaire de choisir une méthode d'entrée")
      fenetre.destroy()
    # Affiche un message d'informations avec toutes les touches utilisables par l'utilisateur
    elif userChosenKeybinds == 1:
      fenetre = Tk()
      fenetre.title("Kino der toten")
      messagebox.showinfo("Kino der toten", "Contrôles du jeu :\n\nZ : Aller vers le haut\nA : Aller à gauche\nS : Aller en bas\nD : Aller à droite\nR : Recharger\nClic gauche de la souris : Tirer")
      fenetre.destroy()
    elif userChosenKeybinds == 2:
      fenetre = Tk()
      fenetre.title("Kino der toten")
      messagebox.showinfo("Kino der toten", "Contrôles du jeu :\n\nW : Aller vers le haut\nA : Aller à gauche\nS : Aller en bas\nD : Aller à droite\nR : Recharger\nClic gauche de la souris : Tirer")
      fenetre.destroy()
    elif userChosenKeybinds == 3:
      fenetre = Tk()
      fenetre.title("Kino der toten")
      messagebox.showinfo("Kino der toten", "Contrôles du jeu :\n\nFlèche du haut : Aller vers le haut\nFlèche de gauche : Aller à gauche\nFlèche du bas : Aller en bas\nFlèche de droite : Aller à droite\nShift Droit : Recharger\nClic gauche de la souris : Tirer")
      fenetre.destroy()
    elif userChosenKeybinds == 4:
      controllerSensitivity, controllerDeadzone = choixSensibiliteEtZoneMorte()
      if controllerSensitivity == -1:
        userChosenKeybinds = -1
      else:
        fenetre = Tk()
        fenetre.title("Kino der toten")
        messagebox.showinfo("Kino der toten", "Contrôles du jeu :\n\nStick gauche : Se déplacer\nStick droit : Viser\n\nXbox :\nBouton A : Tirer\nBouton X : Recharger\n\nPlayStation :\nBouton × : Tirer\nBouton □ : Recharger")
        fenetre.destroy()
    elif userChosenKeybinds == 5:
      controllerSensitivity, controllerDeadzone = choixSensibiliteEtZoneMorte()
      if controllerSensitivity == -1:
        userChosenKeybinds = -1
      else:
        fenetre = Tk()
        fenetre.title("Kino der toten")
        messagebox.showinfo("Kino der toten", "Contrôles du jeu :\n\nFlèche du haut : Aller vers le haut\nFlèche de gauche : Aller à gauche\nFlèche du bas : Aller en bas\nFlèche de droite : Aller à droite\nStick gauche : Viser\n\nXbox :\nBouton A : Tirer\nBouton X : Recharger\n\nPlayStation :\nBouton × : Tirer\nBouton □ : Recharger")
        fenetre.destroy()
  
  if (userChosenKeybinds == 4) or (userChosenKeybinds == 5):
    return (userChosenKeybinds, musicEnabled, soundEnabled, controllerSensitivity, controllerDeadzone)
  else:
    return (userChosenKeybinds, musicEnabled, soundEnabled, None, None)

# Fonction pour demander à l'utilisateur s'il veut quitter le jeu en cours de partie
def gameQuitConfirmationWindow():
  if messagebox.askyesno("Kino der toten", "Voulez-vous quitter le jeu ?"):
    return True

# Lancement du jeu
if sysArgs:
  if sysArgs[0] == "--debug=True":
    debug = True
    debug1, debug2, debug3, debug4, debug5, debug6, debug7, debug8, debug9 = debugSettings()
    if debug1 == -1:
      sysExit()
  if (sysArgs[0] == "--help") or (sysArgs[0] == "--h"):
    print("Pour plus d'informations, veuillez consulter le GitHub du projet : https://github.com/AurelienAudero/KinoDerToten-Projet-Pyxel/")
    sysExit()

userChosenKeybinds, musicEnabled, soundEnabled, controllerSensitivity, controllerDeadzone = askPlayer()

if (userChosenKeybinds != 0) and (userChosenKeybinds != -1):
  resLongueur = 960
  resHauteur = 540
  fps = 60
  if debug:
    if debug9 != 60:
      fps = debug9
  if (userChosenKeybinds == 1) or (userChosenKeybinds == 2) or (userChosenKeybinds == 3):
    del(controllerSensitivity)
    del(controllerDeadzone)
    game = Jeu(resLongueur, resHauteur, fps, userChosenKeybinds, musicEnabled, soundEnabled)
  elif (userChosenKeybinds == 4) or (userChosenKeybinds == 5):
    game = Jeu(resLongueur, resHauteur, fps, userChosenKeybinds, musicEnabled, soundEnabled, controllerSensitivity, controllerDeadzone)
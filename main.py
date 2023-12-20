# Importations des bibliothèques nécéssaires
import pyxel
from random import randint
from tkinter import Tk, Label, Radiobutton, Button, IntVar, messagebox

########################
#   PROGRAMME DU JEU   #
########################
class Personnage:
  def __init__(self, x, y, width, height, keybinds):
    # Création de variables
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.keybinds = keybinds
    self.score = 0
    self.scoreTXT = ""
    self.kills = 0

    # Détermination des touches pour contrôler le personnage
    if self.keybinds == 1 :
      self.personnageHaut = pyxel.KEY_Z
      self.personnageGauche = pyxel.KEY_Q
      self.personnageBas = pyxel.KEY_S
      self.personnageDroite = pyxel.KEY_D
      self.personnageTir = pyxel.MOUSE_BUTTON_LEFT
    elif self.keybinds == 2 :
      self.personnageHaut = pyxel.KEY_W
      self.personnageGauche = pyxel.KEY_A
      self.personnageBas = pyxel.KEY_S
      self.personnageDroite = pyxel.KEY_D
      self.personnageTir = pyxel.MOUSE_BUTTON_LEFT
    elif self.keybinds == 3 :
      self.personnageHaut = pyxel.KEY_UP
      self.personnageGauche = pyxel.KEY_LEFT
      self.personnageBas = pyxel.KEY_DOWN
      self.personnageDroite = pyxel.KEY_RIGHT
      self.personnageTir = pyxel.MOUSE_BUTTON_LEFT

  def move(self):
    if pyxel.btn(self.personnageHaut):
      if (self.y > 0) :
        self.y = self.y - 10
    if pyxel.btn(self.personnageGauche):
      if (self.x > 0) :
        self.x = self.x - 10
    if pyxel.btn(self.personnageBas):
      if (self.y < resHauteur-self.height) :
        self.y = self.y + 10
    if pyxel.btn(self.personnageDroite):
      if (self.x < resLongueur-self.width) :
        self.x = self.x + 10
    if pyxel.btnp(self.personnageTir):
      return self.x+(self.width), self.y+(self.height/2)
    
    return None
          
  def draw(self):
    pyxel.rect(self.x, self.y, self.width, self.height, 9)

class Tir:
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.width = 40
    self.height = 10
    self.alive = True

  def move(self):
    if self.x < 0-self.width or self.x > resLongueur+self.width:
      self.alive = False
    else:
        self.x = self.x + 10

  def draw(self):
    pyxel.rect(self.x, self.y, self.width, self.height, 10)

class Zombie:
  def __init__(self, x, y, width, height, vitesse, personnage):
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.vitesse = vitesse
    self.alive = True
    self.personnage = personnage

  def move(self):
    if (self.y > 0) and (self.y > self.personnage.y) :
      self.y = self.y - self.vitesse
    if (self.x > 0) and (self.x > self.personnage.x-(self.personnage.width-5)) :
      self.x = self.x - self.vitesse
    if (self.y < resHauteur-self.height) and (self.y < self.personnage.y):
      self.y = self.y + self.vitesse
    if (self.x < resLongueur-self.width) and (self.x < self.personnage.x+(self.personnage.width-5)):
      self.x = self.x + self.vitesse

  def draw(self):
    pyxel.rect(self.x, self.y, self.width, self.height, 11)

class Jeu:
  def __init__(self, l, h, fps, keybinds):
    pyxel.init(l, h, title="Kino der toten", fps=fps)
    pyxel.load("KinoDerToten.pyxres")

    self.zombiesList = []
    self.tirsList = []
    self.tempsSpawnMob = 1 # Temps entre chaque spawn de mob (en secondes)
    self.gainScoreKill = 10 # Nombre de points de score gagné en faisant un kill
    self.personnage = Personnage(100, 210, 50, 80, keybinds)

    pyxel.run(self.update, self.draw)
  
  def update(self):
    # Déplacement du personnage joueur
    v = self.personnage.move()
    
    # Création d'un tir si le joueur appuie sur la touche de tir
    if v is not None:
      self.tirsList.append(Tir(v[0], v[1]))

    # Déplacement des tirs existants et suppression des tirs terminés
    for element in self.tirsList:
      element.move()
      if not element.alive:
        self.tirsList.remove(element)

    # Déplacement des zombies en vie et suppression des zombies morts
    for element in self.zombiesList:
      element.move()
      if not element.alive:
        self.zombiesList.remove(element)
    
    # Collisions entre zombies et tirs
    for ennemi in self.zombiesList:
      for tir in self.tirsList:
        #if (tir.y <= ennemi.y and tir.y >= ennemi.y+ennemi.height) and (tir.x+tir.width >= ennemi.x):
        if ennemi.x+ennemi.width > tir.x and tir.x+tir.width > ennemi.x and ennemi.y+ennemi.height > tir.y and tir.y+tir.height > ennemi.y:
          self.tirsList.remove(tir)
          self.zombiesList.remove(ennemi)
          self.personnage.score += self.gainScoreKill
          self.personnage.kills += 1

    # Spawn aléatoire des zombies
    if pyxel.frame_count % (fps*self.tempsSpawnMob) == 0:
      numeroSpawner = randint(1,2)
      if numeroSpawner == 1:
        self.zombiesList.append(Zombie(750, 100, 50, 80, 1, self.personnage))
      elif numeroSpawner == 2:
        self.zombiesList.append(Zombie(750, 300, 50, 80, 1, self.personnage))

  def draw(self):
    # Efface l'écran
    pyxel.cls(13)

    # Affiche le score actuel du joueur
    pyxel.blt(15, 15, 0, 0, 0, 89, 19, 0) # Affiche le texte "Score :"
    self.personnage.scoreTXT = str(self.personnage.score) # Transforme le score du joueur en texte (INT -> STR)
    for i in range(len(self.personnage.scoreTXT)):
      if self.personnage.scoreTXT[i] == "1":
        pyxel.blt(120+(16*i), 15, 0, 0, 24, 11, 19, 0) # Affichage du chiffre 1
      if self.personnage.scoreTXT[i] == "2":
        pyxel.blt(120+(16*i), 15, 0, 16, 24, 11, 19, 0) # Affichage du chiffre 2
      if self.personnage.scoreTXT[i] == "3":
        pyxel.blt(120+(16*i), 15, 0, 32, 24, 11, 19, 0) # Affichage du chiffre 3
      if self.personnage.scoreTXT[i] == "4":
        pyxel.blt(120+(16*i), 15, 0, 48, 24, 11, 19, 0) # Affichage du chiffre 4
      if self.personnage.scoreTXT[i] == "5":
        pyxel.blt(120+(16*i), 15, 0, 64, 24, 11, 19, 0) # Affichage du chiffre 5
      if self.personnage.scoreTXT[i] == "6":
        pyxel.blt(120+(16*i), 15, 0, 80, 24, 11, 19, 0) # Affichage du chiffre 6
      if self.personnage.scoreTXT[i] == "7":
        pyxel.blt(120+(16*i), 15, 0, 96, 24, 11, 19, 0) # Affichage du chiffre 7
      if self.personnage.scoreTXT[i] == "8":
        pyxel.blt(120+(16*i), 15, 0, 112, 24, 11, 19, 0) # Affichage du chiffre 8
      if self.personnage.scoreTXT[i] == "9":
        pyxel.blt(120+(16*i), 15, 0, 128, 24, 11, 19, 0) # Affichage du chiffre 9
      if self.personnage.scoreTXT[i] == "0":
        pyxel.blt(120+(16*i), 15, 0, 144, 24, 11, 19, 0) # Affichage du chiffre 0
    
    # Affichage des trois spawners de zombies
    pyxel.rect(750, 100, 100, 100, 12)
    pyxel.rect(750, 300, 100, 100, 12)
    
    # Affichage du personnage joueur
    self.personnage.draw()
    
    # Affichage des tirs
    for element in self.tirsList:
      element.draw()

    # Affichage des zombies
    for element in self.zombiesList:
      element.draw()

########################
#  PROGRAMME PRINCIPAL #
#######################
def fenetreChoix(question, reponses):
  """
  Crée une fenêtre de choix en utilisant Tkinter
  IN : question (Str) et reponses (list)
  OUT : Indice de la réponse ou -1 si la fenêtre est fermée ou 0 si aucun choix n'as été fait
  """
  
  # Intialisation de la fenêtre et de ses variables
  fenetre = Tk()
  fenetre.title("Kino der toten")
  v = IntVar()
  i = 1

  # Action en cas de fermeture de la fenêtre
  def fermetureFenetre():
    nonlocal v
    if messagebox.askokcancel("Kino der toten", "Voulez-vous quitter le jeu ?"):
      v = -1
      fenetre.destroy()

  # Ajout du contenu à la fenêtre
  Label(fenetre, text=question).pack()
  for element in reponses:
    Radiobutton(fenetre, text=element, variable=v, value=i).pack(anchor="w")
    i += 1
  Button(text="Confirmer", command=fenetre.destroy).pack()

  # Création de la fenêtre
  fenetre.protocol("WM_DELETE_WINDOW", fermetureFenetre)
  fenetre.mainloop()

  # Retour du choix de l'utilisateur
  if v == -1:
    return -1
  else:
    return v.get()

# Demande à l'utilisateur les touches à utiliser
userChosenKeybinds = 0
while userChosenKeybinds == 0 :
  userChosenKeybinds = fenetreChoix("Choissisez votre méthode d'entrée :", ["Clavier - AZERTY", "Clavier - QWERTY", "Clavier - Flèches directionnelles"])
  # Affiche une erreur si aucun choix n'est fait par l'utilisateur
  if userChosenKeybinds == 0:
    fenetre = Tk()
    fenetre.title("Kino der toten")
    messagebox.showwarning("Erreur", "Il est nécéssaire de choisir une méthode d'entrée")
    fenetre.destroy()

# Lancement du jeu
if (userChosenKeybinds == 1) or (userChosenKeybinds == 2) or (userChosenKeybinds == 3):
  resLongueur = 960
  resHauteur = 540
  fps = 60
  game = Jeu(resLongueur, resHauteur, fps, userChosenKeybinds)
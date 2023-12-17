# Importations des bibliothèques nécéssaires
import pyxel
from random import randint
from tkinter import Tk, Label, Radiobutton, Button, IntVar, messagebox

########################
#   PROGRAMME DU JEU   #
########################
class Personnage:
  def __init__(self, x, y, width, height, keybinds):
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.keybinds = keybinds

    # Détermination des touches pour contrôler le personnage
    if self.keybinds == 1 :
      self.personnageHaut = pyxel.KEY_Z
      self.personnageGauche = pyxel.KEY_Q
      self.personnageBas = pyxel.KEY_S
      self.personnageDroite = pyxel.KEY_D
    elif self.keybinds == 2 :
      self.personnageHaut = pyxel.KEY_W
      self.personnageGauche = pyxel.KEY_A
      self.personnageBas = pyxel.KEY_S
      self.personnageDroite = pyxel.KEY_D

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
          
  def draw(self):
    pyxel.rect(self.x, self.y, self.width, self.height, 9)

class Zombie:
  def __init__(self, x, y, width, height, vitesse, personnage):
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.vitesse = vitesse
    self.personnage = personnage

  def move(self):
    if (self.y > 0) and (self.y > self.personnage.y) :
      self.y = self.y - self.vitesse
    if (self.x > 0) and (self.x > self.personnage.x) :
      self.x = self.x - self.vitesse
    if (self.y < resHauteur-self.height) and (self.y < self.personnage.y):
      self.y = self.y + self.vitesse
    if (self.x < resLongueur-self.width) and (self.x < self.personnage.x):
      self.x = self.x + self.vitesse

  def draw(self):
    pyxel.rect(self.x, self.y, self.width, self.height, 11)

class Jeu:
  def __init__(self, l, h, fps, keybinds):
    pyxel.init(l, h, title="Kino der toten", fps=fps)

    self.zombiesList = []
    self.tempsSpawnMob = 5 # Temps entre chaque spawn de mob (en secondes)
    self.personnage = Personnage(360, 240, 50, 80, keybinds)

    pyxel.run(self.update, self.draw)

  def update(self):
    self.personnage.move()
    for element in self.zombiesList:
      element.move()
    if pyxel.frame_count % (fps*self.tempsSpawnMob) == 0:
      self.zombiesList.append(Zombie(randint(20, 250), randint(20, 250), 50, 80, 5, self.personnage))

  def draw(self):
    pyxel.cls(7)
    self.personnage.draw()
    for element in self.zombiesList:
      element.draw()

########################
#  PROGRAMME PRINCIPAL #
########################
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
    if messagebox.askokcancel("Oui", "Voulez-vous quitter le jeu ?"):
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
  userChosenKeybinds = fenetreChoix("Choissisez votre méthode d'entrée :", ["Clavier - AZERTY", "Clavier - QWERTY"])
  # Affiche une erreur si aucun choix n'est fait par l'utilisateur
  if userChosenKeybinds == 0:
    messagebox.showwarning("Erreur", "Il est nécéssaire de choisir une méthode d'entrée")

# Lancement du jeu

if (userChosenKeybinds == 1) or (userChosenKeybinds == 2):
  resLongueur = 720
  resHauteur = 480
  fps = 60
  game = Jeu(resLongueur, resHauteur, fps, userChosenKeybinds)
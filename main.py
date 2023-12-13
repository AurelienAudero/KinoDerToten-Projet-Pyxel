# Importations des bibliothèques nécéssaires
import pyxel
from tkinter import Tk, Label, Radiobutton, Button, IntVar

########################
#   PROGRAMME DU JEU   #
########################
class Personnage:
  def __init__(self, x, y, keybinds):
    self.x = x
    self.y = y
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
      if (self.y < 720) :
        self.y = self.y + 10
    if pyxel.btn(self.personnageDroite):
      if (self.x < 720) :
        self.x = self.x + 10
          
  def draw(self):
    pyxel.rect(self.x, self.y, 50, 80, 9)

class Jeu:
  def __init__(self, l, h, keybinds):
    pyxel.init(l, h, title = "Kino der toten")

    # Sauvegarde de la résolution de la fenêtre
    self.resLongueur = l
    self.resHauteur = h

    # Création du personnage
    self.personnage = Personnage(360, 240, keybinds)

    pyxel.run(self.update, self.draw)

  def update(self):
    self.personnage.move()

  def draw(self):
    pyxel.cls(7)
    self.personnage.draw()

########################
#  PROGRAMME PRINCIPAL #
########################
def fenetreChoix(question, reponses):
  """
  Crée une fenêtre de choix en utilisant Tkinter
  IN : question (Str) et reponses (list)
  OUT : Indice de la réponse
  """
  
  fenetre = Tk()
  Label(fenetre, text=question).pack()
  v = IntVar()
  i = 1
  for element in reponses:
    Radiobutton(fenetre, text=element, variable=v, value=i).pack(anchor="w")
    i += 1
  Button(text="Confirmer", command=fenetre.destroy).pack()
  fenetre.mainloop()
  if v.get() == 0:
    return None
  else:
    return v.get()

# Demande à l'utilisateur les touches à utiliser
userChosenKeybinds = None
while userChosenKeybinds == None :
  userChosenKeybinds = fenetreChoix("Choissisez votre méthode d'entrée :", ["Clavier - AZERTY", "Clavier - QWERTY"])

# Lancement du jeu
Jeu(720, 480, userChosenKeybinds)
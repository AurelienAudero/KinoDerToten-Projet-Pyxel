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
    self.lastSide = "Right"
    self.currentHP = 100.0
    self.maxHP = 100.0

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
    elif self.keybinds == 4 :
      self.personnageAxeY = pyxel.GAMEPAD1_AXIS_LEFTY
      self.personnageAxeX = pyxel.GAMEPAD1_AXIS_LEFTX
      self.personnageTir = pyxel.GAMEPAD1_BUTTON_A
      self.controllerDeadzone = 2000
    elif self.keybinds == 5 :
      self.personnageAxeY = pyxel.GAMEPAD1_AXIS_RIGHTY
      self.personnageAxeX = pyxel.GAMEPAD1_AXIS_RIGHTX
      self.personnageTir = pyxel.GAMEPAD1_BUTTON_A
      self.controllerDeadzone = 2000
    elif self.keybinds == 6 :
      self.personnageHaut = pyxel.GAMEPAD1_BUTTON_DPAD_UP
      self.personnageGauche = pyxel.GAMEPAD1_BUTTON_DPAD_LEFT
      self.personnageBas = pyxel.GAMEPAD1_BUTTON_DPAD_DOWN
      self.personnageDroite = pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT
      self.personnageTir = pyxel.GAMEPAD1_BUTTON_A

  def move(self):
    # Contrôles avec les boutons du clavier ou de la manette
    if (self.keybinds != 4) and (self.keybinds != 5):
      if pyxel.btn(self.personnageHaut):
        if (self.y > 0) :
          self.y = self.y - 10
      if pyxel.btn(self.personnageGauche):
        if (self.x > 0) :
          self.x = self.x - 10
          if self.lastSide != "Left":
            self.lastSide = "Left"
      if pyxel.btn(self.personnageBas):
        if (self.y < resHauteur-self.height) :
          self.y = self.y + 10
      if pyxel.btn(self.personnageDroite):
        if (self.x < resLongueur-self.width) :
          self.x = self.x + 10
          if self.lastSide != "Right":
            self.lastSide = "Right"
      if pyxel.btnp(self.personnageTir):
        if self.lastSide == "Right":
          return self.x+(self.width), self.y+(self.height/2), self.lastSide
        if self.lastSide == "Left":
          return self.x-((self.width/4)*3), self.y+(self.height/2), self.lastSide
    
    # Contrôles avec les sticks analogiques de la manette
    elif (self.keybinds == 4) or (self.keybinds == 5):
      if pyxel.btnv(self.personnageAxeY) < -self.controllerDeadzone:
        if (self.y > 0) :
          self.y = self.y - 10
      if pyxel.btnv(self.personnageAxeX) < -self.controllerDeadzone:
        if (self.x > 0) :
          self.x = self.x - 10
          if self.lastSide != "Left":
            self.lastSide = "Left"
      if pyxel.btnv(self.personnageAxeY) > self.controllerDeadzone:
        if (self.y < resHauteur-self.height) :
          self.y = self.y + 10
      if pyxel.btnv(self.personnageAxeX) > self.controllerDeadzone:
        if (self.x < resLongueur-self.width) :
          self.x = self.x + 10
          if self.lastSide != "Right":
            self.lastSide = "Right"
      if pyxel.btnp(self.personnageTir):
        if self.lastSide == "Right":
          return self.x+(self.width), self.y+(self.height/2), self.lastSide
        if self.lastSide == "Left":
          return self.x-((self.width/4)*3), self.y+(self.height/2), self.lastSide
    
    return None
          
  def draw(self):
    if self.lastSide == "Left":
      pyxel.rect(self.x, self.y, self.width, self.height, 9)
      pyxel.rect(self.x+5, self.y+10, 10, 10, 0)
    if self.lastSide == "Right":
      pyxel.rect(self.x, self.y, self.width, self.height, 9)
      pyxel.rect(self.x+self.width-15, self.y+10, 10, 10, 0)

class Tir:
  def __init__(self, x, y, direction):
    self.x = x
    self.y = y
    self.width = 40
    self.height = 10
    self.alive = True
    self.direction = direction

  def move(self):
    if self.x < 0-self.width or self.x > resLongueur+self.width:
      self.alive = False
    else:
        if self.direction == "Right":
          self.x = self.x + 10
        if self.direction == "Left":
          self.x = self.x - 10

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
    if (self.y > 0) and (self.y-self.height > self.personnage.y) :
      self.y = self.y - self.vitesse
    if (self.x > 0) and (self.x > self.personnage.x-self.personnage.width) :
      self.x = self.x - self.vitesse
    if (self.y < resHauteur-self.height) and (self.y+self.height < self.personnage.y):
      self.y = self.y + self.vitesse
    if (self.x < resLongueur-self.width) and (self.x < self.personnage.x+self.personnage.width):
      self.x = self.x + self.vitesse

  def draw(self):
    pyxel.rect(self.x, self.y, self.width, self.height, 11)
    pyxel.rectb(self.x, self.y, self.width, self.height, 0)

class Jeu:
  def __init__(self, l, h, fps, keybinds):
    pyxel.init(l, h, title="Kino der toten", fps=fps)
    pyxel.load("KinoDerToten.pyxres")

    self.zombiesList = []
    self.tirsList = []
    self.tempsSpawnMob = 1 # Temps entre chaque spawn de mob (en secondes)
    self.gainScoreKill = 10 # Nombre de points de score gagné en faisant un kill
    self.personnage = Personnage(450, 210, 50, 80, keybinds)
    self.perteHP = 0.5 # Nombre de points de vie perdus au contact d'un zombie
    self.partieTerminee = False

    pyxel.run(self.update, self.draw)
  
  def update(self): 
    if not self.partieTerminee:
      # Vérifie si le joueur est mort
      if self.personnage.currentHP <= 0:
        self.partieTerminee = True
      
      # Déplacement du personnage joueur
      v = self.personnage.move()
      
      # Création d'un tir si le joueur appuie sur la touche de tir
      if v is not None:
        self.tirsList.append(Tir(v[0], v[1], v[2]))

      # Déplacement des tirs existants et suppression des tirs terminés
      for element in self.tirsList:
        element.move()
        if not element.alive:
          self.tirsList.remove(element)

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
          self.personnage.currentHP -= self.perteHP

      # Collisions entre zombies et tirs
      for ennemi in self.zombiesList:
        for tir in self.tirsList:
          if ennemi.x+ennemi.width > tir.x and tir.x+tir.width > ennemi.x and ennemi.y+ennemi.height > tir.y and tir.y+tir.height > ennemi.y:
            self.tirsList.remove(tir)
            self.zombiesList.remove(ennemi)
            self.personnage.score += self.gainScoreKill
            self.personnage.kills += 1

      # Spawn aléatoire des zombies
      if pyxel.frame_count % (fps*self.tempsSpawnMob) == 0:
        numeroSpawner = randint(1,3)
        if numeroSpawner == 1:
          self.zombiesList.append(Zombie(725, 50, 50, 80, 1, self.personnage))
        elif numeroSpawner == 2:
          self.zombiesList.append(Zombie(425, 50, 50, 80, 1, self.personnage))
        elif numeroSpawner == 3:
          self.zombiesList.append(Zombie(125, 50, 50, 80, 1, self.personnage))
    
    elif self.partieTerminee:
      # Code à exécuter si la partie est terminée
      pass

  def draw(self):
    if not self.partieTerminee:
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
      
      # Affichage de la barre d'HP du joueur
      pyxel.rect(740, 25, 200, 10, 8)
      pyxel.rect(740, 25, self.personnage.currentHP*2, 10, 11)

      # Affichage des deux spawners de zombies
      pyxel.rect(725, 50, 100, 100, 12)
      pyxel.rect(425, 50, 100, 100, 12)
      pyxel.rect(125, 50, 100, 100, 12)
      
      # Affichage du personnage joueur
      self.personnage.draw()
      
      # Affichage des tirs
      for element in self.tirsList:
        element.draw()

      # Affichage des zombies
      for element in self.zombiesList:
        element.draw()
    
    elif self.partieTerminee:
      # Efface l'écran
      pyxel.cls(14)

      # Affiche le curseur de la souris
      pyxel.mouse(True)

      # Affiche le message de fin de partie
      pyxel.images[0].load(0,0, "GameOverScreen.png")
      pyxel.blt(350, 100, 0, 0, 0, 255, 55, 7) # Affiche le texte "Game Over"
      pyxel.blt(300, 200, 0, 0, 65, 180, 25, 7) # Affiche le texte "Score :"
      pyxel.blt(300, 225, 0, 0, 90, 180, 25, 7) # Affiche le texte "Kills :"
      pyxel.blt(300, 260, 0, 0, 125, 180, 25, 7) # Affiche le texte "PV Perdus :"
      pyxel.blt(300, 285, 0, 0, 150, 180, 25, 7) # Affiche le texte "Nombre de vagues :"

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
  userChosenKeybinds = fenetreChoix("Choissisez votre méthode d'entrée :", ["Clavier - AZERTY", "Clavier - QWERTY", "Clavier - Flèches directionnelles", "Manette - Stick Gauche", "Manette - Stick Droit", "Manette - Flèches directionnelles"])
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
    messagebox.showinfo("Kino der toten", "Contrôles du jeu :\n\nZ : Aller vers le haut\nA : Aller à gauche\nS : Aller en bas\nD : Aller à droite\nClic gauche de la souris : Tirer")
    fenetre.destroy()
  elif userChosenKeybinds == 2:
    fenetre = Tk()
    fenetre.title("Kino der toten")
    messagebox.showinfo("Kino der toten", "Contrôles du jeu :\n\nW : Aller vers le haut\nA : Aller à gauche\nS : Aller en bas\nD : Aller à droite\nClic gauche de la souris : Tirer")
    fenetre.destroy()
  elif userChosenKeybinds == 3:
    fenetre = Tk()
    fenetre.title("Kino der toten")
    messagebox.showinfo("Kino der toten", "Contrôles du jeu :\n\nFlèche du haut : Aller vers le haut\nFlèche de gauche : Aller à gauche\nFlèche du bas : Aller en bas\nFlèche de droite : Aller à droite\n Clic gauche de la souris : Tirer")
    fenetre.destroy()
  elif userChosenKeybinds == 4:
    fenetre = Tk()
    fenetre.title("Kino der toten")
    messagebox.showinfo("Kino der toten", "Contrôles du jeu :\n\nStick gauche : Se déplacer\nBouton A (Xbox) : Tirer\nBouton X (PlayStation) : Tirer")
    fenetre.destroy()
  elif userChosenKeybinds == 5:
    fenetre = Tk()
    fenetre.title("Kino der toten")
    messagebox.showinfo("Kino der toten", "Contrôles du jeu :\n\nStick droit : Se déplacer\nBouton A (Xbox) : Tirer\nBouton X (PlayStation) : Tirer")
    fenetre.destroy()
  elif userChosenKeybinds == 6:
    fenetre = Tk()
    fenetre.title("Kino der toten")
    messagebox.showinfo("Kino der toten", "Contrôles du jeu :\n\nFlèche du haut : Aller vers le haut\nFlèche de gauche : Aller à gauche\nFlèche du bas : Aller en bas\nFlèche de droite : Aller à droite\nBouton A (Xbox) : Tirer\nBouton X (PlayStation) : Tirer")
    fenetre.destroy()

# Lancement du jeu
if (userChosenKeybinds != 0) and (userChosenKeybinds != -1):
  resLongueur = 960
  resHauteur = 540
  fps = 60
  game = Jeu(resLongueur, resHauteur, fps, userChosenKeybinds)
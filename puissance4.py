import pygame
from random import  choice#, choices  sample,
from threading import Thread
from time import sleep
from random import randint, choice

class Cellule():
    """
    Objet qui gere les cellules de la grille
    """
    def __init__(self, etat, i, j, grille):
        """
        i et j sont la position de la cellule dans la matrice
        x et y sont les coordonés dans l'ecran calculés en fonction de la position et largeur/longeur de la case
        """
        self.etat = etat # 0 1 2
        self.grille = grille
        self.game = self.grille.game
        self.i, self.j = i, j
        self.x = i * self.game.largeur + 5 + 5*i
        self.y = j * self.game.longeur + 5 + 5*j
        self.rect = pygame.Rect(self.x, self.y, self.game.largeur, self.game.longeur)

    def resize(self):
        """Methode appelé lors du redimentionement de la fenetre"""
        self.x = self.i * self.game.largeur + 5 + 5*self.i
        self.y = self.j * self.game.longeur + 5 + 5*self.j
    
    def get_etat(self):
        """Retourne l'etat de la case"""
        return self.etat

    def get_pos(self):
        """Retourne la position (i,j) de la case"""
        return self.i, self.j

    def get_coord(self):
        """Retourne les coordonés de la case"""
        return self.x, self.y
    
    def off(self):
        self.etat = 0
    
    def set_etat(self, etat):
        self.etat = etat
    
    def is_clickable(self):
        """Retourne si on peut cliquer sur la case
        (si la cellule s'est pas deja prise ou que la prtie n'est pas arreté)
        """
        return not (self.etat in [1,2] or self.game.etat == 0)

    def selected(self, x):
        """quand la case est selectioné
            :x: int | etat ou player id (meme chose)"""
        self.etat = x
        
    def dessin(self):
        """dessine la couleur du carré de coordonnée x,y"""
        if self.etat == 0:
            pygame.draw.rect(self.game.fenetre, (100,100,100),(self.x,self.y,self.game.largeur,self.game.longeur),0, 7, 7, 7)
        elif self.etat == 1:
            pygame.draw.rect(self.game.fenetre, (204,0,0),(self.x,self.y,self.game.largeur,self.game.longeur),0, 7, 7, 7)
        elif self.etat == 2:
            pygame.draw.rect(self.game.fenetre, (204,204,0),(self.x,self.y,self.game.largeur,self.game.longeur),0, 7, 7, 7)
        
    def __str__(self) -> str:
        return str(self.get_pos())


class Grille():
    """
    Objet qui gere toutes les cellules
    """
    def __init__(self,game):
        self.matrix = []
        self.cellList = []
        self.game = game
        self.CasesLargeur = self.game.taille[0] # nombre de cases en largeur
        self.CasesLongeur = self.game.taille[1] # nombre de cases en longeur

        for i in range(self.CasesLargeur):
            temp = []
            for j in range(self.CasesLongeur):
                cell = Cellule(0, i, j, self)
                temp.append(cell)
                self.cellList.append(cell)
            self.matrix.append(temp)

    def switch_off(self, liste=None):
        """passe toutes le cellules en mode eteinte
        peut etre utilisé pour une liste donnée"""
        if not liste:
            liste = self.cellList
        for cell in liste:
            cell.off()

    def get_matrix(self):
        return self.matrix

    def dessin_cellules(self):
        """
        dessine toutes les cellules
        appelé dans la boucle principale
        """
        for ligne in self.matrix:
            for cell in ligne:
                cell.dessin()
    
    def resize(self):
        """
        Methode appelé lors du redimentionement de la fenetre
        """
        for cell in self.cellList:
            cell.resize()
            
    def __repr__(self) -> str:
        txt = ''
        for ligne in self.matrix:
            for cell in ligne:
                txt += str(cell)
            txt += '\n'
        return txt

class Game():
    """
    Objet qui gere le jeu
    """
    def __init__(self, taille) -> None:
        self.taille = taille
        pygame.init()
        pygame.display.set_caption('Puissance 4') 
        self.fenetre = pygame.display.set_mode((700, 700), pygame.RESIZABLE)# largeur longeur 
        self.backgroundColor = (100, 100, 100)
        self.window_size = pygame.display.get_window_size()
        self.largeur = int((self.window_size[0] - 5 * self.taille[0]) / self.taille[0]) - 0
        self.longeur = int((self.window_size[1] - 5 * self.taille[1]) / self.taille[1]) - 0

        self.grille = Grille(self)

        self.etat = 0 # 0 = off | 1 = peux jouer
        # self.enJeu = False
        # self.attente = False
        self.perdu = False

    def draw(self):
        self.fenetre.fill(self.backgroundColor)
        self.grille.dessin_cellules()

    def resize(self):
        """
        Methode appelé lors du redimentionement de la fenetre
        """
        self.window_size = pygame.display.get_window_size()
        self.largeur = int((self.window_size[0] - 5 * self.taille[0]) / self.taille[0]) - 0
        self.longeur = int((self.window_size[1] - 5 * self.taille[1]) / self.taille[1]) - 0
        self.grille.resize()

    def start(self):
        """
        fct qui demare la manche
        """       
        print('a')
        self.backgroundColor = (10, 10, 10)
        self.attente = False
        self.largeur = int((self.window_size[0] - 5 * self.taille[0]) / self.taille[0]) - 1
        self.longeur = int((self.window_size[1] - 5 * self.taille[1]) / self.taille[1]) - 0
        self.grille = Grille(self)
        self.etat = 1


    def click(self, x, coords):
        """
        si une cellule est selectioné
        """
        clicked = False
        if isinstance(coords, Cellule):
            cell = coords
            colomneId = cell.get_pos()[0]
            for cell in reversed(self.grille.matrix[colomneId]):
                if cell.is_clickable():
                    cell.selected(x)
                    clicked = True
                    break
        else:
            i,j = coords
            for cell in self.grille.cellList:
                if cell.rect.collidepoint(i, j):
                    colomneId = cell.get_pos()[0]
                    for cell in reversed(self.grille.matrix[colomneId]):
                        if cell.is_clickable():
                            cell.selected(x)
                            clicked = True
                            break
                if clicked:
                    break
        
        
        if not clicked:
            print('Impossible de selectioner cette case !')
            return False

        if test(self.grille.matrix, cell.get_pos()):
            self.etat = 0
            self.backgroundColor = (100, 200, 100)
            print('Victoire joueur 1')
            return
        if x ==2:
            testColl = test_coll(self.grille.matrix, cell.get_pos()[0], 2, 4)
            testLigne = test_ligne(self.grille.matrix, cell.get_pos()[1], 2, 4)
            testDiag = test_diag(self.grille.matrix, cell.get_pos(), 2, 4)
            
            if testColl or testLigne or testDiag:
                self.etat = 0
                self.backgroundColor = (200, 100, 100)
                print('Victoire joueur 2')
        else:
            self.bot(cell)

        return True
    
    
    def bot(self, cell):
        """
        Methode qui fait jouer le bot
        """

        if self.test_win(2, execute=True):
            return
        if self.test_win(1, execute=True):
            return
        
        if self.test_win(1, 1, execute=True):
            return
        if self.test_win(2, 1, execute=True):
            return
        

        # aléatoire qui verifie que ca ne fasse pas gagner le joueur
        cell = None
        start = True
        compteur = 10
        while (self.test_win(1, 0, execute=False) and compteur) or start:
            compteur -= 1
            if cell:
                cell.off()
            start = False
            colomne = choice(self.grille.matrix)
            for i in range(len(colomne)):
                if colomne[i].get_etat() == 0:
                    cell = colomne[i]
            if cell:
                cell.set_etat(2)
        if compteur == 0:
            for colomne in self.grille.matrix:
                for i in range(len(colomne)):
                    if colomne[i].get_etat() == 0:
                        cell = colomne[i]
                if cell.is_clickable():
                    break
                else:
                    cell.off()
        if cell:
            cell.off()
            self.click(2, cell)


    def test_win(self, etat, niveau = 0, execute = False):
        """
        Methode qui verifie li le joueur d'etat :etat: peur gagner
        :niveau: int | a quel niveau (nombre de coups la fonction dois repondre)
        """
        for colomne in self.grille.matrix:
            cell = None
            for i in range(len(colomne)):
                if colomne[i].get_etat() == 0:
                    cell = colomne[i]
            if cell:
                cell.set_etat(etat)
                if test(self.grille.matrix, cell.get_pos(), etat):
                    cell.off()
                    if execute:
                        self.click(2, cell)
                    return True
                elif niveau > 0:
                    if self.test_win(etat, niveau-1, execute=False):
                        if etat == 1:
                            cell.set_etat(2)
                        if (self.test_win(1, niveau-1, execute=False) or self.test_win(1, niveau, execute=False)):
                            cell.off()
                            return False
                        elif execute:
                            cell.off()
                            self.click(2, cell)
                        else:
                            cell.off()
                        return True
                    else:
                        cell.off()
                else:
                    cell.off()
        return False 

def test(matrix, pos, etat = 1):
    """
    fonction qui traite si pour une case a la position :pos: donnée
    le joueur de l'etat :etat: peut gagner
    :matrix: lst | liste de liste 
    :pos: tupl | position de la case a tester
    :etat: int | 1 ou 2 etat du joueur a tester
    """
    testColl = test_coll(matrix, pos[0], etat, 4)
    testLigne = test_ligne(matrix, pos[1], etat, 4)
    testDiag = test_diag(matrix, pos, etat, 4)
    if testColl or testLigne or testDiag:
        return True
    return False

def test_diag(matrix, pos, etat, win = 4):
    """
    (A ameliorer)
    genere la liste des cases des 2 diagonales et verifie si il y en a 4 alignés
    """
    xMax = len(matrix)
    yMax = len(matrix[0])
    # verification de la premiere diag.
    x,y = pos
    liste = [(x,y)]
    while x < xMax-1  and y > 0:
        x,y = x+1, y-1    
        liste.append((x,y))

    x, y = pos
    while x > 0 and y < yMax-1:
        x, y = x-1, y+1
        liste.append((x, y))
    
    liste.sort(key=key)
    
    #test
    if len(liste) >= win and test_list(liste, matrix, etat, win):
        return True
    
    # puis de la 2nd
    liste = [pos]
    x, y = pos
    while x < xMax-1 and y < yMax-1:
        x,y = x+1, y+1
        liste.append((x,y))

    x, y = pos
    while x > 0 and y > 0:
        x, y = x-1, y-1
        liste.append((x, y))
    
    liste.sort(key=key)
    
    #test
    if len(liste) >= win and test_list(liste, matrix, etat, win):
        return True
    
    return False


def key(x):
    """clé de tri"""
    return x[0]


def test_list(liste, matrix, etat, x = 4):
    """
    Fonction utilisé par la methode test_diag()

    :liste: lst | liste de positions des cases a tester
    :etat: int | etat a tester
    :x: int | nombre de cases alignés pour renvoyer True(toujours 4)
    """
    compteur = 0
    for coords in liste:
        cell = matrix[coords[0]][coords[1]]
        if cell.get_etat() == etat:
            compteur += 1
            if compteur >= x:
                return liste
        else:
            compteur = 0


def test_coll(matrix, idColl, etat, x=4):
    """
    Fonction utilisé pour tester si un joueur a l'etat donnée peut gagner dans la colomne donnée
    :idColl: int | indice de la colomne a tester
    :etat: int | etat a tester
    :x: int | nombre de cases alignés pour renvoyer True(toujours 4)
    """
    compteur = 0
    for case in matrix[idColl]:
        if case.get_etat() == etat:
            compteur += 1
            if compteur >= x:
                return compteur
        else:
            compteur = 0
    return False


def test_ligne(matrix, idLigne, etat, x=4):
    """
    Fonction utilisé pour tester si un joueur a l'etat donnée peut gagner dans la ligne donnée
    :idLigne: int | indice de la ligne a tester
    :etat: int | etat a tester
    :x: int | nombre de cases alignés pour renvoyer True(toujours 4)
    """
    compteur = 0
    for colomne in matrix:
        if colomne[idLigne].get_etat() == etat:
            compteur += 1
            if compteur >= x:
                return compteur
        else:
            compteur = 0
    return False


def main():
    game = Game((7,6))
    _run = True
    jeu = False
    compteur = 0
    while _run:
        compteur += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _run = False
            if event.type == pygame.MOUSEBUTTONUP:
                pass
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_ESCAPE :
                    _run = False
            if event.type == pygame.KEYUP :
                if event.key == pygame.K_SPACE :
                    jeu = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed() == (1,0,0):
                    game.click(1, pygame.mouse.get_pos())
                if pygame.mouse.get_pressed() == (0,0,1):# pour faire des test et jouer a la place du bot
                    continue
                    game.click(2, pygame.mouse.get_pos())
                                        
        if compteur%200 == 0 and game.window_size != pygame.display.get_window_size():
            game.resize()
        
        if jeu:
            if game.etat in [0,1]:
                game.draw()
                if game.perdu:

                    game.fenetre.fill((100, 100, 100))
        else:
            game.start()
            jeu = True
        pygame.display.flip()
        
    pygame.quit()


if __name__ == "__main__" :    
    main()
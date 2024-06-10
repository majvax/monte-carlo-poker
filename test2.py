from deuces import Card, Evaluator, Deck
from os import system


class Joueur:
    def __init__(self, evaluator: Evaluator):
        self.main = []
        self.evaluator = evaluator

    
    def simuler_partie(self, n, cartes_tapis):
        victoires = 0
        for _ in range(n):
            # On crée un nouveau paquet
            paquet = Deck()
            
            # On retire les cartes du joueur et celles du tapis
            paquet.cards.remove(self.main[0])
            paquet.cards.remove(self.main[1])
            for carte in cartes_tapis:
                paquet.cards.remove(carte)
            
            # On tire les cartes du joueur
            player_main = paquet.draw(2)
    
            # On tire les cartes du tapis
            tapis = [carte for carte in cartes_tapis]
            tapis += [paquet.draw() for _ in range(5 - len(tapis))]
            
            # On évalue les mains
            carlo_score = self.evaluator.evaluate(self.main, tapis)
            player_score = self.evaluator.evaluate(player_main, tapis)
            
            if carlo_score < player_score:
                victoires += 1
        
        return victoires / n


class Poker:
    def __init__(self, n=100_000):
        self.evaluator = Evaluator()
        self.n = n
    
    @staticmethod
    def demander_carte():
        while True:
            carte = input("Entrez une carte (h=coeur, s=pique, d=carreau, c=trefle) :")
            if len(carte) != 2:
                print("Il faut enter deux caractères.")
                continue
            if carte[0] not in "23456789TJQKA":
                print("Valeur invalide.")
                continue
            if carte[1] not in "hsdc":
                print("Couleur invalide.")
                continue
            try:
                carte = Card.new(carte)
                return carte
            except Exception as _:
                print("Carte invalide.")
                continue
        

    def faire_manche(self):
        paquet = Deck()
        carlo = Joueur(self.evaluator)
        tapis = []
        
        # On demande les cartes du joueur
        carlo.main = [self.demander_carte() for _ in range(2)]
        # On retire les cartes du joueur du paquet
        paquet.cards.remove(carlo.main[0])
        paquet.cards.remove(carlo.main[1])   
        # On print les cartes du joueur
        print("Votre main: ", end="")
        Card.print_pretty_cards(carlo.main)
        # Calcul des chances de gagner au preflop
        print(f"Chance de gagner au Preflop: {carlo.simuler_partie(self.n, tapis)*100}%")
        
        
        tapis = [self.demander_carte() for _ in range(3)]
        print("Tapis: ", end="")
        Card.print_pretty_cards(tapis)
        print(f"Chance de gagner au Flop: {carlo.simuler_partie(self.n, tapis)*100}%")
        
        tapis.append(self.demander_carte())
        print("Tapis: ", end="")
        Card.print_pretty_cards(tapis)
        print(f"Chance de gagner à la Turn: {carlo.simuler_partie(self.n, tapis)*100}%")
        
        tapis.append(self.demander_carte())
        print("Tapis: ", end="")
        Card.print_pretty_cards(tapis)
        print(f"Chance de gagner à la River: {carlo.simuler_partie(self.n, tapis)*100}%")
        




    def erreur(self):
        carlo = Joueur(self.evaluator)
        paquet = Deck()
        tapis = []
        
        carlo.main = paquet.draw(2)

        tapis += paquet.draw(5)

        print("Votre main: ", end="")
        Card.print_pretty_cards(carlo.main)
        
        print("Tapis: ", end="")
        Card.print_pretty_cards(tapis)

        print(f"{carlo.simuler_partie(100, tapis)*100}%")
        print(f"{carlo.simuler_partie(1_000, tapis)*100}%")
        print(f"{carlo.simuler_partie(10_000, tapis)*100}%")
        print(f"{carlo.simuler_partie(100_000, tapis)*100}%")
        print(f"{carlo.simuler_partie(1_000_000, tapis)*100}%")


def main():
    while True:
        system('cls')
        Poker().faire_manche()
        if input("Voulez vous rejouer? (y/n): ").lower() != 'y':
            break

main()

    









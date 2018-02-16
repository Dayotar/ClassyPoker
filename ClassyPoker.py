import random
import sys
import operator
import math
import operator

player_hands = {}
players = []
score_hands = {}
player_score = {}
order_of_cards = []

cards = {1:"Two of Diamonds",2:"Three of Diamonds",3:"Four of Diamonds",
4:"Five of Diamonds",5:"Six of Diamonds",6:"Seven of Diamonds",
7:"Eight of Diamonds",8:"Nine of Diamonds",9:"Ten of Diamonds",
10:"Jack of Diamonds",11:"Queen of Diamonds",12:"King of Diamonds",13:"Ace of Diamonds",
14:"Two of Hearts",15:"Three of Hearts",16:"Four of Hearts",
17:"Five of Hearts",18:"Six of Hearts",19:"Seven of Hearts",
20:"Eight of Hearts",21:"Nine of Hearts",22:"Ten of Hearts",
23:"Jack of Hearts",24:"Queen of Hearts",25:"King of Hearts",26:"Ace of Hearts",
27:"Two of Spades",28:"Three of Spades",29:"Four of Spades",
30:"Five of Spades",31:"Six of Spades",32:"Seven of Spades",
33:"Eight of Spades",34:"Nine of Spades",35:"Ten of Spades",
36:"Jack of Spades",37:"Queen of Spades",38:"King of Spades",39:"Ace of Spades",
40:"Two of Clubs",41:"Three of Clubs",42:"Four of Clubs",
43:"Five of Clubs",44:"Six of Clubs",45:"Seven of Clubs",
46:"Eight of Clubs",47:"Nine of Clubs",48:"Ten of Clubs",
49:"Jack of Clubs",50:"Queen of Clubs",51:"King of Clubs",52:"Ace of Clubs"}

ranks = {1:1,2:2,3:3,4:4,5:5,6:6,7:7,8:8,9:9,10:10,11:11,12:12,13:13,
14:1,15:2,16:3,17:4,18:5,19:6,20:7,21:8,22:9,23:10,24:11,25:12,26:13,
27:1,28:2,29:3,30:4,31:5,32:6,33:7,34:8,35:9,36:10,37:11,38:12,39:13,
40:1,41:2,42:3,43:4,44:5,45:6,46:7,47:8,48:9,49:10,50:11,51:12,52:13}

# 1 through 13 represent "Two" through "Ace".

suits = {1:1,2:1,3:1,4:1,5:1,6:1,7:1,8:1,9:1,10:1,11:1,12:1,13:1,
14:2,15:2,16:2,17:2,18:2,19:2,20:2,21:2,22:2,23:2,24:2,25:2,26:2,
27:3,28:3,29:3,30:3,31:3,32:3,33:3,34:3,35:3,36:3,37:3,38:3,39:3,
40:4,41:4,42:4,43:4,44:4,45:4,46:4,47:4,48:4,49:4,50:4,51:4,52:4}

# 1 = "Diamond", 2 = "Heart", 3 = "Spade", 4 = "Club".

converter = {"01":"Two", "02":"Three", "03":"Four", "04":"Five", "05":"Six", "06":"Seven", "07":"Eight",
"08":"Nine", "09":"Ten", "10":"Jack", "1":"Jack", "11":"Queen", "12":"King", "13":"Ace"}

# "10" and "1" both map to "Jack" because Python deletes the trailing 0 for "10" if it is the last digit in the float after the decimal.

class Card:
    """
    This class defines the Card object with rank and suit attributes.
    """

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return cards[self.rank + (self.suit - 1) * 13]

    def get_rank(self):
        return self.rank

    def get_suit(self):
        return self.suit

class Hand:
    """
    This class defines the hands the players use and implements the functions to score them.
    card_list is a list of Card objects.
    """
    def __init__(self, card_list):
        self.card_list = card_list

    def __str__(self):
        hand_string = ""
        for i in range(len(self.card_list)):
            hand_string += (str(self.card_list[i]))
        return hand_string

    def score(self):
        """ 
        This function calculates the score of a hand.
        The digit before the decimal represents the type of hand made, e.g. 2 = pair, 3 = two pair, 4 = three of a kind.
        The digits after the decimal represent the cards in the hand and are used to break ties.
          -  e.g. 2.11 > 2.07  ==>  pair of Queens > pair of 8s.
        """
        for i in players:
            if player_hands[i].straight_flush() > 0:                                     #Dividing by 100 to create a decimal representing the rank of the pair/straight/etc. 2.01 = pair of 2s, 2.02 = pair of 3s, etc.
                player_score[i] = 9 + float(player_hands[i].straight_flush()/100)
            elif player_hands[i].four_of_a_kind() > 0:
                player_score[i] = 8 + float(player_hands[i].four_of_a_kind()/100)
            elif player_hands[i].full_house() > 0:
                player_score[i] = 7 + float(player_hands[i].full_house()/100)
            elif player_hands[i].flush() > 0:
                player_score[i] = 6 + float(player_hands[i].flush()/100)
            elif player_hands[i].straight() > 0:
                player_score[i] = 5 + float(player_hands[i].straight()/100)
            elif player_hands[i].set() > 0:
                player_score[i] = 4 + float(player_hands[i].set()/100)
            elif player_hands[i].two_pair() > 0:
                player_score[i] = 3 + float(player_hands[i].two_pair()/100)
            elif player_hands[i].pair() > 0:
                player_score[i] = 2 + float(player_hands[i].pair()/100)
            else:
                player_score[i] = 1 + float(player_hands[i].high_card()/100)
            

    def straight_flush(self):
        """ 
        This function checks for straight flushes.
        If there is not one, return 0.
        Else, return the value of the highest card in the straight flush. 
        """
        sf_check = []                                                #This line and the next 4 create a list of tuples in decending rank order, with (rank, suit) format.
        for x in self.card_list:
            sf_check.append((x.get_rank(), x.get_suit()))
        sf_check.sort(key = lambda tup: tup[0])
        sf_check = sf_check[::-1]
        sf_final = []
        suits_in_hand = []
        for x in self.card_list:                                     #Creates a list of suits to check if there is a flush.
            suits_in_hand.append(x.get_suit())
        for y in range(1, 5):
            if suits_in_hand.count(y) > 4:
                for i in range(len(sf_check)):                       #If flush, creates a list of associated ranks for checking straight.
                    if sf_check[i][1] == y:
                        sf_final.append(sf_check[i][0])
        for j in range(len(sf_final) - 4):                           #Checks if the flush cards form a straight.
            if len(sf_final) > 4:
                if sf_final[j] == (sf_final[j + 1] + 1) and sf_final[j + 1] == (sf_final[j + 2] + 1) and sf_final[j + 2] == (sf_final[j + 3] + 1) and sf_final[j + 3] == (sf_final[j + 4] + 1):
                    return sf_final[j]
        return 0  

    def four_of_a_kind(self):
        """ 
        This function checks for four of a kind.
        If there is not one, return 0.
        Else, return the the value of the card that there are 4 of plus the value of the highest other card / 100.
        """
        ranks_in_hand = []
        for x in self.card_list:
            ranks_in_hand.append(x.get_rank())
        for y in ranks_in_hand:
            if ranks_in_hand.count(y) > 3:
                high = sorted(set(ranks_in_hand))
                high.remove(y)
                return int(y) + (float(high[-1]) / 100)
        return 0

    def full_house(self):
        """ 
        This function checks for a full house.
        If there is not one, return 0.
        Else, return the value of the of the three of a kind plus the value of the pair / 100.
        """
        ranks_in_hand = []
        for x in self.card_list:
            ranks_in_hand.append(x.get_rank())
        for y in ranks_in_hand:
            for z in ranks_in_hand:
                if ranks_in_hand.count(y) > 2 and ranks_in_hand.count(z) > 1 and y != z:
                    return y + float(z / 100)
        return 0

    def flush(self):
        """ 
        This function checks for a flush.
        If there is not one, return 0.
        Else, return the five highest cards that make up the flush in descending order as pairs of digits in a float.
         - e.g. 11.09070503 = Queen, Ten, Eight, Six Four.
        """
        suits_in_hand = []
        ranks_in_hand = []
        for x in self.card_list:
            suits_in_hand.append(x.get_suit())
        for y in suits_in_hand:                                    #This checks for a flush                                       
            if suits_in_hand.count(y) > 4:
                for i in self.card_list:                           #This finds the highest card in the flush
                    if i.get_suit() == y:
                        ranks_in_hand.append(i.get_rank())
        try: 
            rank_check = list(set(sorted(ranks_in_hand)))[::-1]
            top_rank = (rank_check[0] + (rank_check[1] / 100) + (rank_check[2] / 10000) + (rank_check[3] / 1000000) + (rank_check[4] / 100000000))    #This turns the 5 cards in the flush into a float where each 2 decmials is a card.
            return (top_rank)     
        except: 
            return 0

    def straight(self):
        """ 
        This function checks for a straight.
        If there is not one, return 0.
        Else, return the value of the highest card in the straight.
        """
        straight_check = []
        for x in self.card_list:
            straight_check.append(x.get_rank())
        straight_check = list(set(sorted(straight_check)))
        straight_check = list(reversed(straight_check))
        if len(straight_check) > 4:
            for i in range(len(straight_check) - 4):
                if straight_check[i] == (straight_check[i + 1] + 1) and straight_check[i + 1] == (straight_check[i + 2] + 1) and straight_check[i + 2] == (straight_check[i + 3] + 1) and straight_check[i + 3] == (straight_check[i + 4] + 1):
                    return straight_check[i]
        return 0

    def set(self):
        """ 
        This function checks for a set.
        If there is not one, return 0.
        Else, return the value of the card that makes a set plus the next two highest cards.
        """
        ranks_in_hand = []
        for x in self.card_list:
            ranks_in_hand.append(x.get_rank())
        for y in ranks_in_hand:
            if ranks_in_hand.count(y) > 2:
                high = sorted(set(ranks_in_hand))
                high.remove(y)
                return int(y) + (float(high[-1]) / 100) + (float(high[-2]) / 10000)
        return 0

    def two_pair(self):
        """ 
        This function checks for two pair.
        If there is not one, return 0.
        Else, return the value of the higher pair plus the value of the lower pair / 100 plus the next highest card / 10000.
        """
        ranks_in_hand = []
        for x in self.card_list:
            ranks_in_hand.append(x.get_rank())
        for y in ranks_in_hand:
            for z in ranks_in_hand:
                if ranks_in_hand.count(y) > 1 and ranks_in_hand.count(z) > 1 and y != z:
                    high = sorted(set(ranks_in_hand))
                    high.remove(y)
                    high.remove(z)
                    if y > z:
                        return y + float(z / 100) + (float(high[-1]) / 10000)
                    else:
                        return z + float(y / 100) + (float(high[-1]) / 10000)
        return 0
 
    def pair(self):
        """ 
        This function checks for a pair.
        If there is not one, retun 0.
        Else, return the value of the card that pairs plus the next three highest cards.
        """
        ranks_in_hand = []
        for x in self.card_list:
            ranks_in_hand.append(x.get_rank())
        for y in ranks_in_hand:
            if ranks_in_hand.count(y) > 1:
                high = sorted(set(ranks_in_hand))
                high.remove(y)
                return int(y) + (float(high[-1])/100) + (float(high[-2]) / 10000) + (float(high[-3]) / 1000000)
        return 0

    def high_card(self):
        """ 
        This function returns the highest value card in the hand.
        If there is not one, return 0.
        Else, return the values of the five highest cards as a float.
        """
        ranks_in_hand = []
        for x in self.card_list:
            ranks_in_hand.append(x.get_rank())
        return float(sorted(ranks_in_hand)[-1]) + float(sorted(ranks_in_hand)[-2] / 100) + float(sorted(ranks_in_hand)[-3] / 10000) + float(sorted(ranks_in_hand)[-4] / 1000000) + float(sorted(ranks_in_hand)[-5] / 100000000)

def flop():
    """
    This function handles the flop.
    """
    del order_of_cards[0] #Burns a card
    flop1 = Card(ranks[order_of_cards[0]], suits[order_of_cards[0]])
    flop2 = Card(ranks[order_of_cards[1]], suits[order_of_cards[1]])
    flop3 = Card(ranks[order_of_cards[2]], suits[order_of_cards[2]])
    print("\nThe Flop is - " + str(flop1) + ", " + str(flop2) + ", " + str(flop3) + "\n")
    for i in players:
        player_hands[i].extend((flop1, flop2, flop3))
    del order_of_cards[0:3]

def turn():
    """
    This function handles the turn.
    """
    del order_of_cards[0] #Burns a card.
    turn_card = Card(ranks[order_of_cards[0]], suits[order_of_cards[0]])
    print("\nThe Turn is - " + str(turn_card) + "\n")
    for i in players:
        player_hands[i].append(turn_card)
    del order_of_cards[0]

def river():
    """
    This functions deals the river card and calls the score function on player hands.
    """
    del order_of_cards[0] #Burns a card.
    river_card = Card(ranks[order_of_cards[0]], suits[order_of_cards[0]])
    print("\nThe River is - " + str(river_card) + "\n")
    for i in players:
        player_hands[i].append(river_card)
    del order_of_cards[0]
    
def showdown():
    """
    This function handles a showdown where the players hands are scored and revealed
    """
    parsed = {}
    for i in players:
        player_hands[i] = Hand(player_hands[i])
    print("\n***********************************************************\n")
    for i in players:
        score_hands[i] = player_hands[i].score()
        parsed[i] = hand_parser(player_score[i])  
        print(str(i) + " has " + (parsed[i]))
    print("\nThe winner is " + winner() + " with " + hand_parser(player_score[winner()]) + "\n\n\n        ******* Thank you for playing! *******\n")

def winner():
    """
    This function determines the winner of the game.
    """  
    return max(player_score, key=player_score.get)

def shuffle():
    """ 
    This function creates a deck of 52 cards and shuffles them.
    """
    for x in range(1, 53):
        order_of_cards.append(x)
    random.shuffle(order_of_cards)
    return order_of_cards

def converter(card_number):
    """
    This function converts a two-digit card number string into a string - e.g. 02 -> "Three".
    Args : two digit string.
    Returns : string of card name.
    """
    card_converter = {"01":"Two", "02":"Three", "03":"Four", "04":"Five", "05":"Six", "06":"Seven", "07":"Eight",
                 "08":"Nine", "09":"Ten", "10":"Jack", "1":"Jack", "11":"Queen", "12":"King", "13":"Ace"}
    return card_converter[card_number]

def hand_parser(value):
    """
    This function takes the value of a hand and translates it into a string representing the hand in natural language.
    Args : a float representing hand strength.
    Returns : a string representing the hand in natural language.
    """
    strength = math.floor(value)
    card1 = str(value)[2:4]
    card2 = str(value)[4:6]
    card3 = str(value)[6:8]
    card4 = str(value)[8:10]
    card5 = str(value)[10:12]

    if strength == 9:
        return "a Straight Flush - " + converter(card1) + " high!"
    if strength == 8:
        return "Four " + converter(card1) + "s, " + converter(card2) + " kicker!"
    if strength == 7:
        return "a Full House - " + converter(card1) + "s full of " + converter(card2) + "s!"
    if strength == 6:
        return "a Flush - " + converter(card1) + " high! (" + converter(card2) + ", " + converter(card3) + ", " + converter(card4) + ", " + converter(card5) + ")"
    if strength == 5:
        return "a Straight - " + converter(card1) + " high!"
    if strength == 4:
        return "a Set of " + converter(card1) + "s - " + converter(card2) + " and " + converter(card3) + " for kickers!"
    if strength == 3:
        return "Two Pair - " + converter(card1) + "s and " + converter(card2) + "s, " + converter(card3) + " kicker!"
    if strength == 2:
        return "a Pair of " + converter(card1) + "s! (" + converter(card2) + ", " + converter(card3) + ", " + converter(card4) + ")"
    if strength == 1:
        return "High card - " + converter(card1) + "! (" + converter(card2) + ", " + converter(card3) + ", " + converter(card4) + ", " + converter(card5) + ")"

def start_game():
    """ 
    This function calls shuffle() and deals opening hands to x players.
    If x is greater than 22, the game stops, since the deck can only handle at most 22 players.
    """
    print("\n***********************************************************")
    print("\nWelcome to Classy Poker, an implementation of Texas Hold'em\n\n              Written By -- Andrew Moffatt       ")
    print("\n***********************************************************")    
    num_players = input("\nHow many players?  ")
    if int(num_players) > 22:
        print("\nToo many players for the deck to handle!")
        sys.exit()    
    for player in range(int(num_players)):
        players.append("Player " + str(player + 1))
    shuffle()
    print("\n***********************************************************\n")
    for i in range(int(num_players)):
        print("Player " + str(i + 1) + "'s hand is: " + cards[order_of_cards[i * 2]], "&", cards[order_of_cards[i * 2 + 1]])
    print("")
    for i in players:
        player_hands[i] = [Card(ranks[order_of_cards[0]], suits[order_of_cards[0]]), Card(ranks[order_of_cards[1]], suits[order_of_cards[1]])]
        del order_of_cards[0]
        del order_of_cards[0]
    return player_hands

def new_game():
    """
    This function starts the game and handles the 3 phases of 'flop', 'turn', 'river', and 'showdown', then determines the winner.
    """
    start_game()
    print("***********************************************************\n")
    flop_check = input("        ******* Is there a flop? Yes/No  *******    ")
    if flop_check == "Yes" or flop_check == "y" or flop_check == "yes" or flop_check == "Y":
        flop()
    else:
        print("\nWinner!")
        sys.exit()
    turn_check = input("        ******* Is there a turn? Yes/No  *******    ")
    if turn_check == "Yes" or turn_check == "y" or turn_check == "yes" or turn_check == "Y":
        turn()    
    else:
        print("\nWinner!")
        sys.exit()
    river_check = input("        ******* Is there a river? Yes/No *******    ")    
    if river_check == "Yes" or river_check == "y" or river_check == "yes" or river_check == "Y":
        river()   
    else:
        print("\nWinner!")
        sys.exit()
    showdown_check = input("        ****** Is there a showdown? Yes/No *****    ")
    if showdown_check == "Yes" or showdown_check == "y" or showdown_check == "yes" or showdown_check == "Y":
        showdown()
    else:
        print("\nWinner!")
        sys.exit()        


new_game()
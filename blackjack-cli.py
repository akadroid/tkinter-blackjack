# Danny Huynh

import random, time

lists = []
player_hand = []
dealer_hand = []
suits = ["Diamonds", "Hearts", "Clubs", "Spades"]
values = ["Ace", 2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King"]
face_values = {
    "Ace": {'A': 1, 'B': 11},
    "Jack": 10,
    "Queen": 10,
    "King": 10
    }

class card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
    def print_dealer(self):
        print(f"The Dealer has: {self.value} of {self.suit}")    
    def print_player(self):
        print(f"You Have: {self.value} of {self.suit}")

def deck():
    for i in range(13):
        for b in range(4):
            lists.append(card(values[i], suits[b]))
    random.shuffle(lists)


def draw(number, person):
    # Adds cards to hand and removes them from deck
    if person == 'p':
        for i in range(number):
            player_hand.append(lists[0])
            lists.pop(0)
    else:
        for j in range(number):
            dealer_hand.append(lists[0])
            lists.pop(0)

def hand_value(counter, current_value, person):
    value = 0
    i= 0

    # Determine if calculating hand value for player or dealer
    if person == 'p':
        i = player_hand
    else:
        i = dealer_hand

    # Add card values to the player/dealer's score
    for k in range(counter):
        if i[k].value in face_values:
            if i[k].value == "Ace":
                if current_value < 11:
                    value += face_values[i[k].value]['B']
                else:
                    value += face_values[i[k].value]['A']
            else:
                value += face_values[i[k].value]
        else:
            value += i[k].value  
    return(value)

def print_hand(player_counter, dealer_counter, player, dealer):
    print("\n\n\n\n\n\n")
    
    # Prints the player's hand
    for j in range(player_counter):
        player_hand[j].print_player()
    print(f"Value: {player}")

    # Prints the dealer's hand
    for k in range(dealer_counter):
        dealer_hand[k].print_dealer()
    print(f"Dealer Value: {dealer}")

def main():
    deck()
    print(lists[0])
    player_counter = 2
    dealer_counter = 1
    draw(2, 'p')
    draw(1, 'd')
    player = hand_value(player_counter, 0, 'p')
    dealer = hand_value(dealer_counter, 0, 'd')

    while True:
        print_hand(player_counter, dealer_counter, player, dealer)

        if player == 21:
            print("You win!")
            return True
        elif player > 21:
            print("You lose")
            return False

        response = input("\nHit or Stand? (h/s): ")
        if response == 'h':
            i = player
            player_counter += 1
            draw(1, 'p')
            player = hand_value(player_counter, i, 'p')

        elif response == 's':
            while True:
                time.sleep(1)
                print_hand(player_counter, dealer_counter, player, dealer)
                if dealer < 17:
                    j = dealer
                    dealer_counter += 1
                    draw(1, 'd')
                    dealer = hand_value(dealer_counter, j, 'd')
                else:
                    break

            if dealer == player:
                print("Push")
                return False
            elif dealer > 21:
                print("You win")
                return True
            elif dealer > player:
                print("You lose")
                return False
            elif dealer < player:
                print("You win!")
                return True
            else:
                print("Error.")
main()

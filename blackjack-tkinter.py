# Danny Huynh

import random, time
import tkinter as tk
from PIL import ImageTk, Image  
import os

card_images = []
lists = []
player_hand = []
dealer_hand = []
suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
values = [10, 2, 3, 4, 5, 6, 7, 8, 9, "Ace", "Jack", "King", "Queen"]
face_values = {
    "Ace": {'A': 1, 'B': 11},
    "Jack": 10,
    "Queen": 10,
    "King": 10
    }

class card:
    def __init__(self, value, suit, card_img):
        self.value = value
        self.suit = suit
        self.card_img = card_img

    def print_dealer(self):
        print(f"The Dealer has: {self.value} of {self.suit}")

    def print_player(self):
        print(f"You Have: {self.value} of {self.suit}")

class Player(tk.Frame):
    def __init__(self, container, player_counter, dealer_counter, dealer, player_value, dealer_value):
        super().__init__(container)
        self.container = container
        self.player_counter = player_counter
        self.dealer_counter = dealer_counter
        self.dealer = dealer
        self.player_value = player_value
        self.dealer_value = dealer_value
        self.x = False
        self.var = tk.StringVar()
        self.ivar = tk.IntVar()
        self.container['background'] = 'green'
        
        self.label = tk.Label(self, text='Blackjack')        
        self.value_label = tk.Label(self, textvariable=self.ivar)
        self.win_label = tk.Label(self, textvariable=self.var) 
        self.hit_button = tk.Button(self, text="Hit", command=self.hit)
        self.stand_button = tk.Button(self, text="Stand", command=self.stand)
        
        self.label.pack()
        self.win_label.pack(side='bottom')
        self.stand_button.pack(side='bottom')
        self.hit_button.pack(side='bottom')
        self.value_label.pack(side='bottom')
        
    def draw_player_card(self, img):
        self.img_label = tk.Label(self, image=img)
        self.img_label.pack(side='left')
    
    def hit(self):
        if self.x == False:
            i = self.player_value
            self.player_counter += 1
            draw(1, 'p')
            self.player_value = hand_value(self.player_counter, i, 'p')
            self.draw_player_card(player_hand[self.player_counter - 1].card_img)
        
    def stand(self):
        self.x = True
    
    def stop(self):
        self.container.destroy()
        quit()
        
    def game(self, root):
        self.ivar.set(self.player_value)
        if self.player_value == 21:
            self.var.set("You win!")
            root.after(4000, self.stop)
        if self.player_value > 21:
            self.var.set("You lose...")
            root.after(4000, self.stop)
            
        if self.x == True:
            time.sleep(1)
            if self.dealer_value < 17:
                j = self.dealer_value
                self.dealer_counter += 1
                draw(1, 'd')
                self.dealer_value = hand_value(self.dealer_counter, j, 'd')
                self.dealer.draw_dealer_card(dealer_hand[self.dealer_counter - 1].card_img)
            else:    
                if self.dealer_value == self.player_value:
                    self.var.set("Push")
                    root.after(4000, self.stop)
                elif self.dealer_value > 21:
                    self.var.set("You win!")
                    root.after(4000, self.stop)
                elif self.dealer_value > self.player_value:
                    self.var.set("You lose...")
                    root.after(4000, self.stop)
                elif self.dealer_value < self.player_value:
                    self.var.set("You win!")
                    root.after(4000, self.stop)
                else:
                    print("Lol")
        root.after(100, self.game, root)
        
class Dealer(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.container = container
        self.container['background'] = 'green'
        
        self.label = tk.Label(self, text='Dealer')
        
        self.label.pack()
    def draw_dealer_card(self, img):
        self.img_label = tk.Label(self, image=img)
        self.img_label.pack(side='left')
        
def load_images():
    path = os.getcwd() + "/assets"
    for image in os.listdir(path):
        x = Image.open(os.path.join(path, image))
        card_image = ImageTk.PhotoImage(x.resize((100,146)))
        card_images.append(card_image)
        
def create_deck():
    z = 0
    for i in range(13):
        for b in range(4):
            lists.append(card(values[i], suits[b], card_images[z]))
            z += 1
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
        if i[k].value in face_values: # Checks value if face card
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

def draw_hand_img(player_counter, dealer_counter, tkplayer, tkdealer):
    # Used to draw the initial hand
    for j in range(player_counter):
        tkplayer.draw_player_card(player_hand[j].card_img)
    
    for k in range(dealer_counter):
        tkdealer.draw_dealer_card(dealer_hand[k].card_img)

def main():
    root = tk.Tk()
    root.geometry("1000x750")
    root.title("Blackjack")
    
    player_counter = 2
    dealer_counter = 1
    load_images()
    create_deck()
    
    # add cards to player hand
    draw(2, 'p')
    # add cards to dealer hand
    draw(1, 'd')
    player_value = hand_value(player_counter, 0, 'p')
    dealer_value = hand_value(dealer_counter, 0, 'd')
    
    dealer = Dealer(root)
    app = Player(root, player_counter, dealer_counter, dealer, player_value, dealer_value)
    
    app.pack()
    dealer.pack(pady='50')
    draw_hand_img(player_counter, dealer_counter, app, dealer)
    
    root.after(0, app.game, root)
    root.mainloop() 
main()

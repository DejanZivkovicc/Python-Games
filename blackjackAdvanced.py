import sys
import random
import time

""" Function that assings card to the hand """
def assignCard(cards):
    # Assigning card to hand, either it's players or houses
    randomCard = random.choice(cards)
    
    handSum = 0
    handCards = ""

    # Determining the value of a card
    if randomCard[0] == 'J' or randomCard[0] == 'Q' or randomCard[0] == 'K':
        handSum += 10
    elif randomCard[0] == 'A':
        # if handSum >= 11:
        #     handSum += 1
        # else:
        #     handSum += 11
        handSum += 11
    else:
        handSum += randomCard[0]

    # Adding cards to the hand
    handCards += str(randomCard)
    
    # Removing that card from the deck of cards
    cards.remove(randomCard)

    # Returning value and name of the card
    hand = [handSum, handCards]
    return hand

""" Function that checks is command from the standard input valid """
def checkIsCommandValid(command):
    commands = ['HIT', 'STAND', 'DOUBLE', 'H', 'S', 'D']

    if command not in commands:
        print("Unknown command. Try again:", end=" ")
        return False
    else:
        return True

""" Function that makes action after valid command from stdin """
def checkCommandAction(command):
    if command == 'STAND' or command == 'S':
        return 'S'
    elif command == 'HIT' or command == 'H':
        return 'H'
    else:
        return 'D'

# Player's money
money = 1000

""" Main function """
def main():
    # Introduction to the game
    # print("---------Game: Blackjack---------")

    global money

    # Introcution to the player/place your bets
    try:
        bet = int(input("Enter your bet: $"))
    except ValueError as err:
        print("Incorrect input. Game resets.", err)
        sys.exit(1)
    
    # Subtracking a bet from the total money
    if money >= bet:
        money = money - bet
    else:
        print("You can't bet with more than you have. Try again.")
        return 2
    
    print(f"Hello {name}! Have fun playing :-)")
    print(f"Your balance is ${money}.")
    time.sleep(1)
    print("--------------------------", flush=True)
    print(f"    --Game begins:--")
    print("--------------------------", flush=True)
    time.sleep(1)

    # Initializing deck of cards: 13 cards for each symbol (spades (♠), clubs (♣), hearts (♥) and diamonds (♦))
    cards = [
        ('A', 'S'), (2, 'S'), (3, 'S'), (4, 'S'), (5, 'S'), (6, 'S'), (7, 'S'), (8, 'S'), (9, 'S'), (10, 'S'), ('J', 'S'), ('Q', 'S'), ('K', 'S'),
        ('A', 'C'), (2, 'C'), (3, 'C'), (4, 'C'), (5, 'C'), (6, 'C'), (7, 'C'), (8, 'C'), (9, 'C'), (10, 'C'), ('J', 'C'), ('Q', 'C'), ('K', 'C'),
        ('A', 'H'), (2, 'H'), (3, 'H'), (4, 'H'), (5, 'H'), (6, 'H'), (7, 'H'), (8, 'H'), (9, 'H'), (10, 'H'), ('J', 'H'), ('Q', 'H'), ('K', 'H'),
        ('A', 'D'), (2, 'D'), (3, 'D'), (4, 'D'), (5, 'D'), (6, 'D'), (7, 'D'), (8, 'D'), (9, 'D'), (10, 'D'), ('J', 'D'), ('Q', 'D'), ('K', 'D')
    ]

    # Initializing (first) hand for the player
    playerSum = 0
    playerCards = ""
    numberOfAces = 0

    # Initializing (first) hand for the House
    houseSum = 0
    houseCards = ""

    # Announcing what initial cards do player and house have
    for i in range(3):

        # Adding a card to the player
        if i % 2 == 0:
            hand = assignCard(cards)
            playerSum += hand[0]
            playerCards += hand[1]

            if 'A' in hand[1]:
                numberOfAces += 1

            # If player got a double ACE cards, reduce card sum in his hand by 10 (from 22 to 12)
            if playerSum == 22:
                playerSum -= 10
                numberOfAces -= 1

            if i == 0:
                print(f"Your card is: {playerCards} (SUM: {playerSum})", flush=True)
            else:
                print(f"Your cards are: {playerCards} (SUM: {playerSum})", flush=True)
            time.sleep(1)

        # Adding a card to the house
        else:
            hand = assignCard(cards)
            # print(f"---------->hand = {hand}<----------------", flush=True)
            houseSum += hand[0]
            houseCards += hand[1]

            print(f"Card of the house is: {houseCards} (SUM: {houseSum})", flush=True)
            time.sleep(1)          

    # If player got an ACE and 10, J, Q or K, he wins immidiately
    if playerSum == 21:
        print(f"CONGRATULATIONS, {name}! YOU'VE WON!\nCome back again! :-)")
        money += (bet*3)//2
        # sys.exit(1)
        return 1

    # Adding more cards to the players hand, by players command
    while True:
        print("------Player action------")
        try:
            command = input("Hit, Stand or Double (H/S/D)? ").upper()
        except ValueError:
            print("Invalid command. Game will reset.")
            sys.exit(1)

        if checkIsCommandValid(command) == False:
            continue
        
        if checkCommandAction(command) == 'H':
            hand = assignCard(cards)
            playerSum += hand[0]
            playerCards += hand[1]

            if 'A' in hand[1]:
                numberOfAces += 1

            # If player got ACE and has sum in hands over 21, use ACE = 1 instead ACE = 11
            if 'A' in playerCards and playerSum > 21:
                if numberOfAces > 0:
                    playerSum -= 10
                    numberOfAces -= 1

            # Check is sum of cards in players hand over bound (>21)
            if playerSum > 21:
                print(f"Unfortunately {name}, you've lost.\nYour cards were: {playerCards} (SUM: {playerSum})", flush=True)
                time.sleep(1)
                #sys.exit(1)
                return 1

            print(f"Your cards are: {playerCards} (SUM: {playerSum})", flush=True)
            time.sleep(1)
        elif checkCommandAction(command) == 'D':
            money -= bet
            # print(f"Your balance is ${money}.")
            hand = assignCard(cards)
            playerSum += hand[0]
            playerCards += hand[1]

            # If player got ACE and has sum in hands over 21, use ACE = 1 instead ACE = 11
            if 'A' in playerCards and playerSum > 21:
                playerSum -= 10

            # If player got ACE and has sum in hands over 21, use ACE = 1 instead ACE = 11
            if 'A' in playerCards and playerSum > 21:
                if numberOfAces > 0:
                    playerSum -= 10
                    numberOfAces -= 1
            
            # Check is sum of cards in players hand over bound (>21)
            if playerSum > 21:
                print(f"Unfortunately {name}, you've lost.\nYour cards were: {playerCards} (SUM: {playerSum})", flush=True)
                time.sleep(1)
                # sys.exit(1)
                return 1

            print(f"Your cards are: {playerCards} (SUM: {playerSum})", flush=True)
            time.sleep(1)
            break
        else:
            break
    
    print("------House action------")
    # House's turn: Adding cards to the house's hand
    while True:
        hand = assignCard(cards)
        houseSum += hand[0]
        houseCards += hand[1]

        print(f"Cards of the house are: {houseCards} (SUM: {houseSum})", flush=True)
        time.sleep(1)  

        if houseSum <= 16:
            continue
        elif houseSum >= 17 and houseSum <= 21:
            if houseSum > playerSum:
                print(f"Unfortunately {name}, you've lost. Better luck next time! :-)", flush=True)
                time.sleep(1)
                # sys.exit(1)
                return 1
            elif houseSum == playerSum:
                print(f"Draw! Everyone gets their bet back. It was great playing with you, {name}!", flush=True)
                money += bet
                time.sleep(1)
                # sys.exit(1)
                return 1
            else:
                print(f"CONGRATULATIONS, {name}! YOU'VE WON!\nCome back again! :-)")
                money += bet*2
                # sys.exit(1)
                return 1
        else:
            print(f"CONGRATULATIONS, {name}! YOU'VE WON!\nCome back again! :-)")
            money += bet*2
            # sys.exit(1)
            return 1

# Introduction to the game
print("---------Game: Blackjack---------")

# Enter your name (just once)
try:
    name = input("Enter your name: ")
except ValueError:
    print("Invalid command. Game will reset.")
    sys.exit(1)

# Calling main function
while True:
    if main() == 1:
        print("--------------------------")
        print(f"Your balance is ${money}.")

        if money == 0:
            print("You have lost it all! Now go back to your home, disgrace.")
            sys.exit(1)
        
        print("--------------------------")

        try:
            response = input("Do you want to play again (yes|no)? ")
        except ValueError:
            print("Invalid command. Game will reset.")
            sys.exit(1)
        
        if response == "yes":
            # Introduction to the game
            print("---------------------------------")
            print("---------Game: Blackjack---------")
            continue
        elif response == "no":
            print(f"It was fun playing with you, {name}! Come back soon!")
            sys.exit(1)
        else:
            while True:
                print("Invalid command. Try again: ")
                response = input("Do you want to play again (yes|no)? ")

                if response == "yes":
                    break
                elif response == "no":
                    sys.exit(1)
                else:
                    continue
            continue
    else:
        continue

# Quinton Latimer
# This program is meant to simulate the game of Blackjack with the exception of the "5 charlie" situation. 

# import class for the deck of cards
from DeckOfCards import *


#------Score function and Ace handling--------------------------------------------------------------------------------------------------------------


# function to handle score calculation and ace handling
def calc_score(hand):
    total = 0
    ace_count = 0

    # updates hand total and tracks number of aces in hand
    for card in hand:
        total += card.val
        if card.face == "Ace":
            ace_count += 1
    
    # if the hand total is abover 21 and you have an ace, the total will subtract 10 and the ace count will decrease to show you've "used" the ace
    # to avoid having unlimited -10 occurances
    while total > 21 and ace_count > 0:
        total -= 10
        ace_count -= 1

    # returns the total scor eof the hand after the modifiers
    return total 

# calls the deck of cards class and prints the deck
deck = DeckOfCards()
print("Deck before shuffle\n")


#------Print, Shuffle, and Deal----------------------------------------------------------------------------------------------------------------------------
   

# While loop to shuffle the current deck if the player wants to play agin instead of getting a new deck or restarting the program
x = 0
while x == 0:

    # prints the current deck and then shuffles it, printing the result
    deck.print_deck()
    deck.shuffle_deck()
    print("Deck after shuffle\n")
    deck.print_deck()

#---------Player cards---------

    # deal two cards to the user and prints the card values and score using lists
    players_cards = []
    players_cards.append(deck.get_card())
    players_cards.append(deck.get_card())

    # variable to keep track of how many cards the player and dealer have
    player_card_num = 0

    # prints all cards currently in the players hand or list and updates number of cards
    for card in players_cards:
        player_card_num += 1
        print(f"\nCard number {player_card_num}: {card.face} of {card.suit}")
    score = calc_score(players_cards)

    print("\nYour score is: ", score)

#---------Dealer cards----------

    # deal two cards to the dealer and record the card values and score using lists 
    dealers_cards = []
    dealers_cards.append(deck.get_card())
    dealers_cards.append(deck.get_card())

    # variables to keep track of the dealers number of cards
    dealer_card_num = 0

    # record updated score of dealers hand
    dealer_score = calc_score(dealers_cards)


#------Player-----------------------------------------------------------------------------------------------------------------------------------------
    

    # marker variable for ending while loop
    user_play = 1
    # while loop to append new cards to user hand as long as they want to hit and are not above 21
    while user_play != 0:

        # ask user if they would like a "hit" (another card)
        hit = input("\nWould you like to hit? (y/n)")

        if hit == 'y':
            
            # appends new card to player hand and updates score as well as card number count
            new_card = deck.get_card() # Capture it
            players_cards.append(new_card) # Add it to list
            score = calc_score(players_cards) # Add NEW card value to score
                
            # prints new card and updated score for the player
            print(f"\nCard number {player_card_num}: {new_card.face} of {new_card.suit}")
            print("\nnew score: ", score)

            # if the players score is still above 21 the game ends and they receive a lsoing message
            if score > 21:
                print("\nYOU DONE JUST BUSTED! YOU LOSE!")
                user_play = 0
        
        else:
            break


#------Dealer---------------------------------------------------------------------------------------------------------------------------------------


    # logic to run the rest of the game if the player hasn't busted 
    if score <= 21:

        # while loop to append dealer cards to dealer hand as long as dealer score is less than 17
        dealer_play = 1
        while dealer_play != 0:
            
            # appends new card to dealer hand and updates score
            if dealer_score < 17:
                new_dealer_card = deck.get_card()
                dealers_cards.append(new_dealer_card)
                dealer_score = calc_score(dealers_cards)
                
            else:
                dealer_play = 0


#------Decision-----------------------------------------------------------------------------------------------------------------------------------------


        # main logic to decide who has won and who has lost or to decide if there has been a tie
        # player has won due to dealer busting
        if dealer_score > 21:
            for card in dealers_cards:
                dealer_card_num += 1
                print(f"\nDealer card number {dealer_card_num}: {card.face} of {card.suit}")
            print(f"\nThe Dealer's score is {dealer_score}")
            print(f"\nYour score is {score}")
            print("\nYOU DONE JUST WON, SON!")

        # player has won based on having higher points than the dealer
        elif score > dealer_score and score <= 21:
            
            for card in dealers_cards:
                dealer_card_num += 1
                print(f"\nDealer card number {dealer_card_num}: {card.face} of {card.suit}")
            print(f"\nThe Dealer's score is {dealer_score}")
            print(f"\nYour score is {score}")
            print ("\nYOU DONE JUST WON, SON!")
           
        # player has lost based on having lower points than the dealer
        elif score < dealer_score and score <= 21:
            
            for card in dealers_cards:
                dealer_card_num += 1
                print(f"\nDealer card number {dealer_card_num}: {card.face} of {card.suit}")
            print(f"\nThe Dealer's score is {dealer_score}")
            print(f"\nYour score is {score}")
            print ("\nYOU DONE JUST LOST, SON!")

        # the player and the dealer have a tie
        elif score == dealer_score:

            for card in dealers_cards:
                print(f"\nDealer card number {dealer_card_num}: {card.face} of {card.suit}")
            print(f"\nThe Dealer's score is {dealer_score}")
            print(f"\nYour score is {score}")
            print ("\nTHE DEALER DONE JUST WON ON A PUSH! YOU LOSE!")
    else:
        pass


#------Play Again?---------------------------------------------------------------------------------------------------------------------------------------


    # Option to let user play again or not
    play_again = input("\nHow about another try? (y/n)")
    if play_again == 'y':
        pass
    elif play_again == 'n':
        x = 1
    
print("\nThanks for playing!\n")
    

    

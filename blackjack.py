import random as rand
from network_brython import connect, send
from browser import aio, window, alert
doc = window.document

dealer_total = 0
player_total = 0
dealer_aces = 0
player_aces = 0
player2_total = 0
player2_aces = 0
dealer_hand = []
player_hand = []
dealer_hidden = []
deck = []
to_hit = bool
card_value = []
game_message = ""


def build_deck():
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    suits = ["C", "D", "H", "S"]
    global deck

    for i in suits:
        for j in ranks:
            deck.append(f'{j}-{i}')


def shuffle_deck():
    rand.shuffle(deck)
    print(deck)


def get_value(card):
    global card_value
    global dealer_hidden
    global player_total
    global dealer_total
    data = card.split("-")
    card_value = data[0]

    if card_value == "A":
        return int(1)
    elif card_value == "J":
        return int(10)
    elif card_value == "Q":
        return int(10)
    elif card_value == "K":
        return int(10)
    else:
        return int(card_value, 0)


def check_for_ace(card):
    if (card[0] == "A"):
        return 1
    else:
        return 0


def adjust_for_ace(player_totals, player_ace):
    while player_ace > 0 & player_totals > 21:
        player_totals -= 10
        player_ace -= 1

    return player_totals


def hit(event):
    global to_hit
    global player_total
    global player_aces
    global deck
    global game_message
    if player_total >= 21:
        to_hit = False
    else:
        card_image = doc.createElement("img")
        card = deck.pop()
        card_image.src = "/cards/" + card + ".png"
        card_image.alt = "Altier text"
        player_total += get_value(card)
        player_aces += check_for_ace(card)
        doc.getElementById("player-cards").append(card_image)
        doc.getElementById("player1").innerText = (f"Player 1: {player_total}")


def stay(event):
    global to_hit
    global dealer_hidden
    global dealer_total
    global player_total
    global dealer_aces
    global player_aces
    global game_message
    dealer_total = adjust_for_ace(dealer_total, dealer_aces)
    player_total = adjust_for_ace(player_total, player_aces)

    to_hit = False
    hidden = doc.getElementById("hidden-card")
    hidden.src = "/cards/" + dealer_hidden + ".png"
    hidden.alt = "alt"
    while dealer_total < 17:
        card_image = doc.createElement("img")
        card = deck.pop()
        card_image.src = "./cards/" + card + ".png"
        dealer_total += get_value(card)
        dealer_aces += check_for_ace(card)
        doc.getElementById("dealer-cards").append(card_image)
    doc.getElementById("dealer").innerText = (f"Dealer: {dealer_total}")

    game_message = ""
    if player_total > 21:
        game_message = 'You lose'
    elif dealer_total > 21:
        game_message = 'You win'
    elif player_total == dealer_total:
        game_message = 'Push'
    elif player_total > dealer_total:
        game_message = 'You win'
    elif player_total < dealer_total:
        game_message = 'You lose'
    pass

    alert(game_message)


def deal_hidden():
    global dealer_hidden
    dealer_hidden = deck.pop()
    hidden_card_image = doc.createElement("img")
    hidden_card_image.id = "hidden-card"
    hidden_card_image.src = "/cards/back_of_card.png"
    hidden_card_image.alt = "Alt text"
    doc.getElementById("dealer-cards").append(hidden_card_image)


def initialize_game():
    global dealer_hand
    global dealer_hidden
    global deck
    global dealer_total
    global dealer_aces
    global player_aces
    global player_total
    global game_message
    global player2_total
    global player2_aces
    #alert("Welcome to blackjack!\nDealer hits on all 17s\nPush = Tie\nCan't get ace adjustment to work... :(")
    deal_hidden()
    print(dealer_hidden)
    dealer_total += get_value(dealer_hidden)
    dealer_aces += check_for_ace(dealer_hidden)
    card = deck.pop()
    card_image = doc.createElement("img")
    card_image.src = "/cards/" + card + ".png"
    card_image.alt = "Alt text"
    doc.getElementById("dealer-cards").append(card_image)
    dealer_total += get_value(card)
    dealer_aces += check_for_ace(card)
    doc.getElementById("dealer").innerText = ("Dealer: ?")
    for i in range(2):
        card_image = doc.createElement("img")
        card = deck.pop()
        card_image.src = "/cards/" + card + ".png"
        card_image.alt = "Altier text"
        doc.getElementById("player-cards").append(card_image)
        player_total += get_value(card)
        player_aces += check_for_ace(card)
        doc.getElementById("player1").innerText = (f"Player 1: {player_total}")
        print(f"p: {player_total}, {card}")
    for i in range(2):
        card_image = doc.createElement("img")
        card = deck.pop()
        card_image.src = "/cards/" + card + ".png"
        card_image.alt = "Altest text"
        player2_aces += check_for_ace(card)
        player2_total += get_value(card)
        doc.getElementById("player2-cards").append(card_image)
        doc.getElementById("player2").innerText = (
            f"Player 2: {player2_total}")
        print(f"p: {player2_total}, {card}")
    doc.getElementById("hit-button").addEventListener("click", hit)
    doc.getElementById("stay-button").addEventListener("click", stay)


def deal_card_to_player():
    card_image = doc.createElement("img")
    card = deck.pop()
    card_image.src = "/cards/" + card + ".png"
    card_image.alt = "Altier text"
    doc.getElementById("player-cards").append(card_image)
    player_total += get_value(card)
    player_aces += check_for_ace(card)


window.onload = build_deck(), shuffle_deck(), initialize_game()

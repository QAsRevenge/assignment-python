import random as rand
from network_brython import connect, send
from browser import aio, window, alert
doc = window.document

dealer_total = 0
player_total = 0
player_totals = 0
dealer_aces = 0
player_aces = 0
player_ace = 0
player2_total = 0
player2_aces = 0
dealer_hand = []
player_hand = []
player2_hand = []
dealer_hidden = []
deck = []
to_hit = bool
card_value = []
game_message = ""


game_state = {
    'me': None,
    'opponent': None,
    'is_server': None,     
}


def get_opponent_and_decide_game_runner(user, message):
    # who is the server (= the creator of the channel)
    if 'created the channel' in message:
        name = message.split("'")[1]
        game_state['is_server'] = name == game_state['me']
    # who is the opponent (= the one that joined that is not me)
    if 'joined channel' in message:
        name = message.split(' ')[1]
        if name != game_state['me']:
            game_state['opponent'] = name


def on_network_message(timestamp, user, message):
    if user == 'system':
        get_opponent_and_decide_game_runner(user, message)
    # key_downs (only of interest to the server)
    global player_total, player2_total, dealer_hidden, dealer_total
    if game_state['is_server']:
        if user == game_state['me'] and type(message) is list:
            player_total= set(message)
        if user == game_state['opponent'] and type(message) is list:
            player2_total = set(message)
    # shared state (only of interest to the none-server)
    if type(message) is dict and not game_state['is_server']:
        game_state['shared'] = message
    






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
    global dealer_hidden
    data = card.split("-")
    card_value = data[0]

    if card_value == "A":
        return int(11)
    elif card_value == "J":
        return int(10)
    elif card_value == "Q":
        return int(10)
    elif card_value == "K":
        return int(10)
    else:
        return int(card_value, 0)


def check_for_ace(card):
    if card[0] == "A":
        return 1
    else:
        return 0


def adjust_for_ace(player_totals, player_ace):
    while player_totals > 21 & player_ace > 0:
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
    global player_totals
    global player_ace
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
    elif player_total == 21:
        game_message = 'You win'
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
    

def restart_game(event):
    global player_hand
    global dealer_hand
    global player2_hand
    player_hand = []
    dealer_hand = []
    player2_hand = []
    element = doc.getElementById("hidden-card")
    element.remove()
    elemen = doc.getElementById("card-id")
    elemen.remove()
    eleme = doc.getElementById("player1-cards")
    eleme.remove()
    elem = doc.getElementById("player-2-cards")
    elem.remove()
    ele = doc.getElementById("player1-cards2")
    eleme.remove()
    el = doc.getElementById("player-2-cards2")
    el.remove()

    initialize_game()


def deal_hidden():
    global dealer_hidden
    global dealer_hand
    dealer_hidden = deck.pop()
    hidden_card_image = doc.createElement("img")
    hidden_card_image.id = "hidden-card"
    hidden_card_image.src = "/cards/back_of_card.png"
    hidden_card_image.alt = "Alt text"
    doc.getElementById("dealer-cards").append(hidden_card_image)
    dealer_hand.append(dealer_hidden)


def deal_player1():
    global player_total
    global player_aces
    global player_hand
    card_image = doc.createElement("img")
    card = deck.pop()
    card_image.src = "/cards/" + card + ".png"
    card_image.alt = "Altier text"
    card_image.id = 'player1-cards'
    doc.getElementById("player-cards").append(card_image)
    player_total += get_value(card)
    player_aces += check_for_ace(card)
    doc.getElementById("player1").innerText = (f"Player 1: {player_total}")
    player_hand.append(card)
    print(f"player hand: {player_hand}")

    card_image = doc.createElement("img")
    card = deck.pop()
    card_image.src = "/cards/" + card + ".png"
    card_image.alt = "Altier text"
    card_image.id = 'player1-cards2'
    doc.getElementById("player-cards").append(card_image)
    player_total += get_value(card)
    player_aces += check_for_ace(card)
    doc.getElementById("player1").innerText = (f"Player 1: {player_total}")
    player_hand.append(card)
    print(f"player hand: {player_hand}")

def deal_player2():
    global player2_aces
    global player2_total
    global player2_hand
    card_image = doc.createElement("img")
    card = deck.pop()
    card_image.src = "/cards/" + card + ".png"
    card_image.alt = "Altest text"
    card_image.id = "player-2-cards"
    player2_aces += check_for_ace(card)
    player2_total += get_value(card)
    doc.getElementById("player2-cards").append(card_image)
    doc.getElementById("player2").innerText = (
        f"Player 2: {player2_total}")
    player2_hand.append(card)
    print(f"player2 hand: {player2_hand}")

    card_image = doc.createElement("img")
    card = deck.pop()
    card_image.src = "/cards/" + card + ".png"
    card_image.alt = "Altest text"
    card_image.id = "player-2-cards2"
    player2_aces += check_for_ace(card)
    player2_total += get_value(card)
    doc.getElementById("player2-cards").append(card_image)
    doc.getElementById("player2").innerText = (f"Player 2: {player2_total}")
    player2_hand.append(card)
    print(f"player2 hand: {player2_hand}")

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
    global player_hand
    global player2_hand
    alert("Welcome to blackjack!\nDealer hits on all 17s\nPush = Tie\nCan't get ace adjustment to work... :(")
    deal_hidden()
    print(dealer_hidden)
    dealer_total += get_value(dealer_hidden)
    dealer_aces += check_for_ace(dealer_hidden)
    card = deck.pop()
    card_image = doc.createElement("img")
    card_image.src = "/cards/" + card + ".png"
    card_image.alt = "Alt text"
    card_image.id = "card-id"
    doc.getElementById("dealer-cards").append(card_image)
    dealer_total += get_value(card)
    dealer_aces += check_for_ace(card)
    doc.getElementById("dealer").innerText = ("Dealer: ?")
    dealer_hand.append(card)
    print(f"dealer hand: {dealer_hand}")
    deal_player1()
    deal_player2()
    doc.getElementById("hit-button").addEventListener("click", hit)
    doc.getElementById("stay-button").addEventListener("click", stay)
    doc.getElementById("deal-button").addEventListener("click", restart_game)


window.onload = build_deck(), shuffle_deck(), initialize_game()

import random
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

def initialize_game():
    global human_cards, human_cards_visible, computer_cards, draw_pile, current_turn, last_round, events, last_discarded_card

    # Card deck initialization
    weights = [1, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    cards = random.choices(range(10), weights=weights, k=100)


    # Card allocation to players
    human_cards = cards[:4]
    computer_cards = cards[4:8]
    draw_pile = cards[8:]
    last_round = False
    current_turn = 'human'
    human_cards_visible = [str(human_cards[0]), "X", "X", str(human_cards[3])]
    last_discarded_card = draw_pile.pop()
    events = []

    # Log starting cards
    events.append("The game begins!")
    events.append(f'Human Cards: {human_cards}')
    events.append(f'Computer Cards: {computer_cards}')
    events.append(f'Discard Card: {last_discarded_card}')

# Call initialize_game() to set up the initial game state
initialize_game()

def computer_turn():
    global computer_cards, draw_pile, current_turn

    # computer finds its worst card
    max_card_index = computer_cards.index(max(computer_cards))

    # computer draws a card, always chooses to replace
    # TODO: Make this depend on if computer knows the value of the card
    last_discarded_card = computer_cards[max_card_index]
    computer_cards[max_card_index] = draw_pile.pop()
    current_turn = 'human'

def game():
    global human_cards, human_cards_visible, computer_cards, draw_pile, last_round, current_turn, events

    if current_turn == 'human':
        return render_template('index.html', human_cards=human_cards, human_cards_visible=human_cards_visible, computer_cards=computer_cards, events=events)

    elif current_turn == 'computer':
        computer_turn()
        events.append('Computer drew a card and replaced one of its cards')
        events.append(f'Human Cards: {human_cards}')
        events.append(f'Computer Cards: {computer_cards}')
        events.append(f'Discard Card:{last_discarded_card}')
        return render_template('index.html', human_cards=human_cards, human_cards_visible=human_cards_visible, computer_cards=computer_cards, events=events)

@app.route('/')
def index():
    return game()


@app.route('/replace_card', methods=['GET', 'POST'])
def replace_card():
    global human_cards, human_cards_visible, current_turn, draw_pile

    # draw a new card from the deck
    new_card = draw_pile.pop()

    # render the replace card template with the new card value
    return render_template('replace_card.html',
                           human_cards=human_cards, human_cards_visible=human_cards_visible, new_card=new_card)

# Note that app.route essentially picks up on a request sent from the html that references
# ('/pick_up_discard_card'. But it doesn't have to then go on and render an html page with the same
# name. Here I'm using it to render the 'replace_card.html' page with a different input to new_card
@app.route('/pick_up_discard_card', methods=['GET', 'POST'])
def pick_up_discard_card():
    global human_cards, human_cards_visible, current_turn, draw_pile, last_discarded_card

    # draw a new card from the deck
    new_card = last_discarded_card

    # render the replace card template with the new card value
    return render_template('replace_card.html',
                           human_cards=human_cards, human_cards_visible=human_cards_visible, new_card=new_card)

@app.route('/replace_card_confirm', methods=['GET','POST'])
def replace_card_confirm():
    global human_cards, human_cards_visible, current_turn, draw_pile, last_discarded_card

    # get the card index from the form data
    card_index = int(request.form['card_index'])

    # get the card index and whether to keep the card from the form data
    card_index = int(request.form['card_index'])
    new_card = request.form['new_card']
    keep_card = request.form.get('keep_card')

    # if the player chooses to keep the card, update their hand and the log
    if keep_card == 'true':
        last_discarded_card = human_cards[card_index]
        human_cards[card_index] = int(new_card)
        human_cards_visible[card_index] = str(new_card)
        events.append(f"Player drew card {int(new_card)} and kept it")
    else:
        last_discarded_card = new_card
        events.append(f"Player drew card {int(new_card)} and did not keep it")
    current_turn = 'computer'

    # render the index template with the updated hands
    return redirect(url_for('index'))

@app.route('/last_round', methods=['POST'])
def last_round():
    computer_turn()
    return render_template('result.html', human_score=sum(human_cards), computer_score=sum(computer_cards))

if __name__ == '__main__':
    app.run()


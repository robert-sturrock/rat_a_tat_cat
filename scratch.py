import random
from flask import Flask, request, render_template

app = Flask(__name__)


def initialize_game():
    global human_cards, computer_cards, draw_pile, cards

    # Card deck initialization
    weights = [9, 8, 7, 6, 5, 4, 3, 2, 1, 1]
    cards = random.choices(range(10), weights=weights, k=100)

    # Card allocation to players
    human_cards = cards[:4]
    computer_cards = cards[4:8]
    draw_pile = cards[8:]

def human_turn():
    global human_cards, draw_pile
    card_index = int(request.form['card_index'])
    human_cards[card_index] = draw_pile.pop()

def computer_turn():
    global computer_cards, draw_pile
    max_card_index = computer_cards.index(max(computer_cards))
    computer_cards[max_card_index] = draw_pile.pop()

def game():
    global human_cards, computer_cards, draw_pile, discard_pile, last_round, human_turn
    initialize_game()
    human_turn = True
    while not last_round:
        if human_turn:
            human_turn()
        else:
            computer_turn()
        if len(draw_pile) == 0:
            last_round = True
        human_turn = not human_turn
    last_round()

@app.route('/')
def index():
    game()
    return render_template('index.html', human_cards=human_cards, computer_cards=computer_cards)

@app.route('/replace_card', methods=['POST'])
def replace_card():
    global human_cards, cards

    # get the card index from the form data
    card_index = int(request.form['card_index'])

    # draw a new card from the deck
    new_card = cards.pop()

    # render the replace card template with the new card value
    return render_template('replace_card.html',
                           new_card=new_card, old_card=human_cards[card_index],
                           card_index=card_index,
                           human_cards=human_cards)

@app.route('/replace_card_confirm', methods=['POST'])
def replace_card_confirm():
    global human_cards, human_turn

    # get the card index and whether to keep the card from the form data
    card_index = int(request.form['card_index'])
    keep_card = request.form.get('keep_card')

    # if the player chooses to keep the card, update their hand
    if keep_card == 'true':
        human_cards[card_index] = int(request.form['new_card'])

    # end the human turn
    human_turn = False

    # render the index template with the updated hands
    return render_template('index.html', human_cards=human_cards, computer_cards=computer_cards)


@app.route('/last_round', methods=['POST'])
def last_round():
    computer_turn()
    return render_template('result.html', human_score=sum(human_cards), computer_score=sum(computer_cards))

if __name__ == '__main__':
    app.run()

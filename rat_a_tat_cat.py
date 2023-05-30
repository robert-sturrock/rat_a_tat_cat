import random
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

def initialize_game():
    global human_cards, human_cards_visible, computer_cards, draw_pile, current_turn, last_round, events, human_log, last_discarded_card

    # Card deck initialization
    # There should be four cards for 0-8, and nine 9s (matching the original game) 
    cards = list(range(9)) * 4 + [9] * 9
    random.shuffle(cards)

    # Card allocation to players
    human_cards = cards[:4]
    computer_cards = cards[4:8]
    draw_pile = cards[8:]
    last_round = False
    current_turn = 'human'
    human_cards_visible = [str(human_cards[0]), "X", "X", str(human_cards[3])]
    last_discarded_card = draw_pile.pop()

    # Log starting cards
    events = []
    events.append("The game begins!")
    events.append(f'Human Cards: {human_cards}')
    events.append(f'Computer Cards: {computer_cards}')
    events.append(f'Discard Card: {last_discarded_card}')

    # Log human visible (in game log)
    human_log = []
    human_log.insert(0, "The game begins!")

# Call initialize_game() to set up the initial game state
initialize_game()

def computer_turn():
    global computer_cards, draw_pile, current_turn, last_discarded_card

    # Initially, the computer only knows about the outer cards (0 and 3)
    known_card_indices = [0, 3]
    
    # Check if the discarded card is worth picking up
    known_cards_values = [computer_cards[i] for i in known_card_indices]
    if last_discarded_card < max(known_cards_values):
        # pick up the discarded card and replace the maximum known card
        new_card = last_discarded_card
        last_discarded_card = None
        action = 'picked up the discard'
    else:
        # Draw a new card
        new_card = draw_pile.pop()
        action = 'drew a card'
    
    # Decide whether to replace a known card
    max_known_card_value = max(known_cards_values)
    if new_card < max_known_card_value:
        max_card_index = known_card_indices[known_cards_values.index(max_known_card_value)]
        discarded_card = computer_cards[max_card_index]
        computer_cards[max_card_index] = new_card
        human_log.insert(0, f"Computer {action} and then replaced card {max_card_index + 1}, it was a {discarded_card}.")
    else:
        # Decide whether to replace an unknown card
        unknown_card_indices = [i for i in range(4) if i not in known_card_indices]
        if unknown_card_indices:  # check if there are still unknown cards
            replace_probabilities = [1.0, 0.95, 0.9, 0.85, 0.8, 0.75, 0.7, 0.65, 0.6, 0.55]  # can be tweaked
            if random.random() < replace_probabilities[new_card]:
                unknown_card_index = random.choice(unknown_card_indices)
                discarded_card = computer_cards[unknown_card_index]
                computer_cards[unknown_card_index] = new_card
                known_card_indices.append(unknown_card_index)  # the unknown card now becomes known
                human_log.insert(0, f"Computer {action} and then replaced card {unknown_card_index + 1}, it was a {last_discarded_card}.")
            else:
                discarded_card = new_card  # decide not to replace any card
                human_log.insert(0, f"Computer {action} and then discarded it, it was a {discarded_card}.")
        else:
            discarded_card = new_card  # all cards are known

    last_discarded_card = discarded_card
    current_turn = 'human'
    return computer_cards


def game():
    global human_cards, human_cards_visible, computer_cards, draw_pile, last_round, current_turn, events, last_discarded_card

    if current_turn == 'human':
        events.append('Human turn')
        return render_template('index.html', human_cards=human_cards, human_cards_visible=human_cards_visible,
                                computer_cards=computer_cards, events=events, last_discarded_card=str(last_discarded_card))

    elif current_turn == 'computer':
        computer_turn()
        events.append('Computer turn')
        events.append(human_log[0])
        events.append('Current game state:')
        events.append(f'Human Cards: {human_cards}')
        events.append(f'Computer Cards: {computer_cards}')
        events.append(f'Discard Card: {last_discarded_card}')
        return render_template('index.html', human_cards=human_cards, human_cards_visible=human_cards_visible, 
                               computer_cards=computer_cards, events=events, last_discarded_card=str(last_discarded_card),
                               human_log=human_log)

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
                           human_cards=human_cards, human_cards_visible=human_cards_visible, 
                           new_card=new_card, new_card_str = str(new_card))

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
                           human_cards=human_cards, human_cards_visible=human_cards_visible, new_card=new_card,
                           new_card_str = str(new_card))

@app.route('/replace_card_confirm', methods=['GET','POST'])
def replace_card_confirm():
    global human_cards, human_cards_visible, current_turn, draw_pile, last_discarded_card

    # get the new card value from the form data
    new_card = request.form['new_card']

    # check if the Discard New Card button was pressed
    if 'discard_new_card' in request.form:
        # update the last discarded card and the log
        last_discarded_card = int(new_card)
        events.append(f"Player drew card {int(new_card)} and discarded it")

    else:
        # get the card index from the form data
        card_index = int(request.form['card_index'])

        # update the player's hand and the log
        last_discarded_card = human_cards[card_index]
        human_cards[card_index] = int(new_card)
        human_cards_visible[card_index] = str(new_card)
        events.append(f"Player drew a {int(new_card)} and replaced card {card_index+1}")
    
    events.append(f"Discard card: {last_discarded_card}")

    # set to computer turn
    current_turn = 'computer'

    # render the index template with the updated hands
    return redirect(url_for('index'))


@app.route('/last_round', methods=['POST'])
def last_round():
    global events
    events.append('Human player declares last round! Computer takes one more turn')
    computer_cards = computer_turn() # store returned computer_cards after last turn
    computer_score = sum(computer_cards) # calculate score after last turn
    events.append(human_log[0]) # add computers last turn
    return render_template('result.html', human_score=sum(human_cards), computer_score=computer_score, events=events, 
                           human_cards_str=[str(card) for card in human_cards], computer_cards_str=[str(card) for card in computer_cards])
if __name__ == '__main__':
    app.run(debug=True)


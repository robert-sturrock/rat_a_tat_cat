
# Rat-A-Tat-Cat HTML Game

This project is an implementation of the popular children's card game, Rat-a-Tat-Cat, using HTML and Flask. This game was built with help from OpenAI's ChatGPT and leverages images generated from an AI image generator.

## Installation

### Prerequisites

To play this game locally, you'll need to have Python installed on your machine. You will also need Flask. If you don't have Flask installed, you can do so with pip:

```bash
pip install flask
```

### Installing the Game

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/your_username/rat-a-tat-cat-game.git
   ```
2. Navigate to the project directory:
   ```bash
   cd rat-a-tat-cat-game
   ```
3. Run the Flask application:
   ```bash
   python rat_a_tat_cat.py
   ```
4. Open your web browser and go to `http://localhost:5000`.

## Rules of the Game

Rat-a-Tat-Cat is a game of suspense, strategy, and anticipation. The game's objective is to have the lowest score at the end of the game. 

Here are the simplified rules for our implementation:

1. Each player (in this case, you and the computer) is dealt four cards, with the outer cards privately visible to each player.
2. Each turn, you draw a new card (or pick up from the discard pile). You then decide whether to replace one of your cards with the new card or discard it.
3. Watch out! If you replace a hidden card you may accidentally discard a valueable low points card that your opponent can pick up.
4. The game ends when the human player declares "Last Round" after that the computer player can take one more turn. At that point, the player with the lowest total score wins.

## How to Play

After launching the game in your terminal and clicking on the link (it will say something like "Running on http://127.0.0.1:5000"), you'll see your hand and the computer's hand. Your known card and the newly drawn card will be clearly displayed.

To replace a card in your hand, simply click the "Replace Card" button below the card you wish to replace. If you want to discard the drawn card, click the "Discard New Card" button.

When you replace a hidden card, a message will pop up telling you the value of the replaced card. This helps you keep track of what is happening and the consequences of your actions! 

There is also a log displayed on the main screen that tells you what what the computer has done on every turn.

 

## Built With

- [Flask](https://flask.palletsprojects.com/) - Python micro web framework used.
- [HTML/CSS](https://www.w3schools.com/html/html_css.asp) - Used for structuring and styling the web game.
- [OpenAI's ChatGPT](https://www.openai.com/research/chatgpt) - Provided AI assistance during development.

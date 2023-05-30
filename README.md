
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
   python main.py
   ```
4. Open your web browser and go to `http://localhost:5000`.

## Rules of the Game

Rat-a-Tat-Cat is a game of suspense, strategy, and anticipation. The game's objective is to have the lowest score at the end of the game. 

Here are the simplified rules for our implementation:

1. Each player (in this case, you and the computer) is dealt four cards, with one card visible to both players and the rest hidden.
2. Each turn, you draw a new card. You then decide whether to replace one of your cards with the new card or discard it.
3. If you replace one of your visible cards, both you and the computer will know its value. If you replace a hidden card, its value will be a surprise at the end of the game.
4. The game ends after a certain number of rounds. At that point, the player with the lowest total score wins.

## How to Play

After launching the game in your browser, you'll see your hand and the computer's hand. Your visible card and the newly drawn card will be clearly displayed.

To replace a card in your hand, simply click the "Replace Card" button below the card you wish to replace. If you want to discard the drawn card, click the "Discard New Card" button.

When you replace a hidden card, a message will pop up telling you the value of the replaced card. This helps you keep track of your score but adds a layer of suspense—what if you replaced a low-value card with a high one?

## Built With

- [Flask](https://flask.palletsprojects.com/) - Python micro web framework used.
- [HTML/CSS](https://www.w3schools.com/html/html_css.asp) - Used for structuring and styling the web game.
- [OpenAI's ChatGPT](https://www.openai.com/research/chatgpt) - Provided AI assistance during development.
- [AI Image Generator](https://your-ai-image-generator-url.com) - Provided card images for the game.

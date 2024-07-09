from flask import Flask, render_template, session, redirect, request, jsonify
from boggle import Boggle

boggle_game = Boggle()

app = Flask(__name__)
app.config['SECRET_KEY'] = "my-key"

@app.route('/')
def index():
    """Renders the game board"""

    board = boggle_game.make_board()
    session['board'] = board
    return render_template('index.html', board=board)

@app.route('/check-word', methods=['POST'])
def check_word():
    """Checks if word is valid and on board"""

    word = request.form['word']
    board = session.get('board')
    result = boggle_game.check_valid_word(board, word)
    return jsonify({'result': result})

@app.route('/end-game', methods=['POST'])
def end_game():
    """Ends the game"""

    score = request.json['score']
    session['times_played'] = session.get('times_played', 0) + 1
    session['high_score'] = max(session.get('high_score', 0), score)
    return jsonify({
        'times_played': session['times_played'],
        'high_score': session['high_score']
    })
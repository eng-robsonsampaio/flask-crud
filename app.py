from datetime import timedelta
from re import template
from flask import Flask, Response, render_template, request, url_for, flash, redirect
import os

key = os.urandom(24).hex()
app = Flask(__name__)
app.config['SECRET_KEY'] = key
            

class Game:
    def __init__(self, name: str, category: str, console: str) -> None:
        self.name = name
        self.category = category
        self.console = console

game1 = Game(name='Super Mario', category='Action', console='SNES')
game2 = Game(name='Metal Gear', category='Action', console='PSE')

games = []
games.append(game1)
games.append(game2)

@app.route('/init')
def greeting():
    return render_template('list_of_games.html', title='Game', games=games)

@app.route('/register')
def register():
    return render_template('register.html', title='New Game')

@app.route('/create', methods=['GET', 'POST'])
def create():
    new_game = Game(name=request.form['name'], 
                    category=request.form['category'],
                    console=request.form['console'])
    games.append(new_game)

    return redirect(url_for('greeting'))

app.run()
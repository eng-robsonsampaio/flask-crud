from datetime import timedelta
from re import template
from flask import Flask, Response, render_template, request, url_for, session, redirect, flash
import os

from flask.typing import TemplateFilterCallable

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

@app.route('/')
def index():
    return render_template('list_of_games.html', title='Game', games=games)

@app.route('/register')
def register():
    if('user_logged' not in session or session['user_logged'] == None):
        return redirect('/login')
    return render_template('register.html', title='New Game')

@app.route('/create', methods=['GET', 'POST'])
def create():
    new_game = Game(name=request.form['name'], 
                    category=request.form['category'],
                    console=request.form['console'])
    games.append(new_game)

    return redirect(url_for('index'))

@app.route('/auth', methods=['POST'])
def authentication(): 
    if ('admin' == request.form['password'] and 'user' == request.form['user']):
        flash(request.form['user'] + ' success')
        session['user_logged'] = request.form['user']
        print('Correct')
        return redirect('/')
    else:
        flash('Wrong user or password')
        return redirect('/login')

@app.route('/login')
def login():
    return render_template('login.html', title='Login')

@app.route('/logout')
def logout():
    session['user_logged'] = None
    flash('None user logged!')
    return redirect('/')

app.run(debug=True)
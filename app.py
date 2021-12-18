from datetime import timedelta
from re import template
from flask import Flask, Response, render_template, request, url_for, session, redirect, flash
import os


key = os.urandom(24).hex()
app = Flask(__name__)
app.config['SECRET_KEY'] = key
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://test:@localhost/jogoteca'


class Game:
    def __init__(self, name: str, category: str, console: str) -> None:
        self.name = name
        self.category = category
        self.console = console

class User:
    def __init__(self, id, name, psk) -> None:
        self.id = id
        self.name = name
        self.psk = psk

user1 = User('Robson', 'Robson Sampaio', '9874')
user2 = User('Gabi', 'Gabi Sampaio', '1234')
user3 = User('Admin', 'admin', 'admin')
users = {user1.id: user1, 
         user2.id: user2, 
         user3.id: user3}

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
        return redirect('/login?next=register')
    return render_template('register.html', title='New Game')

@app.route('/create', methods=['GET', 'POST'])
def create():
    new_game = Game(name=request.form['name'], 
                    category=request.form['category'],
                    console=request.form['console'])
    games.append(new_game)

    return redirect(url_for('index'))

@app.route('/auth', methods=['POST',])
def auth():
    if request.method == 'POST':
        print(f'{request.form["user"] in users} and {request.form["password"]}')
        if request.form['user'] in users:
            user = users[request.form['user']]
            print(f'{user.psk} and {request.form["password"]}')
            if user.psk == str(request.form['password']):
                session['user_logged'] = user.id
                flash(user.name + ' success')

                next_page = request.form['next']
                return redirect('/{}'.format(next_page))
            else:
                flash('Wrong password')
                return redirect('/login')
        else: 
            flash('User doesn\'t exist')
            return redirect('/login')


@app.route('/login')
def login():
    next_page = request.args.get('next')
    print(f'Next: {next}')
    return render_template('login.html', next=next_page)
    

@app.route('/logout')
def logout():
    session['user_logged'] = None
    flash('None user logged!')
    return redirect('/')

app.run(debug=True)
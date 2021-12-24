
from flask.helpers import url_for
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, Response
import os, json

from werkzeug.utils import redirect


key = os.urandom(24).hex()
app = Flask(__name__)
app.config['SECRET_KEY'] = key
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://test:1234@localhost/jogoteca'


db = SQLAlchemy(app)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    category = db.Column(db.String(20))
    console = db.Column(db.String(20))

    def to_json(self):
        return {'id': self.id, 'name': self.name, 'category':self.category, 'console':self.console}


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    password = db.Column(db.String(20))

    def to_json(self):
        return {'id': self.id, 'name': self.name, 'password':self.password}


@app.route('/')
def index():
    games = Game.query.all()
    return render_template('list_of_games.html', title='Games', games=games)

@app.route('/register_new_game')
def register_new_game():
    return render_template('register.html', title='New Game')

@app.route('/users', methods=['GET'])
def users():
    users = User.query.all()
    users = [user.to_json() for user in users]
    return my_response(200, 'users', users, 'ok')


@app.route('/add_user', methods=['POST'])
def add_user():
    body = request.get_json()

    try:
        user = User(name=body['name'], password=body['password'])
        db.session.add(user)
        db.session.commit()
        return my_response(200, 'user', user.to_json(), 'Salved')

    except Exception as e:
        print(e)
        print('Could\'nt create user')


@app.route('/games', methods=['GET'])
def games():
    games = Game.query.all()
    games = [game.to_json() for game in games]
    return my_response(200, 'games', games, 'ok')


@app.route('/add_game', methods=['GET', 'POST'],)
def add_game():
    # body = request.get_json()
    name = request.args.get('name')
    category = request.args.get('category')
    console = request.args.get('console')

    try:
        game = Game(name=name, category=category, console=console)
        db.session.add(game)
        db.session.commit()
        return redirect(url_for('index'))

    except Exception as e:
        print(e)
        print('Could\'nt create game')


def my_response(status, content_name, content_value, msg=False):
    body = {}
    body[content_name] = content_value

    if (msg):
        body['mensage'] = msg

    return Response(json.dumps(body), status=status, mimetype="application/json")

# @app.route('/')
# def index():
#     return render_template('list_of_games.html', title='Game', games=games)

# @app.route('/register')
# def register():
#     if('user_logged' not in session or session['user_logged'] == None):
#         return redirect('/login?next=register')
#     return render_template('register.html', title='New Game')

# @app.route('/create', methods=['GET', 'POST'])
# def create():
#     new_game = Game(name=request.form['name'], 
#                     category=request.form['category'],
#                     console=request.form['console'])
#     games.append(new_game)

#     return redirect(url_for('index'))

# @app.route('/auth', methods=['POST',])
# def auth():
#     if request.method == 'POST':
#         print(f'{request.form["user"] in users} and {request.form["password"]}')
#         if request.form['user'] in users:
#             user = users[request.form['user']]
#             print(f'{user.psk} and {request.form["password"]}')
#             if user.psk == str(request.form['password']):
#                 session['user_logged'] = user.id
#                 flash(user.name + ' success')

#                 next_page = request.form['next']
#                 return redirect('/{}'.format(next_page))
#             else:
#                 flash('Wrong password')
#                 return redirect('/login')
#         else: 
#             flash('User doesn\'t exist')
#             return redirect('/login')


# @app.route('/login')
# def login():
#     next_page = request.args.get('next')
#     print(f'Next: {next}')
#     return render_template('login.html', next=next_page)
    

# @app.route('/logout')
# def logout():
#     session['user_logged'] = None
#     flash('None user logged!')
#     return redirect('/')


app.run(debug=True)
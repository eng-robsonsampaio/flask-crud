from flask import Flask, Response, request
import os
from flask_sqlalchemy import SQLAlchemy
import json

key = os.urandom(24).hex()
app = Flask(__name__)
app.config['SECRET_KEY'] = key
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://test:1234@127.0.0.1/test'

db = SQLAlchemy(app)
            
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))

    def to_json(self):
        return {"id":self.id, "name":self.name, "email":self.email}


# retrieve all
@app.route('/', methods=['GET'])
def retrieve_all():
    users = User.query.all()
    users = [user.to_json() for user in users]
    print(users)
    return my_response(200, "users", users, "Ok")


# retrieve one users
@app.route('/user/<id>', methods=['GET'])
def retrieve_user(id):
    user = User.query.get(id)
    user = user.to_json()
    return my_response(200, 'user', user, 'ok')


# add user
@app.route('/user', methods=['POST'])
def insert_user():
    body = request.get_json()

    try:
        user = User(name=body['name'], email=body['email'])
        db.session.add(user)
        db.session.commit()
        return my_response(200, 'user', user.to_json(), 'User created')
    except Exception as e:
        print(e)
        return my_response(400, 'user', {}, 'Erro inserting user')


def my_response(status, content_name, content_value, msg=False):
    body = {}
    body[content_name] = content_value

    if (msg):
        body['mensage'] = msg

    return Response(json.dumps(body), status=status, mimetype="application/json")


# update user info
@app.route('/user/<id>', methods=['PUT'])
def update(id):
    user = User.query.get(id)
    body = request.get_json()
    try:
        if ('name' in body):
            user.name = body['name']
        if ('email' in body):
            user.email = body['email']
        
        db.session.add(user)
        db.session.commit()

        return my_response(200, 'user', {user.to_json()}, 'ok')

    except Exception as e:
        print(e)
        print('Não foi possível atualizar o usuário')

    user = user.to_json()


# delete user by id
@app.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    try:
        db.session.delete(user)
        db.session.commit()

        return my_response(200, 'user', user.to_json(), 'deleted')
    except Exception as e:
        print(e)
        print('Not able to delete user')
        return my_response(400, 'user', {}, 'fail')


def test_query(id=2):
    users = User.query.get(id)
    # users = [user.to_json() for user in users]
    print(users.to_json())

app.run(debug=True)

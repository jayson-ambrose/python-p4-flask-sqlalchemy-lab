#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):

    animal = Animal.query.filter(Animal.id == id).first()

    response_body = f"<ul>ID: {animal.id}</ul>"\
    + f"<ul>Name: {animal.name}</ul>"\
    + f"<ul>Species: {animal.species}</ul>"\
    + f"<ul>Zookeeper: {animal.zookeeper.name}</ul>"\
    + f"<ul>Enclosure: {animal.enclosure.environment}</ul>"
    
    response = make_response(response_body)
    
    return response


@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper = Zookeeper.query.filter(Zookeeper.id == id).first()

    response_body = f'<ul>ID: {zookeeper.id}</ul>'\
    + f"<ul>Name: {zookeeper.name}</ul>"\
    + f"<ul>Birthday: {zookeeper.birthday}</ul>"\
    
    animals = [animal for animal in zookeeper.animals]
    
    for animal in animals:
        response_body = response_body + f"<ul>Animal: {animal.name}</ul>"

    response = make_response(response_body)    
    return response

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    enclosure = Enclosure.query.filter(Enclosure.id == id).first()

    response_body = f'<ul>ID: {enclosure.id}</ul>'\
    + f"<ul>Environment: {enclosure.environment}</ul>"\
    + f"<ul>Open to Visitors: {enclosure.open_to_visitors}</ul>"\
    
    animals = [animal for animal in enclosure.animals]
    for animal in animals:
        response_body = response_body + f"<ul>Animal: {animal.name}</ul>"
    
    response = make_response(response_body)

    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)

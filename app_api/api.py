from flask import Blueprint, request, jsonify, abort, url_for
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
from .modelsSQL import Pelicula, Reparto, Actor, Director, Genero, db

parent_app = None
api = Blueprint('api', __name__)
CORS(api)

# INSERTS CON PUT
# UPDATES con POST
# DELETES con DELETE
# SELECT con GET

def jsonifyData(data): 
    serialData=[e.serialize() for e in data]
    return jsonify(serialData)

@api.route('/actores')
def getActores():
    data = Actor.query.all()
    return jsonifyData(data)

@api.route('/actor/<key>')
def getActorByKey(key):
    data = Actor.query.filter_by(id=key)
    return jsonifyData(data)

@api.route('/actor/<key>', methods = ['PUT'])
def insertActorByKey(key):
    # Ejemplo de insert con llave, no tan util para insert como para update
    try:
        actor = Actor(id=key, nombre=request.json.get('nombre', None), pais=request.json.get('pais', None), nacimiento=request.json.get('nacimiento', None))
        db.session.add(actor)
    except IntegrityError:
        return 'integrity error', 400
    db.session.commit()
    return 'ok'

@api.route('/actor', methods = ['PUT'])
def insertActor():
    # Sin llave, se define con el auto-increment
    try:
        actor = Actor(nombre=request.json.get('nombre', None), pais=request.json.get('pais', None), nacimiento=request.json.get('nacimiento', None))
        db.session.add(actor)
    except IntegrityError:
        return 'integrity error', 400
    db.session.commit()
    return 'ok'

@api.route('/directores')
def getDirectores():
    data = Director.query.all()
    return jsonifyData(data)

@api.route('/generos')
def getGeneros():
    data = Genero.query.all()
    return jsonifyData(data)

@api.route('/peliculas')
def getPeliculas():
    data = Pelicula.query.all()
    return jsonifyData(data)

@api.route('/repartos')
def getRepartos():
    data = Reparto.query.all()
    return jsonifyData(data)


def init_app(app, url_prefix='/api/v1'):
    global parent_app
    parent_app = app
    app.register_blueprint(api, url_prefix=url_prefix)
from flask import Blueprint, request, jsonify, abort, url_for
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
from .modelsMSSQL import MSPelicula, MSReparto, MSActor, MSDirector, MSGenero, db as msDb
from .modelsMySQL import MyPelicula, MyReparto, MyActor, MyDirector, MyGenero, db as myDb

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
    data = MSActor.query.all()
    return jsonifyData(data)

@api.route('/actor/<key>')
def getActorByKey(key):
    data = MSActor.query.filter_by(id=key)
    return jsonifyData(data)

@api.route('/actor', methods = ['PUT'])
def insertActorByKey():
    try:
        msActor = MSActor(id=request.json.get('id', None), nombre=request.json.get('nombre', None), pais=request.json.get('pais', None), nacimiento=request.json.get('nacimiento', None))
        myActor = MyActor(id=request.json.get('id', None), nombre=request.json.get('nombre', None), pais=request.json.get('pais', None), nacimiento=request.json.get('nacimiento', None))
        msDb.session.add(msActor)
        myDb.session.add(myActor)
        # TODO: Error 400 si id se especifica y ya existe 
    except IntegrityError:
        return 'integrity error', 400
    msDb.session.commit()
    myDb.session.commit()
    return 'ok'

@api.route('/directores')
def getDirectores():
    data = MSDirector.query.all()
    return jsonifyData(data)

@api.route('/generos')
def getGeneros():
    data = MSGenero.query.all()
    return jsonifyData(data)

@api.route('/peliculas')
def getPeliculas():
    data = MSPelicula.query.all()
    return jsonifyData(data)

@api.route('/repartos')
def getRepartos():
    data = MSReparto.query.all()
    return jsonifyData(data)


def init_app(app, url_prefix='/api/v1'):
    global parent_app
    parent_app = app
    app.register_blueprint(api, url_prefix=url_prefix)
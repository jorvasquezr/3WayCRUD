from flask import Blueprint, request, jsonify, abort, url_for
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
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

# =====================
#        Actor
# =====================

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

@api.route('/actor/<key>', methods = ['DELETE'])
def deleteActorByKey(key):
    try:
        msActor = MSActor.query.filter_by(id=key).one()
        myActor = MyActor.query.filter_by(id=key).one()
        msDb.session.delete(msActor)
        myDb.session.delete(myActor)
    except NoResultFound:
        abort(404)
        return
    except IntegrityError:
        return "integrity error", 400
    msDb.session.commit()
    myDb.session.commit()
    return 'ok'

# =====================
#        Director
# =====================

@api.route('/directores')
def getDirectores():
    data = MSDirector.query.all()
    return jsonifyData(data)

@api.route('/director/<key>', methods = ['DELETE'])
def deleteDirectorByKey(key):
    try:
        msDirector = MSDirector.query.filter_by(id=key).one()
        myDirector = MyDirector.query.filter_by(id=key).one()
        msDb.session.delete(msDirector)
        myDb.session.delete(myDirector)
    except NoResultFound:
        abort(404)
        return
    except IntegrityError:
        return "integrity error", 400
    msDb.session.commit()
    myDb.session.commit()
    return 'ok'


# =====================
#        Genero
# =====================

@api.route('/generos')
def getGeneros():
    data = MSGenero.query.all()
    return jsonifyData(data)

@api.route('/genero/<key>', methods = ['DELETE'])
def deleteGeneroByKey(key):
    try:
        msGenero = MSGenero.query.filter_by(id=key).one()
        myGenero = MyGenero.query.filter_by(id=key).one()
        msDb.session.delete(msGenero)
        myDb.session.delete(myGenero)
    except NoResultFound:
        abort(404)
        return
    except IntegrityError:
        return "integrity error", 400
    msDb.session.commit()
    myDb.session.commit()
    return 'ok'


# =====================
#        Pelicula
# =====================

@api.route('/peliculas')
def getPeliculas():
    data = MSPelicula.query.all()
    return jsonifyData(data)

@api.route('/pelicula/<key>', methods = ['DELETE'])
def deletePeliculaByKey(key):
    try:
        msPelicula = MSPelicula.query.filter_by(id=key).one()
        myPelicula = MyPelicula.query.filter_by(id=key).one()
        msDb.session.delete(msPelicula)
        myDb.session.delete(myPelicula)
    except NoResultFound:
        abort(404)
        return
    except IntegrityError:
        return "integrity error", 400
    msDb.session.commit()
    myDb.session.commit()
    return 'ok'


# =====================
#        Reparto
# =====================

@api.route('/repartos')
def getRepartos():
    data = MSReparto.query.all()
    return jsonifyData(data)

@api.route('/reparto/<keyPelicula>/<keyActor>', methods = ['DELETE'])
def deletePeliculaByKey(keyPelicula, keyActor):
    try:
        msReparto = MSReparto.query.filter_by(idPelicula=keyPelicula, idActor=keyActor).one()
        myReparto = MyReparto.query.filter_by(idPelicula=keyPelicula, idActor=keyActor).one()
        msDb.session.delete(msReparto)
        myDb.session.delete(myReparto)
    except NoResultFound:
        abort(404)
        return
    except IntegrityError:
        return "integrity error", 400
    msDb.session.commit()
    myDb.session.commit()
    return 'ok'


def init_app(app, url_prefix='/api/v1'):
    global parent_app
    parent_app = app
    app.register_blueprint(api, url_prefix=url_prefix)
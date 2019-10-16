from flask import Blueprint, request, jsonify, abort, url_for
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from .modelsMSSQL import MSPelicula, MSReparto, MSActor, MSDirector, MSGenero, db as msDb
from .modelsMySQL import MyPelicula, MyReparto, MyActor, MyDirector, MyGenero, db as myDb
from .mongo import mongo

parent_app = None
api = Blueprint('api', __name__)
CORS(api)

# INSERTS CON POST
# UPDATES con POST
# DELETES con DELETE
# SELECT con GET


def jsonifyData(data):
    serialData = [e.serialize() for e in data]
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


@api.route('/actor', methods=['POST'])
def insertActor():
    try:
        msActor = MSActor(id=request.json.get('id', None), nombre=request.json.get(
            'nombre', None), pais=request.json.get('pais', None), nacimiento=request.json.get('nacimiento', None))
        msDb.session.add(msActor)
        # Send changes to DB to determine the id and maybe get integrity errors
        msDb.session.flush()
        myActor = MyActor(id=msActor.id, nombre=request.json.get('nombre', None), pais=request.json.get(
            'pais', None), nacimiento=request.json.get('nacimiento', None))
        myDb.session.add(myActor)
        mongo.db.ACTOR.insert_one({
            "_id": msActor.id,
            "nombre": request.json.get('nombre', None),
            "pais": request.json.get('pais', None),
            "nacimiento": request.json.get('nacimiento', None)
        })
    except IntegrityError:
        return 'integrity error', 400
    msDb.session.commit()
    myDb.session.commit()
    return 'ok'


@api.route('/actor/<key>', methods=['PUT'])
def updateActorByKey(key):
    try:
        msDb.session.query(MSActor).filter(MSActor.id == key).update({
            MSActor.nombre: request.json.get('nombre', MSActor.nombre),
            MSActor.pais: request.json.get('pais', MSActor.pais),
            MSActor.nacimiento: request.json.get('nacimiento', MSActor.nacimiento)
        }, synchronize_session=False)

        myDb.session.query(MyActor).filter(MyActor.id == key).update({
            MyActor.nombre: request.json.get('nombre', MyActor.nombre),
            MyActor.pais: request.json.get('pais', MyActor.pais),
            MyActor.nacimiento: request.json.get('nacimiento', MyActor.nacimiento)
        }, synchronize_session=False)
        mongo.db.ACTOR.update_one({"_id": eval(key)},{"$set":request.json})
        # TODO: Update actor en reparto de pelicula.
    except IntegrityError:
        return 'integrity error', 400
    msDb.session.commit()
    myDb.session.commit()
    return 'ok'


@api.route('/actor/<key>', methods=['DELETE'])
def deleteActorByKey(key):
    try:
        msActor = MSActor.query.filter_by(id=key).one()
        myActor = MyActor.query.filter_by(id=key).one()
        msDb.session.delete(msActor)
        myDb.session.delete(myActor)
        mongo.db.ACTOR.delete_one({"_id": eval(key)})
        # TODO: delete actor en reparto de pelicula, ponerlo null
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


@api.route('/director', methods=['POST'])
def insertDirector():
    try:
        msDirector = MSDirector(id=request.json.get('id', None), nombre=request.json.get(
            'nombre', None), pais=request.json.get('pais', None))
        msDb.session.add(msDirector)
        # Send changes to DB to determine the id and maybe get integrity errors
        msDb.session.flush()
        myDirector = MyDirector(id=msDirector.id, nombre=request.json.get(
            'nombre', None), pais=request.json.get('pais', None))
        myDb.session.add(myDirector)
        mongo.db.DIRECTOR.insert_one({
            "_id": msDirector.id,
            "nombre": request.json.get('nombre', None),
            "pais": request.json.get('pais', None)
        })
    except IntegrityError:
        return 'integrity error', 400
    msDb.session.commit()
    myDb.session.commit()
    return 'ok'

@api.route('/director/<key>', methods=['PUT'])
def updateDirectorByKey(key):
    try:
        msDb.session.query(MSDirector).filter(MSDirector.id == key).update({
            MSDirector.nombre: request.json.get('nombre', MSDirector.nombre),
            MSDirector.pais: request.json.get('pais', MSDirector.pais)
        }, synchronize_session=False)

        myDb.session.query(MyDirector).filter(MyDirector.id == key).update({
            MyDirector.nombre: request.json.get('nombre', MyDirector.nombre),
            MyDirector.pais: request.json.get('pais', MyDirector.pais)
        }, synchronize_session=False)

        mongo.db.DIRECTOR.update_one({"_id": eval(key)},{"$set":request.json})
        # TODO: update director en pelicula

    except IntegrityError:
        return 'integrity error', 400
    msDb.session.commit()
    myDb.session.commit()
    return 'ok'

@api.route('/directores')
def getDirectores():
    data = MSDirector.query.all()
    return jsonifyData(data)


@api.route('/director/<key>', methods=['DELETE'])
def deleteDirectorByKey(key):
    try:
        msDirector = MSDirector.query.filter_by(id=key).one()
        myDirector = MyDirector.query.filter_by(id=key).one()
        msDb.session.delete(msDirector)
        myDb.session.delete(myDirector)
        mongo.db.DIRECTOR.delete_one({"_id": eval(key)})
        # TODO: Poner director null en pelicula cuando se elimina
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

@api.route('/genero', methods=['POST'])
def insertGenero():
    try:
        msGenero = MSGenero(id=request.json.get('id', None),
                            nombre=request.json.get('nombre', None))
        msDb.session.add(msGenero)
        # Send changes to DB to determine the id and maybe get integrity errors
        msDb.session.flush()
        myGenero = MyGenero(id=msGenero.id,
                            nombre=request.json.get('nombre', None))
        myDb.session.add(myGenero)
        mongo.db.GENERO.insert_one({
            "_id": msGenero.id,
            "nombre": request.json.get('nombre', None)
        })
    except IntegrityError:
        return 'integrity error', 400
    msDb.session.commit()
    myDb.session.commit()
    return 'ok'

@api.route('/genero/<key>', methods=['PUT'])
def updateGeneroByKey(key):
    try:
        msDb.session.query(MSGenero).filter(MSGenero.id == key).update({
            MSGenero.nombre: request.json.get('nombre', MSGenero.nombre)
        }, synchronize_session=False)

        myDb.session.query(MyGenero).filter(MyGenero.id == key).update({
            MyGenero.nombre: request.json.get('nombre', MyGenero.nombre)
        }, synchronize_session=False)

        mongo.db.GENERO.update_one({"_id": eval(key)},{"$set":request.json})
        # TODO: Update genero dentro de pelicula

    except IntegrityError:
        return 'integrity error', 400
    msDb.session.commit()
    myDb.session.commit()
    return 'ok'

@api.route('/generos')
def getGeneros():
    data = MSGenero.query.all()
    return jsonifyData(data)


@api.route('/genero/<key>', methods=['DELETE'])
def deleteGeneroByKey(key):
    try:
        msGenero = MSGenero.query.filter_by(id=key).one()
        myGenero = MyGenero.query.filter_by(id=key).one()
        msDb.session.delete(msGenero)
        myDb.session.delete(myGenero)
        mongo.db.GENERO.delete_one({"_id": eval(key)})
        # TODO: set genero en pelicula to null
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

@api.route('/pelicula', methods=['POST'])
def insertPelicula():
    try:
        msPelicula = MSPelicula(id=request.json.get('id', None), nombre=request.json.get('nombre', None), genero=request.json.get(
            'genero', None), director=request.json.get('director', None), ano=request.json.get('ano', None), calificacion=request.json.get('calificacion', None))
        msDb.session.add(msPelicula)
        # Send changes to DB to determine the id and maybe get integrity errors
        msDb.session.flush()
        myPelicula = MyPelicula(id=msPelicula.id, nombre=request.json.get('nombre', None), genero=request.json.get(
            'genero', None), director=request.json.get('director', None), ano=request.json.get('ano', None), calificacion=request.json.get('calificacion', None))
        myDb.session.add(myPelicula)
        mongo.db.PELICULA.insert_one({
            "_id": msPelicula.id,
            "nombre": request.json.get('nombre', None),
            "calificacion": request.json.get('calificacion', None),
            "ano": request.json.get('ano', None),
            "reparto": [],
            "director": mongo.db.DIRECTOR.find({"_id":request.json.get('director', None)}),
            "genero": mongo.db.GENERO.find({"_id":request.json.get('genero', None)})
        })
    except IntegrityError:
        return 'integrity error', 400
    msDb.session.commit()
    myDb.session.commit()
    return 'ok'
@api.route('/pelicula/<key>', methods=['PUT'])
def updatePeliculaByKey(key):
    try:
        msDb.session.query(MSPelicula).filter(MSPelicula.id == key).update({
            MSPelicula.nombre: request.json.get('nombre', MSPelicula.nombre),
            MSPelicula.genero: request.json.get('genero', MSPelicula.genero),
            MSPelicula.director: request.json.get('director', MSPelicula.director),
            MSPelicula.ano: request.json.get('ano', MSPelicula.ano),
            MSPelicula.calificacion: request.json.get('calificacion', MSPelicula.nombre),
        }, synchronize_session=False)
        
        myDb.session.query(MyPelicula).filter(MyPelicula.id == key).update({
            MyPelicula.nombre: request.json.get('nombre', MyPelicula.nombre),
            MyPelicula.genero: request.json.get('genero', MyPelicula.genero),
            MyPelicula.director: request.json.get('director', MyPelicula.director),
            MyPelicula.ano: request.json.get('ano', MyPelicula.ano),
            MyPelicula.calificacion: request.json.get('calificacion', MyPelicula.nombre),
        }, synchronize_session=False)

        mongo.db.PELICULA.update_one({"_id": eval(key)},{"$set":request.json})
        # TODO: ver si cambio director o genero y cambiar eso en la pelicula de mongo, revisar que no se pierda el reparto


    except IntegrityError:
        return 'integrity error', 400
    msDb.session.commit()
    myDb.session.commit()
    return 'ok'



@api.route('/peliculas')
def getPeliculas():
    data = MSPelicula.query.all()
    return jsonifyData(data)


@api.route('/pelicula/<key>', methods=['DELETE'])
def deletePeliculaByKey(key):
    try:
        msPelicula = MSPelicula.query.filter_by(id=key).one()
        myPelicula = MyPelicula.query.filter_by(id=key).one()
        msDb.session.delete(msPelicula)
        myDb.session.delete(myPelicula)
        mongo.db.PELICULA.delete_one({"_id": eval(key)})
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

@api.route('/reparto', methods=['POST'])
def insertReparto():
    try:
        msReparto = MSReparto(idPelicula=request.json.get('idPelicula'), idActor=request.json.get('idActor', None), personaje=request.json.get(
            'personaje', None), calificacion=request.json.get('calificacion', None))
        msDb.session.add(msReparto)
        # Send changes to DB to determine the id and maybe get integrity errors
        msDb.session.flush()
        myReparto = MyReparto(idPelicula=request.json.get('idPelicula'), idActor=request.json.get('idActor', None), personaje=request.json.get(
            'personaje', None), calificacion=request.json.get('calificacion', None))
        myDb.session.add(myReparto)
        mongo.db.PELICULA.update(
            { "_id": request.json.get('idPelicula') },
            { "$push": { "reparto": {"actor": mongo.db.ACTOR.find({"_id": request.json.get('idActor')}),
                                     "personaje":request.json.get('personaje', None),
                                     "calificacion": request.json.get('calificacion', None) }}})
    except IntegrityError:
        return 'integrity error', 400
    msDb.session.commit()
    myDb.session.commit()
    return 'ok'


@api.route('/repartos')
def getRepartos():
    data = MSReparto.query.all()
    return jsonifyData(data)

@api.route('/reparto/<keyPelicula>/<keyActor>', methods=['PUT'])
def updateRepartoByKey(keyPelicula, keyActor):
    try:
        msDb.session.query(MSReparto).filter(MSReparto.idPelicula == keyPelicula,MSReparto.idActor == keyActor, ).update({
            MSReparto.personaje: request.json.get('personaje', MSReparto.personaje),
            MSReparto.calificacion: request.json.get('calificacion', MSReparto.calificacion)
        }, synchronize_session=False)
        
        myDb.session.query(MyReparto).filter(MyReparto.idPelicula == keyPelicula,MyReparto.idActor == keyActor, ).update({
            MyReparto.personaje: request.json.get('personaje', MyReparto.personaje),
            MyReparto.calificacion: request.json.get('calificacion', MyReparto.calificacion)
        }, synchronize_session=False)
        mongo.db.PELICULA.update({ "_id": int(keyPelicula) , "reparto.actor":int(keyActor)},
            { "$set": { "reparto.$.personaje": request.json.get('personaje', None),
                        "reparto.$.calificacion": request.json.get('calificacion', None) }})

    except IntegrityError:
        return 'integrity error', 400
    msDb.session.commit()
    myDb.session.commit()
    return 'ok'

@api.route('/reparto/<keyPelicula>/<keyActor>', methods=['DELETE'])
def deleteRepartoByKey(keyPelicula, keyActor):
    try:
        msReparto = MSReparto.query.filter_by(
            idPelicula=keyPelicula, idActor=keyActor).one()
        myReparto = MyReparto.query.filter_by(
            idPelicula=keyPelicula, idActor=keyActor).one()
        msDb.session.delete(msReparto)
        myDb.session.delete(myReparto)
        mongo.db.PELICULA.update(
            { "_id": keyPelicula },
            { "$pull": { "reparto": {"actor._id" :keyActor}}})
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

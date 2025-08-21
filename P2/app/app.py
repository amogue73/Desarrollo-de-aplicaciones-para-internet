#./app/app.py

from bson.json_util import dumps
from pymongo import MongoClient

from flask import Flask, Response, request, jsonify
from bson import ObjectId

app = Flask(__name__)

# Conectar al servicio (docker) "mongo" en su puerto estandar
client = MongoClient("mongo", 27017)

# Base de datos
db = client.cockteles

recipes = db["recipes"]

#Devuleve json con todas las recetas de la base de datos
@app.route('/todas_las_recetas')
def mongo():
    # Encontramos los documentos de la coleccion "recipes"
    recetas = db.recipes.find() # devuelve un cursor(*), no una lista ni un iterador

    lista_recetas = []
    for  receta in recetas:
        app.logger.debug(receta)  # salida consola
        lista_recetas.append(receta)

    response = {
        'len': len(lista_recetas),
        'data': lista_recetas
    }

    # Convertimos los resultados a formato JSON
    resJson = dumps(response)

    # Devolver en JSON al cliente cambiando la cabecera http para especificar que es un json
    return Response(resJson, mimetype='application/json')

#Devuelve json con todas las recetas que tengan el nombre de "Cuba Libre" de la base de datos
@app.route('/recetas_de/cuba_libre')
def cuba_libre():
    recetas = db.recipes.find({"name": "Cuba Libre"})

    lista_recetas = []
    for  receta in recetas:
        app.logger.debug(receta)
        lista_recetas.append(receta)

    response = {
        'len': len(lista_recetas),
        'data': lista_recetas
    }

    resJson = dumps(response)

    return Response(resJson, mimetype='application/json')

#Devuelve todas las recetas en cuyos ingredientes aparezca el nombre pasado por argumento
@app.route('/recetas_con/<string:ing>')
def con_ing(ing):
    #se usa una expresión regular y la opción i para ignorar las mayúsculas
    recetas = db.recipes.find({"ingredients.name": {"$regex": ing, "$options": "i"}})

    lista_recetas = []
    for  receta in recetas:
        app.logger.debug(receta)
        lista_recetas.append(receta)

    response = {
        'len': len(lista_recetas),
        'data': lista_recetas
    }

    resJson = dumps(response)

    return Response(resJson, mimetype='application/json')

#Devuelve un json con las recetas que constan de justamente la cantidad pasada en la url
@app.route('/recetas_compuestas_de/<int:cantidad>/ingredientes')
def cantidad_ingredientes(cantidad):
    recetas = db.recipes.find({"ingredients": {"$size": cantidad}})

    lista_recetas = []
    for  receta in recetas:
        app.logger.debug(receta)  # salida consola
        lista_recetas.append(receta)

    response = {
        'len': len(lista_recetas),
        'data': lista_recetas
    }

    resJson = dumps(response)

    return Response(resJson, mimetype='application/json')



# ---------------------------- API ----------------------------
def crearJson(cursor):
    lista = []
    for recipe in cursor:
        recipe['_id'] = str(recipe['_id'])
        lista.append(recipe)
    return jsonify(lista)


#Api con la que se puede:
# - ver todas las recetas
# - ver todas las recetas que tengan un ingrediente pasado en la url
# - añadir una receta mediante un json enviado con POST
@app.route('/api/recipes', methods=['GET', 'POST'])
def api_1():
    if request.method == 'GET':
        args = request.args
        con = args.get('con')
        
        if con is not None:
            buscados = db.recipes.find({"ingredients.name": {"$regex": con, "$options": "i"}}).sort('name')
        else:
            buscados = db.recipes.find().sort('name')

        return crearJson(buscados)
    if request.method == 'POST':

        receta_mismo_nombre = list(db.recipes.find({"name": request.json['name']}))
        if len(receta_mismo_nombre) == 0:
            new_recipe = {
                "name": request.json['name'],
                "instructions": request.json['instructions'],
                "ingredients": request.json['ingredients'],
                "slug": request.json['slug']
            }
            recipes.insert_one(new_recipe)
            receta_insertada = db.recipes.find({"name": request.json['name']})
            
            return crearJson(receta_insertada)
        else:
            return 'Error, ya existe una receta con este nombre'
#cambiar el return, hacer que devuelva el objeto json
#hacer comprobaciones para manejar los errores

#Api con la que se puede:
# - actualizar una receta que tenga el id pasado en la url y con los datos
#   que aparezcan en un json enviado en la petición PUT
# - eliminar la receta que tenga por id la cadena que aparezca en la url

@app.route('/api/recipes/<string:id>', methods=['PUT', 'DELETE'])
def api_2(id):

    if len(list(db.recipes.find({"_id": ObjectId(id)}))) == 0:
        return "Error. No existe ninguna receta con el id proporcionado"
    else:
        respuesta = ''

        if request.method == 'PUT':

            if "name" in request.json:
                if len(list(db.recipes.find({"name": request.json['name']}))) != 0:
                    return "Error, no se puede actualizar, ya hay una receta con ese nombre"
                else:
                    db.recipes.find_one_and_update(
                        {"_id": ObjectId(id)},
                        {"$set": request.json}
                    )
                    receta_buscada = db.recipes.find({"_id": ObjectId(id)})   
                    respuesta =  crearJson(receta_buscada)

        if request.method == 'DELETE':

            receta_buscada = db.recipes.find({"_id": ObjectId(id)}) 
            respuesta = crearJson(receta_buscada)

            db.recipes.delete_one({"_id": ObjectId(id)})



        return respuesta


#cambiar el return, hacer que devuelva el objeto json
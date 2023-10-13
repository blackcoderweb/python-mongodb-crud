# Me permite definir mis rutas, además importamos los objetos Response y status para las respuestas del servidor
from fastapi import APIRouter, Response, status

# Importar objeto connection
from config.db import connection

# Importo los esquemas para usarlos en las funciones que se ejecutan cuando accedo a una ruta
from schemas.user import userEntity, usersEntity

# Importo el modelo que se va a guardar en la BD
from models.user import User

# Importo hash de la librería passlib para cifrar contraseñas
from passlib.hash import sha256_crypt

# Importo ObjectId para convertir str Id en ObjectId
from bson import ObjectId

# Para importar el tipo de respuesta
from starlette.status import HTTP_204_NO_CONTENT

# Lo almaceno en una variable para usarlo
user = APIRouter()

# Defino mis rutas

#Listar todos los usuarios
@user.get('/users', response_model=list[User], tags=['users'])
def find_all_users():
    # Busca los datos en la colección user
    return usersEntity(connection.fast_api.user.find())

#Crear usuario
@user.post('/users', response_model=User, tags=['users'])
def create_user(user: User):
    new_user = dict(user)
    # Cifro contraseña
    new_user['password'] = sha256_crypt.encrypt(new_user['password'])
    # elimino el id del modelo para dejar solo el que genera MongoDB
    del new_user['id']
    # Inserto el nuevo user y pido que se retorne el id del usuario insertado
    id = connection.fast_api.user.insert_one(new_user).inserted_id

    created_user = connection.fast_api.user.find_one({'_id': id})
    return userEntity(created_user)

#Buscar usuario
@user.get('/users/{id}', response_model=User, tags=['users'])
def find_user(id: str):
    return userEntity(connection.fast_api.user.find_one({'_id': ObjectId(id)}))

#Actualizar usuario
@user.put('/users/{id}', response_model=User, tags=['users'])
def update_user(id: str, user: User):
    connection.fast_api.user.find_one_and_update(
        {'_id': ObjectId(id)}, {'$set': dict(user)})
    return userEntity(connection.fast_api.user.find_one({'_id': ObjectId(id)}))

#Eliminar usuario
@user.delete('/users/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['users'])
def delete_user(id: str):
    userEntity(connection.fast_api.user.find_one_and_delete(
        {'_id': ObjectId(id)}))
    return Response(status_code=HTTP_204_NO_CONTENT)

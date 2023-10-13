#Esta función me devuelve un diccionario con los datos que estamos definiendo
#Cuando necesito devolver un usuario
def userEntity(item) -> dict:
    return {
        'id': str(item['_id']),
        'name': item['name'],
        'email': item['email'],
        'password': item['password']
    }

#Cuando necesito devolver una lista de usuarios  
def usersEntity(entity) -> list:
    #Esto permite generar una lista dinámica
    return [userEntity(item) for item in entity]
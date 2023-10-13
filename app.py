from fastapi import FastAPI
#Importo el módulo para usar las rutas definidas
from routes.user import user

from docs import tags_metadata

#Crear server
app = FastAPI(
    title='REST API with FastAPI and MongoDB',
    description='This is a simple API with FastAPI and MongoDB',
    version='0.0.1',
    openapi_tags=tags_metadata
)

#Le indico a app que utilice este módulo
app.include_router(user)


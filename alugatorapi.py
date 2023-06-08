from fastapi import FastAPI, Request
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import json
import uvicorn

###
#
#   TODO: Criar coleção no MongoDB para os numerar os dispositivos e relacionar ao cliente e o AOSP acessar
###

load_dotenv()
app = FastAPI()

# Config do Banco
client = MongoClient(os.getenv('DATABASE_CONNECTION'))
db = client['alugator']
collection = db['clientes']

# Rota de validação de login e retornar usuario
@app.post('/login')
async def validar_login(request: Request):
    data = await request.json()
    usuario = data.get('usuario')
    senha = data.get('senha')

    query = {'nome': usuario, 'senha': senha}
    result = collection.find_one(query)

    if result:
        return {'message': 'Login válido', 'usuario': result['nome']}

    return {'message': 'Usuário não encontrado'}

# Rota para obter o prazo
@app.get('/prazo')
async def get_prazo(usuario: str):
    query = {'nome': usuario}
    result = collection.find_one(query)

    if result:
        prazo = result['prazo']
        return {'prazo': prazo}

    return {'message': 'Usuário não encontrado'}

# Rota para obter a lista de clientes
@app.get('/clientes')
async def get_clientes():
    clientes = list(collection.find())

    clientes_json = json.dumps(clientes, default=str)

    return clientes_json

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)

import csv
import database
import json
from datetime import datetime

# Funções auxiliares
def date_from_timestamp(timestamp):
  return timestamp.strftime('%Y-%m-%d')

def today():
  return datetime.today().strftime('%Y-%m-%d')

db = database.Database('weather.db')

with db as connection:
    # Insere locais no banco de dados
    with open('data/locais.csv') as file:
        db.load_locais(file)
    
    with open('data/infos.json') as file:
        infos = json.loads(file.read())

    # Registra o acesso
    id_acesso = db.registra_acesso(1, today(), today())

    for obj in infos:
    
        print("Inserindo previsão {} {} {}".format(id_acesso, obj['date'].split()[1], obj['temperature']['temperature']))
        db.registra_previsao(id_acesso, obj['date'].split()[1], obj['temperature']['temperature'])

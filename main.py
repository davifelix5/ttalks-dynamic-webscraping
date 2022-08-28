from datetime import date, datetime
from database import Database

db = Database('./weather.db')

with db as connection:
  print(db.get_acessos(11))

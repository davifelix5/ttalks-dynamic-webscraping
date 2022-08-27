from database import Database

db = Database('./weather.db')

with db as connection:
  # db.add_leitura('2022-08-31 20:42:00', 25, 'São Paulo')
  print(db.get_leituras('2022-08-31', 20, 'São Paulo'))
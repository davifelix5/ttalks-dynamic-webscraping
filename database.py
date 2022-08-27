import sqlite3

class Database:
  def __init__(self, filename):
    """
      Executa quando a instância do banco de dados é criada,
    inicializando a tabela de leituras
    """
    self.connected = False
    self.filename = filename
    self.con = None
    self._init_database()

  def __enter__(self):
    """
      Executa quando o with statement é iniciado, abrindo a 
    conexão e retornando a instância do banco de dados.
    """
    self.con = self._connect()
    return self

  def __exit__(self, exc_type, exc_val, exc_tb):
    """
      Executa quando o with statement é iniciado, fechando a
    conexão.
    """
    self.con.close()

  def _connect(self):
    """
      Abre uma conexão com o banco de dados.
    """
    conn = sqlite3.connect(self.filename)
    self.connected = True
    return conn

  def _check_coonection(self):
    """
      Verifica se existe uma conexão aberta com o banco de dados. Caso
    contrário, levanta uma excessão.
    """
    if not self.con:
      raise Exception('Conexão não foi aberta')

  def _init_database(self):
    """
      Inicializa a tabela de leituras do banco de dados
    """
    conn = self._connect()
    cursor = conn.cursor()
    query = """CREATE TABLE IF NOT EXISTS leituras (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      data_acesso TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
      data_previsao TEXT NOT NULL,
      local VARCHAR(155) NOT NULL,
      temperatura INTEGER NOT NULL
    )"""
    cursor.execute(query)
    conn.commit()
    conn.close()

  def add_leitura(self, data, temperatura, local):
    """
      Adiciona uma leitura de previsão (com data, temperatura e local) 
    ao banco de dados.
    """
    self._check_coonection()      
    
    cursor = self.con.cursor()
    query = "INSERT INTO leituras (data_previsao, temperatura, local) VALUES (?, ?, ?)"
    parameters = (data, temperatura, local)

    cursor.execute(query, parameters)
    self.con.commit()

  def get_leituras(self, data, hora, local):
    """
      Retorna as leituras feitas em um local para uma determinada data
    e hora.
    """
    self._check_coonection()    

    cursor = self.con.cursor()
    query = """SELECT data_previsao, data_acesso, temperatura FROM leituras WHERE 
      date(data_previsao) = date(?)
      AND CAST(strftime('%H', data_previsao) AS INT) = ? 
      AND local = ?"""
    params = (data, hora, local)

    cursor.execute(query, params)
    res = cursor.fetchall()
    labels = ('Data da previsão', 'Acesso em', 'Temperatura (°C)')

    return [dict(zip(labels, prev)) for prev in res] 
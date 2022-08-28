import sqlite3
import csv

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

    # Cria tabelas
    query = """
        CREATE TABLE IF NOT EXISTS local (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            nome VARCHAR(32) NOT NULL UNIQUE,
            url VARCHAR(128) NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS acesso (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            dt_acesso TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
            dt_previsao TEXT NOT NULL,
            id_local INTEGER,
            FOREIGN KEY (id_local) REFERENCES local(id),
            UNIQUE (dt_acesso, dt_previsao, id_local)
        );

        CREATE TABLE IF NOT EXISTS previsao (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            id_acesso INTEGER NOT NULL,
            horario VARCHAR(32),
            temperatura INTEGER,
            FOREIGN KEY (id_acesso) REFERENCES acesso(id)
        );
      """
    
    cursor.executescript(query)
    conn.commit()
    conn.close()

  def load_locais(self, file):
    """
      Lê o CSV que relaciona o nome do local à sua URL no site climatempo
      e insere essas informações na tabela "local"
    """
    reader = csv.reader(file)
    next(reader)
    cursor = self.con.cursor()
    for line in reader:
        query = "INSERT OR IGNORE INTO local (nome, url) VALUES (?, ?)"
        parameters = (line[0], line[1])
        cursor.execute(query, parameters)

    self.con.commit()

  def get_locais(self):
    """
      Retorna lista de dicionários com todos os locais na tabela "local"
      id - primary key do objeto
      nome - nome do local
      url - url do local no site climatempo
    """

    cur = self.con.cursor()
    result = cur.execute("SELECT * FROM local").fetchall()
    self.con.commit()
    return [{"id":x[0], "nome":x[1], "url":x[2]} for x in result]

  def registra_acesso(self, id_local, dt_acesso, dt_previsao):
    """
      Registra o acesso na tabel "acesso" do banco de dados
      e retorna o ID da linha inserida
    """

    cur = self.con.cursor()
    query = "INSERT INTO acesso (id_local, dt_acesso, dt_previsao) VALUES (?, ?, ?)"
    parameters = (id_local, dt_acesso, dt_previsao)
    cur.execute(query, parameters)
    
    self.con.commit()

    return cur.lastrowid

  def get_acessos(self, id=None):
    cur = self.con.cursor()
    if id:
        query = "SELECT * FROM acesso WHERE id=?"
        parameters = (id,)
        result = cur.execute(query, parameters).fetchall()
    else:
        query = "SELECT * FROM acesso"
        result = cur.execute(query).fetchall()
    
    return [{"id":x[0], "dt_acesso":x[1], "dt_previsao":x[2], "id_local":x[3]} for x in result]
  
  def registra_previsao(self, id_acesso, horario, temperatura):
    """
      Registra a previsao na tabela "previsao" do banco de dados
      e retorna o ID da linha inserida
    """

    cur = self.con.cursor()
    query = "INSERT INTO previsao (id_acesso, horario, temperatura) VALUES (?, ?, ?)"
    parameters = (id_acesso, horario, temperatura)
    cur.execute(query, parameters)
    
    self.con.commit()

    return cur.lastrowid

  def get_previsoes(self, id=None):
    cur = self.con.cursor()
    query = "SELECT * FROM previsao"
    parameters = []

    if id:
        query += " WHERE id=?"
        parameters.append(id)

    result = cur.execute(query, parameters).fetchall()
    
    return [{"id":x[0], "id_acesso":x[1], "horario":x[2], "temperatura":x[3]} for x in result]
  
  def get_previsoes_filtradas(self, data_acesso, data_previsao, cidade, time=None):
    cursor = self.con.cursor()
    query = """SELECT p.temperatura, p.horario, a.dt_previsao, a.dt_acesso, l.nome
			FROM previsao p
      INNER JOIN acesso a
      ON p.id_acesso = a.id
			INNER JOIN local l
			ON a.id_local = l.id
      WHERE
			l.nome = ? AND
      a.dt_acesso = ? AND
      a.dt_previsao = ?
    """
    parameters = [cidade, data_acesso, data_previsao]

    if time:
      query += " AND horario = ?"
      parameters.append(time)

    response = cursor.execute(query, parameters).fetchall()
    self.con.commit()
    
    labels = ('temperatura_prevista', 'horario_previsao', 'dt_previsao', 'dt_acesso', 'cidade')
    return [dict(zip(labels, prev)) for prev in response]
from CONECTAR.funcaoConectar import conectar
from flask import Flask, jsonify


app = Flask(__name__)

#Cadastro USUARIOS

@app.route("/CadastroUsuario", methods=["GET"])
def listar_Usuarios():
    conn = conectar()
    #conn.execute("PRAGMA foreign_keys = ON") #ativa as chaves estrangeiras das tabelas (pois, não é ativado por padrão)
    cursor = conn.cursor()
    cursor.execute("SELECT IDUsuario, CPFUsuario, NomeUsuario, SenhaUsuario, NomeInstituicao FROM CadastroUsuario")
    dados = [
        {"idUsuario": row[0], "CPFUsuario": row[1], "NomeUsuario": row[2], "SenhaUsuario": row[3], "NomeInstituicao": row[4]}
        for row in cursor.fetchall()
    ]
    conn.close()
    return jsonify(dados)


#Cadastro LIVROS

@app.route("/CadastroLivro", methods=["GET"])
def listar_Livros():
    conn = conectar()
    #conn.execute("PRAGMA foreign_keys = ON") #ativa as chaves estrangeiras das tabelas (pois, não é ativado por padrão)
    cursor = conn.cursor()
    cursor.execute("SELECT IDLivro, ISBNLivro, TituloLivro, GeneroLivro, NomeEditora FROM CadastroLivro")
    dados = [
        {"idLivro": row[0], "ISBNLivro": row[1], "TituloLivro": row[2], "GeneroLivro": row[3], "NomeEditora": row[4]}
        for row in cursor.fetchall()
    ]
    conn.close()
    return jsonify(dados)


#Cadastro INSTITUIÇÃO

@app.route("/CadastroInstituicao", methods=["GET"])
def listar_Instituicoes():
    conn = conectar()
    #conn.execute("PRAGMA foreign_keys = ON") #ativa as chaves estrangeiras das tabelas (pois, não é ativado por padrão)
    cursor = conn.cursor()
    cursor.execute("SELECT IDInstituicao, NomeInstituicao, CidadeInstituicao FROM CadastroInstituicao")
    dados = [
        {"idInstituicao": row[0], "NomeInstituicao": row[1], "CidadeInstituicao": row[2]}
        for row in cursor.fetchall()
    ]
    conn.close()
    return jsonify(dados)


#Cadastro EDITORA

@app.route("/CadastroEditora", methods=["GET"])
def listar_Editoras():
    conn = conectar()
    #conn.execute("PRAGMA foreign_keys = ON") #ativa as chaves estrangeiras das tabelas (pois, não é ativado por padrão)
    cursor = conn.cursor()
    cursor.execute("SELECT IDEditora, CNPJEditora, NomeEditora FROM CadastroEditora")
    dados = [
        {"idEditora": row[0], "CNPJEditora": row[1], "NomeEditora": row[2]}
        for row in cursor.fetchall()
    ]
    conn.close()
    return jsonify(dados)



#Cadastro RESERVA

@app.route("/CadastroReserva", methods=["GET"])
def listar_Reservas():
    conn = conectar()
    #conn.execute("PRAGMA foreign_keys = ON") #ativa as chaves estrangeiras das tabelas (pois, não é ativado por padrão)
    cursor = conn.cursor()
    cursor.execute("SELECT IDReserva, TituloLivro, Nomeusuario, NomeEditora, SenhaUsuario, DataReserva FROM CadastroReserva")
    dados = [
        {"idReserva": row[0], "TituloLivro": row[1], "Nomeusuario": row[2], "NomeEditora": row[3], "DataReserva": row[4]}
        for row in cursor.fetchall()
    ]
    conn.close()
    return jsonify(dados)



if __name__ == "__main__":
    app.run(debug=True)



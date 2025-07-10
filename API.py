from CONECTAR.funcaoConectar import conectar
from flask import Flask, jsonify


app = Flask(__name__)


@app.route("/CadastroUsuario", methods=[""])
def listar_Cadastros():
    conn = conectar()
    #conn.execute("PRAGMA foreign_keys = ON") #ativa as chaves estrangeiras das tabelas (pois, não é ativado por padrão)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO CadastroUsuario (Email, Senha) VALUES (?, ?)")
    conn.commit()
    dados = [
        {"id": row[0], "Email": row[1], "Senha": row[2]}
        for row in cursor.fetchall()
    ]
    conn.close()
    return jsonify(dados)

if __name__ == "__main__":
    app.run(debug=True)
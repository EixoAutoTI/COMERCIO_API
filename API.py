from CONECTAR.funcaoConectar import conectar
from flask import Flask, jsonify


app = Flask(__name__)

#Cadastro USUARIOS

@app.route("/CadastroUsuario", methods=["GET"])
def listar_usuario():
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


#INSERT USUARIO

@app.route("/CadastroUsuario", methods=["POST"])
def criar_usuario():
    dados = request.get_json(silent=True)
    if not dados:
        abort(400, description="JSON inválido ou ausente")

    # Validação de campos obrigatórios
    campos_obrigatorios = {"IDUsuario, CPFUsuario, NomeUsuario, SenhaUsuario, NomeInstituicao"}
    if not campos_obrigatorios.issubset(dados.keys()):
        abort(400, description=f"Campos obrigatórios: {', '.join(campos_obrigatorios)}")

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO CadastroUsuario (IDUsuario, CPFUsuario, NomeUsuario, SenhaUsuario, NomeInstituicao) "
        "VALUES (?, ?, ?)",
        (dados["IDUsuario"], dados["CPFUsuario"], dados["NomeUsuario"], dados["SenhaUsuario"], dados["NomeInstituicao"])
    )
    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()

    # 201 Created + Location do recurso recém‑criado
    resposta = jsonify({"ID": novo_id, **dados})
    resposta.status_code = 201
    resposta.headers["Location"] = f"/CadastroUsuario/{novo_id}"
    return resposta


#DELETE USUARIO

from flask import jsonify, abort

@app.route("/CadastroUsuario/<int:id_usuario>", methods=["DELETE"])
def deletar_usuario(id_usuario):
    conn = conectar()
    cursor = conn.cursor()

    # tenta apagar o registro informado
    cursor.execute("DELETE FROM CadastroUsuario WHERE IDCadastroUsuario = ?", (id_usuario,))
    conn.commit()

    # cursor.rowcount informa quantas linhas foram afetadas
    if cursor.rowcount == 0:
        conn.close()
        # nenhum registro com esse ID → devolve 404
        abort(404, description="Essa Usuario não foi cadastrada")

    conn.close()
    # 204 = No Content (padrão para deleções bem‑sucedidas)
    return ("", 204)

#UPDATE USUARIO

@app.route("/CadastroUsuario/<int:id_usuario>", methods=["PUT", "PATCH"])
def atualizar_usuario(id_usuario):
    dados = request.get_json(silent=True)
    if not dados:
        abort(400, description="JSON inválido ou ausente")

    # Para PUT, garanta que todos os campos estejam presentes
    if request.method == "PUT":
        campos_esperados = {"IDUsuario","CPFUsuario","NomeUsuario","SenhaUsuario","NomeInstituicao"}
        if not campos_esperados.issubset(dados.keys()):
            abort(400, description=f"PUT requer todos os campos: {', '.join(campos_esperados)}")

    # Monta dinamicamente o SQL somente com os campos enviados
    campos_validos = {"IDUsuario","CPFUsuario","NomeUsuario","SenhaUsuario","NomeInstituicao"}
    set_clauses = []
    valores = []
    for campo in campos_validos & dados.keys():
        set_clauses.append(f"{campo} = ?")
        valores.append(dados[campo])

    if not set_clauses:
        abort(400, description="Nenhum campo válido para atualizar")

    valores.append(id_usuario)  # último parâmetro é o WHERE

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        f"UPDATE CadastroUsuario SET {', '.join(set_clauses)} WHERE IDCadastroUsuario = ?",
        tuple(valores)
    )
    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        abort(404, description="Usuário não encontrada")

    conn.close()
    # 204 = No Content, mas você pode devolver 200 com o JSON atualizado se preferir
    return ("", 204)


#----------------------------------------------------------------------------------------------------#



#Cadastro LIVROS

@app.route("/CadastroLivro", methods=["GET"])
def listar_livro():
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


#INSERT LIVROS

@app.route("/CadastroLivro", methods=["POST"])
def criar_livro():
    dados = request.get_json(silent=True)
    if not dados:
        abort(400, description="JSON inválido ou ausente")

    # Validação de campos obrigatórios
    campos_obrigatorios = {"IDLivro, ISBNLivro, TituloLivro, GeneroLivro, NomeEditora"}
    if not campos_obrigatorios.issubset(dados.keys()):
        abort(400, description=f"Campos obrigatórios: {', '.join(campos_obrigatorios)}")

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO CadastroLivro (IDLivro, ISBNLivro, TituloLivro, GeneroLivro, NomeEditora) "
        "VALUES (?, ?, ?)",
        (dados["IDLivro"], dados["ISBNLivro"], dados["TituloLivro"], dados["GeneroLivro"], dados["NomeEditora"])
    )
    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()

    # 201 Created + Location do recurso recém‑criado
    resposta = jsonify({"ID": novo_id, **dados})
    resposta.status_code = 201
    resposta.headers["Location"] = f"/CadastroLivro/{novo_id}"
    return resposta


#DELETE LIVROS

from flask import jsonify, abort

@app.route("/CadastroLivro/<int:id_livro>", methods=["DELETE"])
def deletar_livro(id_livro):
    conn = conectar()
    cursor = conn.cursor()

    # tenta apagar o registro informado
    cursor.execute("DELETE FROM CadastroLivro WHERE IDCadastroLivro = ?", (id_livro,))
    conn.commit()

    # cursor.rowcount informa quantas linhas foram afetadas
    if cursor.rowcount == 0:
        conn.close()
        # nenhum registro com esse ID → devolve 404
        abort(404, description="Esse livro não foi cadastrado")

    conn.close()
    # 204 = No Content (padrão para deleções bem‑sucedidas)
    return ("", 204)

#UPDATE LIVROS

@app.route("/CadastroLivro/<int:id_livro>", methods=["PUT", "PATCH"])
def atualizar_livro(id_livro):
    dados = request.get_json(silent=True)
    if not dados:
        abort(400, description="JSON inválido ou ausente")

    # Para PUT, garanta que todos os campos estejam presentes
    if request.method == "PUT":
        campos_esperados = {"IDLivro", "ISBNLivro", "TituloLivro", "GeneroLivro", "NomeEditora"}
        if not campos_esperados.issubset(dados.keys()):
            abort(400, description=f"PUT requer todos os campos: {', '.join(campos_esperados)}")

    # Monta dinamicamente o SQL somente com os campos enviados
    campos_validos = {"IDLivro", "ISBNLivro", "TituloLivro", "GeneroLivro", "NomeEditora"}
    set_clauses = []
    valores = []
    for campo in campos_validos & dados.keys():
        set_clauses.append(f"{campo} = ?")
        valores.append(dados[campo])

    if not set_clauses:
        abort(400, description="Nenhum campo válido para atualizar")

    valores.append(id_livro)  # último parâmetro é o WHERE

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        f"UPDATE CadastroLivro SET {', '.join(set_clauses)} WHERE IDCadastroLivro = ?",
        tuple(valores)
    )
    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        abort(404, description="Livro não encontrado")

    conn.close()
    # 204 = No Content, mas você pode devolver 200 com o JSON atualizado se preferir
    return ("", 204)


#---------------------------------------------------------------------------------------------#


#Cadastro INSTITUIÇÃO

@app.route("/CadastroInstituicao", methods=["GET"])
def listar_instituicao():
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

#INSERT INSTITUIÇÃO

@app.route("/CadastroInstituicao", methods=["POST"])
def criar_instituicao():
    dados = request.get_json(silent=True)
    if not dados:
        abort(400, description="JSON inválido ou ausente")

    # Validação de campos obrigatórios
    campos_obrigatorios = {"IDInstituicao, NomeInstituicao, CidadeInstituicao"}
    if not campos_obrigatorios.issubset(dados.keys()):
        abort(400, description=f"Campos obrigatórios: {', '.join(campos_obrigatorios)}")

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO CadastroInstituicao (IDInstituicao, NomeInstituicao, CidadeInstituicao) "
        "VALUES (?, ?, ?)",
        (dados["IDInstituicao"], dados["NomeInstituicao"], dados["CidadeInstituicao"])
    )
    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()

    # 201 Created + Location do recurso recém‑criado
    resposta = jsonify({"ID": novo_id, **dados})
    resposta.status_code = 201
    resposta.headers["Location"] = f"/CadastroInstituicao/{novo_id}"
    return resposta


#DELETE INSTITUIÇÃO

from flask import jsonify, abort

@app.route("/CadastroInstituicao/<int:id_instituicao>", methods=["DELETE"])
def deletar_instituicao(id_instituicao):
    conn = conectar()
    cursor = conn.cursor()

    # tenta apagar o registro informado
    cursor.execute("DELETE FROM CadastroInstituicao WHERE IDCadastroInstituicao = ?", (id_instituicao,))
    conn.commit()

    # cursor.rowcount informa quantas linhas foram afetadas
    if cursor.rowcount == 0:
        conn.close()
        # nenhum registro com esse ID → devolve 404
        abort(404, description="Essa instituição não foi cadastrado")

    conn.close()
    # 204 = No Content (padrão para deleções bem‑sucedidas)
    return ("", 204)

#UPDATE INSTITUIÇÃO

@app.route("/CadastroInstituicao/<int:id_instituicao>", methods=["PUT", "PATCH"])
def atualizar_instituicao(id_instituicao):
    dados = request.get_json(silent=True)
    if not dados:
        abort(400, description="JSON inválido ou ausente")

    # Para PUT, garanta que todos os campos estejam presentes
    if request.method == "PUT":
        campos_esperados = {"IDInstituicao", "NomeInstituicao", "CidadeInstituicao"}
        if not campos_esperados.issubset(dados.keys()):
            abort(400, description=f"PUT requer todos os campos: {', '.join(campos_esperados)}")

    # Monta dinamicamente o SQL somente com os campos enviados
    campos_validos = {"IDInstituicao", "NomeInstituicao", "CidadeInstituicao"}
    set_clauses = []
    valores = []
    for campo in campos_validos & dados.keys():
        set_clauses.append(f"{campo} = ?")
        valores.append(dados[campo])

    if not set_clauses:
        abort(400, description="Nenhum campo válido para atualizar")

    valores.append(id_instituicao)  # último parâmetro é o WHERE

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        f"UPDATE CadastroInstituicao SET {', '.join(set_clauses)} WHERE IDCadastroInstituicao = ?",
        tuple(valores)
    )
    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        abort(404, description="Instituição não encontrado")

    conn.close()
    # 204 = No Content, mas você pode devolver 200 com o JSON atualizado se preferir
    return ("", 204)


#------------------------------------------------------------------------------------------#

#Cadastro EDITORA

@app.route("/CadastroEditora", methods=["GET"])
def listar_editora():
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

#INSERT EDITORA

@app.route("/CadastroEditora", methods=["POST"])
def criar_editora():
    dados = request.get_json(silent=True)
    if not dados:
        abort(400, description="JSON inválido ou ausente")

    # Validação de campos obrigatórios
    campos_obrigatorios = {"IDEditora, CNPJEditora, NomeEditora"}
    if not campos_obrigatorios.issubset(dados.keys()):
        abort(400, description=f"Campos obrigatórios: {', '.join(campos_obrigatorios)}")

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO CadastroEditora (IDEditora, CNPJEditora, NomeEditora) "
        "VALUES (?, ?, ?)",
        (dados["IDEditora"], dados["CNPJEditora"], dados["NomeEditora"])
    )
    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()

    # 201 Created + Location do recurso recém‑criado
    resposta = jsonify({"ID": novo_id, **dados})
    resposta.status_code = 201
    resposta.headers["Location"] = f"/CadastroEditora/{novo_id}"
    return resposta


#DELETE EDITORA

from flask import jsonify, abort

@app.route("/CadastroEditora/<int:id_Editora>", methods=["DELETE"])
def deletar_editora(id_editora):
    conn = conectar()
    cursor = conn.cursor()

    # tenta apagar o registro informado
    cursor.execute("DELETE FROM CadastroEditora WHERE IDCadastroEditora = ?", (id_editora,))
    conn.commit()

    # cursor.rowcount informa quantas linhas foram afetadas
    if cursor.rowcount == 0:
        conn.close()
        # nenhum registro com esse ID → devolve 404
        abort(404, description="Essa editora não foi cadastrada")

    conn.close()
    # 204 = No Content (padrão para deleções bem‑sucedidas)
    return ("", 204)

#UPDATE EDITORA

@app.route("/CadastroEditora/<int:id_editora>", methods=["PUT", "PATCH"])
def atualizar_editora(id_editora):
    dados = request.get_json(silent=True)
    if not dados:
        abort(400, description="JSON inválido ou ausente")

    # Para PUT, garanta que todos os campos estejam presentes
    if request.method == "PUT":
        campos_esperados = {"IDEditora", "CNPJEditora", "NomeEditora"}
        if not campos_esperados.issubset(dados.keys()):
            abort(400, description=f"PUT requer todos os campos: {', '.join(campos_esperados)}")

    # Monta dinamicamente o SQL somente com os campos enviados
    campos_validos = {"IDEditora", "CNPJEditora", "NomeEditora"}
    set_clauses = []
    valores = []
    for campo in campos_validos & dados.keys():
        set_clauses.append(f"{campo} = ?")
        valores.append(dados[campo])

    if not set_clauses:
        abort(400, description="Nenhum campo válido para atualizar")

    valores.append(id_editora)  # último parâmetro é o WHERE

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        f"UPDATE CadastroEditora SET {', '.join(set_clauses)} WHERE IDCadastroEditora = ?",
        tuple(valores)
    )
    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        abort(404, description="Editora não encontrada")

    conn.close()
    # 204 = No Content, mas você pode devolver 200 com o JSON atualizado se preferir
    return ("", 204)


#--------------------------------------------------------------------------------------#



#Cadastro RESERVA

@app.route("/CadastroReserva", methods=["GET"])
def listar_reserva():
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

#INSERT Reserva

@app.route("/CadastroReserva", methods=["POST"])
def criar_reserva():
    dados = request.get_json(silent=True)
    if not dados:
        abort(400, description="JSON inválido ou ausente")

    # Validação de campos obrigatórios
    campos_obrigatorios = {"IDReserva, TituloLivro, Nomeusuario, NomeEditora, SenhaUsuario, DataReserva"}
    if not campos_obrigatorios.issubset(dados.keys()):
        abort(400, description=f"Campos obrigatórios: {', '.join(campos_obrigatorios)}")

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO CadastroReserva (IDReserva, TituloLivro, Nomeusuario, NomeEditora, SenhaUsuario, DataReserva) "
        "VALUES (?, ?, ?)",
        (dados["IDReserva"], dados["TituloLivro"], dados["Nomeusuario"], dados["NomeEditora"], dados["SenhaUsuario"], dados["DataReserva"])
    )
    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()

    # 201 Created + Location do recurso recém‑criado
    resposta = jsonify({"ID": novo_id, **dados})
    resposta.status_code = 201
    resposta.headers["Location"] = f"/CadastroReserva/{novo_id}"
    return resposta


#DELETE Reserva

from flask import jsonify, abort

@app.route("/CadastroReserva/<int:id_reserva>", methods=["DELETE"])
def deletar_reserva(id_reserva):
    conn = conectar()
    cursor = conn.cursor()

    # tenta apagar o registro informado
    cursor.execute("DELETE FROM CadastroReserva WHERE IDCadastroReserva = ?", (id_reserva,))
    conn.commit()

    # cursor.rowcount informa quantas linhas foram afetadas
    if cursor.rowcount == 0:
        conn.close()
        # nenhum registro com esse ID → devolve 404
        abort(404, description="Essa Reserva não foi cadastrada")

    conn.close()
    # 204 = No Content (padrão para deleções bem‑sucedidas)
    return ("", 204)

#UPDATE Reserva

@app.route("/CadastroReserva/<int:id_reserva>", methods=["PUT", "PATCH"])
def atualizar_reserva(id_reserva):
    dados = request.get_json(silent=True)
    if not dados:
        abort(400, description="JSON inválido ou ausente")

    # Para PUT, garanta que todos os campos estejam presentes
    if request.method == "PUT":
        campos_esperados = {"IDReserva", "TituloLivro", "Nomeusuario", "NomeEditora", "SenhaUsuario", "DataReserva"}
        if not campos_esperados.issubset(dados.keys()):
            abort(400, description=f"PUT requer todos os campos: {', '.join(campos_esperados)}")

    # Monta dinamicamente o SQL somente com os campos enviados
    campos_validos = {"IDReserva", "TituloLivro", "Nomeusuario", "NomeEditora", "SenhaUsuario", "DataReserva"}
    set_clauses = []
    valores = []
    for campo in campos_validos & dados.keys():
        set_clauses.append(f"{campo} = ?")
        valores.append(dados[campo])

    if not set_clauses:
        abort(400, description="Nenhum campo válido para atualizar")

    valores.append(id_reserva)  # último parâmetro é o WHERE

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        f"UPDATE CadastroReserva SET {', '.join(set_clauses)} WHERE IDCadastroReserva = ?",
        tuple(valores)
    )
    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        abort(404, description="Reserva não encontrada")

    conn.close()
    # 204 = No Content, mas você pode devolver 200 com o JSON atualizado se preferir
    return ("", 204)


if __name__ == "__main__":
    app.run(debug=True)
from datetime import datetime

from flask import (
    Flask, abort, flash, redirect, render_template, request, url_for
)
from database import init_db, get_db

app = Flask(__name__)
app.secret_key = "faculends-chave-de-desenvolvimento"
init_db()


# ---------- Catálogo ----------
@app.route("/")
@app.route("/catalogo")
def catalogo():
    busca = request.args.get("busca", "").strip()
    categoria = request.args.get("categoria", "").strip()

    conn = get_db()
    categorias = conn.execute(
        "SELECT DISTINCT categoria FROM materiais ORDER BY categoria"
    ).fetchall()

    sql = "SELECT * FROM materiais WHERE 1=1"
    parametros = []

    if busca:
        sql += " AND (nome LIKE ? OR descricao LIKE ?)"
        parametros.extend([f"%{busca}%", f"%{busca}%"])

    if categoria:
        sql += " AND categoria = ?"
        parametros.append(categoria)

    sql += " ORDER BY nome"
    materiais = conn.execute(sql, parametros).fetchall()
    conn.close()

    return render_template(
        "catalogo.html",
        materiais=materiais,
        categorias=categorias,
        busca=busca,
        categoria_selecionada=categoria,
    )


# ---------- Solicitações ----------
@app.route("/solicitacoes")
def solicitacoes():
    conn = get_db()
    lista = conn.execute(
        "SELECT * FROM solicitacoes ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return render_template("solicitacoes.html", solicitacoes=lista)


@app.route("/solicitar/<int:material_id>", methods=["GET", "POST"])
def solicitar(material_id):
    conn = get_db()
    material = conn.execute(
        "SELECT * FROM materiais WHERE id = ?", (material_id,)
    ).fetchone()

    if material is None:
        conn.close()
        abort(404)

    erro = None
    solicitante = ""

    if request.method == "POST":
        solicitante = request.form.get("solicitante", "").strip()

        if len(solicitante) < 3:
            erro = "Informe seu nome (mínimo de 3 caracteres)."
        elif len(solicitante) > 80:
            erro = "O nome pode ter no máximo 80 caracteres."
        elif material["quantidade_disponivel"] <= 0:
            erro = "Este material não está disponível no momento."
        else:
            data = datetime.now().strftime("%Y-%m-%d %H:%M")
            conn.execute(
                """
                INSERT INTO solicitacoes
                (material_id, solicitante, data_solicitacao, status)
                VALUES (?, ?, ?, 'pendente')
                """,
                (material_id, solicitante, data),
            )
            conn.commit()
            conn.close()
            flash(f"Solicitação de {material['nome']} enviada com sucesso!")
            return redirect(url_for("solicitacoes"))

    conn.close()
    return render_template(
        "solicitar.html", material=material, erro=erro, solicitante=solicitante
    )


if __name__ == "__main__":
    app.run(debug=True)
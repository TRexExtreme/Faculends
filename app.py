from flask import Flask, render_template, request
from database import init_db, get_db

app = Flask(__name__)
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


if __name__ == "__main__":
    app.run(debug=True)
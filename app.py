from flask import Flask, render_template
from database import init_db, get_db

app = Flask(__name__)
init_db()


# ---------- Catálogo ----------
@app.route("/")
@app.route("/catalogo")
def catalogo():
    conn = get_db()
    materiais = conn.execute("SELECT * FROM materiais ORDER BY nome").fetchall()
    conn.close()
    return render_template("catalogo.html", materiais=materiais)


if __name__ == "__main__":
    app.run(debug=True)
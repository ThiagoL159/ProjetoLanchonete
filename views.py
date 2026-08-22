from flask import render_template
from flask import Flask
app = Flask(__name__)


@app.route("/")
def homepage():
    return render_template("homepage.html")


@app.route("/pedidos")
def pedid():
    return "historico de pedidos"


@app.route("/relatorio")
def relator():
    return "Relatorios dia e mes"

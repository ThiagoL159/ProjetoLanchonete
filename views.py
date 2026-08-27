from flask import Flask, render_template, request, jsonify
from models import registrar_pedido, buscar_ultimos_pedidos, consulta_pedido, relatorio_dia, relatorio_mes
app = Flask(__name__)


@app.route("/")
def homepage():
    return render_template("homepage.html")


@app.route("/pedidos")
def pedid():
    return "historico de pedidos"


@app.route("/relatorio")
def relator():
    return render_template("relatorio.html")

@app.route("/api/relatorio/dia/<string:data>")
def get_relatorio_dia(data):
    resultados = relatorio_dia(data)
    pedidos_formatados = []
    total = 0
    for res in resultados:
        valor, forma_pgto, hora = res
        pedidos_formatados.append({
            "valor": valor,
            "forma_pagamento": forma_pgto,
            "data_hora": hora
        })
        total += valor
    return jsonify({"pedidos": pedidos_formatados, "total": total})

@app.route("/api/relatorio/mes/<string:mes>")
def get_relatorio_mes(mes):
    # mes vem no formato YYYY-MM
    resultados = relatorio_mes(mes + "-01")
    pedidos_formatados = []
    total = 0
    for res in resultados:
        valor, forma_pgto, hora = res
        pedidos_formatados.append({
            "valor": valor,
            "forma_pagamento": forma_pgto,
            "data_hora": hora
        })
        total += valor
    return jsonify({"pedidos": pedidos_formatados, "total": total})

@app.route("/api/pedido", methods=["POST"])
def receber_pedido():
    dados = request.get_json()
    itens_json = dados.get("itens", [])
    forma_pagamento = "Dinheiro"
    itens_tuplas = []
    for item in itens_json:
        itens_tuplas.append((item["id"],item ["quantidade"]))

    try:
        registrar_pedido(forma_pagamento, itens_tuplas)
        return jsonify({"status": "sucesso", "mensagem": "Pedido registrado com sucesso!"})
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500


@app.route("/api/historico")
def historico_pedidos():
    pedidos_brutos = buscar_ultimos_pedidos()
    pedidos_formatados = []
    for pedido in pedidos_brutos:
        id_pedido, hora, valor = pedido
        pedidos_formatados.append({
            "id" : id_pedido,
            "hora": hora,
            "valor": valor
        })
    return jsonify(pedidos_formatados)
    
@app.route("/api/pedido/<int:id_pedido>")
def detalhes_pedido(id_pedido):
    itens_brutos = consulta_pedido(id_pedido)
    
    itens_formatados = []
    for item in itens_brutos:
        nome, qtd, valor = item
        itens_formatados.append({
            "nome": nome,
            "quantidade": qtd,
            "valor": valor
        })
        
    return jsonify(itens_formatados)

import sqlite3
conexao = sqlite3.connect("banco.db")
cursor = conexao.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS produtos  (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                nomedoproduto TEXT NOT NULL UNIQUE,
                valordoproduto FLOAT NOT NULL
                )""")
# produtos = [
#     ("Salgado", 10.00),
#     ("Hamburguer", 9.00),
#     ("Bacon Burguer", 14.00),
#     ("X Burguer", 13.00),
#     ("X Salada", 14.50),
#     ("Egg Burguer", 11.50),
#     ("Egg X Burguer", 15.00),
#     ("Egg X Burguer Especial", 15.50),
#     ("Egg Bacon", 15.00),
#     ("X bacon", 16.00),
#     ("Egg X Bacon", 17.00),
#     ("Frango", 16.00),
#     ("Frango Hamburguer", 17.50),
#     ("X Frango", 17.50),
#     ("Egg Frango", 17.50),
#     ("Egg X Frango", 18.50),
#     ("X Frango Bacon", 19.00),
#     ("Egg X Frango Bacon", 21.00),
#     ("X tudo", 24.00),
#     ("Paladar", 27.00),
#     ("Ovo", 3.00),
#     ("Carne", 5.00),
#     ("Frango", 6.00),
#     ("Presunto", 3.00),
#     ("Queijo", 5.00),
#     ("Bacon", 5.00),
#     ("Guaravita", 3.00),
#     ("LATA", 7.00),
#     ("refriKS", 5.00),
#     ("2 Litros", 13.00),
#     ("Guaraviton", 5.00),
#     ("AguaCom", 3.50),
#     ("AguaSem", 3.00)
# ]

# cursor.executemany("""INSERT OR IGNORE INTO produtos
#                 (nomedoproduto, valordoproduto) VALUES (?,?)
#                 """, produtos)

cursor.execute("""CREATE TABLE IF NOT EXISTS pedidos  (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
                forma_pagamento TEXT NOT NULL,
                valortotal FLOAT NOT NULL
                )""")
cursor.execute("""CREATE TABLE IF NOT EXISTS itens_pedido (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                pedido_id INTEGER NOT NULL,
                produto_id INTEGER NOT NULL,
                quantidade INTEGER NOT NULL,
                valorunitario FLOAT NOT NULL,
                FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
                FOREIGN KEY (produto_id) REFERENCES produtos(id)
                )""")


def relatorio_dia(dia):
    cursor.execute(
        """SELECT valortotal, forma_pagamento, data_hora FROM pedidos WHERE date(data_hora) = date(?)""", (dia,))
    res = cursor.fetchall()
    return res


def relatorio_mes(mes):
    cursor.execute(
        "SELECT valortotal, forma_pagamento, data_hora FROM pedidos WHERE strftime('%y-%m', data_hora) = strftime('%y-%m', ?)", (mes,))
    resultado = cursor.fetchall()
    return resultado


def consulta_pedido(pedido_id):
    cursor.execute("""SELECT pedidos.id, pedidos.data_hora, pedidos.forma_pagamento, pedidos.valortotal, produtos.nomedoproduto, itens_pedido.quantidade, itens_pedido.valorunitario FROM pedidos
    JOIN itens_pedido ON pedidos.id = itens_pedido.pedido_id
    JOIN produtos ON itens_pedido.produto_id = produtos.id
    WHERE pedidos.id = ?""", (pedido_id,))
    resultado = cursor.fetchall()

    id, data_hora, forma_pagamento, valortotal, nomedoproduto, quantidade, valorunitario = resultado[
        0]

    print(f"""Id do pedido: {id} | Data : {data_hora}""")
    for linha in resultado:
        id, data_hora, forma_pagamento, valortotal, nomedoproduto, quantidade, valorunitario = linha
        print(f"""Qtd: {quantidade} {nomedoproduto} Valor: {valorunitario} """)
    print(
        f"""Valor Total: {valortotal} | Forma de pagamento: {forma_pagamento}""")
    print("\n")


def registrar_pedido(forma_pagamento, itens):

    valor_total = 0
    for item in itens:
        produto_id, quantidade = item
        cursor.execute(
            """SELECT valordoproduto FROM produtos WHERE id = ?""", (produto_id,))
        valorunitario = cursor.fetchone()[0]
        valor_total += quantidade * valorunitario
    cursor.execute("""INSERT INTO pedidos (forma_pagamento, valortotal) 
                    VALUES (?, ?)""", (forma_pagamento, valor_total))

    pedido_id = cursor.lastrowid

    for item in itens:
        produto_id, quantidade = item
        cursor.execute(
            """SELECT valordoproduto FROM produtos WHERE id = ?""", (produto_id,))
        valorunitario = cursor.fetchone()[0]
        cursor.execute("""INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, valorunitario)
                            VALUES (?, ?, ?, ?)""", (pedido_id, produto_id, quantidade, valorunitario))

    conexao.commit()

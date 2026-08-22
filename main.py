from views import *
from models import relatorio_dia, relatorio_mes, consulta_pedido, registrar_pedido
from flask import Flask


if __name__ == "__main__":
    app.run()


# registrar_pedido("cartao", [(11, 1), (27, 2)])

print(relatorio_mes("2026-08-13"))

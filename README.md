# Sistema de PDV para Lanchonete 🍔

Este projeto é um trabalho de extensão universitária que consegui alinhar com uma necessidade real, consiste no desenvolvimento de um sistema de Ponto de Venda (PDV) moderno, responsivo e intuitivo para a lanchonete dos meus pais. O objetivo é o controle de pedidos e garantir agilidade no atendimento.

## Sobre o Projeto e Layout

O sistema usa a fonte **Inter** e um fundo cinza claro (`#f4f7f6`) , com painéis brancos e sombras suaves.

Toda a estrutura do layout foi desenvolvida utilizando **HTML** e **CSS** trabalhando com Grids e Flexboxs, separando a interface nas seguintes seções:

*   **Barra Esquerda (`.telahistorico`)**: Exibe uma lista com o histórico dos últimos pedidos realizados.
*   **Área Principal (`.telaprodutos`)**:
    *   **Topo**: janela de busca para filtrar os produtos.
    *   **Meio**: Exibe os produtos de forma listada, separados em duas categorias: **Comida** e **Bebida**. Essa área possui suporte à scroll horizontal. Os produtos apresentados nesta versão são fixos, não havendo funcionalidade para cadastro de novos produtos através da interface, pois nao é uma necessidade real do local.
*   **Carrinho (`.telacarrinho`)**:
    *   Lista todos os produtos que foram adicionados ao pedido atual e possui o botão de "Confirmar", que computa e finaliza o pedido.

## Tecnologias Utilizadas:

*   **Front-end:** HTML, CSS, JavaScript.
*   **Design/UI:** Tipografia Inter, paleta de cores claras com painéis destacados por sombras suaves.
*   **Back-end:** Python com o framework Flask.
*   **Banco de Dados:** SQLite.

## Como Executar o Projeto:

1.  Certifique-se de possuir o [Python](https://www.python.org/) instalado em sua máquina.
2.  Clone ou faça o download deste repositório.
3.  Abra o terminal na pasta do projeto e instale o Flask (caso não tenha instalado):
    ```bash
    pip install flask
    ```
4.  Execute o arquivo principal para iniciar o servidor:
    ```bash
    python main.py
    ```
5.  Acesse o endereço exibido no terminal (geralmente `http://127.0.0.1:5000/`) no seu navegador.

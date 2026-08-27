let carrinho = []
function adicionaraocarrinho(id, nome, preco) {
    let itemexistente = carrinho.find(item => item.id === id);
    if (itemexistente) {
        itemexistente.quantidade += 1;
    } else {
        carrinho.push({
            id: id,
            nome: nome,
            preco: preco,
            quantidade: 1
        })
    }
    atualizartelacarrinho()
}
function atualizartelacarrinho() {
    let divlista = document.querySelector('.lista-pedido')
    let divtotal = document.querySelector('.total-texto strong')
    divlista.innerHTML = ''
    let valortotal = 0
    carrinho.forEach(item => {
        valortotal += (item.preco * item.quantidade)
        let htmldoitem = `
                    <div class="item-pedido">
                        <div class="item-info">
                            <span class="item-qtd">${item.quantidade}x</span>
                            <span class="item-nome">${item.nome}</span>
                        </div>
                        <div style="display: flex; gap: 15px; align-items: center;">
                            <span class="item-preco">R$ ${(item.preco * item.quantidade).toFixed(2).replace('.', ',')}</span>
                            <span class="btn-remover" onclick="removerdocarrinho(${item.id})" title="Remover item">X</span>
                        </div>
                    </div>`
        divlista.innerHTML += htmldoitem
    })
    divtotal.innerHTML = `R$ ${valortotal.toFixed(2).replace('.', ',')}`
}
function enviarPedido() {
    if (carrinho.length === 0) {
        alert("o carrinho está vazio!")
        return
    }
    let dadosDoPedido = {
        itens: carrinho
    }
    fetch("/api/pedido", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(dadosDoPedido)
    })
        .then(resposta => resposta.json())
        .then(dados => {
            if (dados.status === "sucesso") {
                carrinho = []
                atualizartelacarrinho()
                carregar_historico()
                alert("Pedido enviado com sucesso!")
            }
            else {
                alert("Erro ao enviar pedido: " + dados.mensagem)
            }
        })
        .catch(erro => {
            alert("Erro de conexão! O seu servidor Flask (main.py) está rodando?");
            console.error(erro);
        })
}
function carregar_historico() {
    fetch("/api/historico")
        .then(resposta => resposta.json())
        .then(pedidos => {
            let divHistorico = document.querySelector('.telahistorico')
            divHistorico.innerHTML = ''
            pedidos.forEach(pedido => {
                let htmlDoPedido = `
                    <div class="card-pedido" onclick="detalhesdopedido(${pedido.id})">
                        <div class="pedido-cabecalho">
                            <span class="pedido-numero">#00${pedido.id}</span>
                            <span class="pedido-hora">${pedido.hora}</span>
                        </div>
                        <div class="pedido-info">
                            <span class="pedido-itens">Fechado</span>
                            <span class="pedido-total">R$ ${pedido.valor.toFixed(2).replace('.', ',')}</span>
                        </div>
                    </div>
                    `
                divHistorico.innerHTML += htmlDoPedido
            })
        })
        .catch(erro => console.error("Erro ao carregar historico", erro))
}
carregar_historico()
function filtrarProdutos() {
    let textoBusca = document.querySelector('.input-busca').value.toLowerCase()
    let todosCartoes = document.querySelectorAll('.card-produto')
    todosCartoes.forEach(cartao => {
        let tagNome = cartao.querySelector('.nome-produto').innerHTML.toLowerCase()
        if (tagNome.includes(textoBusca)) {
            cartao.style.display = 'flex'
        }
        else {
            cartao.style.display = 'none'
        }
    })

}
function removerdocarrinho(id) {
    let index = carrinho.findIndex(item => item.id === id)
    if (index !== -1) {
        if (carrinho[index].quantidade > 1) {
            carrinho[index].quantidade -= 1
        } else {
            carrinho.splice(index, 1)
        }
    }
    atualizartelacarrinho()
}
function fecharModal() {
    document.getElementById('modal-pedido').style.display = 'none';
}

function detalhesdopedido(id) {
    document.getElementById('modal-pedido').style.display = 'flex';
    document.getElementById('lista-detalhes').innerHTML = '<p>Carregando...</p>';
    fetch("/api/pedido/" + id)
        .then(resposta => resposta.json())
        .then(itens => {
            let divDetalhes = document.getElementById('lista-detalhes');
            divDetalhes.innerHTML = '';
            itens.forEach(item => {
                let htmlItem = `
                            <div class="item-detalhe">
                                <span><strong>${item.quantidade}x</strong> ${item.nome}</span>
                                <span><strong>R$ ${item.valor.toFixed(2).replace('.', ',')}</strong></span>
                            </div>
                        `;
                divDetalhes.innerHTML += htmlItem;
            });
        })
        .catch(erro => console.error("Erro no modal:", erro));
}

function abrirModalRelatorio() {
    document.getElementById('modal-relatorio').style.display = 'flex';
}

function fecharModalRelatorio() {
    document.getElementById('modal-relatorio').style.display = 'none';
}

function mudarTipoInput() {
    let tipo = document.getElementById('tipo-relatorio').value;
    let inputData = document.getElementById('data-input');
    if (tipo === 'dia') {
        inputData.type = 'date';
    } else {
        inputData.type = 'month';
    }
}

async function buscarRelatorio() {
    let tipo = document.getElementById('tipo-relatorio').value;
    let data = document.getElementById('data-input').value;
    
    if (!data) {
        alert("Por favor, selecione uma data ou mês.");
        return;
    }

    let url = `/api/relatorio/${tipo}/${data}`;
    
    try {
        let response = await fetch(url);
        let result = await response.json();
        
        let lista = document.getElementById('lista-resultados-relatorio');
        let totalDiv = document.getElementById('total-resultado-relatorio');
        
        lista.innerHTML = '';
        
        if (result.pedidos.length === 0) {
            lista.innerHTML = '<p style="text-align:center; color:#888;">Nenhum pedido encontrado para esta data.</p>';
            totalDiv.style.display = 'none';
            return;
        }
        
        result.pedidos.forEach(pedido => {
            let div = document.createElement('div');
            div.className = 'item-detalhe';
            div.innerHTML = `
                <div style="display: flex; flex-direction: column; gap: 5px;">
                    <span style="font-size: 12px; color: #888;">${pedido.data_hora}</span>
                    <span><strong>Pagamento:</strong> ${pedido.forma_pagamento}</span>
                </div>
                <span><strong>R$ ${pedido.valor.toFixed(2).replace('.', ',')}</strong></span>
            `;
            lista.appendChild(div);
        });
        
        totalDiv.querySelector('strong').innerHTML = `R$ ${result.total.toFixed(2).replace('.', ',')}`;
        totalDiv.style.display = 'block';
        
    } catch (error) {
        console.error("Erro ao buscar relatório:", error);
        alert("Ocorreu um erro ao buscar o relatório.");
    }
}

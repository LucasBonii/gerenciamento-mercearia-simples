from models import Pessoa, Produtos, Fornecedor, Categoria, Estoque, Venda, Funcionario
from DAO import DaoCategoria, DaoEstoque, DaoFornecedor, DaoFuncionario, DaoPessoa, DaoVenda
from datetime import datetime

class ControllerCategoria:
    def cadastraCategoria(self, novaCategoria):
        existe = False
        x = DaoCategoria.ler()
        for i in x:
            if i.categoria == novaCategoria:
                existe == True
        
        if not existe:
            DaoCategoria.salvar(novaCategoria)
            print('Categoria cadastrada com sucesso!')
        else:
            print('A categoria já existe.')

    def removerCategoria(self, categoriaRemover):

        x = DaoCategoria.ler()
        cat = list(filter(lambda x: x.categoria == categoriaRemover, x))

        if len(cat) <= 0:
            print("Essa categoria não existe.")
        else:
            for i in range(len(x)):
                if x[i].categoria == categoriaRemover:
                    del x[i]
                    break
            print('Categoria removida com sucesso!')
            #TODO: Remover no estoque
            with open('categoria.txt', 'w') as arq:
                for i in x:
                    arq.writelines(i.categoria)
                    arq.writelines('\n')

    def alterarCategoria(self, categoriaAlterar, categoriaAlterada):
    
        x = DaoCategoria.ler()

        cat = list(filter(lambda x: x.categoria == categoriaAlterar, x))

        if len(cat) >=0:
            cat1 = list(filter(lambda x: x.categoria == categoriaAlterada, x))
            if len(cat1) == 0:
                x = list(map(lambda x: Categoria(categoriaAlterada) if(x.categoria==categoriaAlterar) else(x)), x)
                print('Alteração efetuada com sucesso.')
            else:
                print('A categoria já existe.')
        
        else:
            print('A categoria não existe.')
        #TODO: Alterar no estoque
        with open('categoria.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.categoria)
                arq.writelines('\n')

    def mostrarCategoria(self):
        categorias = DaoCategoria.ler()
        if len(categorias) == 0:
            print('Nenhuma categoria encontrada')
            return 0
        else:
            for i in categorias:
                print(f'Categoria: {i.categoria}')

class ControllerEstoque:
    def cadastrarProduto(self, nome, preco, cateogira, quantidade):
        x = DaoEstoque.ler()
        y = DaoCategoria.ler()

        h = list(filter(lambda x: x.categoria == cateogira, y))
        est = list(filter(lambda x: x.produto.nome == nome, x))

        if len(h) > 0:
            if len(est) == 0:
                produto = Produtos(nome, preco, cateogira)
                DaoEstoque.salvar(produto, quantidade)
                print('Produto cadastrado com sucesso')
            else:
                print('Produto já existe em estoque')
        else:
            print("Categoria inexistente")

    def removerProduto(self, nome):
        x = DaoCategoria.ler()
        est = list(filter(lambda x: x.produto.nome == nome, x))

        if len(est) > 0:
            for i in range(len(x)):
                if x[i].produto.nome == nome:
                    del x[i]
                    print("Produto removido com sucesso.")
                    break
        else:
            print('O produto não existe')

        with open('estoque.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.produto.nome + "|" + i.produto.preco + "|" +
                           i.categoria + "|" + str(i.quantidade))
            arq.writelines('\n')

    def alterarProduto(self, nomeAlterar, novoNome, novaCategoria, novoPreco, novaQuantidade):
        x = DaoEstoque.ler()
        cat = DaoCategoria.ler()

        y = list(filter(lambda x: x.categoria == novaCategoria, cat))

        if len(y) >0:
            est = list(filter(lambda x: x.produto.nome == nomeAlterar, x))
            if len(est) > 0:
                est = list(filter(lambda x: x.produto.nome == novoNome, x))
                if len(est) == 0:
                    x = list(map(lambda x: Estoque(Produtos(novoNome, novoPreco, novaCategoria, novaQuantidade) if(x.produto.nome == nomeAlterar) else(x), x)))
                    print('Produto alterado com sucesso')
            else:
                print("Produto inexistente")

            with open('estoque.txt', 'w') as arq:
                for i in x:
                    arq.writelines(i.produto.nome + "|" + i.produto.preco + "|" +
                            i.categoria + "|" + str(i.quantidade))
                arq.writelines('\n')

        else:
            print('A categoria informada não existe.')

    def mostrarEstoque(self):
            estoque = DaoEstoque.ler()
            if len(estoque) == 0:
                print("Estoque vazio.")
            else:
                print("=======Produtos=======")
                for i in estoque:
                    print(f"Nome: {i.produto.nome}\n"
                          f"Preco: {i.produto.preco}\n"
                          f"Categoria: {i.produto.categoria}\n"
                          f"Quantidade: {i.quantidade}\n")
                    print("------------------------------")

class ControllerVenda:
    def cadastrarVenda(self, nomeProduto, vendedor, comprador, quantidadeVendida):
        x = DaoEstoque.ler()
        temp = []
        existe = False
        quantidade = False

        for i in x:
            if existe == False:
                if i.produto.nome == nomeProduto:
                    existe = True
                    if int(i.quantidade) >= int(quantidadeVendida):
                        quantidade = True
                        i.quantidade = int(i.quantidade) - int(quantidadeVendida)

                        vendido = Venda(Produtos(i.produto.nome, i.produto.preco, i.produto.categoria), vendedor, comprador, quantidadeVendida)

                        valorCompra = int(quantidadeVendida) * i.produto.preco

                        DaoVenda.salvar(vendido)
            temp.append([Produtos(i.produto.nome, i.produto.preco, i.produto.categoria), i.quantidade])

        arq = open('estoque.txt', 'w')
        arq.write("")

        for i in temp:
            with open('estoque.txt', 'w') as arq:
                arq.writelines(i.produto.nome + '|' + i.produto.preco + '|' + i.produto.categoria + '|' + str(i.quantidade))
                arq.writelines('\n')

        if existe == False:
            print("O produto não existe")
            return None
        elif not quantidade:
            print('A quantidade não está disponível em estoque')
            return None
        else:
            print("Venda realizada com sucesso!")
            return valorCompra
        
    def relatorioProdutos(self):
        vendas = DaoVenda.ler()
        produtos = []
        ordenado = []
        for i in vendas:
            nome = i.itensVendidos.nome
            quantidade = i.quantidadeVendida
            tamanho = list(filter(lambda x: x['produto'] == nome, produtos))
            if len(tamanho) > 0:
                produtos = list(map(lambda x: {'produto': nome, 'quantidade': int(x['quantidade'])+int(quantidade)}
                                    if(x['produto'] == nome) else(x), produtos))
            else:
                produtos.append({'produto': nome, 'quantidade': quantidade})

        ordenado = sorted(produtos, key=lambda k: k['quantidade'], reverse=True)
        print("Esses são os produtos mais vendidos:")
        a = 1
        for i in ordenado:
            print(f"=============Produto {a} =============")
            print(f"Produto: {i['produto']}\n"
                  f"Quantidade: {i['quantidade']}\n")
            
            a+=1

    def mostrarVenda(self, dataInicio, dataTermino):
        vendas = DaoVenda.ler()
        dataInicio1 = datetime.strptime(dataInicio, '%d/%m/%Y')
        dataTermino1 = datetime.strptime(dataTermino, '%d/%m/%Y')

        vendas_selecionadas = list(filter(lambda x: datetime.strptime(x.data, '%d/%m/%Y') >= dataInicio1 and 
                                          datetime.strptime(x.data, '%d/%m/%Y') <= dataTermino1), vendas)
        
        cont = 1
        total = 0

        for i in vendas_selecionadas:
            print(f"========== Venda {cont} ==========")
            print(f"Nome: {i.itensVendido.nome}\n"
                  f"Categoria: {i.itensVendido.categoria}\n"
                  f"Data: {i.data}\n"
                  f"Quantidade: {i.quantidadeVendida}\n"
                  f"Cliente: {i.comprador}\n"
                  f"Vendedor: {i.vendedor}")
            
            total += int(i.itensVendido.preco) * int(i.quantidadeVendida)
            cont +=1

        print(f"Total vendido: {total}")
        
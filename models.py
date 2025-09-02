from datetime import datetime

class Categoria:
    def __init__(self, categoria):
        self.categoria = categoria

class Produtos:
    def __init__(self, nome, preco, categoria):
        self.categoria = categoria
        self.nome = nome
        self.preco = preco

class Estoque:
    def __init__(self, produto: Produtos, quantidade):
        self.produto = produto
        self.quantidade = quantidade

class Venda:
    def __init__(self, itensVendidos: Produtos, vendedor, comprador, quantidadeVendida, data=datetime.now().strftime("%d/%m/%Y")):
        self.itensVendidos =  itensVendidos
        self.vendedor =  vendedor
        self.comprador =  comprador
        self.quantidadeVendida =  quantidadeVendida
        self.data = data

class Fornecedor:
    def __init__(self, nome, cnpj, telefone, categoria):
        self.nome = nome
        self.cnpj = cnpj
        self.telefone = telefone
        self.categoria = categoria

class Pessoa:
    def __init__(self, nome, telefone, cpf, endereco):
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.endereco = endereco

class Funcionario(Pessoa):
    def __init__(self, clt, nome, telefone, cpf, endereco):
        self.clt = clt
        super().__init__(nome, telefone, cpf, endereco)
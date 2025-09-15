import json
from datetime import datetime

class Pessoa:
    def __init__(self, nome, cpf, email):
        self.nome = nome
        self.cpf = cpf
        self.email = email
    
    def __str__(self):
        return f"Nome: {self.nome}, CPF: {self.cpf}, Email: {self.email}"

class Cliente:
    id_counter = 1
    
    def __init__(self, pessoa):
        self.id = Cliente.id_counter
        Cliente.id_counter += 1
        self.pessoa = pessoa
    
    def __str__(self):
        return f"ID: {self.id}, {self.pessoa}"

class Produto:
    id_counter = 1
    
    def __init__(self, nome, preco, estoque):
        self.id = Produto.id_counter
        Produto.id_counter += 1
        self.nome = nome
        self.preco = preco
        self.estoque = estoque
    
    def __str__(self):
        return f"ID: {self.id}, Nome: {self.nome}, Preço: R${self.preco:.2f}, Estoque: {self.estoque}"

class ItemPedido:
    def __init__(self, produto, quantidade):
        self.produto = produto
        self.quantidade = quantidade
    
    def calcular_subtotal(self):
        return self.produto.preco * self.quantidade
    
    def __str__(self):
        return f"{self.produto.nome} - Quantidade: {self.quantidade}, Subtotal: R${self.calcular_subtotal():.2f}"

class Pedido:
    id_counter = 1
    
    def __init__(self, cliente):
        self.id = Pedido.id_counter
        Pedido.id_counter += 1
        self.cliente = cliente
        self.data = datetime.now()
        self.itens = []
        self.status = "Pendente"
    
    def adicionar_item(self, produto, quantidade):
        if quantidade <= produto.estoque:
            self.itens.append(ItemPedido(produto, quantidade))
            produto.estoque -= quantidade
            return True
        else:
            print(f"Estoque insuficiente para {produto.nome}. Estoque disponível: {produto.estoque}")
            return False
    
    def calcular_total(self):
        return sum(item.calcular_subtotal() for item in self.itens)
    
    def finalizar_pedido(self):
        self.status = "Finalizado"
    
    def __str__(self):
        pedido_str = f"Pedido ID: {self.id}\nCliente: {self.cliente.pessoa.nome}\nData: {self.data.strftime('%d/%m/%Y %H:%M')}\nStatus: {self.status}\nItens:\n"
        for item in self.itens:
            pedido_str += f"  - {item}\n"
        pedido_str += f"Total: R${self.calcular_total():.2f}\n"
        return pedido_str

class Menu:
    def __init__(self):
        self.clientes = {}
        self.produtos = {}
        self.pedidos = []
    
    def cadastrar_cliente(self):
        print("\n--- Cadastro de Cliente ---")
        nome = input("Nome: ")
        cpf = input("CPF: ")
        email = input("Email: ")
        
        pessoa = Pessoa(nome, cpf, email)
        cliente = Cliente(pessoa)
        self.clientes[cliente.id] = cliente
        print(f"Cliente cadastrado com sucesso! ID: {cliente.id}")
    
    def cadastrar_produto(self):
        print("\n--- Cadastro de Produto ---")
        nome = input("Nome do produto: ")
        preco = float(input("Preço: "))
        estoque = int(input("Estoque inicial: "))
        
        produto = Produto(nome, preco, estoque)
        self.produtos[produto.id] = produto
        print(f"Produto cadastrado com sucesso! ID: {produto.id}")
    
    def listar_clientes(self):
        print("\n--- Lista de Clientes ---")
        if not self.clientes:
            print("Nenhum cliente cadastrado.")
        else:
            for cliente in self.clientes.values():
                print(cliente)
    
    def listar_produtos(self):
        print("\n--- Lista de Produtos ---")
        if not self.produtos:
            print("Nenhum produto cadastrado.")
        else:
            for produto in self.produtos.values():
                print(produto)
    
    def criar_pedido(self):
        print("\n--- Criar Pedido ---")
        
        if not self.clientes:
            print("Não há clientes cadastrados. Cadastre um cliente primeiro.")
            return
        
        if not self.produtos:
            print("Não há produtos cadastrados. Cadastre produtos primeiro.")
            return
        
        self.listar_clientes()
        cliente_id = int(input("Digite o ID do cliente: "))
        
        if cliente_id not in self.clientes:
            print("Cliente não encontrado.")
            return
        
        cliente = self.clientes[cliente_id]
        pedido = Pedido(cliente)
        
        while True:
            print("\nAdicionar produto ao pedido:")
            self.listar_produtos()
            produto_id = int(input("Digite o ID do produto (0 para finalizar): "))
            
            if produto_id == 0:
                break
            
            if produto_id not in self.produtos:
                print("Produto não encontrado.")
                continue
            
            produto = self.produtos[produto_id]
            quantidade = int(input("Digite a quantidade: "))
            
            if pedido.adicionar_item(produto, quantidade):
                print(f"Produto {produto.nome} adicionado ao pedido.")
            else:
                print("Falha ao adicionar produto ao pedido.")
        
        if pedido.itens:
            pedido.finalizar_pedido()
            self.pedidos.append(pedido)
            print(f"Pedido {pedido.id} criado com sucesso!")
            print(pedido)
        else:
            print("Pedido vazio. Não foi criado.")
    
    def listar_pedidos(self):
        print("\n--- Lista de Pedidos ---")
        if not self.pedidos:
            print("Nenhum pedido realizado.")
        else:
            for pedido in self.pedidos:
                print(pedido)
    
    def salvar_dados(self):
        dados = {
            "clientes": {
                cid: {
                    "nome": cliente.pessoa.nome,
                    "cpf": cliente.pessoa.cpf,
                    "email": cliente.pessoa.email
                } for cid, cliente in self.clientes.items()
            },
            "produtos": {
                pid: {
                    "nome": produto.nome,
                    "preco": produto.preco,
                    "estoque": produto.estoque
                } for pid, produto in self.produtos.items()
            },
            "pedidos": [
                {
                    "id": pedido.id,
                    "cliente_id": pedido.cliente.id,
                    "data": pedido.data.isoformat(),
                    "status": pedido.status,
                    "itens": [
                        {
                            "produto_id": item.produto.id,
                            "quantidade": item.quantidade
                        } for item in pedido.itens
                    ]
                } for pedido in self.pedidos
            ]
        }
        
        with open("ecommerce_data.json", "w") as f:
            json.dump(dados, f, indent=4)
        
        print("Dados salvos com sucesso!")
    
    def carregar_dados(self):
        try:
            with open("ecommerce_data.json", "r") as f:
                dados = json.load(f)
            
            # Restaurar contadores
            if dados["clientes"]:
                Cliente.id_counter = max(map(int, dados["clientes"].keys())) + 1
            if dados["produtos"]:
                Produto.id_counter = max(map(int, dados["produtos"].keys())) + 1
            if dados["pedidos"]:
                Pedido.id_counter = max(pedido["id"] for pedido in dados["pedidos"]) + 1
            
            # Restaurar clientes
            for cid, cliente_data in dados["clientes"].items():
                pessoa = Pessoa(cliente_data["nome"], cliente_data["cpf"], cliente_data["email"])
                cliente = Cliente(pessoa)
                cliente.id = int(cid)  # Manter o ID original
                self.clientes[cliente.id] = cliente
            
            # Restaurar produtos
            for pid, produto_data in dados["produtos"].items():
                produto = Produto(produto_data["nome"], produto_data["preco"], produto_data["estoque"])
                produto.id = int(pid)  # Manter o ID original
                self.produtos[produto.id] = produto
            
            # Restaurar pedidos
            for pedido_data in dados["pedidos"]:
                cliente = self.clientes[pedido_data["cliente_id"]]
                pedido = Pedido(cliente)
                pedido.id = pedido_data["id"]
                pedido.data = datetime.fromisoformat(pedido_data["data"])
                pedido.status = pedido_data["status"]
                
                for item_data in pedido_data["itens"]:
                    produto = self.produtos[item_data["produto_id"]]
                    pedido.itens.append(ItemPedido(produto, item_data["quantidade"]))
                
                self.pedidos.append(pedido)
            
            print("Dados carregados com sucesso!")
        except FileNotFoundError:
            print("Nenhum dado anterior encontrado. Iniciando com dados vazios.")
    
    def exibir_menu(self):
        while True:
            print("\n=== Sistema de Gerenciamento de E-commerce ===")
            print("1. Cadastrar cliente")
            print("2. Cadastrar produto")
            print("3. Listar clientes")
            print("4. Listar produtos")
            print("5. Criar pedido")
            print("6. Listar pedidos")
            print("7. Salvar dados")
            print("8. Carregar dados")
            print("0. Sair")
            
            opcao = input("Escolha uma opção: ")
            
            if opcao == "1":
                self.cadastrar_cliente()
            elif opcao == "2":
                self.cadastrar_produto()
            elif opcao == "3":
                self.listar_clientes()
            elif opcao == "4":
                self.listar_produtos()
            elif opcao == "5":
                self.criar_pedido()
            elif opcao == "6":
                self.listar_pedidos()
            elif opcao == "7":
                self.salvar_dados()
            elif opcao == "8":
                self.carregar_dados()
            elif opcao == "0":
                print("Saindo do sistema...")
                break
            else:
                print("Opção inválida. Tente novamente.")

# Executar o sistema
if __name__ == "__main__":
    sistema = Menu()
    sistema.carregar_dados()  # Tentar carregar dados anteriores
    sistema.exibir_menu()
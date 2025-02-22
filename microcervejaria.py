class Database:
    def __init__(self):
        self.receitas = {}
        self.ingredientes = {}
        self.id_counter = {"receita": 1, "ingrediente": 1}

    def get_next_id(self, entity):
        next_id = self.id_counter[entity]
        self.id_counter[entity] += 1
        return next_id

class Receita:
    def __init__(self, id, nome, descricao, ingredientes):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.ingredientes = ingredientes

    def __str__(self):
        return f"Receita(id={self.id}, nome='{self.nome}', ingredientes={self.ingredientes})"

class Ingrediente:
    def __init__(self, id, nome, fornecedor, preco, validade, estoque):
        self.id = id
        self.nome = nome
        self.fornecedor = fornecedor
        self.preco = preco
        self.validade = validade
        self.estoque = estoque

    def __str__(self):
        return f"Ingrediente(id={self.id}, nome='{self.nome}', estoque={self.estoque})"

class ReceitaCRUD:
    def __init__(self, db):
        self.db = db

    def create_receita(self, nome, descricao, ingredientes):
        id_receita = self.db.get_next_id("receita")
        nova_receita = Receita(id_receita, nome, descricao, ingredientes)
        self.db.receitas[id_receita] = nova_receita
        return nova_receita

    def read_receita(self, id_receita):
        return self.db.receitas.get(id_receita)

    def update_receita(self, id_receita, nome=None, descricao=None, ingredientes=None):
        receita = self.db.receitas.get(id_receita)
        if not receita:
            return None
        if nome:
            receita.nome = nome
        if descricao:
            receita.descricao = descricao
        if ingredientes is not None:
            receita.ingredientes = ingredientes
        return receita

    def delete_receita(self, id_receita):
        return self.db.receitas.pop(id_receita, None)

    def list_receitas(self):
        return list(self.db.receitas.values())

class IngredienteCRUD:
    def __init__(self, db):
        self.db = db

    def create_ingrediente(self, nome, fornecedor, preco, validade, estoque):
        id_ingrediente = self.db.get_next_id("ingrediente")
        novo_ingrediente = Ingrediente(id_ingrediente, nome, fornecedor, preco, validade, estoque)
        self.db.ingredientes[id_ingrediente] = novo_ingrediente
        return novo_ingrediente

    def read_ingrediente(self, id_ingrediente):
        return self.db.ingredientes.get(id_ingrediente)

    def update_ingrediente(self, id_ingrediente, nome=None, fornecedor=None, preco=None, validade=None, estoque=None):
        ingrediente = self.db.ingredientes.get(id_ingrediente)
        if not ingrediente:
            return None
        if nome:
            ingrediente.nome = nome
        if fornecedor:
            ingrediente.fornecedor = fornecedor
        if preco is not None:
            ingrediente.preco = preco
        if validade:
            ingrediente.validade = validade
        if estoque is not None:
            ingrediente.estoque = estoque
        return ingrediente

    def delete_ingrediente(self, id_ingrediente):
        return self.db.ingredientes.pop(id_ingrediente, None)

    def list_ingredientes(self):
        return list(self.db.ingredientes.values())

def main():
    db = Database()
    receita_crud = ReceitaCRUD(db)
    ingrediente_crud = IngredienteCRUD(db)

    while True:
        print("\n--- MENU DA CERVEJARIA ---")
        print("1. Cadastrar receita")
        print("2. Listar receitas")
        print("3. Atualizar receita")
        print("4. Excluir receita")
        print("5. Cadastrar ingrediente")
        print("6. Listar ingredientes")
        print("7. Atualizar ingrediente")
        print("8. Excluir ingrediente")
        print("9. Sair")

        opcao = input("Escolha uma opção: ")

        # 1. Cadastrar receita
        if opcao == '1':
            nome = input("Nome da receita: ")
            descricao = input("Descrição da receita: ")
            ingredientes_str = input("Informe os IDs dos ingredientes que compõem a receita, separados por vírgula (ex.: 1,2,3): ")
            if ingredientes_str.strip():
                lista_ids = [int(x.strip()) for x in ingredientes_str.split(',')]
            else:
                lista_ids = []
            
            nova_receita = receita_crud.create_receita(nome, descricao, lista_ids)
            print(f"\nReceita cadastrada com sucesso: {nova_receita}")

        # 2. Listar receitas
        elif opcao == '2':
            receitas = receita_crud.list_receitas()
            if receitas:
                print("\n--- LISTA DE RECEITAS ---")
                for r in receitas:
                    print(r)
            else:
                print("\nNenhuma receita cadastrada.")

        # 3. Atualizar receita
        elif opcao == '3':
            try:
                id_receita = int(input("Informe o ID da receita a ser atualizada: "))
            except ValueError:
                print("ID inválido.")
                continue

            receita_existente = receita_crud.read_receita(id_receita)
            if not receita_existente:
                print("Receita não encontrada.")
                continue

            novo_nome = input(f"Novo nome (ou Enter para manter '{receita_existente.nome}'): ")
            nova_descricao = input(f"Nova descrição (ou Enter para manter '{receita_existente.descricao}'): ")
            nova_lista_str = input(f"Novos IDs de ingredientes (separados por vírgula) ou Enter para manter {receita_existente.ingredientes}: ")
            
            if not novo_nome:
                novo_nome = receita_existente.nome
            if not nova_descricao:
                nova_descricao = receita_existente.descricao
            
            if nova_lista_str.strip():
                nova_lista_ids = [int(x.strip()) for x in nova_lista_str.split(',')]
            else:
                nova_lista_ids = receita_existente.ingredientes

            receita_atualizada = receita_crud.update_receita(
                id_receita,
                nome=novo_nome,
                descricao=nova_descricao,
                ingredientes=nova_lista_ids
            )
            print(f"\nReceita atualizada: {receita_atualizada}")

        # 4. Excluir receita
        elif opcao == '4':
            try:
                id_receita = int(input("Informe o ID da receita a ser excluída: "))
            except ValueError:
                print("ID inválido.")
                continue

            removida = receita_crud.delete_receita(id_receita)
            if removida:
                print(f"\nReceita '{removida.nome}' removida com sucesso!")
            else:
                print("Receita não encontrada.")

        # 5. Cadastrar ingrediente
        elif opcao == '5':
            nome = input("Nome do ingrediente: ")
            fornecedor = input("Fornecedor: ")
            try:
                preco = float(input("Preço: "))
            except ValueError:
                preco = 0.0
            validade = input("Data de validade (YYYY-MM-DD): ")
            try:
                estoque = int(input("Quantidade em estoque: "))
            except ValueError:
                estoque = 0

            novo_ingrediente = ingrediente_crud.create_ingrediente(
                nome, fornecedor, preco, validade, estoque
            )
            print(f"\nIngrediente cadastrado com sucesso: {novo_ingrediente}")

        # 6. Listar ingredientes
        elif opcao == '6':
            ingredientes = ingrediente_crud.list_ingredientes()
            if ingredientes:
                print("\n--- LISTA DE INGREDIENTES ---")
                for ing in ingredientes:
                    print(ing)
            else:
                print("\nNenhum ingrediente cadastrado.")

        # 7. Atualizar ingrediente
        elif opcao == '7':
            try:
                id_ingrediente = int(input("Informe o ID do ingrediente a ser atualizado: "))
            except ValueError:
                print("ID inválido.")
                continue

            ingrediente_existente = ingrediente_crud.read_ingrediente(id_ingrediente)
            if not ingrediente_existente:
                print("Ingrediente não encontrado.")
                continue

            novo_nome = input(f"Novo nome (ou Enter para manter '{ingrediente_existente.nome}'): ")
            novo_fornecedor = input(f"Novo fornecedor (ou Enter para manter '{ingrediente_existente.fornecedor}'): ")
            try:
                novo_preco = input(f"Novo preço (ou Enter para manter '{ingrediente_existente.preco}'): ")
                novo_preco = float(novo_preco) if novo_preco.strip() else ingrediente_existente.preco
            except ValueError:
                novo_preco = ingrediente_existente.preco

            nova_validade = input(f"Nova validade (ou Enter para manter '{ingrediente_existente.validade}'): ")
            if not nova_validade:
                nova_validade = ingrediente_existente.validade

            try:
                novo_estoque = input(f"Novo estoque (ou Enter para manter '{ingrediente_existente.estoque}'): ")
                novo_estoque = int(novo_estoque) if novo_estoque.strip() else ingrediente_existente.estoque
            except ValueError:
                novo_estoque = ingrediente_existente.estoque

            ingrediente_atualizado = ingrediente_crud.update_ingrediente(
                id_ingrediente,
                nome=novo_nome,
                fornecedor=novo_fornecedor,
                preco=novo_preco,
                validade=nova_validade,
                estoque=novo_estoque
            )
            print(f"\nIngrediente atualizado: {ingrediente_atualizado}")

        # 8. Excluir ingrediente
        elif opcao == '8':
            try:
                id_ingrediente = int(input("Informe o ID do ingrediente a ser excluído: "))
            except ValueError:
                print("ID inválido.")
                continue

            removido = ingrediente_crud.delete_ingrediente(id_ingrediente)
            if removido:
                print(f"\nIngrediente '{removido.nome}' removido com sucesso!")
            else:
                print("Ingrediente não encontrado.")

        # 9. Sair
        elif opcao == '9':
            print("Saindo do sistema...")
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()

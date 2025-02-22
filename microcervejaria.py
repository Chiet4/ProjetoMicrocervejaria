import json

# Arquivo para persistência de dados
ARQUIVO_DADOS = "cervejaria.json"

def carregar_dados():
    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
            return json.load(f)

    except FileNotFoundError:
        return {"receitas": [], "ingredientes": []}

def salvar_dados(dados):
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


dados = carregar_dados()

def cadastrar_receita(nome=None, ingredientes=None, descricao=None):
    """
    Cadastra uma receita. Se os parâmetros não forem fornecidos, utiliza input().
    """
    if nome is None:
        nome = input("Nome da receita: ")
        ingredientes_str = input("Ingredientes (separados por vírgula): ")
        ingredientes = [i.strip() for i in ingredientes_str.split(",")]
        descricao = input("Descrição da receita: ")
    receita = {
        "nome": nome,
        "ingredientes": ingredientes,
        "descricao": descricao
    }
    dados["receitas"].append(receita)
    salvar_dados(dados)
    print("Receita cadastrada com sucesso!")

def listar_receitas():
    print("\nReceitas cadastradas:")
    for r in dados["receitas"]:
        print(f"- {r['nome']} (Ingredientes: {', '.join(r['ingredientes'])}) | Descrição: {r['descricao']}")

def remover_receita(nome=None):
    if nome is None:
        nome = input("Nome da receita a remover: ")
    dados["receitas"] = [r for r in dados["receitas"] if r["nome"] != nome]
    salvar_dados(dados)
    print("Receita removida com sucesso!")

def cadastrar_ingrediente(nome=None, fornecedor=None, preco=None, validade=None, quantidade=None):
    """
    Cadastra um ingrediente. Se os parâmetros não forem fornecidos, utiliza input().
    """
    if nome is None:
        nome = input("Nome do ingrediente: ")
        fornecedor = input("Fornecedor do ingrediente: ")
        preco = float(input("Preço do ingrediente: "))
        validade = input("Validade do ingrediente: ")
        quantidade = int(input("Quantidade em estoque: "))
    ingrediente = {
        "nome": nome,
        "fornecedor": fornecedor,
        "preco": preco,
        "validade": validade,
        "quantidade": quantidade
    }
    dados["ingredientes"].append(ingrediente)
    salvar_dados(dados)
    print("Ingrediente cadastrado com sucesso!")

def listar_ingredientes():
    print("\nIngredientes cadastrados:")
    for i in dados["ingredientes"]:
        print(f"- {i['nome']} | Fornecedor: {i['fornecedor']} | Preço: {i['preco']} | Validade: {i['validade']} | Quantidade: {i['quantidade']}")

def remover_ingrediente(nome=None):
    if nome is None:
        nome = input("Nome do ingrediente a remover: ")
    dados["ingredientes"] = [i for i in dados["ingredientes"] if i["nome"] != nome]
    salvar_dados(dados)
    print("Ingrediente removido com sucesso!")

def menu():
    while True:
        print("\nMenu:")
        print("1. Cadastrar Receita")
        print("2. Listar Receitas")
        print("3. Remover Receita")
        print("4. Cadastrar Ingrediente")
        print("5. Listar Ingredientes")
        print("6. Remover Ingrediente")
        print("7. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_receita()
        elif opcao == "2":
            listar_receitas()
        elif opcao == "3":
            remover_receita()
        elif opcao == "4":
            cadastrar_ingrediente()
        elif opcao == "5":
            listar_ingredientes()
        elif opcao == "6":
            remover_ingrediente()
        elif opcao == "7":
            print("Saindo do programa...")
            break

        else:
            print("Opção inválida, tente novamente.")

def main():
    menu()

if __name__ == "__main__":
    main()

import microcervejaria

def testar_crud():
    print("=== Teste: Cadastro de Ingrediente ===")
    microcervejaria.cadastrar_ingrediente("Malte Pilsen", "Fornecedor A", 10.5, "01/2026", 100)
    
    print("=== Teste: Cadastro de Receita ===")
    microcervejaria.cadastrar_receita("IPA Clássica", ["Malte Pilsen", "Lúpulo Amarillo"], "Uma IPA equilibrada e aromática.")
    
    print("=== Teste: Listar Ingredientes ===")
    microcervejaria.listar_ingredientes()
    
    print("=== Teste: Listar Receitas ===")
    microcervejaria.listar_receitas()
    
    print("=== Teste: Remover Ingrediente ===")
    microcervejaria.remover_ingrediente("Malte Pilsen")
    
    print("=== Teste: Remover Receita ===")
    microcervejaria.remover_receita("IPA Clássica")
    
if __name__ == "__main__":
    testar_crud()

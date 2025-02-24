import microcervejaria
import io
import sys
from unittest.mock import patch

def testar_crud():
    """Função principal de testes com casos mais completos e verificações.
    Durante a execução, são impressos os passos e informações das operações realizadas.
    Ao final, os dados originais do JSON são restaurados."""
    
    # Backup dos dados originais do JSON
    dados_backup = microcervejaria.carregar_dados()

    def capturar_saida(funcao, *args, **kwargs):
        """Captura a saída impressa no terminal e retorna o conteúdo."""
        capturada = io.StringIO()
        sys.stdout = capturada
        funcao(*args, **kwargs)
        sys.stdout = sys.__stdout__
        return capturada.getvalue()

    def reiniciar_dados():
        """Reseta os dados para o estado inicial dos testes (sem afetar o backup original)."""
        microcervejaria.dados = {"receitas": [], "ingredientes": []}
        microcervejaria.salvar_dados(microcervejaria.dados)
        print("Dados reiniciados para o estado inicial dos testes.")

    print("\n=== Início dos Testes ===")
    
    # Teste 1: Cadastro básico de ingrediente e receita
    print("\n=== Teste 1: Cadastro básico ===")
    reiniciar_dados()
    print("Cadastrando ingrediente 'Lúpulo Cascade'...")
    microcervejaria.cadastrar_ingrediente("Lúpulo Cascade", "Fornecedor B", 15.99, "12/2025", 50)
    print("Cadastrando receita 'APA Tropical'...")
    microcervejaria.cadastrar_receita("APA Tropical", ["Lúpulo Cascade", "Malte Vienna"], "Receita refrescante")
    
    print("Verificando cadastros...")
    assert len(microcervejaria.dados["ingredientes"]) == 1, "Falha no cadastro de ingrediente"
    assert len(microcervejaria.dados["receitas"]) == 1, "Falha no cadastro de receita"
    print("Teste 1 concluído com sucesso.")

    # Teste 2: Tentativa de duplicatas
    print("\n=== Teste 2: Prevenção de duplicatas ===")
    print("Tentando cadastrar ingrediente duplicado 'Lúpulo Cascade'...")
    saida = capturar_saida(microcervejaria.cadastrar_ingrediente, "Lúpulo Cascade", "Fornecedor C", 18.50, "06/2026", 30)
    assert "já existe" in saida, "Falha na prevenção de ingrediente duplicado"
    
    print("Tentando cadastrar receita duplicada 'APA Tropical'...")
    saida = capturar_saida(microcervejaria.cadastrar_receita, "APA Tropical", [], "")
    assert "já existe" in saida, "Falha na prevenção de receita duplicada"
    print("Teste 2 concluído com sucesso.")

    # Teste 3: Remoção de itens
    print("\n=== Teste 3: Remoção de registros ===")
    print("Removendo ingrediente 'Lúpulo Cascade'...")
    microcervejaria.remover_ingrediente("Lúpulo Cascade")
    print("Removendo receita 'APA Tropical'...")
    microcervejaria.remover_receita("APA Tropical")
    
    assert len(microcervejaria.dados["ingredientes"]) == 0, "Falha na remoção de ingrediente"
    assert len(microcervejaria.dados["receitas"]) == 0, "Falha na remoção de receita"
    print("Teste 3 concluído com sucesso.")

    # Teste 4: Validação de entrada numérica
    print("\n=== Teste 4: Validação de dados numéricos ===")
    with patch('builtins.input', side_effect=["Malte Inválido", "Fornecedor X", "dez", "15", "01/2025", "vinte", "30"]):
        saida = capturar_saida(microcervejaria.cadastrar_ingrediente)
        assert "Valor inválido" in saida, "Falha na validação de preço ou quantidade"
    print("Teste 4 concluído com sucesso.")

    # Teste 5: Campos obrigatórios
    print("\n=== Teste 5: Validação de campos obrigatórios ===")
    with patch('builtins.input', side_effect=["", "Fornecedor Y", "10", "01/2025", "50"]):
        saida = capturar_saida(microcervejaria.cadastrar_ingrediente)
        assert "não pode ser vazio" in saida.lower(), "Falha na validação de nome vazio"
    print("Teste 5 concluído com sucesso.")

    # Teste 6: Integridade dos dados salvos
    print("\n=== Teste 6: Integridade dos dados salvos ===")
    print("Cadastrando ingrediente 'Levedura US-05' e receita 'American Stout'...")
    microcervejaria.cadastrar_ingrediente("Levedura US-05", "Fermentis", 8.90, "10/2024", 200)
    microcervejaria.cadastrar_receita("American Stout", ["Levedura US-05", "Malte Chocolate"], "Receita encorpada")
    
    print("Recarregando dados do arquivo...")
    dados_recarregados = microcervejaria.carregar_dados()
    assert any(i["nome"] == "Levedura US-05" for i in dados_recarregados["ingredientes"]), "Falha na persistência de ingrediente"
    assert any(r["nome"] == "American Stout" for r in dados_recarregados["receitas"]), "Falha na persistência de receita"
    print("Teste 6 concluído com sucesso.")

    # Teste 7: Verificação case-insensitive
    print("\n=== Teste 7: Verificação case-insensitive ===")
    print("Removendo ingrediente 'levedura us-05' (case-insensitive)...")
    saida = capturar_saida(microcervejaria.remover_ingrediente, "levedura us-05")
    assert "removido" in saida.lower(), "Falha na remoção case-insensitive"
    print("Teste 7 concluído com sucesso.")

    # Teste 8: Listagem vazia
    print("\n=== Teste 8: Listagem de registros vazios ===")
    reiniciar_dados()
    print("Listando ingredientes quando nenhum está cadastrado...")
    saida = capturar_saida(microcervejaria.listar_ingredientes)
    assert "Nenhum ingrediente" in saida, "Falha na listagem vazia de ingredientes"
    
    print("Listando receitas quando nenhuma está cadastrada...")
    saida = capturar_saida(microcervejaria.listar_receitas)
    assert "Nenhuma receita" in saida, "Falha na listagem vazia de receitas"
    print("Teste 8 concluído com sucesso.")

    # Teste 9: Atualização de quantidade
    print("\n=== Teste 9: Atualização de quantidade ===")
    print("Cadastrando ingrediente 'Malte Munich'...")
    microcervejaria.cadastrar_ingrediente("Malte Munich", "Fornecedor Z", 12.75, "06/2025", 100)

    print("Atualizando a quantidade de 'Malte Munich' para 75...")
    for ingrediente in microcervejaria.dados["ingredientes"]:
        if ingrediente["nome"] == "Malte Munich":
            ingrediente["quantidade"] = 75
            break

    microcervejaria.salvar_dados(microcervejaria.dados)  # Garante a persistência

    print("Recarregando dados para verificar a atualização...")
    dados_recarregados = microcervejaria.carregar_dados()
    salvo = any(i["quantidade"] == 75 and i["nome"] == "Malte Munich" for i in dados_recarregados["ingredientes"])
    assert salvo, "Falha na atualização de dados: Quantidade não persistiu corretamente"
    print("Teste 9 concluído com sucesso.")

    # Limpeza final dos dados de teste (reinicia para estado vazio)
    reiniciar_dados()
    
    # Restaura os dados originais no final dos testes
    microcervejaria.salvar_dados(dados_backup)
    print("\n✅ Todos os testes foram concluídos com sucesso! Os dados originais foram restaurados.")

if __name__ == "__main__":
    testar_crud()

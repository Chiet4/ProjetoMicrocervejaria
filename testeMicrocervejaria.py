import microcervejaria
import io
import sys
from unittest.mock import patch

def testar_crud():
    """Função principal de testes com casos mais completos e verificações"""
    
    def capturar_saida(funcao, *args, **kwargs):
        """Captura a saída impressa no terminal"""
        capturada = io.StringIO()
        sys.stdout = capturada
        funcao(*args, **kwargs)
        sys.stdout = sys.__stdout__
        return capturada.getvalue()

    def reiniciar_dados():
        """Reseta os dados para o estado inicial"""
        microcervejaria.dados = {"receitas": [], "ingredientes": []}
        microcervejaria.salvar_dados(microcervejaria.dados)

    # Teste 1: Cadastro básico de ingrediente e receita
    reiniciar_dados()
    print("\n=== Teste 1: Cadastro básico ===")
    microcervejaria.cadastrar_ingrediente("Lúpulo Cascade", "Fornecedor B", 15.99, "12/2025", 50)
    microcervejaria.cadastrar_receita("APA Tropical", ["Lúpulo Cascade", "Malte Vienna"], "Receita refrescante")
    
    assert len(microcervejaria.dados["ingredientes"]) == 1, "Falha no cadastro de ingrediente"
    assert len(microcervejaria.dados["receitas"]) == 1, "Falha no cadastro de receita"

    # Teste 2: Tentativa de duplicatas
    print("\n=== Teste 2: Prevenção de duplicatas ===")
    saida = capturar_saida(microcervejaria.cadastrar_ingrediente, "Lúpulo Cascade", "Fornecedor C", 18.50, "06/2026", 30)
    assert "já existe" in saida, "Falha na prevenção de ingrediente duplicado"
    
    saida = capturar_saida(microcervejaria.cadastrar_receita, "APA Tropical", [], "")
    assert "já existe" in saida, "Falha na prevenção de receita duplicada"

    # Teste 3: Remoção de itens
    print("\n=== Teste 3: Remoção de registros ===")
    microcervejaria.remover_ingrediente("Lúpulo Cascade")
    microcervejaria.remover_receita("APA Tropical")
    
    assert len(microcervejaria.dados["ingredientes"]) == 0, "Falha na remoção de ingrediente"
    assert len(microcervejaria.dados["receitas"]) == 0, "Falha na remoção de receita"

    # Teste 4: Validação de entrada numérica
    print("\n=== Teste 4: Validação de dados numéricos ===")
    with patch('builtins.input', side_effect=["Malte Inválido", "Fornecedor X", "dez", "15", "01/2025", "vinte", "30"]):
        saida = capturar_saida(microcervejaria.cadastrar_ingrediente)
        assert "Valor inválido" in saida, "Falha na validação de preço"
        assert "Valor inválido" in saida, "Falha na validação de quantidade"

    # Teste 5: Campos obrigatórios
    print("\n=== Teste 5: Validação de campos obrigatórios ===")
    with patch('builtins.input', side_effect=["", "Fornecedor Y", "10", "01/2025", "50"]):
        saida = capturar_saida(microcervejaria.cadastrar_ingrediente)
        assert "não pode ser vazio" in saida.lower(), "Falha na validação de nome vazio"  # <--- Ajuste aqui

    # Teste 6: Teste de integridade de dados
    print("\n=== Teste 6: Integridade dos dados salvos ===")
    microcervejaria.cadastrar_ingrediente("Levedura US-05", "Fermentis", 8.90, "10/2024", 200)
    microcervejaria.cadastrar_receita("American Stout", ["Levedura US-05", "Malte Chocolate"], "Receita encorpada")
    
    # Recarrega dados do arquivo para verificar persistência
    dados_recarregados = microcervejaria.carregar_dados()
    assert any(i["nome"] == "Levedura US-05" for i in dados_recarregados["ingredientes"]), "Falha na persistência de ingrediente"
    assert any(r["nome"] == "American Stout" for r in dados_recarregados["receitas"]), "Falha na persistência de receita"

    # Teste 7: Case-insensitivity
    print("\n=== Teste 7: Verificação case-insensitive ===")
    saida = capturar_saida(microcervejaria.remover_ingrediente, "levedura us-05")
    assert "removido" in saida.lower(), "Falha na remoção case-insensitive"
    
    # Teste 8: Listagem vazia
    print("\n=== Teste 8: Listagem de registros vazios ===")
    reiniciar_dados()
    saida = capturar_saida(microcervejaria.listar_ingredientes)
    assert "Nenhum ingrediente" in saida, "Falha na listagem vazia de ingredientes"
    
    saida = capturar_saida(microcervejaria.listar_receitas)
    assert "Nenhuma receita" in saida, "Falha na listagem vazia de receitas"

    # Teste 9: Atualização de quantidade
    print("\n=== Teste 9: Atualização de quantidade ===")
    microcervejaria.cadastrar_ingrediente("Malte Munich", "Fornecedor Z", 12.75, "06/2025", 100)

    # Atualiza a quantidade diretamente no objeto salvo
    for ingrediente in microcervejaria.dados["ingredientes"]:
        if ingrediente["nome"] == "Malte Munich":
            ingrediente["quantidade"] = 75
            break

    microcervejaria.salvar_dados(microcervejaria.dados)  # Garante a persistência

    # Recarrega dados do arquivo para verificar
    dados_recarregados = microcervejaria.carregar_dados()
    salvo = any(i["quantidade"] == 75 and i["nome"] == "Malte Munich" 
         for i in dados_recarregados["ingredientes"])

    assert salvo, "Falha na atualização de dados: Quantidade não persistiu corretamente"

    # Limpeza final
    reiniciar_dados()
    print("\n✅ Todos os testes foram concluídos com sucesso!")

if __name__ == "__main__":
    testar_crud()
    
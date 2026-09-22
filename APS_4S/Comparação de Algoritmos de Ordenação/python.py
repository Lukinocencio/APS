import os
caminho_arquivo = os.path.join(os.path.dirname(__file__), '1000_numbers.txt')

# Abre o arquivo selecionado e verifica  o conteúdo
with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
    for linha in arquivo:
        print(linha.strip())

input("\nPressione Enter para fechar...")
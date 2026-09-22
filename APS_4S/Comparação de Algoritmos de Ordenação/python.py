import os
caminho_arquivo = os.path.join(os.path.dirname(__file__), '1000_numbers.txt')

# Abre o arquivo selecionado e verifica  o conteúdo
with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
    for i in caminho_arquivo:
        leitura_linha = arquivo.readline()
        print("\n "+ leitura_linha)       
    #conteudo = arquivo.read()


#print(conteudo)
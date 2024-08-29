# Obtém o caminho do arquivo que será lido
caminho_arquivo = r'c:/wamp64/www/APS_1s_v1.0.0/1000_numbers.txt'

# Abre o arquivo selecionado e verifica  o conteúdo
with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
    for i in caminho_arquivo:
        leitura_linha = arquivo.readline()
        print("\n "+ leitura_linha)       
    #conteudo = arquivo.read()


#print(conteudo)
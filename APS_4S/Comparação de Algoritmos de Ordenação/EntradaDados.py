def Entrada():
    CaminhoArquivo = r'C:\wamp64\www\APS\1000_numbers.txt'
    LinhasArquivo = []
    with open(CaminhoArquivo, 'r', encoding='utf-8') as ArquivoTxt:
        for Linha in ArquivoTxt:
            LinhasArquivo.append(int(Linha.strip()))
        return LinhasArquivo
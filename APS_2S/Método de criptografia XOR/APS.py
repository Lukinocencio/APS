import random 
import string

#Declarando funções 

# Função para criptografar

def criptografar(texto, chave):
    criptografado = [] # lista que armazenda os bytes.
    for i in range(len(texto)):
        criptografado.append(texto[i] ^ chave[i % len(chave)]) 
        #Aqui ocorre a criptografia, onde sera comparado cada bit da mensagem inserida com cada bit da chave gerada usando a operação logica XOR, onde se os bits forem iguais,
        #temos resultado 0 e se forem diferentes resultado 1.
    return bytes(criptografado) #aqui ele devolve a lista em bytes.

import os

CHAVES_FILE = os.path.join(os.path.dirname(__file__), "chaves.txt")

# Função para gerar uma chave aleatoria e associar com uma chave 'string'

def criar_chave_aleatoria(nome_chave):
    random_key = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32)) #aqui eu uso a biblioteca random e a biblioteca string para pegar letras e digitos aleatorios para criar uma chave.
    chaves[nome_chave] = random_key.encode('utf-8') # aqui eu vou associar a chave gerada ao nome da chave inserido.
    salvar_chaves()

# Função para verificar e validar a chave 

def buscar_chave(nome_chave):
    if nome_chave in chaves:
        return chaves[nome_chave]
    try:
        return bytes.fromhex(nome_chave)
    except ValueError:
        return None
    
# Função que gera e salva as chaves em um arquivo '.txt'

def salvar_chaves():
    with open(CHAVES_FILE, "w") as arquivo: #aqui eu abro o arquivo com write para escrever a chave_input e a chave gerada em formato de dicionario.
        for chave_nome, chave in chaves.items():
            arquivo.write(f"{chave_nome}:{chave.hex()}\n")

# Dicionario criado para armazenar as chaves

chaves = {}

# Abrindo o arquivo para verificar se a chave existe

try:
    with open(CHAVES_FILE, "r") as arquivo: #aqui abre o arquivo em modo leitura
        linhas = arquivo.readlines() # aqui ele le as linha sdo arquivo 
        for linha in linhas: # aqui a gente percorre as linhas
            partes = linha.strip().split(":") # removemos os espaços e divide a mensagem usando :
            if len(partes) == 2: # aqui verificar se a chave esta separadas em 2 partes (nome:chavegerada)
                chave_nome, chave = partes
                chaves[chave_nome] = bytes.fromhex(chave)
except FileNotFoundError:
    pass

# Função para verificar se o codigo inserido é hexadecimal

def input_mensagem_cifrada_hex():
    while True:
        mensagem_cifrada_hex = input("Insira a frase criptografada em hexadecimal: ")
        if is_hexadecimal(mensagem_cifrada_hex):
            return mensagem_cifrada_hex
        else:
            print("O texto inserido não é um valor hexadecimal válido. Tente novamente.")

def is_hexadecimal(texto): # essa função é um comparador de hexadecimal.
    try:
        bytes.fromhex(texto)
        return True
    except ValueError:
        return False

# Funçaõ de descriptografia

def descriptografar(textocriptografado, chave):
    descriptografado = []
    for i in range(len(textocriptografado)):
        descriptografado.append(textocriptografado[i] ^ chave[i % len(chave)]) # O processo de descriptografia segue a mesma logica de criptografia, mas aqui eu vou comparar o hexadecimal criptografado com a chave salva.
    return bytes(descriptografado) 



while True:
    print("\nOpções:")
    print("1. Criptografar")
    print("2. Descriptografar")
    print("3. Criar Chave Aleatória")   # Menu usando while, enquanto o usuario nao digitar a função 5 o programa continuara funcioando.
    print("4. Verificar Chave")
    print("5. Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == '1':
        chave_nome = input("Nome da chave ou chave hexadecimal: ")  # pede a chave, ou seu respectivo hexadecimal gerado.
        chave = buscar_chave(chave_nome) #aqui ele usa a função declarada acima para buscar a chave inserida a cima no dicionario.

        if chave: # aqui é mais um verificador, caso a chave for encontrada o codigo abaixo ira criptografar.
            mensagem = input("Insira a frase que deseja criptografar: ") # input da mensagem a ser criptografada;
            if mensagem: # verifica se o usuario inseriu algo
                mensagem_bytes = mensagem.encode('utf-8') # variavel que recebe a mensagem e a transforma em bytes usando UTF-8
                mensagem_cifrada = criptografar(mensagem_bytes, chave) # variavel que vai executar a função de criptografia e receber os dados em bytes.
                print("Frase criptografada:", mensagem_cifrada.hex()) # aqui um print da variavel acima sendo mostrada em hexadecimal.
            else:
                print("Nenhuma frase inserida. Operação de criptografia cancelada.")
        else:
            print("Chave não encontrada ou inválida.")
    
    if opcao == '2':
        chave_nome = input("Nome da chave ou chave hexadecimal: ") #faz o mesmo processo da criptografia, pede a chave e depois busca no dicionario.
        chave = buscar_chave(chave_nome)
        if chave: #caso a chave existe o codigo abaixo descriptografa
            mensagem_cifrada_hex = input_mensagem_cifrada_hex() #aqui ele usa a função declarada acima para verificar se é um hexadecimal 
            mensagem_cifrada = bytes.fromhex(mensagem_cifrada_hex) #aqui ele pega nossa mensagem hexadecimal a cima e a converte em bytes.
            mensagem_decifrada = descriptografar(mensagem_cifrada, chave) # aqui usamos nossa função declarada e fazemos o processo de descriptografia 
            print("Frase descriptografada:", mensagem_decifrada.decode('utf-8', errors='ignore')) # nessa função apresentamos a mensagem descriptografada e a decodifica os bytes usando UTF-8
        else:
            print("Chave não encontrada ou inválida.")
        

    elif opcao == '3':
        chave_nome = input("Nome da nova chave: ")  # Input para uma chave nova
        if chave_nome not in chaves: # verificador de chave, caso existe uma chave com nome igual.
            criar_chave_aleatoria(chave_nome) #executa a função declarada acima.
            print("Chave aleatória gerada e associada a", chave_nome)
        else:
            print("Já existe uma chave com esse nome.")

    elif opcao == '4':
        chave_nome = input("Digite o nome da chave para verificar: ") #input para verificar a chaves existentes 
        if chave_nome in chaves: # verifica se a chave esta no dicionario
            chave_bytes = chaves[chave_nome]
            print(f"Chave associada a {chave_nome}:{chave_bytes.hex()}") # mostra a chave e seu hex.
        else:
            print("Chave não encontrada.")

    elif opcao == '5': # encerra o programa
        break
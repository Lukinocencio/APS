# Repositório de APS - Ciência da Computação

Bem-vindo ao repositório consolidado dos projetos das Atividades Práticas Supervisionadas (APS) do curso de Ciência da Computação. Este repositório está organizado cronologicamente por semestres (APS_1S até APS_8S) e aborda diversas tecnologias, paradigmas de programação e resoluções de problemas.

## Índice
1. [APS_1S - Transporte Sustentável no Vale do Paraíba](#aps_1s---transporte-sustentável-no-vale-do-paraíba)
2. [APS_2S - Método de Criptografia XOR](#aps_2s---método-de-criptografia-xor)
3. [APS_3S - Calculadora de Painel Solar](#aps_3s---calculadora-de-painel-solar)
4. [APS_4S - Comparação de Algoritmos de Ordenação](#aps_4s---comparação-de-algoritmos-de-ordenação)
5. [APS_5S - Chat Criptografado Cliente/Servidor](#aps_5s---chat-criptografado-clienteservidor)
6. [APS_6S - Sistema de Reconhecimento Facial/Biometria](#aps_6s---sistema-de-reconhecimento-facialbiometria)
7. [APS_7S - Arquitetura Blockchain para Registro Veicular](#aps_7s---arquitetura-blockchain-para-registro-veicular)
8. [APS_8S - Reservado](#aps_8s---reservado)

---

### APS_1S - Transporte Sustentável no Vale do Paraíba
**Linguagens:** HTML5, CSS3

**Descrição:** 
Uma aplicação web estática que aborda os conceitos de mobilidade urbana e sustentabilidade aplicados na região do Vale do Paraíba, São Paulo. A interface apresenta seções de acessibilidade, sustentabilidade e informações tarifárias, incentivando o uso de transporte público eficiente.

**Como executar:**
Abra o arquivo `index.html` em qualquer navegador web moderno. Não há dependências de backend ou servidores locais.

---

### APS_2S - Método de Criptografia XOR
**Linguagens:** Python

**Descrição:**
Programa em Python operando em linha de comando (CLI) que demonstra os conceitos fundamentais de criptografia utilizando o operador lógico XOR (Ou Exclusivo). O software permite gerar chaves aleatórias, criptografar mensagens de texto para hexadecimal e descriptografar arquivos cifrados salvando as chaves em um dicionário de acesso rápido (`chaves.txt`).

**Como executar:**
Abra o terminal no diretório da APS 2S e execute o script principal:
```bash
python APS.py
```

---

### APS_3S - Calculadora de Painel Solar
**Linguagens:** Java (Swing)

**Descrição:**
Aplicativo com Interface Gráfica de Usuário (GUI) construído em Java puro (Swing) que calcula o retorno do investimento, número de placas necessárias e dimensionamento de consumo (comercial/residencial) para a implantação de painéis solares em unidades consumidoras, com base na incidência solar.

**Como executar:**
Compile o código na raiz do pacote `calculo`:
```bash
javac -d . *.java
java calculo.Interface
```

---

### APS_4S - Comparação de Algoritmos de Ordenação
**Linguagens:** Python

**Descrição:**
Projeto focado em Estrutura de Dados e Análise de Algoritmos. O código importa *datasets* de diferentes tamanhos (1.000, 5.000 e 10.000 números) para testar e comparar a eficiência empírica dos algoritmos de ordenação `Insertion Sort`, `Binary Insertion Sort` e `Merge Sort`.

**Como executar:**
Abra o terminal no diretório e execute o analisador:
```bash
python python.py
```

---

### APS_5S - Chat Criptografado Cliente/Servidor
**Linguagens:** Python (Bibliotecas: `socket`, `threading`, `tkinter`, `cryptography`)

**Descrição:**
Um sistema de comunicação cliente-servidor assíncrono com interface gráfica (GUI). O software utiliza _sockets Berkeley_ para gerenciar a transmissão de dados em rede de forma não bloqueante com _threads_. A segurança é garantida pela biblioteca `Fernet` (baseada no padrão AES-128), criptografando a comunicação ponta a ponta para preservar a confidencialidade das mensagens. 

**Como executar:**
1. Instale as dependências caso ainda não o tenha feito:
```bash
pip install cryptography
```
2. Inicialize o servidor em um terminal:
```bash
python server.py
```
3. Em outra janela (ou em computadores distintos da rede local), execute os clientes e aponte para o IP gerado pelo servidor:
```bash
python client.py
```

---

### APS_6S - Sistema de Reconhecimento Facial/Biometria
**Linguagens:** Python (Bibliotecas: `customtkinter`, `opencv-python`, `sqlalchemy`)

**Descrição:**
Aplicação com arquitetura MVC focada em biometria e controle de acesso restrito. Faz a identificação e o cadastro facial de usuários salvando *features* através de redes neurais com suporte da OpenCV. O sistema controla fluxos logísticos e valida níveis hierárquicos para o acesso de documentações sigilosas do banco de dados relacional.

**Como executar:**
1. Instale as dependências recomendadas utilizando o arquivo requirements ou via `pip`:
```bash
pip install customtkinter opencv-python sqlalchemy
```
2. Inicialize a aplicação:
```bash
python main.py
```

---

### APS_7S - Arquitetura Blockchain para Registro Veicular
**Descrição:**
Trabalho acadêmico e modelagem (UML e Diagramas de Fluxo) para solucionar problemas de clonagem veicular no Brasil usando redes descentralizadas. A documentação (`DocumentoAPS.pdf`) abrange o uso teórico da *Hyperledger Fabric* e de Contratos Inteligentes (*Chaincodes*). (Apenas documentação analítica).

---

### APS_8S - Reservado
**Descrição:**
Diretório reservado para o projeto prático do 8º Semestre (Vazio atualmente).

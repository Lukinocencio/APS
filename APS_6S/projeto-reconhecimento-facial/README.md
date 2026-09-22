# Sistema de Reconhecimento Facial

## Bibliotecas Necessárias

Instale os seguintes pacotes Python antes de rodar o sistema:

```
pip install pillow opencv-python opencv-contrib-python sqlalchemy customtkinter pymupdf python-docx
```

- **pillow**: Manipulação de imagens (PIL)
- **opencv-python**: Processamento de imagens e vídeo
- **opencv-contrib-python**: Algoritmos extras do OpenCV (LBPH)
- **sqlalchemy**: ORM para banco de dados SQLite
- **customtkinter**: Interface gráfica moderna
- **pymupdf**: Leitura de arquivos PDF
- **python-docx**: Leitura de arquivos DOCX

## Estrutura do Projeto

- `main.py`: Ponto de entrada. Inicializa banco de dados, interface e controlador principal.
- `controller.py`: Gerencia navegação entre telas e lógica global.
- `core/`: Lógica de reconhecimento facial (`logica.py`) e manipulação de documentos (`logica_documentos.py`).
- `database/`: Modelos ORM (`models.py`) e setup do banco (`setup.py`).
- `interface/`: Telas de login, cadastro e principal (CustomTkinter).
- `assets/`: Arquivos de apoio (classificador Haar, vídeo de teste, dataset de imagens, modelo treinado).
- `arquivos_gerenciados/`: Documentos salvos pelo sistema.

## Funcionamento Geral

1. **Login e Cadastro**
   - Usuário pode se cadastrar informando nome, CPF e nível de acesso.
   - Durante o cadastro, o sistema captura automaticamente 30 fotos do rosto para treinar o modelo biométrico.
   - Após cadastro, o modelo é treinado e o usuário pode acessar o sistema via reconhecimento facial.

2. **Reconhecimento Facial**
   - O sistema utiliza OpenCV (LBPH) para identificar o usuário pela webcam ou vídeo de teste.
   - O modelo é treinado com as imagens capturadas e salvo em `assets/trainer/trainer.yml`.
   - O acesso é concedido se o rosto for reconhecido com confiança suficiente.

3. **Gestão de Documentos**
   - Usuários podem visualizar, criar, editar e deletar documentos conforme seu nível de acesso.
   - Documentos suportados: PDF, DOCX, TXT, imagens (PNG, JPG, etc).
   - Os arquivos são salvos em `arquivos_gerenciados/` e registrados no banco de dados.
   - Permissões são controladas por níveis: Ministro, Diretor, Servidor.

4. **Banco de Dados**
   - Utiliza SQLite, gerenciado via SQLAlchemy.
   - Tabelas: `usuarios` (dados pessoais, nível de acesso), `documentos` (metadados e permissões).

## Fluxo Resumido

- Cadastro → Captura de fotos → Treinamento do modelo → Login por biometria → Acesso à tela principal → Gestão de documentos conforme permissões.

## Observações

- O sistema pode ser executado em modo simulação (usando vídeo de teste) ou com webcam real.
- Todos os diretórios necessários são criados automaticamente.
- Para rodar, basta executar:

```
python main.py
```

## Requisitos Adicionais

- Python 3.10 ou superior recomendado.
- Sistema testado no Windows.

---

Para dúvidas sobre funcionamento ou extensões, consulte os arquivos de código e as docstrings explicativas.

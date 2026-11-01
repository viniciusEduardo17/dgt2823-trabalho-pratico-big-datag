# DGT2823 — Trabalho Prático: Tecnologias para Desenvolvimento de Soluções de Big Data

**Projeto completo em Python e Pandas**, desenvolvido a partir do roteiro de 10 páginas fornecido para a disciplina DGT2823. Contém o conjunto de dados obrigatório, as cinco microatividades, o tratamento final exigido, um notebook executável, exportações, documentação e testes automatizados.

## Resultado validado

| Indicador | Resultado |
|---|---:|
| Registros no CSV original | **32** |
| Colunas | **6** |
| Registros sem calorias | **2** (IDs 18 e 28) |
| Registros sem data | **1** (ID 22) |
| Data irregular corrigida | **ID 26: 20201226 → 2020/12/26** |
| Registros excluídos | **1** (ID 22) |
| Registros no CSV tratado | **31** |
| Valores nulos no CSV tratado | **0** |

## Como executar (Windows, sem Docker)

**Opção rápida:** com o Python instalado, dê dois cliques em `executar_windows.bat`. O arquivo cria um ambiente virtual, instala o Pandas e executa o projeto, sem Docker. Se preferir usar o terminal, siga os comandos abaixo.

Pré-requisito: **Python 3.10 ou superior** com `pip` instalado.

1. Baixe o projeto ZIP e extraia a pasta (ou clone o repositório).
2. Abra o terminal **na pasta do projeto** (aquela que contém `main.py`).
3. Execute os comandos a seguir:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

Se o PowerShell bloquear a ativação, use `.venv\Scripts\python.exe -m pip install -r requirements.txt` e `.venv\Scripts\python.exe main.py` sem ativar o ambiente. No Prompt de Comando (CMD), a ativação é `.venv\Scripts\activate.bat`.

**Alternativa macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

Ao executar, o programa exibe a análise da base original e cada etapa da limpeza. Os resultados são gravados automaticamente em:

- `resultados/dados_tratados.csv` — dados prontos, separados por `;`.
- `resultados/relatorio_execucao.txt` — resumo textual dos resultados.

Para uma saída mais curta no terminal, execute `python main.py --resumido`.

## Notebook Jupyter com respostas às cinco microatividades

Inicie o ambiente Jupyter na pasta do projeto:

```bash
python -m jupyterlab
```

No navegador, abra `notebooks/trabalho_pratico_dgt2823.ipynb` e selecione **Run / Run All Cells** (executar todas as células). O notebook inclui explicações, código e saídas já executadas para facilitar a revisão.

**Google Colab:** carregue a pasta do projeto para o ambiente do Colab (por exemplo, faça upload do ZIP, extraia com `!unzip`, entre na pasta com `%cd` e abra ou copie o notebook). O CSV precisa estar disponível junto à estrutura `data/`, como fornecido neste ZIP.

## Testes automatizados

```bash
python -m pytest -q
```

Os testes verificam o arquivo original, o preenchimento de calorias, o tratamento das datas, a exclusão exata do registro sem data, a integridade dos outros valores e a geração dos artefatos. O projeto também vem com um workflow de testes do GitHub Actions.

## Estrutura dos arquivos

```text
dgt2823-trabalho-pratico-big-data/
├── main.py                        # Executa todas as transformações
├── executar_windows.bat          # Iniciar no Windows com dois cliques
├── src/
│   ├── __init__.py
│   └── tratamento.py               # Leitura, limpeza e relatório
├── data/
│   └── dados_originais.csv        # Base obrigatória do enunciado
├── notebooks/
│   └── trabalho_pratico_dgt2823.ipynb  # 5 microatividades + trabalho prático
├── resultados/
│   ├── dados_tratados.csv         # Saída pronta, também recriada na execução
│   └── relatorio_execucao.txt     # Relatório pronto, também recriado na execução
├── docs/
│   └── RELATORIO_TECNICO.md      # Relatório técnico em Markdown
├── tests/
│   └── test_tratamento.py         # Testes automatizados
├── .github/workflows/testes.yml  # Pipeline de testes no GitHub
├── requirements.txt
├── .gitignore
└── README.md
```

## Cobertura do roteiro

| Requisito do PDF | Local da implementação |
|---|---|
| Microatividade 1: `read_csv` | Notebook, seção 1; `src/tratamento.py: ler_dados()` |
| Microatividade 2: subconjunto com três colunas | Notebook, seção 2 |
| Microatividade 3: `display.max_rows = 9999` e `to_string()` | Notebook, seção 3; rotina `executar_tratamento()` |
| Microatividade 4: `head(10)` e `tail(10)` | Notebook, seção 4 |
| Microatividade 5: `info()`, nulos, tipos e memória | Notebook, seção 5; `resumo_dataframe()` |
| Trabalho Prático, passos 1 a 13 | Notebook, seção 6; `tratar_dados()`; `main.py` |
| Entrega por repositório Git público | Repositório público publicado e GitHub Actions |

## Informações importantes sobre a fonte

O PDF de origem apresenta uma **quebra visual na passagem do ID 20 para o ID 21**: o dígito `2` aparece ao final da linha do ID 20 e o `1` no início da seguinte. No CSV, o registro foi recomposto como `21;60;'2020/12/21';108;131;3642`, e as calorias do ID 20 foram mantidas em `2430`.

O enunciado também diz que a data temporária `1900/01/01` causaria erro de conversão com `%Y/%m/%d`. Na prática, essa data **é válida para esse formato**; a remoção do marcador foi mantida porque o roteiro a exige. O CSV contém ainda **aspas simples como caracteres** nas datas, exigindo removê-las antes da conversão. A outra data problemática é `20201226`, corrigida especificamente como requerido.

Outras ocorrências, como `Duration=450` (ID 7), data repetida (IDs 11 e 12) e `Pulse > Maxpulse` (ID 23), **foram preservadas** porque sua modificação não é exigida no trabalho.

## Repositório público para a entrega

O projeto já está publicado na conta GitHub do aluno:

**https://github.com/viniciusEduardo17/dgt2823-trabalho-pratico-big-datag**

Compartilhe esse endereço com o tutor na Sala de Aula Virtual, na aba Trabalhos.

> O projeto não requer Docker, banco de dados ou conexão à internet para executar após a instalação das dependências.
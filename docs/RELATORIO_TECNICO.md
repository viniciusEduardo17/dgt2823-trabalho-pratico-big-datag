# Relatório técnico — Trabalho Prático DGT2823

**Disciplina:** Tecnologias para Desenvolvimento de Soluções de Big Data  
**Tecnologia:** Python + Pandas

## Fonte dos dados
O CSV obrigatório é transcrito do PDF com as colunas ID, Duration, Date, Pulse, Maxpulse e Calories, separadas por ponto e vírgula. São 32 registros. As calorias dos IDs 18 e 28 estão ausentes e a data do ID 22 é nula. A data do ID 26 aparece como 20201226. A linha 21 foi recomposta de uma quebra de formatação do PDF.

## Cinco microatividades
1. Leitura do CSV com pandas.read_csv e separador ';', engine='python', encoding='utf-8'.
2. Criação do subconjunto de três colunas ID, Date e Calories.
3. Configuração de display.max_rows=9999 e exibição com to_string.
4. Visualização com head(10) e tail(10).
5. Consulta com info(), isna().sum(), dtypes e memory_usage().

As cinco etapas estão demonstradas no notebook notebooks/trabalho_pratico_dgt2823.ipynb.

## Trabalho prático — limpeza dos dados
1. Ler a base original e apresentar as estatísticas iniciais.
2. Criar uma cópia independente para tratamento.
3. Substituir por zero as calorias ausentes nos IDs 18 e 28.
4. Preencher provisoriamente a data nula do ID 22 com 1900/01/01.
5. Trocar essa data artificial por valor ausente e retirar aspas extras da transcrição.
6. Corrigir especificamente a data 20201226 para 2020/12/26.
7. Converter as datas com pandas.to_datetime usando formato %Y/%m/%d.
8. Excluir o único registro que permaneceu sem data, ID 22.
9. Exportar resultados/dados_tratados.csv e resultados/relatorio_execucao.txt.

## Indicadores
| Indicador | Antes | Depois |
|---|---:|---:|
| Registros | 32 | 31 |
| Colunas | 6 | 6 |
| Datas nulas | 1 | 0 |
| Calorias nulas | 2 | 0 |
| Total de valores nulos | 3 | 0 |

A data 1900/01/01 é compatível com %Y/%m/%d, apesar da interpretação sugerida no roteiro. Ela é removida como marcador artificial. Os dados inconsistentes não abrangidos pela tarefa — Duration=450 no ID 7, duplicidade dos IDs 11 e 12 e Pulse>Maxpulse no ID 23 — foram mantidos.

## Como verificar
Instale as dependências com python -m pip install -r requirements.txt, execute python main.py e rode python -m pytest -q. O arquivo .github/workflows/testes.yml também executa a validação no GitHub Actions.

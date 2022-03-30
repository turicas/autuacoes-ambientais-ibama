# Extrator de PDFs de Autuações Ambientais do IBAMA

Esse script baixa, converte e limpa [arquivos PDFs de autuações ambientais
gerados pelo
IBAMA](https://servicos.ibama.gov.br/ctf/publico/areasembargadas/ConsultaPublicaAreasEmbargadas.php).
O resultado é exportado para CSV.

Metodologia:
- Para cada estado brasileiro:
  - acessa o site do IBAMA (linkar form)
  - preenche o estado
  - para cada ano desde 1980 ao ano atual:
    - preenche data de início/fim
    - baixa e salva o PDF (estado/ano)
    - extrai os dados do PDF e converte para CSV
- Criei um programa que acessa a página https://servicos.ibama.gov.br/ctf/publico/areasembargadas/ConsultaPublicaAreasEmbargadas.php e então:
- Na parte "Consulta Pública", marca "autuações ambientais"
- Na parte "Dados da Infração", seleciona um dos estados (o programa pode passar por todos os estados - mas esse caso, só fiz para o PA)
- Preenche o período de 01/01/ANO até 31/12/ANO, onde "ANO" varia de 1980 a 2021 (o programa roda uma vez para cada ano possível, porque o máximo permitido é 1 ano)- Baixa o PDF resultante da busca- Converte o PDF para CSV- Limpa o arquivo CSV (corrige nomes de municípios, adiciona código IBGE dos municípios etc.)


## Instalando

Testado em Python 3.9.5 (pode funcionar em outras versões, mas não é
garantido).

```bash
pip install -r requirements.txt
```

## Utilização

apenas extrair
baixar e extrair


```bash
time python -m autuacoes.spider data/download/ data/output/autuacao.csv.gz
```

01/janeiro a 31/dez

- `--log-level`: nível de logging do script (padrão: INFO)
- `--start-year`: ano inicial do download (padrão: 1980)
- `--end-year`: ano final (padrão: ano atual)


## Extrator

em CSVs, utilizando o algoritmo `rects-boundaries` da extração de PDFs da
biblioteca [rows](https://github.com/turicas/rows).

```bash
python -m autuacoes.parser arquivo.pdf arquivo.csv
```

Você pode utilizar o arquivo que vem com esse repositório como exemplo (como
são 64 páginas, irá demorar em torno de 1min35s):

```bash
time python -m autuacoes.parser data/amazonas-2010.pdf data/amazonas-2010.csv
```

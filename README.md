# Extrator de PDFs de Autuações Ambientais do IBAMA

Esse script converte [arquivos PDFs de autuações ambientais gerados pelo
IBAMA](https://servicos.ibama.gov.br/ctf/publico/areasembargadas/ConsultaPublicaAreasEmbargadas.php)
em CSVs, utilizando o algoritmo `rects-boundaries` da extração de PDFs da
biblioteca [rows](https://github.com/turicas/rows).

## Instalando

```bash
pip install -r requirements.txt
```

## Rodando

```bash
python extrair.py arquivo.pdf arquivo.csv
```

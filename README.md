# Gimimo Relatórios

Análise de dados de vendas da **Gimimo**, uma loja de e-commerce que vende kits de bótons e pins temáticos de bandas de rock, operando pela Shopee e gerenciada pelo Tiny ERP.

Os relatórios são exportados manualmente do Tiny ERP em formato CSV e processados com Python para gerar análises e visualizações.

## Análises disponíveis

### `vendas.py` — Análise de Clientes
- Consolidação de múltiplos relatórios de vendas
- Limpeza e separação de nome e CPF
- Ranking dos maiores compradores por valor total
- Cálculo de faturamento total e ticket médio
- Gráfico de barras com top 10 clientes
- Exportação para Excel

### `faturamento.py` — Evolução Mensal
- Leitura de relatórios de evolução de faturamento por período
- Agrupamento e soma por mês
- Gráfico de linha com evolução do faturamento ao longo do tempo
- Exportação para Excel

### `produtos.py` — Análise de Produtos
- Consolidação de relatórios de notas fiscais por produto
- Limpeza dos nomes de produto (remoção de descrições longas do marketplace)
- Ranking por receita gerada
- Ranking por quantidade vendida
- Dois gráficos de barras comparativos
- Exportação para Excel

## Estrutura do projeto

```
gimimo_relatorios/
├── vendas.py
├── faturamento.py
├── produtos.py
├── clientes/        # CSVs de relatório de vendas por cliente
├── evolucao/        # CSVs de evolução de faturamento mensal
└── produtos/        # CSVs de notas fiscais por produto
```

## Tecnologias utilizadas

- Python 3.14
- pandas
- matplotlib
- glob

## Como usar

1. Clone o repositório
2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   ```
3. Instale as dependências:
   ```bash
   pip install pandas matplotlib openpyxl
   ```
4. Exporte os relatórios do Tiny ERP em formato CSV e coloque nas pastas correspondentes
5. Execute o script desejado:
   ```bash
   python vendas.py
   python faturamento.py
   python produtos.py
   ```

## Autor

Igor

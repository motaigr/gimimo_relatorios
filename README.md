# Gimimo Relatórios

Análise de dados de vendas da **Gimimo**, uma loja de e-commerce que vende kits de bótons e pins temáticos de bandas de rock, operando pela Shopee e gerenciada pelo Tiny ERP.

Os relatórios são exportados manualmente do Tiny ERP em formato CSV e processados com Python para gerar análises e visualizações.

## Análises disponíveis

### `dashboard.py` — Dashboard Interativo
- Dashboard web com todas as análises consolidadas
- Métricas de faturamento total, pedidos e ticket médio
- Gráfico de evolução do faturamento mensal
- Ranking dos top 10 clientes por faturamento
- Ranking dos top 10 produtos por receita e por quantidade
- Atualização automática ao adicionar novos CSVs

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
├── dashboard.py
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
- streamlit
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
   python -m pip install pandas matplotlib openpyxl streamlit
   ```
4. Exporte os relatórios do Tiny ERP em formato CSV e coloque nas pastas correspondentes

5. Para rodar o dashboard:
   ```bash
   python -m streamlit run dashboard.py
   ```

6. Para rodar os scripts individuais:
   ```bash
   python vendas.py
   python faturamento.py
   python produtos.py
   ```

## Dashboard Online

Acesse o dashboard em tempo real:
[gimimorelatorios-dashboard.streamlit.app](https://gimimorelatorios-dashboard.streamlit.app)

## Autor

Igor

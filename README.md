# Sprint4-Dynamic_Programming
#(Programação Dinâmica aplicada ao SupplyFlow)

---

## O que foi adicionado

1. **Formulação do problema — Reposição Ótima**
   Modelamos a decisão de reposição como um problema de Programação Dinâmica no estilo “lote econômico com horizonte finito” para **minimizar o custo total** de pedidos + estocagem, dado um intervalo de `n` dias e uma previsão simples de demanda por dia.

* **Estados (`t`)**: o “próximo dia a atender” no horizonte, com `t ∈ {0,…,n}`.
* **Decisões (`r`)**: quantos dias *consecutivos* a partir de `t` serão cobertos por **um único pedido** feito no dia `t` (limite superior `L`).
* **Função de transição**: escolher `r` implica avançar de `t` para `t + r`.
* **Função objetivo**:
  [
  f(t) \;=\; \min_{1 \le r \le \min(L, n-t)} \Big[\, K \;+\; \text{hold_cost}(d, t, r, h) \;+\; f(t+r) \Big]
  ]
  com condição de contorno ( f(n) = 0 ).
  *Onde*:

  * `K` = custo fixo por pedido;
  * `h` = custo de manutenção (carregamento) por unidade-dia;
  * `d[i]` = demanda prevista no dia `i`;
  * `hold_cost(d, t, r, h) = \sum_{j=0}^{r-1} h \\cdot j \\cdot d[t+j]` (o que é pedido para o dia `t+j` fica estocado `j` dias).

2. **Duas versões da solução**

* **Recursiva com memoização**: `dp_reposicao_rec_memo(d, K, h, L)`
  Implementada com cache (decorator `lru_cache`) para guardar `f(t)` e evitar recomputações exponenciais.
* **Iterativa bottom-up**: `dp_reposicao_bottom_up(d, K, h, L)`
  Preenche um vetor `dp[t]` de trás para frente e um vetor `choice[t]` para reconstruir o plano ótimo.

3. **Garantia de resultados idênticos**
   A função `plano_dp_para_insumo(...)` executa **as duas versões**, compara **custo mínimo** e **plano** (`ok = (c1 == c2 and p1 == p2)`) e **alerta** se houver divergência (não esperado). Assim atendemos ao critério “ambas produzem os mesmos resultados”.

4. **Integração no fluxo da aplicação**
   Quando a **Checagem Periódica** detecta itens críticos (≤ 50 unidades), o sistema:

* gera uma **previsão simples de demanda** via média do histórico (`prever_demanda`), com *fallback* para 5% do estoque atual;
* calcula o **plano ótimo de reposição** com PD;
* exibe o plano já formatado no modal da checagem.

> **Onde encontrar no código**:
> `SistemaEstoque._hold_cost`, `SistemaEstoque.dp_reposicao_rec_memo`, `SistemaEstoque.dp_reposicao_bottom_up`, `SistemaEstoque.prever_demanda`, `SistemaEstoque.plano_dp_para_insumo` e a chamada dentro de `SistemaEstoque.checagemPeriodica`.

---

## Complexidade e observações

* **Complexidade temporal**: (O(n \cdot L)) nas duas abordagens (cada estado `t` testa até `L` alcances).
* **Espaço**: (O(n)) para `dp`/`choice` (bottom-up) e cache de `f(t)` (memoização).
* **Parâmetros**: `K`, `h`, `L` e `dias` são ajustáveis em `plano_dp_para_insumo`.
* **Pré-requisito**: uma previsão `d` coerente com a realidade (o modelo é tão bom quanto a demanda prevista).

---

## Outras técnicas estruturais já presentes da ultima entrega:

* **Filas e Pilhas**: saídas registradas em **FIFO** (`fila_consumo`) e **LIFO** (`pilha_consumo`) para visualizações cronológica e inversa.
* **Buscas**: **sequencial** e **binária** sobre a lista de nomes (mantida ordenada).
* **Ordenações**: **Merge Sort** para nomes e **Quick Sort** por quantidade ao exibir estoques.

---

## Como usar (rápido)

1. Rode o script e abra a **Checagem Periódica**.
2. Se houver itens críticos, o sistema mostra, para cada um, **quando pedir** e **quanto pedir** para cobrir `r` dias ao menor custo estimado.
3. Pode-se ajustar `K`, `h`, `L` e o **horizonte de dias** conforme a realidade da unidade.

---

## Participantes — Sala 2ESPx

* **Carlos Henrique** — RM558003
* **Mauricio Alves** — RM556214
* **Ian Monteiro** — RM558652
* **Bruno Silva** — RM550416
* **João Hoffmann** — RM550763



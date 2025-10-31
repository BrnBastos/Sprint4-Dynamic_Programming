# Sprint4-Dynamic_Programming
#(Programação Dinâmica aplicada ao SupplyFlow)

A ideia desse readme é explicar de forma simples **o que fizemos**, **como funciona** e **como usar**. Escrevemos como explicaríamos para colegas de sala.

Fizemos os novos requisitos implementados ao projeto da última sprint

---

## 1) Resumo rápido

Nesta sprint **colocamos** uma lógica de **Programação Dinâmica (PD)** para decidir **quando** fazer pedidos de reposição e **quanto** pedir de cada insumo. O objetivo é **gastar menos** somando o custo do pedido com o custo de deixar itens parados no estoque.

* **K** = custo fixo de cada pedido.
* **h** = custo por **unidade por dia** guardada.
* **d[i]** = demanda prevista no dia `i` (usamos uma previsão simples).

Tudo isso roda dentro do sistema que já existia (estoque, prateleiras, buscas, etc.).

## 2) Como **pensamos** o problema (sem fórmula)

* **Estado (t)**: qual é o **dia** do planejamento que ainda precisamos atender.
* **Decisão (r)**: se fizermos **um pedido hoje**, por **quantos dias seguidos** ele vai cobrir (ex.: 3 dias)?
* **Transição**: se cobrimos 3 dias, pulamos de `t` para `t+3` e continuamos.
* **Objetivo**: escolher os `r` de cada passo para **dar o menor custo total** até o fim do período.

Em outras palavras: a cada dia escolhemos “cobrimos 1, 2, 3… dias de uma vez?”, pagamos o custo, e queremos terminar o planejamento **pagando o mínimo possível**.

---

## 3) Dois jeitos de resolver (usamos os dois)

1. **Recursivo com memoização**

   * A função chama ela mesma e **guarda resultados** já calculados para não repetir conta.
2. **Iterativo (bottom‑up)**

   * Monta uma tabela de trás pra frente (`dp`) e **guarda a melhor escolha** em cada dia.

> **Importante:** no nosso código **rodamos os dois** e comparamos. Se der qualquer diferença (não é esperado), aparece um aviso. Na tela da checagem também mostramos **qual método** foi usado e podemos imprimir os **dois planos lado a lado**.

## 4) O que aparece na Checagem Periódica

Quando clicamos em **Checagem Periódica**:

1. O sistema marca como **crítico** quem está com **≤ 50 unidades**.
2. Para cada item crítico, fazemos uma **previsão simples** de demanda (média do histórico; se não tiver histórico, usamos 5% do estoque atual como chute inicial).
3. Rodamos a PD e **mostramos o plano de pedidos** (dia e quantidade).
4. Escrevemos **qual método** foi usado e podemos imprimir **Iterativo** e **Recursivo** com os custos e os passos.

Exemplo que aparece no modal:

```text
— Sugestões de Reposição (Programação Dinâmica) —
DP para 'Frascos de Vidro' (dias=7, K=50, h=1, L=5)
• Iterativa (bottom-up): custo mínimo = 118
   - pedir no dia 0 cobrindo 3 dias → qty=6
   - pedir no dia 3 cobrindo 4 dias → qty=8
• Recursiva (memoização): custo mínimo = 118
   - pedir no dia 0 cobrindo 3 dias → qty=6
   - pedir no dia 3 cobrindo 4 dias → qty=8
⇒ Métodos consistentes: SIM
```

## 5) Como usar

1. **Rodar o script** normalmente (Python) e abrir a janela.
2. Clicar em **Checagem Periódica**.
3. Ver os itens críticos e o **plano de pedidos** para cada um.

Dica: se quisermos começar já forçando o método **recursivo** (ou o **iterativo**), dá para mudar uma variável no código antes de rodar. Também existe uma versão com **seletor** na interface para trocar o método na hora.

## 6) Onde **ajustamos** os números (K, h, L, dias)

No código, dentro das funções de plano/checagem, podemos mudar:

* **K**: custo fixo do pedido
* **h**: custo de manter em estoque por unidade/dia
* **L**: quantos dias no máximo um único pedido pode cobrir
* **dias**: tamanho do horizonte de planejamento (ex.: 7 dias)

Esses valores mudam o plano e servem para testar cenários diferentes.


## 7) O que já tinha da entrega anterior

* **Fila (FIFO)** e **Pilha (LIFO)** para registrar/visualizar saídas.
* **Buscas**: sequencial e binária para achar insumos rapidamente.
* **Ordenações**: Merge Sort (por nome) e Quick Sort (por quantidade) para listar o estoque organizado.


## 8) Limitações e ideias

* A previsão de demanda é **bem simples**. Se a demanda real for bem diferente, o plano pode não ser o ideal. Podemos melhorar isso depois.
* Os custos `K` e `h` podem mudar conforme o lugar. Vale testar valores realistas.

## Participantes — Sala 2ESPX

* **Carlos Henrique** — RM558003
* **Mauricio Alves** — RM556214
* **Ian Monteiro** — RM558652
* **Bruno Silva** — RM550416
* **João Hoffmann** — RM550763



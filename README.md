# Sprint4-Dynamic_Programming
# Como cada estrutura/algoritmo foi usado no contexto do problema

## Contexto rápido

Nas unidades de diagnóstico, precisamos registrar e consultar **consumo diário de insumos** (reagentes/descartáveis) e **organizar o estoque**. A solução usa estruturas clássicas para dar conta de três cenários: registrar eventos em ordem, consultar rapidamente se um item existe e ordenar listas para visualização/gestão.

---

## Fila (FIFO)

**Onde:** `SistemaEstoque.fila_consumo` (tipo `deque`).
**Quando é usada:** toda vez que há retirada de um insumo (`retirar_insumo` → `_registrar_consumo_evento`).
**Para quê:** manter o **histórico cronológico** dos consumos. Assim, conseguimos ver “o que saiu” **na ordem em que aconteceu**, que é o que o requisito pede para uma fila (primeiro que entra, primeiro que sai).
**Como aparece para o usuário:** em **“Consultar histórico”**, a seção *Fila (FIFO)* lista os eventos na **ordem do dia/hora**.

---

## Pilha (LIFO)

**Onde:** `SistemaEstoque.pilha_consumo` (lista).
**Quando é usada:** nos mesmos eventos de retirada, em `_registrar_consumo_evento`.
**Para quê:** permitir consultas que priorizam **os últimos consumos** – útil para conferir **o que acabou de sair** (ex.: auditoria rápida ou erro de lançamento).
**Como aparece para o usuário:** em **“Consultar histórico”**, a seção *Pilha (LIFO)* mostra os eventos do **mais recente para o mais antigo**.

---

## Busca Sequencial

**Onde:** `SistemaEstoque.busca_sequencial`.
**Quando é usada:** em `buscar_insumo`, junto com a binária (redundância intencional para cumprir o requisito e comparar abordagens).
**Para quê:** é a forma mais simples de **procurar nome a nome**. Em listas curtas ou para fins didáticos, ela é suficiente.
**Observação:** custo linear (cresce conforme a lista), por isso é bom ter também a busca binária.

---

## Busca Binária

**Onde:** `SistemaEstoque.busca_binaria`.
**Pré‑requisito:** a lista de nomes **precisa estar ordenada**.
**Como garantimos isso:** sempre que um novo insumo é cadastrado, a lista global de nomes é reordenada via **Merge Sort** (`merge_sort`).
**Quando é usada:** em `buscar_insumo` para **localizar rapidamente** se o item existe.
**Benefício:** muito mais rápida em listas médias/grandes do que a sequencial.

---

## Ordenação por Merge Sort (nomes)

**Onde:** `SistemaEstoque.merge_sort` e `_merge`.
**Quando é usada:** após cadastrar/atualizar a lista de nomes de insumos.
**Para quê:** manter `lista_insumos` **ordenada alfabeticamente**, o que viabiliza a **busca binária** e uma listagem limpa para o usuário.
**Motivo da escolha:** algoritmo **estável** e com desempenho garantido **O(n log n)**, adequado para manter a lista sempre em boa ordem.

---

## Ordenação por Quick Sort (quantidades)

**Onde:** `SistemaEstoque.quick_sort` e `_insumos_ordenados_por_quantidade`.
**Quando é usada:** em **“Exibir estoque total”**, para mostrar cada prateleira **do maior para o menor estoque**.
**Para quê:** facilitar decisões de reposição e priorização (o que está acabando aparece por último, ou invertendo, pode-se ver o que está mais crítico primeiro).
**Motivo da escolha:** algoritmo clássico, simples de implementar, e **eficiente na prática** para coleções típicas do problema (**O(n log n)** na média).
**Observação:** aqui ordenamos por **quantidade** (o requisito aceita “quantidade consumida ou validade”). O campo de validade não existe no modelo, mas pode ser adicionado e ordenado da mesma forma.

---

## Integração com o fluxo do problema

1. **Registro do consumo** (retirada): gera **um evento** que vai para **fila** e **pilha** e atualiza o **histórico agregado por data**.
2. **Consulta de existência** (buscar): usa **busca binária** (com apoio do **Merge Sort**) e, por completude, também a **sequencial**.
3. **Visão do estoque**: usa **Quick Sort** para ordenar **por quantidade**, tornando a leitura e a tomada de decisão mais objetivas.

---

## Por que essa combinação atende o caso real

* **Fila + Pilha** cobrem duas visões complementares do histórico (cronológica e reversa).
* **Buscas** permitem responder rápido “existe ou não existe este insumo?”.
* **Ordenação** organiza as listas de um jeito útil: **por nome** (para achar/ver) e **por quantidade** (para gerir/decidir).

---

## Possíveis extensões

* Adicionar **validade** no modelo do insumo e oferecer uma ordenação por **data de vencimento**.
* Persistir os eventos em arquivo/BD para manter histórico entre execuções.
* Expor botões separados para *Fila* e *Pilha* (hoje as duas visões aparecem dentro do histórico).


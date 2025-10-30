# -*- coding: utf-8 -*-
"""
SUMÁRIO — Onde cada técnica foi usada

• Fila (FIFO):
  - SistemaEstoque.fila_consumo (collections.deque)
  - Registro: SistemaEstoque._registrar_consumo_evento
  - Visualização: SistemaEstoque.exibir_historico (bloco "Fila")

• Pilha (LIFO):
  - SistemaEstoque.pilha_consumo (list)
  - Registro: SistemaEstoque._registrar_consumo_evento
  - Visualização: SistemaEstoque.exibir_historico (bloco "Pilha")

• Buscas:
  - Sequencial: SistemaEstoque.busca_sequencial (usada em buscar_insumo)
  - Binária:    SistemaEstoque.busca_binaria    (usada em buscar_insumo)

• Ordenação:
  - Merge Sort por nome: SistemaEstoque.merge_sort/_merge (manter lista de nomes)
  - Quick Sort por quantidade: SistemaEstoque.quick_sort (exibir estoque total)

• Programação Dinâmica — Reposição Ótima:
  - Funções: SistemaEstoque._hold_cost, dp_reposicao_rec_memo, dp_reposicao_bottom_up
  - Previsão simples: SistemaEstoque.prever_demanda (usa histórico para média) 
  - Geração de plano: SistemaEstoque.plano_dp_para_insumo (usa DP e formata)
  - Integração: resultado aparece em Checagem Periódica quando item está crítico
"""

import time
import tkinter as tk
from tkinter import simpledialog, messagebox
from collections import deque
from functools import lru_cache

# logo rápido (3s)

def logo_SupplyFlow():
    logo = r"""
███████╗██╗   ██╗██████╗ ██████╗ ██╗   ███╗   ███
██╔════╝██║   ██║██╔══██╗██╔══██╗██║    ███╗ ███
███████╗██║   ██║██████╔╝██████╔╝██║      ████╔╝
╚════██║██║   ██║██╔═══╝ ██╔═══╝ ██║       ██╔╝
███████║╚██████╔╝██║     ██║     ███████╗  ██║
╚══════╝ ╚═════╝ ╚═╝     ╚═╝     ╚══════╝  ╚═╝
███████╗██╗      █████╗ ██╗    ██╗
██╔════╝██║     ██╔══██╗██║    ██║
█████╗  ██║     ██║  ██║██║ █╗ ██║
██╔══╝  ██║     ██║  ██║██║███╗██║
██║     ███████╗ █████╔╝╚███╔███╔╝
╚═╝     ╚══════╝ ╚════╝  ╚══╝╚══╝
"""
    root = tk.Tk()
    root.title("SupplyFlow - Estoque")
    root.geometry("800x500")
    tk.Label(root, text=logo, font=("Courier", 10), justify="left").pack(padx=10, pady=10)
    root.after(3000, root.destroy)
    root.mainloop()

# modelos simples

class insumo:
    def __init__(self, nome, quantidade):
        self.nome = nome
        self.quantidade = quantidade

    def __repr__(self):
        return f"{self.nome}: {self.quantidade}"

class Prateleira:
    def __init__(self, id):
        self.id = id
        self.insumos = {}

    def adicionar_insumo(self, nome, quantidade):
        if nome in self.insumos:
            self.insumos[nome].quantidade += quantidade
        else:
            self.insumos[nome] = insumo(nome, quantidade)

    def exibir_estoque(self):
        s = f"\nPrateleira {self.id}:\n"
        if self.insumos:
            for i in self.insumos.values():
                s += f"- {i}\n"
        else:
            s += "Estoque vazio.\n"
        return s

# lógica do sistema (backend)

class SistemaEstoque:
    def __init__(self):
        self.estoque = {f"Prateleira_{i}": Prateleira(f"Prateleira_{i}") for i in range(1, 6)}
        self.lista_insumos = []            # nomes (ordenados por Merge Sort)
        self.historico_saidas = {}         # { "dd/mm": {nome: total} }
        self.fila_consumo = deque()        # FIFO
        self.pilha_consumo = []            # LIFO

        # carga inicial
        self._cadastrar_inicial("Seringas", 1000, "Prateleira_1")
        self._cadastrar_inicial("Luvas", 150, "Prateleira_1")
        self._cadastrar_inicial("Frascos de Vidro", 50, "Prateleira_2")
        self._cadastrar_inicial("Agulhas", 5000, "Prateleira_2")
        self._cadastrar_inicial("Álcool", 30, "Prateleira_3")
        self._cadastrar_inicial("Papel", 100, "Prateleira_4")
        self._cadastrar_inicial("Máscaras", 400, "Prateleira_5")

    # cadastro + manter lista ordenada por nome (Merge Sort)
    def _cadastrar_inicial(self, nome, qtd, prateleira_id):
        self.estoque[prateleira_id].adicionar_insumo(nome, qtd)
        self.lista_insumos.append(nome)
        self.lista_insumos = self.merge_sort(self.lista_insumos)

    # MERGE SORT (por nome)
    def merge_sort(self, lista):
        if len(lista) <= 1:
            return lista
        m = len(lista) // 2
        e = self.merge_sort(lista[:m])
        d = self.merge_sort(lista[m:])
        return self._merge(e, d)

    def _merge(self, esq, dir):
        r, i, j = [], 0, 0
        while i < len(esq) and j < len(dir):
            if esq[i].lower() <= dir[j].lower():
                r.append(esq[i]); i += 1
            else:
                r.append(dir[j]); j += 1
        r.extend(esq[i:]); r.extend(dir[j:])
        return r

    # QUICK SORT (por quantidade)
    def quick_sort(self, arr, key=lambda x: x, reverse=False):
        if len(arr) <= 1:
            return arr[:]
        p = key(arr[len(arr)//2])
        menores = [x for x in arr if key(x) < p]
        iguais  = [x for x in arr if key(x) == p]
        maiores = [x for x in arr if key(x) > p]
        out = self.quick_sort(menores, key) + iguais + self.quick_sort(maiores, key)
        return list(reversed(out)) if reverse else out

    def _insumos_ordenados_por_quantidade(self, prateleira, decrescente=True):
        lst = list(prateleira.insumos.values())
        return self.quick_sort(lst, key=lambda i: i.quantidade, reverse=decrescente)

    # buscas
    def busca_binaria(self, lista, alvo):
        i, f = 0, len(lista) - 1
        alvo_l = alvo.lower()
        while i <= f:
            m = (i + f) // 2
            v = lista[m].lower()
            if v == alvo_l:
                return True
            if v < alvo_l:
                i = m + 1
            else:
                f = m - 1
        return False

    def busca_sequencial(self, lista, alvo):
        alvo_l = alvo.lower()
        for item in lista:
            if item.lower() == alvo_l:
                return True
        return False

    # exibições
    def exibir_lista_insumos(self):
        if not self.lista_insumos:
            messagebox.showinfo("Insumos Cadastrados", "Nenhum insumo cadastrado.")
            return
        t = "📋 Insumos (ordenados por nome / Merge Sort):\n\n"
        for n in self.lista_insumos:
            t += f"• {n}\n"
        messagebox.showinfo("Insumos Cadastrados", t)

    def exibir_estoque_total(self):
        s = ""
        for p in self.estoque.values():
            s += f"\nPrateleira {p.id} (por quantidade / Quick Sort):\n"
            for ins in self._insumos_ordenados_por_quantidade(p, decrescente=True):
                s += f"- {ins.nome}: {ins.quantidade}\n"
        messagebox.showinfo("Estoque Total", s)

    # operações
    def adicionar_mais_estoque(self, nome, quantidade):
        for p in self.estoque.values():
            if nome in p.insumos:
                p.adicionar_insumo(nome, quantidade)
                return True
        return False

    def _registrar_consumo_evento(self, data, nome, quantidade):
        hora = time.strftime("%H:%M:%S")
        ev = (data, hora, nome, quantidade)
        self.fila_consumo.append(ev)
        self.pilha_consumo.append(ev)
        self.popular_historico(data, nome, quantidade)

    def retirar_insumo(self, nome, quantidade):
        data = time.strftime("%d/%m")
        for p in self.estoque.values():
            if nome in p.insumos:
                i = p.insumos[nome]
                if i.quantidade >= quantidade:
                    i.quantidade -= quantidade
                    self._registrar_consumo_evento(data, nome, quantidade)
                    messagebox.showinfo("Retirada", f"{quantidade} unidades de '{nome}' retiradas.")
                    return
                else:
                    messagebox.showwarning("Estoque insuficiente", f"Apenas {i.quantidade} disponíveis.")
                    return
        messagebox.showwarning("Não encontrado", f"Insumo '{nome}' não localizado.")

    def popular_historico(self, data, nome, quantidade):
        if data not in self.historico_saidas:
            self.historico_saidas[data] = {}
        self.historico_saidas[data][nome] = self.historico_saidas[data].get(nome, 0) + quantidade

    def exibir_historico(self):
        if not self.historico_saidas and not self.fila_consumo:
            messagebox.showinfo("Histórico", "Nenhuma saída registrada.")
            return
        s = ""
        for d, itens in self.historico_saidas.items():
            s += f"{d}:\n"
            for n, q in itens.items():
                s += f"  {n}: {q} unidades\n"
        if self.fila_consumo:
            s += "\n--- Fila (FIFO) — cronológica ---\n"
            for (d, h, n, q) in self.fila_consumo:
                s += f"{d} {h}  {n}: -{q}\n"
        if self.pilha_consumo:
            s += "\n--- Pilha (LIFO) — inversa ---\n"
            for (d, h, n, q) in reversed(self.pilha_consumo):
                s += f"{d} {h}  {n}: -{q}\n"
        messagebox.showinfo("Histórico de Saídas", s)

    # --- Programação Dinâmica: Reposição ---
    def _hold_cost(self, d, t, r, h):
        # custo de segurar as quantidades por j dias
        return sum(h * j * d[t + j] for j in range(r))

    def dp_reposicao_rec_memo(self, d, K, h, L):
        n = len(d)

        @lru_cache(maxsize=None)
        def f(t):
            if t >= n:
                return 0
            best = 10**18
            for r in range(1, min(L, n - t) + 1):
                c = K + self._hold_cost(d, t, r, h) + f(t + r)
                if c < best:
                    best = c
            return best

        plano = []
        t = 0
        while t < n:
            best = 10**18; best_r = 1
            for r in range(1, min(L, n - t) + 1):
                c = K + self._hold_cost(d, t, r, h) + f(t + r)
                if c < best:
                    best = c; best_r = r
            qty = sum(d[t:t + best_r])
            plano.append({"dia": t, "cobre_dias": best_r, "quantidade": qty})
            t += best_r
        return f(0), plano

    def dp_reposicao_bottom_up(self, d, K, h, L):
        n = len(d)
        dp = [0] * (n + 1)
        choice = [0] * n
        for t in range(n - 1, -1, -1):
            best = 10**18; best_r = 1
            for r in range(1, min(L, n - t) + 1):
                c = K + self._hold_cost(d, t, r, h) + dp[t + r]
                if c < best:
                    best = c; best_r = r
            dp[t] = best; choice[t] = best_r
        plano = []
        t = 0
        while t < n:
            r = choice[t]
            qty = sum(d[t:t + r])
            plano.append({"dia": t, "cobre_dias": r, "quantidade": qty})
            t += r
        return dp[0], plano

    def prever_demanda(self, nome, dias=7):
        # média simples do histórico por dia; fallback para demanda pequena
        totais = []
        for data, itens in self.historico_saidas.items():
            if nome in itens:
                totais.append(itens[nome])
        media = max(1, round(sum(totais) / len(totais))) if totais else  max(1, round(self._quantidade_atual(nome) * 0.05))
        return [media for _ in range(dias)]

    def _quantidade_atual(self, nome):
        for p in self.estoque.values():
            if nome in p.insumos:
                return p.insumos[nome].quantidade
        return 0

    def plano_dp_para_insumo(self, nome, dias=7, K=50, h=1, L=5):
        d = self.prever_demanda(nome, dias)
        c1, p1 = self.dp_reposicao_bottom_up(d, K, h, L)
        c2, p2 = self.dp_reposicao_rec_memo(tuple(d), K, h, L)  # tuple para cache
        ok = (c1 == c2 and p1 == p2)
        linhas = [f"DP para '{nome}' (dias={dias}, K={K}, h={h}, L={L}) — custo mínimo = {c1}"]
        for ped in p1:
            linhas.append(f"  • pedir no dia {ped['dia']} cobrindo {ped['cobre_dias']} dias → qty={ped['quantidade']}")
        if not ok:
            linhas.append("  ! Aviso: versões recursiva e iterativa divergiram (usando bottom-up).")
        return "\n".join(linhas)

    def checagemPeriodica(self):
        s = ""
        criticos = []
        for p in self.estoque.values():
            for i in p.insumos.values():
                if i.quantidade <= 50:
                    s += f"⚠️ {i.nome} na {p.id} com {i.quantidade} unidades (repor).\n"
                    criticos.append(i.nome)
                else:
                    s += f"✔️ {i.nome} na {p.id} com {i.quantidade} unidades.\n"
        # anexa plano de reposição por DP para itens críticos
        if criticos:
            s += "\n— Sugestões de Reposição (Programação Dinâmica) —\n"
            for nome in criticos:
                s += self.plano_dp_para_insumo(nome, dias=7, K=50, h=1, L=5) + "\n"
        messagebox.showinfo("Checagem de Estoque", s)

    def buscar_insumo(self, nome):
        ok = self.busca_binaria(self.lista_insumos, nome) or self.busca_sequencial(self.lista_insumos, nome)
        if ok:
            for p in self.estoque.values():
                if nome in p.insumos:
                    q = p.insumos[nome].quantidade
                    messagebox.showinfo("Encontrado", f"{nome} está na {p.id} com {q} unidades.")
                    return True
        else:
            messagebox.showwarning("Não encontrado", f"Insumo '{nome}' não cadastrado.")
            return False

    def prateleira_com_menos_insumos(self):
        alvo, menor = None, float('inf')
        for p in self.estoque.values():
            total = sum(i.quantidade for i in p.insumos.values())
            if total < menor:
                menor, alvo = total, p
        return alvo

    def adicionar_insumo_novo(self, nome, quantidade):
        p = self.prateleira_com_menos_insumos()
        p.adicionar_insumo(nome, quantidade)
        self.lista_insumos.append(nome)
        self.lista_insumos = self.merge_sort(self.lista_insumos)
        messagebox.showinfo("Novo Insumo", f"'{nome}' adicionado à {p.id} com {quantidade} unidades.")

# UI (inalterada)

class Main:
    def __init__(self, sistema):
        self.sistema = sistema
        self.root = tk.Tk()
        self.root.title("Sistema de Estoque - SupplyFlow")
        self.root.geometry("500x520")
        self.criar_interface()
        self.root.mainloop()

    def criar_interface(self):
        tk.Label(self.root, text="SupplyFlow", font=("Arial", 20, "bold")).pack(pady=10)
        botoes = [
            ("Exibir estoque total", self.sistema.exibir_estoque_total),
            ("Adicionar à insumo existente", self.adicionar_estoque),
            ("Cadastrar novo insumo", self.cadastrar_novo_insumo),
            ("Retirar insumo", self.retirar_insumo),
            ("Buscar insumo", self.buscar_insumo),
            ("Ver insumos cadastrados", self.sistema.exibir_lista_insumos),
            ("Consultar histórico", self.sistema.exibir_historico),
            ("Checagem periódica", self.sistema.checagemPeriodica),
            ("Sair", self.root.quit)
        ]
        for texto, cmd in botoes:
            tk.Button(self.root, text=texto, width=50, command=cmd).pack(pady=5)

    def adicionar_estoque(self):
        nome = simpledialog.askstring("Adicionar Estoque", "Nome do insumo:")
        if nome:
            qtd = simpledialog.askinteger("Quantidade", f"Quantidade para '{nome}':")
            if qtd:
                if self.sistema.adicionar_mais_estoque(nome, qtd):
                    messagebox.showinfo("Sucesso", f"{qtd} unidades adicionadas a '{nome}'.")
                else:
                    messagebox.showwarning("Erro", f"Insumo '{nome}' não encontrado.")

    def cadastrar_novo_insumo(self):
        nome = simpledialog.askstring("Novo Insumo", "Nome do novo insumo:")
        if nome:
            qtd = simpledialog.askinteger("Quantidade", f"Quantidade inicial de '{nome}':")
            if qtd:
                self.sistema.adicionar_insumo_novo(nome, qtd)

    def retirar_insumo(self):
        nome = simpledialog.askstring("Retirar Estoque", "Nome do insumo:")
        if nome:
            qtd = simpledialog.askinteger("Quantidade", f"Quantidade a retirar de '{nome}':")
            if qtd:
                self.sistema.retirar_insumo(nome, qtd)

    def buscar_insumo(self):
        nome = simpledialog.askstring("Buscar Insumo", "Nome do insumo:")
        if nome:
            self.sistema.buscar_insumo(nome)

if __name__ == "__main__":
    logo_SupplyFlow()
    sistema = SistemaEstoque()
    Main(sistema)


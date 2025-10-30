"""
SUMÁRIO — Onde cada técnica foi usada

• Fila (FIFO):
  - Estrutura: SistemaEstoque.fila_consumo (collections.deque)
  - Registro de eventos: SistemaEstoque._registrar_consumo_evento
  - Exibição em ordem cronológica: SistemaEstoque.exibir_historico (bloco "Fila")

• Pilha (LIFO):
  - Estrutura: SistemaEstoque.pilha_consumo (list)
  - Registro de eventos: SistemaEstoque._registrar_consumo_evento
  - Exibição em ordem inversa: SistemaEstoque.exibir_historico (bloco "Pilha")

• Buscas:
  - Sequencial: SistemaEstoque.busca_sequencial (usada em buscar_insumo)
  - Binária:    SistemaEstoque.busca_binaria    (usada em buscar_insumo)

• Ordenação:
  - Merge Sort por nome (insumos): SistemaEstoque.merge_sort/_merge (usado ao cadastrar e listar)
  - Quick Sort por quantidade:     SistemaEstoque.quick_sort (usado em exibir_estoque_total)
"""

import time
import tkinter as tk
from tkinter import simpledialog, messagebox
from collections import deque

# Logo simples em janela por 3s

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

# Modelos simples

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

# Lógica do sistema (backend)

class SistemaEstoque:
    def __init__(self):
        self.estoque = {f"Prateleira_{i}": Prateleira(f"Prateleira_{i}") for i in range(1, 6)}
        self.lista_insumos = []           # nomes (ordenados por Merge Sort)
        self.historico_saidas = {}        # { data: {nome: total} }
        self.fila_consumo = deque()       # FIFO
        self.pilha_consumo = []           # LIFO

        # carga inicial
        self._cadastrar_inicial("Seringas", 1000, "Prateleira_1")
        self._cadastrar_inicial("Luvas", 150, "Prateleira_1")
        self._cadastrar_inicial("Frascos de Vidro", 50, "Prateleira_2")
        self._cadastrar_inicial("Agulhas", 5000, "Prateleira_2")
        self._cadastrar_inicial("Álcool", 30, "Prateleira_3")
        self._cadastrar_inicial("Papel", 100, "Prateleira_4")
        self._cadastrar_inicial("Máscaras", 400, "Prateleira_5")

    # cadastro + manutenção da lista ordenada por nome (Merge Sort)
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
        while i <= f:
            m = (i + f) // 2
            v = lista[m].lower()
            if v == alvo.lower():
                return True
            if v < alvo.lower():
                i = m + 1
            else:
                f = m - 1
        return False

    def busca_sequencial(self, lista, alvo):
        for item in lista:
            if item.lower() == alvo.lower():
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

    def checagemPeriodica(self):
        s = ""
        for p in self.estoque.values():
            for i in p.insumos.values():
                if i.quantidade <= 50:
                    s += f"⚠️ {i.nome} na {p.id} com {i.quantidade} unidades (repor).\n"
                else:
                    s += f"✔️ {i.nome} na {p.id} com {i.quantidade} unidades.\n"
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


import os
import sqlite3
import tkinter as tk
from tkinter import messagebox, Toplevel, Listbox, Scrollbar, Button, Frame, Label, Entry
from fpdf import FPDF
from pathlib import Path

# Conexão com o banco de dados
conn = sqlite3.connect('agenda_clinica.db')
cursor = conn.cursor()

# Criar a tabela se não existir
cursor.execute('''
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    cpf TEXT NOT NULL,
    telefone TEXT NOT NULL,
    data TEXT NOT NULL,
    procedimento TEXT NOT NULL,
    local TEXT NOT NULL,
    valor TEXT NOT NULL,
    pagamento TEXT NOT NULL
)
''')

# Função para limpar os campos
def limpar_campos():
    for entry in entries:
        entry.delete(0, tk.END)

# Função para adicionar um cliente
def adicionar_cliente():
    nome = entry_nome.get()
    cpf = entry_cpf.get()
    telefone = entry_telefone.get()
    data = entry_data.get()
    procedimento = entry_procedimento.get()
    local = entry_local.get()
    valor = entry_valor.get()
    pagamento = entry_pagamento.get()

    if nome and cpf and telefone and data and procedimento and local and valor and pagamento:
        cursor.execute('''
            INSERT INTO clientes (nome, cpf, telefone, data, procedimento, local, valor, pagamento)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (nome, cpf, telefone, data, procedimento, local, valor, pagamento))
        conn.commit()
        messagebox.showinfo('Sucesso', 'Cliente adicionado com sucesso!')
        limpar_campos()
        consultar_clientes()
    else:
        messagebox.showerror('Erro', 'Por favor, preencha todos os campos.')

# Função para consultar clientes
def consultar_clientes():
    consulta_janela = Toplevel(root)
    consulta_janela.title("Consulta de Clientes")
    consulta_janela.geometry("600x400")

    lista_clientes = Listbox(consulta_janela, width=80, height=20)
    lista_clientes.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = Scrollbar(consulta_janela)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    lista_clientes.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=lista_clientes.yview)

    # Limpa a lista antes de adicionar novos clientes
    lista_clientes.delete(0, tk.END)

    cursor.execute("SELECT id, nome, cpf, telefone, data, procedimento FROM clientes")
    clientes = cursor.fetchall()

    if not clientes:
        messagebox.showinfo('Informação', 'Nenhum cliente encontrado.')
        return

    for cliente in clientes:
        lista_clientes.insert(tk.END, f"ID: {cliente[0]} | Nome: {cliente[1]} | CPF: {cliente[2]} | Tel: {cliente[3]} | Data: {cliente[4]} | Proced.: {cliente[5]}")

    # Adicionando botão de exportação PDF na tela de consulta
    def exportar_pdf():
        periodo = entry_periodo.get()
        
        # Verificando se o período tem o formato MM/AAAA
        if len(periodo) != 7 or periodo[2] != '/':
            messagebox.showerror('Erro', 'Por favor, insira o período no formato MM/AAAA.')
            return
        
        mes, ano = periodo.split('/')
        
        # Usando substr para pegar o mês e ano da data e comparar
        cursor.execute("""
            SELECT * FROM clientes 
            WHERE substr(data, 4, 2) = ? AND substr(data, 7, 4) = ?
        """, (mes, ano))
        clientes = cursor.fetchall()

        if not clientes:
            messagebox.showerror('Erro', 'Nenhum cliente encontrado para o período informado.')
            return

        # Criar o PDF
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, f"Relatório de Clientes - Período: {periodo}", ln=True, align='C')

        for cliente in clientes:
            pdf.cell(200, 10, f"Nome: {cliente[1]}", ln=True)
            pdf.cell(200, 10, f"CPF: {cliente[2]}", ln=True)
            pdf.cell(200, 10, f"Telefone: {cliente[3]}", ln=True)
            pdf.cell(200, 10, f"Data: {cliente[4]}", ln=True)
            pdf.cell(200, 10, f"Procedimento: {cliente[5]}", ln=True)
            pdf.cell(200, 10, f"Local: {cliente[6]}", ln=True)
            pdf.cell(200, 10, f"Valor: {cliente[7]}", ln=True)
            pdf.cell(200, 10, f"Forma de Pagamento: {cliente[8]}", ln=True)
            pdf.cell(200, 10, "", ln=True)  # Linha em branco entre os clientes

        # Obter diretório de Downloads
        download_folder = str(Path.home() / "Downloads")
        file_path = os.path.join(download_folder, "relatorio_clientes.pdf")
        
        # Salvar o arquivo na pasta Downloads
        pdf.output(file_path)
        messagebox.showinfo('Sucesso', f'Relatório exportado como {file_path}')

    # Frame para os campos de filtro de período e botão de exportação
    frame_filtro_exportacao = tk.Frame(consulta_janela)
    frame_filtro_exportacao.pack(fill='x', pady=10)

    entry_periodo = Entry(frame_filtro_exportacao)
    entry_periodo.pack(side=tk.LEFT, padx=10)
    entry_periodo.insert(0, "Digite o período (MM/AAAA)")

    btn_exportar = tk.Button(frame_filtro_exportacao, text='Exportar PDF', command=exportar_pdf)
    btn_exportar.pack(side=tk.LEFT, padx=10)

# Função para remover cliente (agora removendo pelo nome)
def remover_cliente():
    nome_cliente = entry_nome.get()  # Agora usamos o campo "Nome Completo"
    if nome_cliente:
        cursor.execute("DELETE FROM clientes WHERE nome = ?", (nome_cliente,))
        conn.commit()
        messagebox.showinfo('Sucesso', f'Cliente {nome_cliente} removido com sucesso!')
        consultar_clientes()
    else:
        messagebox.showerror('Erro', 'Informe um nome válido.')

# Configuração da interface gráfica
root = tk.Tk()
root.title('Agenda Clínica Odontológica')

# Frame para os campos de entrada
frame_campos = tk.Frame(root)
frame_campos.pack(fill='x', padx=10, pady=10)

# Labels e campos de entrada
labels = ['Nome Completo', 'CPF', 'Telefone', 'Data do Procedimento', 'Procedimento', 'Local', 'Valor', 'Forma de Pagamento']
entries = []

for label_text in labels:
    row = tk.Frame(frame_campos)
    row.pack(side=tk.TOP, fill=tk.X, pady=5)
    label = tk.Label(row, text=label_text + ':', width=20, anchor='w')
    label.pack(side=tk.LEFT)
    entry = tk.Entry(row)
    entry.pack(side=tk.RIGHT, fill=tk.X, expand=True)
    entries.append(entry)

(entry_nome, entry_cpf, entry_telefone, entry_data, entry_procedimento, entry_local, entry_valor, entry_pagamento) = entries

# Frame para os botões
frame_botoes = tk.Frame(root)
frame_botoes.pack(pady=10)

btn_adicionar = tk.Button(frame_botoes, text='Adicionar Cliente', command=adicionar_cliente)
btn_adicionar.grid(row=0, column=0, padx=10)

btn_consultar = tk.Button(frame_botoes, text='Consultar Clientes', command=consultar_clientes)
btn_consultar.grid(row=0, column=1, padx=10)

btn_remover = tk.Button(frame_botoes, text='Remover Cliente', command=remover_cliente)
btn_remover.grid(row=0, column=2, padx=10)

# Iniciar o loop da interface
root.mainloop()

# Fechar conexão com o banco de dados ao encerrar o programa
conn.close()



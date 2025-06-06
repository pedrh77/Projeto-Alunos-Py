import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import Banco.Repository as banco
import Controller


def abrir_tela_alunos():
    aluno_selecionado = None

    def refresh_lista():
        listbox.delete(0, tk.END)
        for aluno in banco.listar_alunos():
            listbox.insert(tk.END, f"{aluno[0]} - {aluno[1]} | CPF: {aluno[2]} | Tel: {aluno[3]}")
        limpar_campos()


    def formatar_nome():
        atual = entry_nome.get()
        formatado = atual.title()
        entry_nome.delete(0, tk.END)
        entry_nome.insert(0, formatado)
        
    def limpar_campos():
        combo_ano.set('')
        combo_semestre.set('')
        entry_nome.delete(0, tk.END)
        entry_cpf.delete(0, tk.END)
        entry_telefone.delete(0, tk.END)
        btn_salvar.config(state="disabled")

    def gerar_matricula(ano, semestre):
        agora = datetime.now()
        hora = agora.strftime("%H%M%S") 
        return f"{ano}.{semestre}.{hora}"

    def validar_cpf(event):
        atual = entry_cpf.get().strip()
        if len(atual) > 11:
            entry_cpf.delete(11, tk.END) 

    def validar_nome(nome):
        partes = nome.strip().split()
        return len(partes) >= 2

    def inserir():
        ano = combo_ano.get()
        semestre = combo_semestre.get()
        nome = entry_nome.get().strip()
        cpf = entry_cpf.get().strip()
        telefone = entry_telefone.get().strip()

        if not ano or not semestre:
            messagebox.showwarning("Atenção", "Selecione Ano e Semestre.")
            return

        if not nome or not validar_nome(nome):
            messagebox.showwarning("Atenção", "Informe Nome e Sobrenome.")
            return


        
        matricula = gerar_matricula(ano, semestre)

        try:
            banco.inserir_aluno(matricula, nome, cpf, telefone)
            messagebox.showinfo("Sucesso", "Aluno cadastrado com sucesso.")
            refresh_lista()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao inserir aluno: {e}")

    def editar():
        nonlocal aluno_selecionado
        selecionado = listbox.curselection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um aluno para editar.")
            return

        aluno = banco.listar_alunos()[selecionado[0]]
        aluno_selecionado = aluno[0]  # matrícula

        matricula_partes = aluno[0].split(".")
        if len(matricula_partes) == 2:
            combo_ano.set(matricula_partes[0])
            combo_semestre.set(matricula_partes[1])
        else:
            combo_ano.set('')
            combo_semestre.set('')

        entry_nome.delete(0, tk.END)
        entry_nome.insert(0, aluno[1])

        entry_cpf.delete(0, tk.END)
        entry_cpf.insert(0, aluno[2])
        entry_cpf.configure(state="disabled")

        entry_telefone.delete(0, tk.END)
        entry_telefone.insert(0, aluno[3])

        btn_salvar.config(state="normal")

    def salvar_alteracoes():
        if aluno_selecionado is None:
            messagebox.showwarning("Atenção", "Nenhum aluno selecionado.")
            return

        nome = entry_nome.get().strip()
        telefone = entry_telefone.get().strip()

        if not nome or not validar_nome(nome):
            messagebox.showwarning("Atenção", "Informe Nome e Sobrenome.")
            return

        nome = validar_nome(nome)

        try:
            banco.atualizar_aluno(aluno_selecionado, nome, telefone)
            messagebox.showinfo("Sucesso", "Aluno atualizado com sucesso.")
            entry_cpf.configure(state="normal")
            refresh_lista()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar: {e}")

    def deletar():
        selecionado = listbox.curselection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um aluno para deletar.")
            return

        aluno = banco.listar_alunos()[selecionado[0]]
        confirmar = messagebox.askyesno("Confirmação", f"Deseja deletar o aluno '{aluno[1]}'?")
        if confirmar:
            try:
                banco.deletar_aluno(aluno[0])
                messagebox.showinfo("Sucesso", "Aluno deletado.")
                refresh_lista()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao deletar: {e}")

    def voltar():
        janela.destroy()
        Controller.abrir_tela_principal()

    # ==== JANELA PRINCIPAL ====
    janela = tk.Tk()
    janela.title("Gerenciamento de Alunos")
    janela.geometry("650x550")
    janela.resizable(False, False)

    frame_form = tk.Frame(janela)
    frame_form.pack(pady=10)

    tk.Label(frame_form, text="Ano:", font=("Arial", 12)).grid(row=0, column=0, sticky="e")
    combo_ano = ttk.Combobox(frame_form, values=[str(i) for i in range(2020, 2026)],
                              width=10, font=("Arial", 12), state="readonly")
    combo_ano.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    tk.Label(frame_form, text="Semestre:", font=("Arial", 12)).grid(row=0, column=2, sticky="e")
    combo_semestre = ttk.Combobox(frame_form, values=["1", "2"],
                                   width=5, font=("Arial", 12), state="readonly")
    combo_semestre.grid(row=0, column=3, padx=10, pady=5, sticky="w")

    tk.Label(frame_form, text="Nome:", font=("Arial", 12)).grid(row=1, column=0, sticky="e")
    entry_nome = tk.Entry(frame_form, width=40, font=("Arial", 12))
    entry_nome.grid(row=1, column=1, columnspan=3, padx=10, pady=5, sticky="w")
    entry_nome.bind("<KeyRelease>", lambda e: formatar_nome())

    tk.Label(frame_form, text="CPF:", font=("Arial", 12)).grid(row=2, column=0, sticky="e")
    entry_cpf = tk.Entry(frame_form, width=20, font=("Arial", 12))
    entry_cpf.grid(row=2, column=1, padx=10, pady=5, sticky="w")
    entry_cpf.bind('<KeyRelease>', validar_cpf)

    tk.Label(frame_form, text="Telefone:", font=("Arial", 12)).grid(row=2, column=2, sticky="e")
    entry_telefone = tk.Entry(frame_form, width=20, font=("Arial", 12))
    entry_telefone.grid(row=2, column=3, padx=10, pady=5, sticky="w")

    btn_inserir = tk.Button(janela, text="Inserir Aluno", font=("Arial", 14),
                             bg="#4CAF50", fg="white", command=inserir)
    btn_inserir.pack(pady=10)

    listbox = tk.Listbox(janela, width=80, height=10, font=("Arial", 12))
    listbox.pack(pady=10)

    frame_botoes = tk.Frame(janela)
    frame_botoes.pack()

    btn_editar = tk.Button(frame_botoes, text="Editar", font=("Arial", 12), command=editar)
    btn_editar.grid(row=0, column=0, padx=10)

    btn_salvar = tk.Button(frame_botoes, text="Salvar", font=("Arial", 12),
                            command=salvar_alteracoes, state="disabled")
    btn_salvar.grid(row=0, column=1, padx=10)

    btn_deletar = tk.Button(frame_botoes, text="Deletar", font=("Arial", 12), command=deletar)
    btn_deletar.grid(row=0, column=2, padx=10)

    btn_voltar = tk.Button(janela, text="Voltar", font=("Arial", 12),
                            bg="#f44336", fg="white", command=voltar)
    btn_voltar.pack(pady=10)

    refresh_lista()
    janela.mainloop()

import tkinter as tk
from tkinter import messagebox
import Banco.Repository as banco
import Controller

def abrir_tela_disciplinas():
    disciplina_selecionada = None  

    def refresh_lista():
        listbox.delete(0, tk.END)
        for d in banco.listar_disciplinas():
            listbox.insert(tk.END, f"{d[0]} - {d[1]} | Ano: {d[2]} | Sem: {d[3]} | Prof: {d[4]}")
        limpar_campos()

    def limpar_campos():
        entry_nome.delete(0, tk.END)
        entry_ano.delete(0, tk.END)
        entry_semestre.delete(0, tk.END)
        entry_professor.delete(0, tk.END)
        btn_salvar.config(state="disabled")

    def inserir():
        nome = entry_nome.get()
        ano = entry_ano.get()
        semestre = entry_semestre.get()
        professor = entry_professor.get()

        if not nome or not ano or not semestre or not professor:
            messagebox.showwarning("Atenção", "Preencha todos os campos")
            return

        try:
            ano_int = int(ano)
            semestre_int = int(semestre)
        except ValueError:
            messagebox.showerror("Erro", "Ano e Semestre devem ser números inteiros")
            return

        banco.inserir_disciplina(nome, ano_int, semestre_int, professor)
        messagebox.showinfo("Sucesso", "Disciplina inserida")
        refresh_lista()

    def editar():
        nonlocal disciplina_selecionada
        selecionado = listbox.curselection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione uma disciplina para editar")
            return
        idx = selecionado[0]
        dados = banco.listar_disciplinas()[idx]
        disciplina_selecionada = dados[0]  
        entry_nome.delete(0, tk.END)
        entry_nome.insert(0, dados[1])

        entry_ano.delete(0, tk.END)
        entry_ano.insert(0, dados[2])

        entry_semestre.delete(0, tk.END)
        entry_semestre.insert(0, dados[3])

        entry_professor.delete(0, tk.END)
        entry_professor.insert(0, dados[4])

        btn_salvar.config(state="normal")

    def voltar():
        janela.destroy()
        Controller.abrir_tela_principal()

    def salvar_alteracoes():
        if disciplina_selecionada is None:
            messagebox.showwarning("Atenção", "Nenhuma disciplina selecionada para editar")
            return

        nome = entry_nome.get()
        ano = entry_ano.get()
        semestre = entry_semestre.get()
        professor = entry_professor.get()

        if not nome or not ano or not semestre or not professor:
            messagebox.showwarning("Atenção", "Preencha todos os campos")
            return

        try:
            ano_int = int(ano)
            semestre_int = int(semestre)
        except ValueError:
            messagebox.showerror("Erro", "Ano e Semestre devem ser números inteiros")
            return

        banco.atualizar_disciplina(disciplina_selecionada, nome, ano_int, semestre_int, professor)
        messagebox.showinfo("Sucesso", "Disciplina atualizada")
        refresh_lista()

    def deletar():
        selecionado = listbox.curselection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione uma disciplina para deletar")
            return
        idx = selecionado[0]
        dados = banco.listar_disciplinas()[idx]

        confirmar = messagebox.askyesno("Confirmação", f"Quer deletar a disciplina '{dados[1]}'?")
        if confirmar:
            banco.deletar_disciplina(dados[0])
            messagebox.showinfo("Sucesso", "Disciplina deletada")
            refresh_lista()

   
    janela = tk.Tk()
    janela.title("Gerenciar Disciplinas")
    janela.geometry("600x500")
    janela.resizable(False, False)

    frame_form = tk.Frame(janela)
    frame_form.pack(pady=10)

    tk.Label(frame_form, text="Nome:", font=("Arial", 12)).grid(row=0, column=0, sticky="e")
    entry_nome = tk.Entry(frame_form, width=40, font=("Arial", 12))
    entry_nome.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(frame_form, text="Ano:", font=("Arial", 12)).grid(row=1, column=0, sticky="e")
    entry_ano = tk.Entry(frame_form, width=10, font=("Arial", 12))
    entry_ano.grid(row=1, column=1, sticky="w", padx=10, pady=5)

    tk.Label(frame_form, text="Semestre:", font=("Arial", 12)).grid(row=2, column=0, sticky="e")
    entry_semestre = tk.Entry(frame_form, width=10, font=("Arial", 12))
    entry_semestre.grid(row=2, column=1, sticky="w", padx=10, pady=5)

    tk.Label(frame_form, text="Nome Professor:", font=("Arial", 12)).grid(row=3, column=0, sticky="e")
    entry_professor = tk.Entry(frame_form, width=40, font=("Arial", 12))
    entry_professor.grid(row=3, column=1, padx=10, pady=5)

    btn_inserir = tk.Button(janela, text="Inserir Disciplina", font=("Arial", 14), bg="#4CAF50", fg="white", command=inserir)
    btn_inserir.pack(pady=10)

    listbox = tk.Listbox(janela, width=80, height=10, font=("Arial", 12))
    listbox.pack(pady=10)

    frame_botoes = tk.Frame(janela)
    frame_botoes.pack()

    btn_editar = tk.Button(frame_botoes, text="Editar Selecionada", font=("Arial", 12), command=editar)
    btn_editar.grid(row=0, column=0, padx=10)

    btn_salvar = tk.Button(frame_botoes, text="Salvar Alterações", font=("Arial", 12), command=salvar_alteracoes, state="disabled")
    btn_salvar.grid(row=0, column=1, padx=10)

    btn_deletar = tk.Button(frame_botoes, text="Deletar Selecionada", font=("Arial", 12), command=deletar)
    btn_deletar.grid(row=0, column=2, padx=10)
    
    

    btn_voltar = tk.Button(janela, text="Voltar", font=("Arial", 12), bg="#f44336", fg="white", command=voltar)
    btn_voltar.pack(pady=10)

    refresh_lista()
    janela.mainloop()

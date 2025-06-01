import tkinter as tk
from tkinter import messagebox
import Banco.Repository as banco
import Controller


def abrir_tela_alunos():
    aluno_selecionado = None

    def refresh_lista():
        listbox.delete(0, tk.END)
        for aluno in banco.listar_alunos():
            listbox.insert(tk.END, f"{aluno[0]} - {aluno[1]} | CPF: {aluno[2]} | Tel: {aluno[3]}")
        limpar_campos()

    def limpar_campos():
        entry_matricula.delete(0, tk.END)
        entry_nome.delete(0, tk.END)
        entry_cpf.delete(0, tk.END)
        entry_telefone.delete(0, tk.END)
        btn_salvar.config(state="disabled")

    def inserir():
        matricula = entry_matricula.get().strip()
        nome = entry_nome.get().strip()
        cpf = entry_cpf.get().strip()
        telefone = entry_telefone.get().strip()

        if not matricula or not nome or not cpf:
            messagebox.showwarning("Atenção", "Preencha Matrícula, Nome e CPF.")
            return

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
        aluno_selecionado = aluno[0]  # Matrícula antiga

        entry_matricula.delete(0, tk.END)
        entry_matricula.insert(0, aluno[0])
        entry_matricula.configure(state="disabled")

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

        if not nome:
            messagebox.showwarning("Atenção", "O campo Nome não pode estar vazio.")
            return

        try:
            banco.atualizar_aluno(aluno_selecionado, nome, telefone)
            messagebox.showinfo("Sucesso", "Aluno atualizado com sucesso.")
            entry_matricula.configure(state="normal")
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

    # Construção da janela
    janela = tk.Tk()
    janela.title("Gerenciamento de Alunos")
    janela.geometry("650x550")
    janela.resizable(False, False)

    frame_form = tk.Frame(janela)
    frame_form.pack(pady=10)

    tk.Label(frame_form, text="Matrícula:", font=("Arial", 12)).grid(row=0, column=0, sticky="e")
    entry_matricula = tk.Entry(frame_form, width=20, font=("Arial", 12))
    entry_matricula.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(frame_form, text="Nome:", font=("Arial", 12)).grid(row=1, column=0, sticky="e")
    entry_nome = tk.Entry(frame_form, width=40, font=("Arial", 12))
    entry_nome.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(frame_form, text="CPF:", font=("Arial", 12)).grid(row=2, column=0, sticky="e")
    entry_cpf = tk.Entry(frame_form, width=20, font=("Arial", 12))
    entry_cpf.grid(row=2, column=1, sticky="w", padx=10, pady=5)

    tk.Label(frame_form, text="Telefone:", font=("Arial", 12)).grid(row=3, column=0, sticky="e")
    entry_telefone = tk.Entry(frame_form, width=20, font=("Arial", 12))
    entry_telefone.grid(row=3, column=1, sticky="w", padx=10, pady=5)

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
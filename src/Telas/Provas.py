from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import Banco.Repository as banco
import Controller


def abrir_tela_provas():
    prova_selecionada = None

    def carregar_disciplinas():
        disciplinas = banco.listar_disciplinas_dropbox()
        disciplina_map.clear()
        disciplina_combobox['values'] = []
        lista_nomes = []
        for disc in disciplinas:
            disciplina_map[disc[1]] = disc[0] 
            lista_nomes.append(disc[1])
        disciplina_combobox['values'] = lista_nomes

    def carregar_alunos():
        alunos = banco.listar_alunos()
        aluno_map.clear()
        aluno_combobox['values'] = []
        lista_nomes = []
        for aluno in alunos:
            aluno_map[aluno[1]] = aluno[0]  
            lista_nomes.append(aluno[1])
        aluno_combobox['values'] = lista_nomes
    
    
    def refresh_lista():
        listbox.delete(0, tk.END)
        for prova in banco.listar_provas():
            print(prova)
            disciplina = banco.buscar_disciplina_por_id(prova[1])
            aluno = banco.buscar_aluno_por_matricula(prova[2])

            nome_disciplina = disciplina[1] if disciplina else "Disciplina não encontrada"
            nome_aluno = aluno[1] if aluno else "Aluno não encontrado"

            status = 'APROVADO' if prova[7] > 6 else 'REPROVADO'

            listbox.insert(
                tk.END,
                f"ID: {prova[0]} | Aluno: {nome_aluno} | Disciplina: {nome_disciplina} | "
                f"SM1: {prova[3]} | SM2: {prova[4]} | AV: {prova[5]} | AVS: {prova[6]} | "
                f"NF: {prova[7]} | STATUS: {status}"
            )
        limpar_campos()

    def limpar_campos():
        disciplina_combobox.set('')
        aluno_combobox.set('')
        entry_sm1.delete(0, tk.END)
        entry_sm2.delete(0, tk.END)
        entry_av.delete(0, tk.END)
        entry_avs.delete(0, tk.END)
        entry_nf.config(state="normal")
        entry_nf.delete(0, tk.END)
        entry_nf.config(state="disabled")
        btn_salvar.config(state="disabled")

    def calcular_nf(*args):
        try:
            sm1 = float(entry_sm1.get() or 0)
            sm2 = float(entry_sm2.get() or 0)
            av = float(entry_av.get() or 0)
            avs = float(entry_avs.get() or 0)

            sm1 = min(max(sm1, 0), 1)
            sm2 = min(max(sm2, 0), 1)
            av = min(max(av, 0), 10)
            avs = min(max(avs, 0), 10)

            nota_av_final = max(av, avs)
            nf = sm1 + sm2 + nota_av_final

            entry_nf.config(state="normal")
            entry_nf.delete(0, tk.END)
            entry_nf.insert(0, f"{nf:.2f}")
            entry_nf.config(state="disabled")
        except ValueError:
            entry_nf.config(state="normal")
            entry_nf.delete(0, tk.END)
            entry_nf.config(state="disabled")

    def inserir():
        try:
            disciplina_nome = disciplina_combobox.get()
            disciplina_id = disciplina_map.get(disciplina_nome)

            aluno_nome = aluno_combobox.get()
            aluno_id = aluno_map.get(aluno_nome)

            if not disciplina_id:
                messagebox.showwarning("Atenção", "Selecione uma disciplina válida.")
                return

            if not aluno_id:
                messagebox.showwarning("Atenção", "Selecione um aluno válido.")
                return
            
            if banco.existe_prova(disciplina_id, aluno_id):
                messagebox.showwarning("Atenção", "Esse aluno já possui uma prova cadastrada para essa disciplina.")
                return

            sm1 = float(entry_sm1.get() or 0)
            sm2 = float(entry_sm2.get() or 0)
            av = float(entry_av.get() or 0)
            avs = float(entry_avs.get() or 0)

            sm1 = min(max(sm1, 0), 1)
            sm2 = min(max(sm2, 0), 1)
            av = min(max(av, 0), 10)
            avs = min(max(avs, 0), 10)

            nota_av_final = max(av, avs)
            nf = sm1 + sm2 + nota_av_final


            banco.inserir_prova(disciplina_id, aluno_id, sm1, sm2, av, avs, nf)
            messagebox.showinfo("Sucesso", "Prova cadastrada com sucesso.")
            refresh_lista()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao inserir prova: {e}")

    def editar():
        nonlocal prova_selecionada
        selecionado = listbox.curselection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione uma prova para editar.")
            return

        prova = banco.listar_provas()[selecionado[0]]
        prova_selecionada = prova[0]

        disciplina = banco.buscar_disciplina_por_id(prova[1])
        aluno = banco.buscar_aluno_por_matricula(prova[2])

        disciplina_combobox.set(disciplina[1])
        aluno_combobox.set(aluno[1])

        entry_sm1.delete(0, tk.END)
        entry_sm1.insert(0, prova[3])

        entry_sm2.delete(0, tk.END)
        entry_sm2.insert(0, prova[4])

        entry_av.delete(0, tk.END)
        entry_av.insert(0, prova[5])

        entry_avs.delete(0, tk.END)
        entry_avs.insert(0, prova[6])

        calcular_nf()
        btn_inserir.config(state="disabled")
        btn_salvar.config(state="normal")

    def salvar_alteracoes():
        if prova_selecionada is None:
            messagebox.showwarning("Atenção", "Nenhuma prova selecionada.")
            return

        try:
            disciplina_nome = disciplina_combobox.get()
            disciplina_id = disciplina_map.get(disciplina_nome)

            aluno_nome = aluno_combobox.get()
            aluno_id = aluno_map.get(aluno_nome)

            if not disciplina_id:
                messagebox.showwarning("Atenção", "Selecione uma disciplina válida.")
                return

            if not aluno_id:
                messagebox.showwarning("Atenção", "Selecione um aluno válido.")
                return

            sm1 = float(entry_sm1.get() or 0)
            sm2 = float(entry_sm2.get() or 0)
            av = float(entry_av.get() or 0)
            avs = float(entry_avs.get() or 0)
            nf = sm1 + sm2 + av + avs

            banco.atualizar_prova(prova_selecionada, disciplina_id, aluno_id, sm1, sm2, av, avs, nf)
            messagebox.showinfo("Sucesso", "Prova atualizada com sucesso.")
            refresh_lista()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar prova: {e}")

    def deletar():
        selecionado = listbox.curselection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione uma prova para deletar.")
            return

        prova = banco.listar_provas()[selecionado[0]]
        confirmar = messagebox.askyesno("Confirmação", f"Deseja deletar a prova ID {prova[0]}?")
        if confirmar:
            try:
                banco.deletar_prova(prova[0])
                messagebox.showinfo("Sucesso", "Prova deletada.")
                refresh_lista()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao deletar: {e}")

    def voltar():
        janela.destroy()
        Controller.abrir_tela_principal()

    janela = tk.Tk()
    janela.title("Gerenciamento de Provas")
    janela.geometry("950x600")
    janela.resizable(False, False)

    disciplina_map = {}
    aluno_map = {}

    frame_form = tk.Frame(janela)
    frame_form.pack(pady=10)

    tk.Label(frame_form, text="Disciplina:", font=("Arial", 12)).grid(row=0, column=0, sticky="e")
    disciplina_combobox = ttk.Combobox(frame_form, width=30, font=("Arial", 12))
    disciplina_combobox.grid(row=0, column=1, padx=10, pady=5)

   
    tk.Label(frame_form, text="Aluno:", font=("Arial", 12)).grid(row=0, column=2, sticky="e")
    aluno_combobox = ttk.Combobox(frame_form, width=30, font=("Arial", 12))
    aluno_combobox.grid(row=0, column=3, padx=10, pady=5)

   
    tk.Label(frame_form, text="SM1:", font=("Arial", 12)).grid(row=1, column=0, sticky="e")
    entry_sm1 = tk.Entry(frame_form, width=5, font=("Arial", 12))
    entry_sm1.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(frame_form, text="SM2:", font=("Arial", 12)).grid(row=1, column=2, sticky="e")
    entry_sm2 = tk.Entry(frame_form, width=5, font=("Arial", 12))
    entry_sm2.grid(row=1, column=3, padx=10, pady=5)

    tk.Label(frame_form, text="AV:", font=("Arial", 12)).grid(row=2, column=0, sticky="e")
    entry_av = tk.Entry(frame_form, width=5, font=("Arial", 12))
    entry_av.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(frame_form, text="AVS:", font=("Arial", 12)).grid(row=2, column=2, sticky="e")
    entry_avs = tk.Entry(frame_form, width=5, font=("Arial", 12))
    entry_avs.grid(row=2, column=3, padx=10, pady=5)

    tk.Label(frame_form, text="NF:", font=("Arial", 12)).grid(row=3, column=0, sticky="e")
    entry_nf = tk.Entry(frame_form, width=10, font=("Arial", 12), state="disabled")
    entry_nf.grid(row=3, column=1, padx=10, pady=5)

    entry_sm1.bind('<KeyRelease>', calcular_nf)
    entry_sm2.bind('<KeyRelease>', calcular_nf)
    entry_av.bind('<KeyRelease>', calcular_nf)
    entry_avs.bind('<KeyRelease>', calcular_nf)

    btn_inserir = tk.Button(janela, text="Inserir Prova", font=("Arial", 14),
                             bg="#4CAF50", fg="white", command=inserir)
    btn_inserir.pack(pady=10)

    listbox = tk.Listbox(janela, width=120, height=10, font=("Arial", 11))
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

    carregar_disciplinas()
    carregar_alunos()
    refresh_lista()

    janela.mainloop()

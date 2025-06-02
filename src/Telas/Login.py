import tkinter as tk
from tkinter import messagebox
import Controller
from Banco.Repository import validar_aluno

def abrir_tela_login():
    def login():
        usuario = entry_usuario.get()
        cpf = entry_cpf.get()

        if validar_aluno(usuario, cpf) or True:
            messagebox.showinfo("Login", "Login realizado com sucesso!")
            janela_login.destroy()
            Controller.abrir_tela_principal()
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos!")


    def validar_cpf(event):
        atual = entry_cpf.get().strip()
        if len(atual) > 11:
            entry_cpf.delete(11, tk.END) 
            
    janela_login = tk.Tk()
    janela_login.title("Tela de Login")
    janela_login.geometry("400x400")
    janela_login.configure(bg="#e0e0e0")
    janela_login.resizable(False, False)

    titulo = tk.Label(janela_login, text="Sistema de Notas", font=("Arial", 20, "bold"), bg="#e0e0e0")
    titulo.pack(pady=(30, 20))

    label_usuario = tk.Label(janela_login, text="Matrícula:", font=("Arial", 14), bg="#e0e0e0")
    label_usuario.pack(pady=(0, 5))

    entry_usuario = tk.Entry(janela_login, width=30, font=("Arial", 14))
    entry_usuario.pack(pady=(0, 15))

    label_cpf = tk.Label(janela_login, text="CPF:", font=("Arial", 14), bg="#e0e0e0")
    label_cpf.pack(pady=(0, 5))

    entry_cpf = tk.Entry(janela_login, width=30, font=("Arial", 14), show="*")
    entry_cpf.pack(pady=(0, 25))

    entry_cpf.bind('<KeyRelease>', validar_cpf)


    botao_login = tk.Button(
        janela_login,
        text="Login",
        font=("Arial", 14),
        bg="#4CAF50",
        fg="white",
        width=20,
        command=login
    )
    botao_login.pack()

    janela_login.mainloop()

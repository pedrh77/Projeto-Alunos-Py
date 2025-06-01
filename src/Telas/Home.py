import tkinter as tk
import Controller



def abrir_tela_principal():
    
    def inserir_disciplinas():
        janela_home.destroy()
        Controller.abrir_tela_disciplinas()

    def inserir_alunos():
        janela_home.destroy()
        Controller.abrir_tela_Alunos()

    def visualizar_alunos():
       janela_home.destroy()
       Controller.abrir_tela_Provas()

    janela_home = tk.Tk()
    janela_home.title("Tela Principal")
    janela_home.geometry("400x400")
    janela_home.resizable(False, False)

    titulo = tk.Label(janela_home, text="Sistema de Notas - Menu Principal", font=("Arial", 16, "bold"))
    titulo.pack(pady=30)

    btn_disciplinas = tk.Button(janela_home, text="Disciplinas", font=("Arial", 14), width=20, command=inserir_disciplinas)
    btn_disciplinas.pack(pady=10)

    btn_alunos = tk.Button(janela_home, text="Alunos", font=("Arial", 14), width=20, command=inserir_alunos)
    btn_alunos.pack(pady=10)

    btn_visualizar = tk.Button(janela_home, text="Provas", font=("Arial", 14), width=20, command=visualizar_alunos)
    btn_visualizar.pack(pady=10)

    janela_home.mainloop()

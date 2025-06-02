import sqlite3

def IniciaProj() :
    try:
        conexao = sqlite3.connect('database2.bd')
        cursor = conexao.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Alunos (
            matricula TEXT PRIMARY KEY,
            nome TEXT NOT NULL,
            cpf TEXT NOT NULL UNIQUE,
            telefone TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Disciplinas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            ano INTEGER NOT NULL,
            semestre INTEGER NOT NULL,
            professor TEXT NOT NULL
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Provas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            disciplina_id INTEGER NOT NULL,
            aluno_matricula TEXT NOT NULL,
            nota_sm1 REAL,
            nota_sm2 REAL,
            av REAL,
            avs REAL,
            nf REAL,
            FOREIGN KEY (disciplina_id) REFERENCES Disciplina(id) ON DELETE CASCADE,
            FOREIGN KEY (aluno_matricula) REFERENCES Aluno(matricula) ON DELETE CASCADE
        )
        """)
    except  sqlite3.DatabaseError as Err:
        print("Erro banco", Err)

    finally:
        if conexao:
            cursor.close()
            conexao.close()


def validar_aluno(matricula, cpf):
    try:
        conexao = sqlite3.connect('database2.bd')
        cursor = conexao.cursor()
        query = "SELECT * FROM Alunos WHERE matricula = ? AND cpf = ?"
        cursor.execute(query, (matricula, cpf))
        resultado = cursor.fetchone()

        conexao.close()

        if resultado is not None:  
            return True
        else:
            return False

    except Exception as e:
        print(f"Erro ao validar aluno: {e}")
        return False



def inserir_disciplina(nome, ano, semestre, professor):
    conexao = sqlite3.connect('database2.bd')
    cursor = conexao.cursor()
    cursor.execute("""
    INSERT INTO Disciplinas (Nome, Ano, Semestre, Professor)
    VALUES (?, ?, ?, ?)
    """, (nome, ano, semestre, professor))
    conexao.commit()

def listar_disciplinas():
    with sqlite3.connect('database2.bd') as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM Disciplinas")
        return cursor.fetchall()


def listar_disciplinas_dropbox():
    conexao = sqlite3.connect('database2.bd')
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome FROM disciplinas")
    disciplinas = cursor.fetchall()
    return disciplinas

def atualizar_disciplina(id, nome, ano, semestre, professor):
    conexao = sqlite3.connect('database2.bd')
    cursor = conexao.cursor()
    
    cursor.execute("""
    UPDATE Disciplinas
    SET nome = ?, ano = ?, Semestre = ?, Professor = ?
    WHERE id = ?
    """, (nome, ano, semestre, professor, id))
    conexao.commit()

def deletar_disciplina(id):
    conexao = sqlite3.connect('database2.bd')
    cursor = conexao.cursor()

    cursor.execute("DELETE FROM Disciplinas WHERE id = ?", (id,))
    conexao.commit()
    

def inserir_aluno(matricula, nome, cpf, telefone):
    conexao = sqlite3.connect('database2.bd')
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO Alunos (matricula, nome, cpf, telefone)
        VALUES (?, ?, ?, ?)
    """, (matricula, nome, cpf, telefone))
    conexao.commit()
    conexao.close()


def listar_alunos():
    conexao = sqlite3.connect('database2.bd')
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM Alunos")
    alunos = cursor.fetchall()
    conexao.close()
    return alunos


def atualizar_aluno(matricula,  nome, telefone):
    conexao = sqlite3.connect('database2.bd')
    cursor = conexao.cursor()
    cursor.execute("""
        UPDATE Alunos
        SET  nome = ?, telefone = ?
        WHERE matricula = ?
    """, ( nome, telefone, matricula))
    conexao.commit()
    conexao.close()


def deletar_aluno(matricula):
    conexao = sqlite3.connect('database2.bd')
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM Alunos WHERE matricula = ?", (matricula,))
    conexao.commit()
    conexao.close()


def inserir_prova(disciplina_id, aluno_matricula, sm1, sm2, av, avs, nf):
    conexao = sqlite3.connect('database2.bd')
    cursor = conexao.cursor()
    cursor.execute('''
        INSERT INTO provas 
        (disciplina_id, aluno_matricula, nota_sm1, nota_sm2, av, avs, nf) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (disciplina_id, aluno_matricula, sm1, sm2, av, avs, nf))
    conexao.commit()
    conexao.close()


def existe_prova(disciplina_id, aluno_matricula):
    conexao = sqlite3.connect('database2.bd')
    cursor = conexao.cursor()
    cursor.execute( '''SELECT COUNT(*) FROM provas WHERE disciplina_id = ? AND aluno_matricula = ?''',(disciplina_id, aluno_matricula))
    count = cursor.fetchone()[0]
    return count > 0

def listar_provas():
    conexao = sqlite3.connect('database2.bd')
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM provas')
    resultado = cursor.fetchall()
    conexao.close()
    return resultado

def atualizar_prova(id, disciplina_id, aluno_matricula, sm1, sm2, av, avs, nf):
    conexao = sqlite3.connect('database2.bd')
    cursor = conexao.cursor()
    cursor.execute('''
        UPDATE provas SET 
            disciplina_id = ?, aluno_matricula = ?, nota_sm1 = ?, nota_sm2 = ?, av = ?, avs = ?, nf = ?
        WHERE id = ?
    ''', (disciplina_id, aluno_matricula, sm1, sm2, av, avs, nf, id))
    conexao.commit()
    conexao.close()

def deletar_prova(id):
    conexao = sqlite3.connect('database2.bd')
    cursor = conexao.cursor()
    cursor.execute('DELETE FROM provas WHERE id = ?', (id,))
    conexao.commit()
    conexao.close()


def buscar_disciplina_por_id(id):
    conexao = sqlite3.connect('database2.bd')
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM disciplinas WHERE id = ?', (id,))
    resultado = cursor.fetchone()
    conexao.close()
    return resultado



def buscar_aluno_por_matricula(matricula):
    conexao = sqlite3.connect('database2.bd')
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM alunos WHERE matricula = ?', (matricula,))
    resultado = cursor.fetchone()
    conexao.close()
    return resultado
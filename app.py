import customtkinter as ctk
import sqlite3

ctk.set_appearance_mode('dark')

conn = sqlite3.connect("usuarios.db")
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL
    )
''')
conn.commit()
conn.close()

def validar_login():
    
    usuario = entry_usuario.get()
    senha = entry_senha.get()

    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND senha = ?", (usuario, senha))
    user = cursor.fetchone()
    
    conn.close()

    if user:
        status_login.configure(text="Login bem-sucedido!", text_color="green")
    else:
        status_login.configure(text="Usuário ou senha incorretos!", text_color="red")

def abrir_janela_cadastro():

    janela_cadastro = ctk.CTkToplevel(app)
    janela_cadastro.title("Cadastro de Usuário")
    janela_cadastro.geometry("300x250")

    ctk.CTkLabel(janela_cadastro, text="Novo Usuário:").pack(pady=5)
    entry_novo_usuario = ctk.CTkEntry(janela_cadastro, placeholder_text="Digite um usuário")
    entry_novo_usuario.pack(pady=5)

    ctk.CTkLabel(janela_cadastro, text="Nova Senha:").pack(pady=5)
    entry_nova_senha = ctk.CTkEntry(janela_cadastro, placeholder_text="Digite uma senha", show="*")
    entry_nova_senha.pack(pady=5)

    def cadastrar_usuario():
    
        novo_usuario = entry_novo_usuario.get()
        nova_senha = entry_nova_senha.get()

        if novo_usuario and nova_senha:
            conn = sqlite3.connect("usuarios.db")
            cursor = conn.cursor()

            try:
                cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (novo_usuario, nova_senha))
                conn.commit()
                status_cadastro.configure(text="Usuário cadastrado com sucesso!", text_color="green")
            except sqlite3.IntegrityError:
                status_cadastro.configure(text="Erro: Usuário já existe!", text_color="red")

            conn.close()
        else:
            status_cadastro.configure(text="Preencha todos os campos!", text_color="red")

    button_confirmar = ctk.CTkButton(janela_cadastro, text="Cadastrar", command=cadastrar_usuario)
    button_confirmar.pack(pady=10)

    status_cadastro = ctk.CTkLabel(janela_cadastro, text="")
    status_cadastro.pack(pady=5)

app = ctk.CTk()
app.title('Sistema de Login')
app.geometry('300x350')

ctk.CTkLabel(app, text='Usuário:').pack(pady=5)
entry_usuario = ctk.CTkEntry(app, placeholder_text='Digite seu usuário')
entry_usuario.pack(pady=5)

ctk.CTkLabel(app, text='Senha:').pack(pady=5)
entry_senha = ctk.CTkEntry(app, placeholder_text='Digite sua senha', show="*")
entry_senha.pack(pady=5)

button_login = ctk.CTkButton(app, text='Login', command=validar_login)
button_login.pack(pady=10)

status_login = ctk.CTkLabel(app, text='')
status_login.pack(pady=10)

button_cadastro = ctk.CTkButton(app, text='Criar Conta', command=abrir_janela_cadastro)
button_cadastro.pack(pady=10)

app.mainloop()

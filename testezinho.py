import tkinter as tk
from tkinter import filedialog
from cryptography.fernet import Fernet
import os

# Variáveis globais
global fernet, key, caminho_arquivo
fernet = None
key = None
caminho_arquivo = None

def escolher_arquivo():
    """Seleciona um arquivo para criptografia ou descriptografia."""
    global caminho_arquivo
    caminho_arquivo = filedialog.askopenfilename()
    if caminho_arquivo:
        label_arquivo.config(text=f"Arquivo selecionado: {caminho_arquivo}")

def encriptografar():
    """Criptografa o arquivo selecionado e salva a chave automaticamente."""
    global key, fernet, caminho_arquivo
    if not caminho_arquivo:
        label_arquivo.config(text="Erro: Nenhum arquivo selecionado!")
        return

    key = Fernet.generate_key()
    fernet = Fernet(key)

    with open(caminho_arquivo, "rb") as file:
        dados = file.read()

    dados_encriptados = fernet.encrypt(dados)
    
    with open(caminho_arquivo + ".enc", "wb") as file:
        file.write(dados_encriptados)

    # Salvar a chave
    caminho_key = caminho_arquivo + ".key"
    with open(caminho_key, "wb") as file:
        file.write(key)

    label_arquivo.config(text="Arquivo encriptografado com sucesso!")

def descriptografar():
    """Descriptografa um arquivo .enc usando a chave correspondente."""
    global fernet, key, caminho_arquivo

    if not caminho_arquivo:
        label_arquivo.config(text="Erro: Nenhum arquivo selecionado!")
        return
    
    if not caminho_arquivo.endswith(".enc"):
        label_arquivo.config(text="Erro: Selecione um arquivo .enc!")
        return

    # Tentar carregar a chave automaticamente
    caminho_key = os.path.splitext(caminho_arquivo)[0] + ".key"
    if os.path.exists(caminho_key):
        with open(caminho_key, "rb") as file:
            key = file.read()
        fernet = Fernet(key)
    else:
        label_arquivo.config(text="Erro: Chave não encontrada!")
        return

    try:
        with open(caminho_arquivo, "rb") as file:
            dados_encriptados = file.read()

        dados_descriptografados = fernet.decrypt(dados_encriptados)

        caminho_descriptografado = caminho_arquivo.replace(".enc", ".dec")
        with open(caminho_descriptografado, "wb") as file:
            file.write(dados_descriptografados)

        label_arquivo.config(text="Arquivo descriptografado com sucesso!")
    except Exception:
        label_arquivo.config(text="Erro: Arquivo inválido ou chave incorreta!")

# Criando a interface gráfica
window = tk.Tk()
window.title("Criptografia de Arquivos")
window.geometry("700x500")

# Botões e labels
botao_selecionar = tk.Button(window, text="Escolher Arquivo", bg="#085178", fg="blue", width=25, height=2, command=escolher_arquivo)
botao_selecionar.pack(pady=10)

label_arquivo = tk.Label(window, text="Nenhum arquivo selecionado")
label_arquivo.pack()

botao_encriptografar = tk.Button(window, text="Encriptografar", bg="#0077b6", fg="blue", width=25, height=2, command=encriptografar)
botao_encriptografar.pack(pady=10)

botao_descriptografar = tk.Button(window, text="Descriptografar", bg="#62C4D5", fg="blue", width=25, height=2, command=descriptografar)
botao_descriptografar.pack(pady=10)

# Iniciar o loop da interface gráfica
window.mainloop()
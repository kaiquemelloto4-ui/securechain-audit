import json
import os
import getpass
import bcrypt
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from blockchain.blockchain import adicionar_bloco

USERS_FILE = os.path.join(os.path.dirname(__file__), "usuarios.json")


def carregar_usuarios():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as arquivo:
        return json.load(arquivo)


def salvar_usuarios(usuarios):
    with open(USERS_FILE, "w") as arquivo:
        json.dump(usuarios, arquivo, indent=4)


def cadastrar_usuario():
    usuarios = carregar_usuarios()

    nome = input("Novo usuário: ").strip()
    perfil = input("Perfil [admin/analista/visitante]: ").strip().lower()

    if perfil not in ["admin", "analista", "visitante"]:
        print("Perfil inválido.")
        return

    if nome in usuarios:
        print("Usuário já existe.")
        return

    senha = getpass.getpass("Senha: ")
    senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()

    usuarios[nome] = {
        "senha": senha_hash,
        "perfil": perfil
    }

    salvar_usuarios(usuarios)
    adicionar_bloco(f"Usuário criado: {nome} com perfil {perfil}")
    print("[OK] Usuário cadastrado.")


def login():
    usuarios = carregar_usuarios()

    nome = input("Usuário: ").strip()
    senha = getpass.getpass("Senha: ")

    if nome not in usuarios:
        adicionar_bloco(f"Tentativa de login negada para usuário inexistente: {nome}")
        print("Acesso negado.")
        return

    senha_hash = usuarios[nome]["senha"].encode()

    if bcrypt.checkpw(senha.encode(), senha_hash):
        perfil = usuarios[nome]["perfil"]
        adicionar_bloco(f"Login realizado: {nome} perfil {perfil}")
        print(f"[OK] Login autorizado. Perfil ativo: {perfil}")
    else:
        adicionar_bloco(f"Tentativa de acesso negada para usuário: {nome}")
        print("Senha incorreta.")


def menu():
    while True:
        print("\nSECURECHAIN AUTH")
        print("1 - Cadastrar usuário")
        print("2 - Login")
        print("3 - Sair")

        opcao = input("Opção: ")

        if opcao == "1":
            cadastrar_usuario()
        elif opcao == "2":
            login()
        elif opcao == "3":
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()

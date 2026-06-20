import json
import hashlib
import os
from datetime import datetime

CHAIN_FILE = os.path.join(os.path.dirname(__file__), "chain.json")


def calcular_hash(bloco):
    bloco_copia = bloco.copy()
    bloco_copia.pop("hash_atual", None)
    bloco_string = json.dumps(bloco_copia, sort_keys=True).encode()
    return hashlib.sha256(bloco_string).hexdigest()


def carregar_chain():
    if not os.path.exists(CHAIN_FILE) or os.path.getsize(CHAIN_FILE) == 0:
        bloco_genesis = {
            "id": 0,
            "timestamp": datetime.now().isoformat(),
            "evento": "Bloco gênesis criado",
            "hash_anterior": "0",
            "hash_atual": ""
        }
        bloco_genesis["hash_atual"] = calcular_hash(bloco_genesis)
        salvar_chain([bloco_genesis])
        return [bloco_genesis]

    with open(CHAIN_FILE, "r") as arquivo:
        return json.load(arquivo)


def salvar_chain(chain):
    with open(CHAIN_FILE, "w") as arquivo:
        json.dump(chain, arquivo, indent=4)


def adicionar_bloco(evento):
    chain = carregar_chain()
    ultimo = chain[-1]

    novo_bloco = {
        "id": len(chain),
        "timestamp": datetime.now().isoformat(),
        "evento": evento,
        "hash_anterior": ultimo["hash_atual"],
        "hash_atual": ""
    }

    novo_bloco["hash_atual"] = calcular_hash(novo_bloco)
    chain.append(novo_bloco)
    salvar_chain(chain)

    print(f"[OK] Bloco criado: {evento}")


def validar_chain():
    chain = carregar_chain()

    for i in range(len(chain)):
        bloco = chain[i]
        hash_recalculado = calcular_hash(bloco)

        if bloco["hash_atual"] != hash_recalculado:
            print(f"[ALERTA] Bloco {bloco['id']} foi adulterado.")
            return False

        if i > 0:
            bloco_anterior = chain[i - 1]
            if bloco["hash_anterior"] != bloco_anterior["hash_atual"]:
                print(f"[ALERTA] Quebra de encadeamento no bloco {bloco['id']}.")
                return False

    print("[OK] Blockchain íntegra.")
    return True


if __name__ == "__main__":
    carregar_chain()
    adicionar_bloco("Teste manual de criação de bloco")
    validar_chain()

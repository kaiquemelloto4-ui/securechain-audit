import subprocess
import os
from datetime import datetime
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from blockchain.blockchain import adicionar_bloco

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RELATORIO_DIR = os.path.join(BASE_DIR, "auditoria", "relatorios")


def executar_comando(comando):
    try:
        resultado = subprocess.check_output(comando, shell=True, text=True, stderr=subprocess.STDOUT)
        return resultado
    except subprocess.CalledProcessError as erro:
        return erro.output


def gerar_relatorio():
    data = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    arquivo_relatorio = os.path.join(RELATORIO_DIR, f"auditoria_{data}.txt")

    comandos = {
        "Usuários conectados - who": "who",
        "Histórico de logins - last": "last -n 10",
        "Portas e serviços em escuta - ss": "ss -tulpn",
        "Interfaces de rede - ip a": "ip a"
    }

    with open(arquivo_relatorio, "w") as arquivo:
        arquivo.write("RELATÓRIO DE AUDITORIA DO SISTEMA OPERACIONAL\n")
        arquivo.write(f"Data: {datetime.now().isoformat()}\n\n")

        for titulo, comando in comandos.items():
            arquivo.write("=" * 70 + "\n")
            arquivo.write(titulo + "\n")
            arquivo.write("=" * 70 + "\n")
            arquivo.write(executar_comando(comando))
            arquivo.write("\n\n")

    adicionar_bloco(f"Relatório de auditoria gerado: {arquivo_relatorio}")
    print(f"[OK] Relatório gerado em: {arquivo_relatorio}")


if __name__ == "__main__":
    gerar_relatorio()

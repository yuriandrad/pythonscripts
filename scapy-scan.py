#!/usr/bin/env python3
import sys
from scapy.all import *
import argparse

# Cores para o terminal
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"
YELLOW = "\033[93m"

# 25 portas mais conhecidas (adaptar se necessário)
portas_comuns = [21, 22, 23, 25, 53, 80, 110, 139, 443, 445, 1433, 1521, 3306, 3389, 5432, 5900, 8080, 8443, 10000, 27017, 27018, 5000, 9000, 9090, 9200]

parser = argparse.ArgumentParser(description="Scanner de portas TCP com Scapy.")
parser.add_argument("alvo", nargs="?", default="", help="Endereço IP ou nome de domínio do alvo")
parser.add_argument("-p", "--portas", nargs="+", type=int, help="Portas a serem verificadas (separadas por espaço)") # Sem valor default
parser.add_argument("-v", "--verbose", action="store_true", help="Ativar modo verbose")
args = parser.parse_args()

alvo = args.alvo
portas = args.portas
verbose = args.verbose

if not alvo and not portas:  # Nenhum argumento fornecido
    print(f"{YELLOW}Modo de uso:{RESET}")
    print(f"  python {sys.argv[0]} <alvo> [-p <porta1> <porta2> ...] [-v]")
    print(f"  Exemplo: python {sys.argv[0]} 192.168.1.100 -p 80 443")
    print(f"{YELLOW}Escaneando as 25 portas mais comuns em localhost...{RESET}")
    alvo = "localhost"
    portas = portas_comuns # Usa as portas comuns como padrão

elif not portas:  # Apenas o alvo foi fornecido
    print(f"{YELLOW}Escaneando as 25 portas mais comuns em {alvo}...{RESET}")
    portas = portas_comuns # Usa as portas comuns como padrão

try:
    sr(IP(dst=alvo), timeout=2, verbose=0)
    conf.verb = 0 if not verbose else 1

    pacote = IP(dst=alvo)/TCP(dport=portas, flags="S")
    resp, noresp = sr(pacote, timeout=5)

    for enviado, recebido in resp:
        if recebido[TCP].flags == "SA":
            porta_aberta = recebido[TCP].sport
            print(f"{GREEN}Porta {porta_aberta} ABERTA{RESET}")
        elif verbose:
            porta_fechada = enviado[TCP].dport
            print(f"{RED}Porta {porta_fechada} FECHADA ou FILTRADA{RESET}")

except Exception as e:
    print(f"Erro: {e}")

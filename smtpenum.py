#!/usr/bin/python3
import socket
import sys

#Validação do programa
if len(sys.argv) != 3:
    print("Modo de uso: python3 smtpenum.py IP usuario")
    sys.exit(0)
#!= representa DIFERENTE

# Cria o socket TCP
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    tcp.connect((sys.argv[1], 25))  # Conecta ao IP fornecido na porta 25 (SMTP)
except Exception as e:
    print(f"Erro ao conectar: {e}")
    sys.exit(1)

# Recebe o banner do servidor SMTP
banner = tcp.recv(1024).decode(errors='ignore')
print(banner)

# Enviando comando VRFY para verificar o usuário
tcp.send(f"VRFY {sys.argv[2]}\r\n".encode())
#\r\n pula uma linha

# Recebe a resposta do servidor
user = tcp.recv(1024).decode(errors='ignore')
print(user)

# Fecha a conexão
tcp.close()

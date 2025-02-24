#!/usr/bin/python3
import socket
import sys
import re

if len(sys.argv) != 2:
    print("Modo de uso: python3 smtpenum.py IP")
    sys.exit(0)

try:
    with open("lista.txt", "r") as file:
        for linha in file:
            linha = linha.strip()  

       
            tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                tcp.connect((sys.argv[1], 25))
                banner = tcp.recv(1024).decode(errors='ignore')
                
                tcp.send(f"VRFY {linha}\r\n".encode())

              
                user = tcp.recv(1024).decode(errors='ignore')

              
                if re.search(r"^252", user):
                    user_clean = re.sub(r"252 2.0.0", "", user).strip()
                    print(f"Usuário encontrado: {user_clean}")

            except Exception as e:
                print(f"Erro ao conectar ou enviar dados: {e}")

            finally:
                tcp.close() 

except FileNotFoundError:
    print("Erro: Arquivo 'lista.txt' não encontrado.")
    sys.exit(1)

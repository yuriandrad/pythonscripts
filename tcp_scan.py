#!/usr/bin/python

import socket

# Solicita ao usuário o IP do servidor
ip = input("Digite o IP do servidor FTP: ")

# Cria o socket TCP
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.connect((ip, 21))

print("Conectando ao Servidor...")
banner = tcp.recv(1024)  # Quantidade de bytes recebidos
print(banner.decode())

print("Enviando usuario...")
tcp.send(b"USER ftp\r\n")
user = tcp.recv(1024)
print(user.decode())

print("Enviando a senha...")
tcp.send(b"PASS ftp\r\n")
pw = tcp.recv(1024)
print(pw.decode())

if b"530" in pw:  # Se a primeira tentativa falhar, fecha a conexão e tenta anonymous:anonymous
    print("Primeira tentativa falhou. Fechando conexão e tentando login como anonymous...")
    tcp.close()
    
    # Nova conexão
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.connect((ip, 21))
    
    print("Conectando ao Servidor...")
    banner = tcp.recv(1024)
    print(banner.decode())
    
    tcp.send(b"USER anonymous\r\n")
    user = tcp.recv(1024)
    print(user.decode())
    
    tcp.send(b"PASS anonymous\r\n")
    pw = tcp.recv(1024)
    print(pw.decode())

print("Enviando comando...")
tcp.send(b"PWD\r\n")
cmd = tcp.recv(2048)
print(cmd.decode())

# Fecha a conexão
tcp.close()

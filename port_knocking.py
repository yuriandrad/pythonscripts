import socket
import time

def port_knock(host, ports, delay=0.5, timeout=3):
    """
    Envia pacotes TCP para uma sequência de portas em um host específico,
    mudando a porta de origem a cada batida.
    
    Parâmetros:
        host (str): Endereço IP ou domínio do host alvo.
        ports (list): Lista de portas a serem "batidas" na sequência.
        delay (float): Intervalo entre cada tentativa de conexão.
        timeout (int): Tempo de timeout para cada tentativa de conexão.
    """
    for port in ports:
        try:
            # Cria um socket TCP
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)  # Define o timeout
            
            # Gera uma porta de origem aleatória
            source_port = 49152 + (port % 16384)  
            
            # Faz o bind do socket à porta de origem
            sock.bind(('', source_port))
            
            # Tenta conectar à porta
            sock.connect((host, port))
            print(f"Batendo na porta {port} usando a porta de origem {source_port}")
            
            # Fecha a conexão
            sock.close()
            
            # Aguarda antes de bater na próxima porta
            time.sleep(delay)
        
        except socket.error as e:
            print(f"Erro ao bater na porta {port}: {e}")
            pass

if __name__ == "__main__":
    host = ""  #IP do servidor alvo
  
    ports = []  # Sequência de portas para a tentativa de autenticação

    delay = 0.5  # Atraso das conexões em segundos

    timeout = 3  # Tempo de timeout para evitar erros frequentes

    # Executa o port knocking
    port_knock(host, ports, delay, timeout)

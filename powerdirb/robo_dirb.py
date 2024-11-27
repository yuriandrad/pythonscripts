import subprocess
import os
from colorama import Fore, Style, init

# Inicializa cores no terminal
init(autoreset=True)

# Configurações
URLS_FILE = "urls.txt"  # Arquivo com os domínios
WORDLIST_FILE = "wordlist.txt"  # Arquivo com a wordlist
OUTPUT_FILE = "resultados.txt"  # Arquivo único para salvar os resultados

# Função para exibir a introdução com ASCII Art 
def print_intro():
    ascii_art = f"""
{Fore.MAGENTA}

░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓███████▓▒░ ░▒▓██████▓▒░       ░▒▓███████▓▒░░▒▓█▓▒░▒▓███████▓▒░░▒▓███████▓▒░  
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓███████▓▒░░▒▓███████▓▒░  
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓███████▓▒░ ░▒▓██████▓▒░       ░▒▓███████▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░  
                                                                                                             
{Fore.CYAN}                         Automated Directory Mapper Tool
{Style.RESET_ALL}"""
    print(ascii_art)

# Função para verificar se `dirb` está instalado
def check_dirb():
    try:
        subprocess.run(["dirb", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except FileNotFoundError:
        return False

# Função para executar o dirb em uma URL e salvar o resultado no arquivo principal
def run_dirb(url, output_file):
    try:
        print(f"{Fore.YELLOW}[PROCESSANDO]{Style.RESET_ALL} Executando dirb em: {url}")
        
        # Executa o dirb
        result = subprocess.run(
            ["dirb", url, WORDLIST_FILE],
            capture_output=True,
            text=True,
            timeout=300
        )

        # Salva os resultados no arquivo de saída
        with open(output_file, "a") as outfile:
            outfile.write(f"\n{'=' * 50}\n")
            outfile.write(f"Resultados para: {url}\n")
            outfile.write(f"{'=' * 50}\n")
            outfile.write(result.stdout)
            outfile.write("\n")
        
        print(f"{Fore.GREEN}[SUCESSO]{Style.RESET_ALL} Resultado salvo no arquivo principal.")
    
    except subprocess.TimeoutExpired:
        print(f"{Fore.RED}[TIMEOUT]{Style.RESET_ALL} O scan para {url} demorou muito e foi cancelado.")
    except Exception as e:
        print(f"{Fore.RED}[ERRO]{Style.RESET_ALL} Falha ao executar dirb em {url}: {e}")

# Função principal
def main():
    print_intro()

    if not os.path.exists(URLS_FILE) or not os.path.exists(WORDLIST_FILE):
        print(f"{Fore.RED}[ERRO]{Style.RESET_ALL} Arquivos {URLS_FILE} ou {WORDLIST_FILE} não encontrados!")
        return

    if not check_dirb():
        print(f"{Fore.RED}[ERRO]{Style.RESET_ALL} A ferramenta 'dirb' não está instalada. Instale com:")
        print(f"  {Fore.YELLOW}sudo apt install dirb{Style.RESET_ALL}")
        return

    # Lê as URLs do arquivo
    with open(URLS_FILE, "r") as urls:
        url_list = [f"https://{url.strip()}" for url in urls if url.strip()]

    # Limpa ou cria o arquivo de saída
    with open(OUTPUT_FILE, "w") as outfile:
        outfile.write("Resultados do scan com dirb\n")
        outfile.write("=" * 50 + "\n")

    # Executa o dirb para cada URL
    for url in url_list:
        run_dirb(url, OUTPUT_FILE)

    print(f"\n{Fore.GREEN}[FINALIZADO]{Style.RESET_ALL} Todos os resultados foram salvos no arquivo: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()

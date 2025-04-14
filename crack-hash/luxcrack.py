#!/usr/bin/python3
import crypt
import argparse
import subprocess
import sys
from itertools import product
from string import ascii_letters, digits, punctuation
from colorama import init, Fore, Back, Style

# Inicializa colorama
init(autoreset=True)

def print_banner():
    banner = f"""{Fore.YELLOW}
    ██╗     ██╗   ██╗██╗  ██╗ ██████╗██████╗  █████╗  ██████╗██╗  ██╗
    ██║     ██║   ██║╚██╗██╔╝██╔════╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝
    ██║     ██║   ██║ ╚███╔╝ ██║     ██████╔╝███████║██║     █████╔╝ 
    ██║     ██║   ██║ ██╔██╗ ██║     ██╔══██╗██╔══██║██║     ██╔═██╗ 
    ███████╗╚██████╔╝██╔╝ ██╗╚██████╗██║  ██║██║  ██║╚██████╗██║  ██╗
    ╚══════╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
    {Style.RESET_ALL}"""
    print(banner)

def colored_print(message, color=Fore.WHITE, bright=False):
    """Imprime mensagem colorida"""
    style = Style.BRIGHT if bright else Style.NORMAL
    print(f"{style}{color}{message}{Style.RESET_ALL}")

def crack_with_wordlist(hashed_password, salt, wordlist_path):
    """Tenta quebrar a senha usando uma wordlist"""
    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            total_words = sum(1 for _ in f)
            f.seek(0)
            
            colored_print(f"[*] Wordlist carregada: {wordlist_path}", Fore.CYAN)
            colored_print(f"[*] Total de palavras: {total_words}", Fore.CYAN)
            colored_print("[*] Iniciando teste...", Fore.BLUE)
            
            for i, word in enumerate(f, 1):
                word = word.strip()
                if i % 1000 == 0:
                    progress = (i / total_words) * 100
                    sys.stdout.write(f"\r{Fore.YELLOW}[*] Progresso: {progress:.2f}% ({i}/{total_words}){Style.RESET_ALL}")
                    sys.stdout.flush()
                
                if crypt.crypt(word, salt) == hashed_password:
                    print("\n")
                    return word
                    
    except FileNotFoundError:
        colored_print(f"[-] ERRO: Wordlist não encontrada: {wordlist_path}", Fore.RED)
    except Exception as e:
        colored_print(f"[-] ERRO: {str(e)}", Fore.RED)
    return None

def crack_with_john(hashed_password):
    """Usa John the Ripper para quebrar a senha"""
    try:
        # Cria arquivo temporário no formato que John espera
        with open("temp_john_hash.txt", "w") as f:
            f.write(f"temp_user:{hashed_password}")
        
        colored_print("[*] Executando John the Ripper...", Fore.MAGENTA)
        colored_print("[*] Isso pode levar algum tempo...", Fore.MAGENTA)
        
        # Executa John
        subprocess.run(["john", "--format=crypt", "temp_john_hash.txt"], check=True)
        
        # Mostra resultados
        result = subprocess.run(["john", "--show", "temp_john_hash.txt"], 
                               capture_output=True, text=True)
        
        if "password hash cracked" in result.stdout.lower():
            colored_print("[+] SENHA ENCONTRADA COM JOHN THE RIPPER!", Fore.GREEN, bright=True)
            print(result.stdout)
            return result.stdout.split(":")[1]
        else:
            colored_print("[-] John não conseguiu quebrar a senha", Fore.YELLOW)
            return None
            
    except subprocess.CalledProcessError as e:
        colored_print(f"[-] Erro ao executar John: {e}", Fore.RED)
    except FileNotFoundError:
        colored_print("[-] John the Ripper não está instalado", Fore.RED)
    return None

def main():
    print_banner()
    
    parser = argparse.ArgumentParser(description='Quebrador Avançado de Senhas Linux')
    parser.add_argument('hash', help='Hash completo da senha (ex: $6$salt$hash)')
    parser.add_argument('--wordlist', help='Caminho para wordlist')
    parser.add_argument('--john', action='store_true', help='Usar John the Ripper')
    
    args = parser.parse_args()
    
    # Extrai o salt do hash (formato: $id$salt$hash)
    if args.hash.count('$') >= 3:
        salt = '$' + args.hash.split('$')[1] + '$' + args.hash.split('$')[2] + '$'
    else:
        colored_print("[-] Formato de hash inválido", Fore.RED)
        return
    
    colored_print(f"[*] Hash analisado: {args.hash}", Fore.CYAN)
    colored_print(f"[*] Salt extraído: {salt}", Fore.CYAN)
    
    if args.wordlist:
        result = crack_with_wordlist(args.hash, salt, args.wordlist)
        if result:
            colored_print(f"\n[+] SENHA ENCONTRADA: {result}", Fore.GREEN, bright=True)
        else:
            colored_print("\n[-] Senha não encontrada na wordlist", Fore.RED)
    elif args.john:
        result = crack_with_john(args.hash)
        if not result:
            colored_print("[-] Nenhuma senha encontrada com John", Fore.YELLOW)
    else:
        colored_print("[!] Selecione um método: --wordlist ou --john", Fore.RED)

if __name__ == "__main__":
    main()

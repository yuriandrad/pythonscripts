import httpx
import asyncio
from pathlib import Path
from datetime import datetime
import platform

# Cores 
COLORS = {
    'green': '\033[92m',
    'red': '\033[91m',
    'yellow': '\033[94m',
    'blue': '\033[94m',
    'magenta': '\033[95m',
    'cyan': '\033[96m',
    'white': '\033[97m',
    'reset': '\033[0m',
    'bold': '\033[1m',
    'underline': '\033[4m'
}

def print_banner():
    """Exibe um banner estilizado"""
    banner = f"""
{COLORS['cyan']}{'='*60}
{COLORS['bold']}{COLORS['magenta']}          ___  __  ____  ____  ____  ____  ____          
         / __)/  \(  _ \(  __)(  _ \(  __)(  _ \         
        ( (__(  O ))   / ) _)  )   / ) _)  )   /         
         \___)\__/(__\_)(____)(__\_)(____)(__\_)         
{COLORS['reset']}{COLORS['cyan']}{'='*60}
{COLORS['reset']}{COLORS['bold']}        URL STATUS CHECKER - v1.0 | {datetime.now().strftime('%d/%m/%Y %H:%M')}
{COLORS['cyan']}{'='*60}{COLORS['reset']}
"""
    print(banner)

def print_system_info():
    """Exibe informações do sistema"""
    print(f"{COLORS['yellow']}{COLORS['bold']}Sistema Operacional: {COLORS['reset']}{platform.system()} {platform.release()}")
    print(f"{COLORS['yellow']}{COLORS['bold']}Python Version: {COLORS['reset']}{platform.python_version()}")
    print(f"{COLORS['yellow']}{COLORS['bold']}HTTPX Version: {COLORS['reset']}{httpx.__version__}")
    print(f"{COLORS['cyan']}{'-'*60}{COLORS['reset']}\n")

async def check_url(client, url):
    """Verifica o status de uma URL"""
    try:
        response = await client.get(url, timeout=10.0, follow_redirects=True)
        return (url, response.status_code, None)
    except httpx.HTTPStatusError as e:
        return (url, e.response.status_code, str(e))
    except Exception as e:
        return (url, None, str(e))

def format_status(status):
    """Formata o código de status com cores"""
    if status and status < 400:
        return f"{COLORS['green']}{status}{COLORS['reset']}"
    elif status:
        return f"{COLORS['red']}{status}{COLORS['reset']}"
    else:
        return f"{COLORS['red']}ERROR{COLORS['reset']}"

async def main():
    # Configurações
    arquivo_urls = 'urls.txt'  # Arquivo com uma URL por linha
    
    # Exibir banner e informações
    print_banner()
    print_system_info()
    
    # Lê
    try:
        urls = [url.strip() for url in Path(arquivo_urls).read_text().splitlines() if url.strip()]
        print(f"{COLORS['bold']}Verificando {len(urls)} URLs...{COLORS['reset']}\n")
    except FileNotFoundError:
        print(f"{COLORS['red']}Erro: Arquivo '{arquivo_urls}' não encontrado!{COLORS['reset']}")
        return
    
    up = []
    down = []
    
    # Verificar URLs
    async with httpx.AsyncClient() as client:
        tasks = [check_url(client, url) for url in urls]
        results = await asyncio.gather(*tasks)
        
        for url, status, error in results:
            if status and status < 400:
                up.append((url, status))
            else:
                down.append((url, error or status))

    # Exibir resultados
    print(f"\n{COLORS['bold']}{COLORS['underline']}RESULTADOS:{COLORS['reset']}\n")
    
    print(f"{COLORS['bold']}{COLORS['green']}=== URLs UP ({len(up)}) ==={COLORS['reset']}")
    for url, status in up:
        print(f"  {format_status(status)} - {url}")
    
    print(f"\n{COLORS['bold']}{COLORS['red']}=== URLs DOWN ({len(down)}) ==={COLORS['reset']}")
    for url, reason in down:
        if isinstance(reason, int):
            print(f"  {format_status(reason)} - {url}")
        else:
            print(f"  {format_status(None)} - {url} ({reason})")
    
    # Estatísticas
    percent_up = (len(up) / len(urls)) * 100 if urls else 0
    print(f"\n{COLORS['bold']}{COLORS['cyan']}=== ESTATÍSTICAS ==={COLORS['reset']}")
    print(f"  Total de URLs: {len(urls)}")
    print(f"  URLs UP: {COLORS['green']}{len(up)} ({percent_up:.1f}%){COLORS['reset']}")
    print(f"  URLs DOWN: {COLORS['red']}{len(down)}{COLORS['reset']}")
    print(f"\n{COLORS['cyan']}{'='*60}{COLORS['reset']}")

if __name__ == "__main__":
    asyncio.run(main())

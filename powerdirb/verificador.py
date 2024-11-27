import os

# Configurações
RESULTADOS_FILE = "resultados.txt"  # Arquivo de resultados gerado pelo dirb
OUTPUT_FILE = "urls_com_resultados.txt"  # Arquivo com URLs que possuem algo relevante
ERRO_PADRAO = "NOT FOUND"  # Indicador de falha (case insensitive)

# Função para processar o arquivo de resultados
def processar_resultados():
    if not os.path.exists(RESULTADOS_FILE):
        print(f"[ERRO] Arquivo de resultados '{RESULTADOS_FILE}' não encontrado!")
        return

    # Abre o arquivo de resultados para leitura
    with open(RESULTADOS_FILE, "r") as infile:
        linhas = infile.readlines()

    # Lista para armazenar URLs válidas
    urls_validas = []
    url_atual = None
    possui_resultado = False

    for linha in linhas:
        # Identifica onde começam as URLs testadas
        if linha.startswith("--> Testing:"):
            # Se havia uma URL anterior sem erros, adiciona à lista de válidas
            if url_atual and possui_resultado:
                urls_validas.append(url_atual)
            # Atualiza para a nova URL
            url_atual = linha.strip().replace("--> Testing: ", "")
            possui_resultado = False  # Reseta o indicador de resultado válido
        
        # Verifica se a linha atual contém algo que não seja erro
        if ERRO_PADRAO.lower() not in linha.lower() and "CODE:" in linha:
            possui_resultado = True

    # Adiciona a última URL processada, caso ela tenha resultados válidos
    if url_atual and possui_resultado:
        urls_validas.append(url_atual)

    # Salva as URLs válidas no arquivo de saída
    if urls_validas:
        with open(OUTPUT_FILE, "w") as outfile:
            for url in urls_validas:
                outfile.write(url + "\n")
        print(f"[SUCESSO] URLs válidas salvas em '{OUTPUT_FILE}'.")
    else:
        print("[AVISO] Nenhuma URL válida encontrada.")

# Função principal
def main():
    processar_resultados()

if __name__ == "__main__":
    main()

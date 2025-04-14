Pré-requisitos
Python 3.x

John the Ripper (opcional, para modo --john)

bash
Copy
# Clonar o repositório
git clone https://github.com/seuusuario/quebrador-senhas-linux.git
cd quebrador-senhas-linux

# Instalar dependências
pip install colorama
Como Usar
Sintaxe Básica
bash
Copy
python3 quebrador_senhas.py <hash> [--wordlist CAMINHO] [--john]
Exemplos
Ataque com wordlist:

bash
Copy
python3 quebrador_senhas.py '$6$salt$hash' --wordlist rockyou.txt
Ataque com John the Ripper:

bash
Copy
python3 quebrador_senhas.py '$6$salt$hash' --john
Opções de Linha de Comando
Opção	Descrição
hash	Hash completo da senha para quebrar
--wordlist	Caminho para arquivo de wordlist
--john	Usar John the Ripper ao invés

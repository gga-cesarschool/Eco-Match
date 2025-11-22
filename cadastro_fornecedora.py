# Importação das bibliotecas
import os, json, bcrypt #1-Operações do sistema 2- Para leitura e escrita de dados em formato json 3-criptografia/validação
from utils import validar_cnpj 
from pathlib import Path #importação com segurança pra usar diretórios 

ROOT_FOLDER = Path(__file__).parent #pra definir a pasta atual
INFO_EMPRESAS_FORNECEDORAS = ROOT_FOLDER / 'banco_de_dados' / 'info_empresas_fornecedoras.json' #caminho até o json. Os dados estarão no BD

#Carregar/ salvar 
def carregar_empresas(): #Função de carregamento dos dados das empresas
    if os.path.exists(INFO_EMPRESAS_FORNECEDORAS): # verificação do json
        with open(INFO_EMPRESAS_FORNECEDORAS, "r", encoding="utf-8") as f: #abertura do arquivo para leitura
            try: 
                return json.load(f)
            except json.JSONDecodeError: 
                return {} #Try -> tenta ler o json e return --> retorna em forma de dicionário
    return {} #Caso n tenha um arquivo => dicionário vazio

def salvar_empresas(empresas):
    with open(INFO_EMPRESAS_FORNECEDORAS, "w", encoding="utf-8") as f: #abre o json (utf-8 para nossa linguagem, acentuação e afins)
        json.dump(empresas, f, indent=4, ensure_ascii=False) # salva os dados em json, formatando com identação


#Sistema EcoMatch

def sistema_ecomatch():
    empresas = carregar_empresas()

    while True:
        print(" === Bem-vindo ao Sistema Eco-Match! ===")
        print("1. Cadastrar Empresa")
        print("2. Validar Cadastro")
        print("3. Listar empresas")
        print("4. Sair")
        opcao = input("Escolha uma opção: ")

        #Cadastro das empresas 
        if opcao == "1":
            print("=== CADASTRO DE EMPRESA ===")
            nome = input("Informe o nome da empresa: ")
            cnpj = input("Informe o CNPJ: ")

            if not validar_cnpj(cnpj):
                print(" CNPJ inválido! Tente novamente.")
                continue

            if cnpj in empresas:
                print(" CNPJ já cadastrado!")
                continue

            email = input("Informe o e-mail: ")
            telefone = input("Informe o telefone de contato: ")
            senha_plana = input("Senha: ")

            # Criptografia da senha usando o bcrypt
            senha_hash = bcrypt.hashpw(senha_plana.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            empresas[cnpj] = { # armazenando os dados no dicionario
                "nome": nome,
                "email": email,
                "telefone": telefone,
                "senha": senha_hash    # <-- senha criptografada
            }

            salvar_empresas(empresas)
            empresas = carregar_empresas()
            print(" Empresa cadastrada com sucesso!")

        #Validação do cadastro
        elif opcao == "2":
            print("=== VALIDAR CADASTRO ===")
            cnpj = input("CNPJ: ")
            senha = input("Senha: ")

            if cnpj not in empresas:
                print(" CNPJ ou senha incorretos.")
                continue

            senha_hash_salva = empresas[cnpj]["senha"].encode('utf-8') #recuperação da senha criptografada --> Conversão para bytes

            # Verificação da senha criptografada
            if bcrypt.checkpw(senha.encode('utf-8'), senha_hash_salva): #comparação de senha inserida e senha criptografada
                print(f" O seu cadastro está validado com sucesso! Bem-vindo(a), {empresas[cnpj]['nome']}.")
            else:
                print(" CNPJ ou senha incorretos.")

        # Listagem de empresas
        elif opcao == "3":
            print("=== EMPRESAS CADASTRADAS ===")
            if not empresas:
                print("Nenhuma empresa cadastrada.")
            else:
                for cnpj, dados in empresas.items():
                    print(f"{dados['nome']} - {cnpj} - {dados['email']} - {dados['telefone']}")

        #Saída
        elif opcao == "4":
            print("Encerrando o sistema... ")
            break

        else:
            print(" Opção inválida. Tente novamente.")


if __name__ == "__main__": #Execução do sistema somente se o arquivo for rodado de forma direta
    sistema_ecomatch()

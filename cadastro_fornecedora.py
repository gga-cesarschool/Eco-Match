# Importação das bibliotecas
import os, json, bcrypt #1-Operações do sistema 2- Para leitura e escrita de dados em formato json 3-criptografia/validação
from utils import validar_cnpj 
from pathlib import Path #importação com segurança pra usar diretórios 

ROOT_FOLDER = Path(__file__).parent #pra definir a pasta atual
INFO_EMPRESAS_FORNECEDORAS = ROOT_FOLDER / 'banco_de_dados' / 'info_empresas_fornecedoras.json' 
INFO_EMPRESAS_RECICLADORAS = ROOT_FOLDER / 'banco_de_dados' / 'info_empresas_recicladoras.json'

#Carregar/ salvar 
def carregar_empresas_fornecedoras(): #Função de carregamento dos dados das empresas
    if os.path.exists(INFO_EMPRESAS_FORNECEDORAS): # verificação do json
        with open(INFO_EMPRESAS_FORNECEDORAS, "r", encoding="utf-8") as f: #abertura do arquivo para leitura
            try: 
                return json.load(f)
            except json.JSONDecodeError: 
                return {} #Try -> tenta ler o json e return --> retorna em forma de dicionário
    return {} #Caso n tenha um arquivo => dicionário vazio

def carregar_empresas_recicladoras(): #Função de carregamento dos dados das empresas
    if os.path.exists(INFO_EMPRESAS_RECICLADORAS): # verificação do json
        with open(INFO_EMPRESAS_RECICLADORAS, "r", encoding="utf-8") as f: #abertura do arquivo para leitura
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
    empresas_fornecedoras = carregar_empresas_fornecedoras()
    empresas_recicladoras = carregar_empresas_recicladoras()

    print("=== Bem-vindo ao Sistema Eco-Match! ===")
    while True:
        print("\n Menu:")
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

            if cnpj in empresas_fornecedoras or cnpj in empresas_recicladoras:
                print(" CNPJ já cadastrado!")
                continue

            email = input("Informe o e-mail: ")
            telefone = input("Informe o telefone de contato: ")
            senha_plana = input("Senha: ")

            # Criptografia da senha usando o bcrypt
            senha_hash = bcrypt.hashpw(senha_plana.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            empresas_fornecedoras[cnpj] = { # armazenando os dados no dicionario
                "nome": nome,
                "email": email,
                "telefone": telefone,
                "senha": senha_hash    # <-- senha criptografada
            }

            salvar_empresas(empresas_fornecedoras)
            empresas = carregar_empresas_fornecedoras()
            print(" Empresa cadastrada com sucesso!")

        #Validação do cadastro
        elif opcao == "2":
            print("=== VALIDAR CADASTRO ===")
            cnpj = input("CNPJ: ")
            senha = input("Senha: ")

            if cnpj not in empresas_fornecedoras:
                print(" CNPJ ou senha incorretos.")
                continue

            senha_hash_salva = empresas_fornecedoras[cnpj]["senha"].encode('utf-8') #recuperação da senha criptografada --> Conversão para bytes

            # Verificação da senha criptografada
            if bcrypt.checkpw(senha.encode('utf-8'), senha_hash_salva): #comparação de senha inserida e senha criptografada
                print(f" O seu cadastro está validado com sucesso! Bem-vindo(a), {empresas_fornecedoras[cnpj]['nome']}.")
            else:
                print(" CNPJ ou senha incorretos.")

        # Listagem de empresas
        elif opcao == "3":
            print("=== EMPRESAS CADASTRADAS ===")
            if not empresas_fornecedoras:
                print("Nenhuma empresa cadastrada.")
            else:
                for cnpj, dados in empresas_fornecedoras.items():
                    print(f"{dados['nome']} - {cnpj} - {dados['email']} - {dados['telefone']}")

        #Saída
        elif opcao == "4":
            print("Encerrando o sistema... ")
            break

        else:
            print(" Opção inválida. Tente novamente.")


if __name__ == "__main__": #Execução do sistema somente se o arquivo for rodado de forma direta
    sistema_ecomatch()

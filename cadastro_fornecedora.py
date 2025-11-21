import os, json, bcrypt 
from utils import validar_cnpj
from pathlib import Path

ROOT_FOLDER = Path(__file__).parent
INFO_EMPRESAS_FORNECEDORAS = ROOT_FOLDER / 'banco_de_dados' / 'info_empresas_fornecedoras.json'

#CARREGAR / SALVAR 

def carregar_empresas():
    if os.path.exists(INFO_EMPRESAS_FORNECEDORAS):
        with open(INFO_EMPRESAS_FORNECEDORAS, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def salvar_empresas(empresas):
    with open(INFO_EMPRESAS_FORNECEDORAS, "w", encoding="utf-8") as f:
        json.dump(empresas, f, indent=4, ensure_ascii=False)


# SISTEMA 

def sistema_ecomatch():
    empresas = carregar_empresas()

    while True:
        print(" === Bem-vindo ao Sistema Eco-Match! ===")
        print("1. Cadastrar Empresa")
        print("2. Validar Cadastro")
        print("3. Listar empresas")
        print("4. Sair")
        opcao = input("Escolha uma opção: ")

        # CADASTRO DE EMPRESAS 
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

            # CRIPTOGRAFAR SENHA 
            senha_hash = bcrypt.hashpw(senha_plana.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            empresas[cnpj] = {
                "nome": nome,
                "email": email,
                "telefone": telefone,
                "senha": senha_hash    # <-- senha criptografada
            }

            salvar_empresas(empresas)
            empresas = carregar_empresas()
            print(" Empresa cadastrada com sucesso!")

        # VALIDAÇÃO CADASTRO 
        elif opcao == "2":
            print("=== VALIDAR CADASTRO ===")
            cnpj = input("CNPJ: ")
            senha = input("Senha: ")

            if cnpj not in empresas:
                print(" CNPJ ou senha incorretos.")
                continue

            senha_hash_salva = empresas[cnpj]["senha"].encode('utf-8')

            # VERIFICAR SENHA CRIPTOGRAFADA 
            if bcrypt.checkpw(senha.encode('utf-8'), senha_hash_salva):
                print(f" O seu cadastro está validado com sucesso! Bem-vindo(a), {empresas[cnpj]['nome']}.")
            else:
                print(" CNPJ ou senha incorretos.")

        # LISTAR EMPRESAS 
        elif opcao == "3":
            print("=== EMPRESAS CADASTRADAS ===")
            if not empresas:
                print("Nenhuma empresa cadastrada.")
            else:
                for cnpj, dados in empresas.items():
                    print(f"{dados['nome']} - {cnpj} - {dados['email']} - {dados['telefone']}")

        #  SAIR 
        elif opcao == "4":
            print("Encerrando o sistema... ")
            break

        else:
            print(" Opção inválida. Tente novamente.")


if __name__ == "__main__":
    sistema_ecomatch()

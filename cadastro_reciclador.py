import os, json, bcrypt
from utils import validar_cnpj
from pathlib import Path

# -------------------- CONFIGURAÇÕES DE ARQUIVO --------------------
ROOT_FOLDER = Path(__file__).parent
INFO_EMPRESAS_FORNECEDORAS = ROOT_FOLDER / 'banco_de_dados' / 'info_empresas_fornecedoras.json' 
INFO_EMPRESAS_RECICLADORAS = ROOT_FOLDER / 'banco_de_dados' / 'info_empresas_recicladoras.json'


# -------------------- CARREGAR / SALVAR --------------------
# CARREGA O BANCO DE DADOS DE RECICLADORAS
def carregar_empresas_recicladoras():
    if os.path.exists(INFO_EMPRESAS_RECICLADORAS): 
        with open(INFO_EMPRESAS_RECICLADORAS, "r", encoding="utf-8") as f:
            try:
                return json.load(f) # 
            except json.JSONDecodeError: 
                return {}
    return {}

def carregar_empresas_fornecedoras(): #Função de carregamento dos dados das empresas
    if os.path.exists(INFO_EMPRESAS_FORNECEDORAS): # verificação do json
        with open(INFO_EMPRESAS_FORNECEDORAS, "r", encoding="utf-8") as f: #abertura do arquivo para leitura
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {} #Try -> tenta ler o json e return --> retorna em forma de dicionário
    return {} #Caso n tenha um arquivo => dicionário vazio

# SALVA OS DADOS NO ARQUIVO JSON
def salvar_recicladoras(recicladoras):
    with open(INFO_EMPRESAS_RECICLADORAS, "w", encoding="utf-8") as f:
        json.dump(recicladoras, f, indent=4, ensure_ascii=False)


# -------------------- SISTEMA --------------------

def sistema_recicladoras():
    recicladoras = carregar_empresas_recicladoras() #Carrega os dados das recicladoras
    empresas_fornecedoras = carregar_empresas_fornecedoras()

    while True:
        print("\n=== SISTEMA DE RECICLADORAS ===")
        print("1. Cadastrar Recicladora")
        print("2. Validar Cadastro (Login)")
        print("3. Listar Recicladoras")
        print("4. Sair")
        opcao = input("Escolha uma opção: ")

        # ---------------- CADASTRAR -------------------
        if opcao == "1":
            print("\n=== CADASTRO DE RECICLADORA ===")
            nome = input("Nome da empresa recicladora: ")
            cnpj = input("CNPJ: ")

            # ---- VALIDAR CNPJ ----
            if not validar_cnpj(cnpj):
                print("CNPJ inválido!")
                continue
            #-- VERIFICAR SE JÁ ESTÁ CADASTRADO ----
            if cnpj in recicladoras or cnpj in empresas_fornecedoras:
                print("CNPJ já cadastrado!")
                continue
            #---- COLETAR DEMAIS INFORMAÇÕES ----
            endereco = input("Endereço: ")
            contato = input("Contato (telefone ou e-mail): ")
            materiais = input("Materiais que recicla: ")
            senha_plana = input("Senha: ")

            # ---- CRIPTOGRAFAR SENHA ----
            senha_hash = bcrypt.hashpw(
                senha_plana.encode("utf-8"),
                bcrypt.gensalt()
            ).decode("utf-8")
            # ---- ARMAZENAR DADOS NO DICIONÁRIO ----
            recicladoras[cnpj] = {
                "nome": nome,
                "endereco": endereco,
                "contato": contato,
                "materiais": materiais,
                "senha": senha_hash
            }

            salvar_recicladoras(recicladoras) # Salva os dados no arquivo JSON
            recicladoras = carregar_empresas_recicladoras() # Recarrega os dados atualizados

            print("Recicladora cadastrada com sucesso!")

        # ---------------- VALIDAR CADASTRO (LOGIN) -------------------
        elif opcao == "2":
            print("\n=== VALIDAR CADASTRO ===")
            cnpj = input("CNPJ: ")
            senha = input("Senha: ")
            # Verificar se o CNPJ está cadastrado
            if cnpj not in recicladoras:
                print("CNPJ ou senha incorretos.")
                continue
            #RECUPERAR A SENHA CRIPTOGRAFADA
            senha_hash_salva = recicladoras[cnpj]["senha"].encode("utf-8")
            #VALIDA COM A SENHA INFORMADA COM A FUNÇÃO bcrypt.checkpw
            if bcrypt.checkpw(senha.encode("utf-8"), senha_hash_salva):
                print(f"Bem-vindo(a), {recicladoras[cnpj]['nome']}!")
            else:
                print("CNPJ ou senha incorretos.")

        # ---------------- LISTAR -------------------
        elif opcao == "3":
            print("\n=== RECICLADORAS CADASTRADAS ===")
            if not recicladoras:
                print("Nenhuma recicladora cadastrada.")
            else:
                # EXIBIR DADOS DAS RECICLADORAS
                for cnpj, r in recicladoras.items():
                    print(
                        f"{r['nome']} - CNPJ: {cnpj}\n"
                        f"Endereço: {r['endereco']}\n"
                        f"Contato: {r['contato']}\n"
                        f"Materiais: {r['materiais']}\n"
                    )

        # ---------------- SAIR -------------------
        elif opcao == "4":
            print("Encerrando o sistema...")
            break

        else:
            print("Opção inválida.")

#EXECUTA O SISTEMA APENAS SE O ARQUIVO FOR EXECUTADO DIRETAMENTE
if __name__ == "__main__":
    sistema_recicladoras()

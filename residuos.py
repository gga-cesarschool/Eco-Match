import json
import os
import bcrypt
from pathlib import Path
from datetime import datetime

# Caminhos dos arquivos JSON
ROOT = Path(__file__).parent
ARQUIVO_RESIDUOS = ROOT / "banco_de_dados" / "residuos.json"
ARQUIVO_FORNECEDORES = ROOT / "banco_de_dados" / "info_empresas_fornecedoras.json"
ARQUIVO_HISTORICO = ROOT / "banco_de_dados" / "historico_fornecimentos.json"


# -------------------- FUNÇÕES BASE JSON --------------------

def carregar_json(caminho, padrao):
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return padrao
    return padrao


def salvar_json(caminho, conteudo):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(conteudo, f, indent=4, ensure_ascii=False)


# -------------------- RESÍDUOS --------------------

def carregar_residuos():
    return carregar_json(ARQUIVO_RESIDUOS, [])


def salvar_residuos(residuos):
    salvar_json(ARQUIVO_RESIDUOS, residuos)


# -------------------- HISTÓRICO DE FORNECIMENTO --------------------

def carregar_historico():
    return carregar_json(ARQUIVO_HISTORICO, [])


def salvar_historico(historico):
    salvar_json(ARQUIVO_HISTORICO, historico)


# -------------------- LOGIN DO FORNECEDOR --------------------

def carregar_fornecedores():
    return carregar_json(ARQUIVO_FORNECEDORES, {})


def login_fornecedor():
    fornecedores = carregar_fornecedores()

    print("\n=== LOGIN DO FORNECEDOR ===")
    cnpj = input("CNPJ: ")
    senha = input("Senha: ")

    if cnpj not in fornecedores:
        print("CNPJ ou senha incorretos.")
        return None

    senha_hash = fornecedores[cnpj]["senha"].encode("utf-8")

    if bcrypt.checkpw(senha.encode("utf-8"), senha_hash):
        print(f"Login realizado! Bem-vindo(a), {fornecedores[cnpj]['nome']}.\n")
        return cnpj

    print("CNPJ ou senha incorretos.")
    return None


# -------------------- CRUD RESÍDUOS --------------------

def cadastrar_residuo(cnpj_fornecedor):
    print("\n=== CADASTRAR RESÍDUO ELETRÔNICO ===")
    nome = input("Nome do resíduo: ")
    tipo = input("Tipo (Pilha, Celular, Computador, etc.): ")
    peso = input("Peso (kg): ")
    origem = input("Origem: ")

    res = {
        "cnpj_fornecedor": cnpj_fornecedor,
        "nome": nome,
        "tipo": tipo,
        "peso": peso,
        "origem": origem
    }

    # --- Salvar no arquivo de resíduos ---
    residuos = carregar_residuos()
    residuos.append(res)
    salvar_residuos(residuos)

    # --- Registrar no histórico ---
    historico = carregar_historico()

    historico.append({
        "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cnpj_fornecedor": cnpj_fornecedor,
        "nome_residuo": nome,
        "tipo": tipo,
        "peso": peso,
        "origem": origem
    })

    salvar_historico(historico)

    print("Resíduo cadastrado e registrado no histórico!\n")


def listar_residuos_do_fornecedor(cnpj):
    residuos = carregar_residuos()
    meus = [r for r in residuos if r["cnpj_fornecedor"] == cnpj]

    if not meus:
        print("Nenhum resíduo cadastrado por você.\n")
        return

    print("\n=== SEUS RESÍDUOS CADASTRADOS ===")
    for i, r in enumerate(meus, start=1):
        print(f"{i}. {r['nome']} | {r['tipo']} | {r['peso']}kg | Origem: {r['origem']}")
    print()


def editar_residuo(cnpj):
    residuos = carregar_residuos()
    meus = [r for r in residuos if r["cnpj_fornecedor"] == cnpj]

    if not meus:
        print("Você não cadastrou nenhum resíduo.")
        return

    listar_residuos_do_fornecedor(cnpj)

    indice = input("Número do resíduo para editar: ")

    if not indice.isdigit() or int(indice) < 1 or int(indice) > len(meus):
        print("Número inválido.")
        return

    item = meus[int(indice) - 1]
    print("\nPressione ENTER para manter o valor atual.")

    novo_nome = input(f"Novo nome [{item['nome']}]: ") or item['nome']
    novo_tipo = input(f"Novo tipo [{item['tipo']}]: ") or item['tipo']
    novo_peso = input(f"Novo peso [{item['peso']}]: ") or item['peso']
    nova_origem = input(f"Nova origem [{item['origem']}]: ") or item['origem']

    # Atualiza no JSON geral
    for r in residuos:
        if r is item:
            r["nome"] = novo_nome
            r["tipo"] = novo_tipo
            r["peso"] = novo_peso
            r["origem"] = nova_origem

    salvar_residuos(residuos)
    print("Resíduo atualizado com sucesso!\n")


def excluir_residuo(cnpj):
    residuos = carregar_residuos()
    meus = [r for r in residuos if r["cnpj_fornecedor"] == cnpj]

    if not meus:
        print("Nenhum resíduo para excluir.")
        return

    listar_residuos_do_fornecedor(cnpj)

    indice = input("Número do resíduo para excluir: ")

    if not indice.isdigit() or int(indice) < 1 or int(indice) > len(meus):
        print("Número inválido.")
        return

    item = meus[int(indice) - 1]
    residuos.remove(item)
    salvar_residuos(residuos)

    print(f"Resíduo '{item['nome']}' excluído!\n")


# -------------------- MENU PRINCIPAL --------------------

def menu_residuos():
    print("\n=== SISTEMA DE RESÍDUOS (FORNECEDOR) ===")
    print("1 - Cadastrar resíduo")
    print("2 - Listar meus resíduos")
    print("3 - Editar resíduo")
    print("4 - Excluir resíduo")
    print("0 - Sair")

    return input("Escolha: ")


def sistema_residuos():
    cnpj_logado = login_fornecedor()
    if not cnpj_logado:
        return

    while True:
        opc = menu_residuos()

        if opc == "1":
            cadastrar_residuo(cnpj_logado)
        elif opc == "2":
            listar_residuos_do_fornecedor(cnpj_logado)
        elif opc == "3":
            editar_residuo(cnpj_logado)
        elif opc == "4":
            excluir_residuo(cnpj_logado)
        elif opc == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    sistema_residuos()

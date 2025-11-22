import json
import os
import bcrypt
from pathlib import Path

ROOT = Path(__file__).parent
ARQUIVO_RESIDUOS = ROOT / "banco_de_dados" / "residuos.json"
ARQUIVO_RECICLADOS = ROOT / "banco_de_dados" / "residuos_reciclados.json"
ARQUIVO_RECICLADORAS = ROOT / "banco_de_dados" / "info_empresas_recicladoras.json"


# -------------------- CARREGAR / SALVAR --------------------

def carregar_json(caminho, padrao):
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return padrao
    return padrao


def salvar_json(caminho, conteudo):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(conteudo, f, indent=4, ensure_ascii=False)


def carregar_residuos():
    return carregar_json(ARQUIVO_RESIDUOS, [])


def salvar_residuos(residuos):
    salvar_json(ARQUIVO_RESIDUOS, residuos)


def carregar_reciclados():
    return carregar_json(ARQUIVO_RECICLADOS, [])


def salvar_reciclados(lista):
    salvar_json(ARQUIVO_RECICLADOS, lista)


def carregar_recicladoras():
    return carregar_json(ARQUIVO_RECICLADORAS, {})


# -------------------- LOGIN DA RECICLADORA --------------------

def login_recicladora():
    recicladoras = carregar_recicladoras()

    print("\n=== LOGIN DA EMPRESA RECICLADORA ===")
    cnpj = input("CNPJ: ")
    senha = input("Senha: ")

    if cnpj not in recicladoras:
        print("CNPJ ou senha incorretos.")
        return None

    senha_hash = recicladoras[cnpj]["senha"].encode("utf-8")

    if bcrypt.checkpw(senha.encode("utf-8"), senha_hash):
        print(f"Login realizado! Bem-vindo(a), {recicladoras[cnpj]['nome']}.\n")
        return cnpj

    print("CNPJ ou senha incorretos.")
    return None


# -------------------- LISTAGEM --------------------

def listar_residuos_disponiveis():
    residuos = carregar_residuos()

    if not residuos:
        print("Nenhum resíduo disponível no momento.\n")
        return

    print("\n=== RESÍDUOS DISPONÍVEIS PARA RECICLAGEM ===")
    for i, r in enumerate(residuos, start=1):
        print(f"{i}. {r['nome']} | {r['tipo']} | {r['peso']}kg | Origem: {r['origem']} | Fornecedor: {r['cnpj_fornecedor']}")
    print()


# -------------------- RECICLAGEM --------------------

def reciclar_residuo(cnpj_recicladora):
    residuos = carregar_residuos()

    if not residuos:
        print("Nenhum resíduo para reciclar.")
        return

    listar_residuos_disponiveis()

    indice = input("Número do resíduo que deseja RECICLAR: ")

    if not indice.isdigit() or int(indice) < 1 or int(indice) > len(residuos):
        print("Número inválido.")
        return

    i = int(indice) - 1
    residuo = residuos.pop(i)

    reciclados = carregar_reciclados()

    residuo_reciclado = {
        "nome": residuo["nome"],
        "tipo": residuo["tipo"],
        "peso": residuo["peso"],
        "origem": residuo["origem"],
        "cnpj_fornecedor": residuo["cnpj_fornecedor"],
        "cnpj_recicladora": cnpj_recicladora
    }

    reciclados.append(residuo_reciclado)

    salvar_residuos(residuos)
    salvar_reciclados(reciclados)

    print(f"Resíduo '{residuo['nome']}' RECICLADO com sucesso!\n")


# -------------------- MENU PRINCIPAL DA RECICLADORA --------------------

def menu_recicladora():
    print("\n=== SISTEMA DE RECICLAGEM ===")
    print("1 - Ver resíduos disponíveis")
    print("2 - Reciclar resíduo")
    print("0 - Sair")

    return input("Escolha: ")


def sistema_recicladora():
    cnpj_logado = login_recicladora()
    if not cnpj_logado:
        return

    while True:
        opc = menu_recicladora()

        if opc == "1":
            listar_residuos_disponiveis()
        elif opc == "2":
            reciclar_residuo(cnpj_logado)
        elif opc == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    sistema_recicladora()

import os
os.system ('cls')

import json
import os

ARQUIVO = "residuos.json" # tem que "codar" esse arquivo pois ele está vazio


def carregar_dados():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def salvar_dados(residuos):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(residuos, f, indent=4, ensure_ascii=False)


def cadastrar_residuo():
    print(" CADASTRAR RESÍDUO ELETRÔNICO ")
    nome = input("Nome do resíduo: ")
    tipo = input("Tipo (Ex: Pilha, Bateria, Celular, Computador...): ")
    peso = input("Peso (em kg): ")
    origem = input("Origem (Empresa, Pessoa Física, etc): ")

    residuo = {
        "nome": nome,
        "tipo": tipo,
        "peso": peso,
        "origem": origem
    }

    residuos = carregar_dados()
    residuos.append(residuo)
    salvar_dados(residuos)

    print(" Resíduo cadastrado com sucesso!")


def listar_residuos():
    residuos = carregar_dados()
    if not residuos:
        print(" Nenhum resíduo cadastrado.")
        return

    print("\n--- LISTA DE RESÍDUOS ELETRÔNICOS ---")
    for i, r in enumerate(residuos, start=1):
        print(f"{i}. Nome: {r['nome']} | Tipo: {r['tipo']} | Peso: {r['peso']} kg | Origem: {r['origem']}")


def editar_residuo():
    residuos = carregar_dados()
    if not residuos:
        print(" Nenhum resíduo cadastrado para editar.")
        return

    listar_residuos()
    indice = input("\nDigite o número do resíduo que deseja editar: ")

    if not indice.isdigit() or int(indice) < 1 or int(indice) > len(residuos):
        print("\nNúmero inválido.")
        return

    i = int(indice) - 1
    r = residuos[i]

    print(f"\nEditando '{r['nome']}' (pressione ENTER para manter o valor atual)")

    novo_nome = input(f"Novo nome [{r['nome']}]: ") or r['nome']
    novo_tipo = input(f"Novo tipo [{r['tipo']}]: ") or r['tipo']
    novo_peso = input(f"Novo peso [{r['peso']}]: ") or r['peso']
    nova_origem = input(f"Nova origem [{r['origem']}]: ") or r['origem']

    residuos[i] = {
        "nome": novo_nome,
        "tipo": novo_tipo,
        "peso": novo_peso,
        "origem": nova_origem
    }

    salvar_dados(residuos)
    print(" Resíduo atualizado com sucesso!")


def excluir_residuo():
    residuos = carregar_dados()
    if not residuos:
        print(" Nenhum resíduo cadastrado para excluir. ")
        return

    listar_residuos()
    indice = input("Digite o número do resíduo que deseja excluir: ")

    if not indice.isdigit() or int(indice) < 1 or int(indice) > len(residuos):
        print("Número inválido.")
        return

    i = int(indice) - 1
    removido = residuos.pop(i)
    salvar_dados(residuos)
    print(f"Resíduo '{removido['nome']}' excluído com sucesso!")


def menu():
    while True:
        print("SISTEMA DE CADASTRO DE RESÍDUOS ELETRÔNICOS ")
        print("1 - Cadastrar resíduo")
        print("2 - Listar resíduos")
        print("3 - Editar resíduos")
        print("4 - Excluir resíduos")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_residuo()
        elif opcao == "2":
            listar_residuos()
        elif opcao == "3":
            editar_residuo()
        elif opcao == "4":
            excluir_residuo()
        elif opcao == "0":
            print("Encerrando o sistema... ")
            break
        else:
            print("Opção inválida, tente novamente.")

if __name__== "__main__":
    menu()
import os
os.system ('cls')

from time import sleep

recicladores = []
id_atual = 1


def cadastrar_reciclador(id_atual):
    print('Cadastrar Reciclador:')
    nome = input('Nome do reciclador ou empresa: ')
    cnpj = input('CNPJ/CPF: ')
    endereco = input('Endereço: ')
    contato = input('Contato (telefone ou e-mail): ')
    materiais = input('Materiais que recicla: ')

    reciclador = [id_atual, nome, cnpj, endereco, contato, materiais]
    recicladores.append(reciclador)
    print('\nReciclador cadastrado!\n')
    return id_atual + 1


def listar_recicladores():
    print('Lista de Recicladores:')
    if not recicladores:
        print('\nNenhum reciclador cadastrado.\n')
    else:
        for r in recicladores:
            print(f'ID: {r[0]} | Nome: {r[1]} | CNPJ/CPF: {r[2]} | '
                  f'Endereço: {r[3]} | Contato: {r[4]} | Materiais: {r[5]}')
        print()


def atualizar_reciclador():
    print('Atualizar Reciclador:')
    id_busca = int(input('Digite o ID do reciclador a atualizar: '))
    for r in recicladores:
        if r[0] == id_busca:
            novo_nome = input('Novo nome: ') or r[1]
            novo_cnpj = input('Novo CNPJ/CPF: ') or r[2]
            novo_endereco = input('Novo endereço: ') or r[3]
            novo_contato = input('Novo contato: ') or r[4]
            novos_materiais = input('Novos materiais: ') or r[5]

            r[1:] = [novo_nome, novo_cnpj, novo_endereco, novo_contato, novos_materiais]
            print('Reciclador atualizado!\n')
            return
    print('\nID não encontrado.\n')


def excluir_reciclador():
    print('Excluir Reciclador:')
    id_busca = int(input('Digite o ID do reciclador a excluir: '))
    for r in recicladores:
        if r[0] == id_busca:
            recicladores.remove(r)
            print('Reciclador excluído com sucesso!\n')
            return
    print('ID não encontrado.\n')


def menu():
    print('Sistema de Gestão de Lixo Eletrônico - Recicladores:')
    print('\n1 - Cadastrar reciclador')
    print('2 - Listar recicladores')
    print('3 - Atualizar reciclador')
    print('4 - Excluir reciclador')
    print('5 - Sair')
    return input('\nEscolha uma opção: ')


while True:
    opcao = menu()

    if opcao == '1':
        id_atual = cadastrar_reciclador(id_atual)
    elif opcao == '2':
        listar_recicladores()
    elif opcao == '3':
        atualizar_reciclador()
    elif opcao == '4':
        excluir_reciclador()
    elif opcao == '5':
        print('Encerrando o sistema...')
        sleep(2)
        break
    else:
        print('Opção inválida.\n')
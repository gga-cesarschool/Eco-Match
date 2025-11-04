def sistema_ecomatch():
    empresas = {}  # Dicionário onde a chave será o CNPJ e o valor será outro dicionário com os dados

    while True:  # Menu de opções
        print("\n Bem-vindo ao Sistema EcoMatch! O melhor sistema de todos ")
        print("1. Cadastrar Empresa ")
        print("2. Fazer login ")
        print("3. Listar empresas ")
        print("4. Sair ")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            print("\n CADASTRO DE EMPRESA ")
            nome = input("Informe o nome da empresa: ")
            cnpj = input("Informe o CNPJ: ")
            email = input("Informe o e-mail: ")
            telefone = input("Informe o telefone de contato: ")
            senha = input("Senha: ")

            if cnpj in empresas:
                print("\n CNPJ já cadastrado!")
            else:
                empresas[cnpj] = {
                    "nome": nome,
                    "email": email,
                    "telefone": telefone,
                    "senha": senha
                }
                print("\n Empresa cadastrada com sucesso! ")

        elif opcao == "2":
            print("\n LOGIN ")
            cnpj = input("CNPJ: ")
            senha = input("Senha: ")

            if cnpj in empresas and empresas[cnpj]["senha"] == senha:
                print(f"\nLogin realizado com sucesso! Bem-vindo(a), {empresas[cnpj]['nome']}.")
            else:
                print("\nCNPJ ou senha incorretos.")

        elif opcao == "3":
            print("\n EMPRESAS CADASTRADAS ")
            if not empresas:
                print("Nenhuma empresa cadastrada.")
            else:
                for cnpj, dados in empresas.items():
                    print(f"{dados['nome']} - {cnpj} - {dados['email']} - {dados['telefone']}")

        elif opcao == "4":
            print("\n Encerrando o sistema... ")
            break

        else:
            print("\n Opção inválida. Tente novamente.")


if __name__ == "__main__":
    sistema_ecomatch()  # aqui é pra chamar a função, ao invés do return
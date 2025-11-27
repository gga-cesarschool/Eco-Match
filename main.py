from cadastro_fornecedora import sistema_cadastro_fornecedoras
from cadastro_reciclador import sistema_cadastro_recicladoras
from reciclagem import sistema_recicladora
from relatorio import gerar_pdf
from residuos import sistema_residuos

if __name__ == "__main__":
    print("=== Bem-vindo ao Sistema Eco-Match! ===")

    while True:
        print("\n Menu:")
        print("1. Cadastrar Empresa Fornecedora")
        print("2. Cadastrar Empresa Recicladora")
        print("3. Cadastrar Resíduos (Exclusivo das Empresas Fornecedoras)")
        print("4. Reciclar Resíduos (Exclusivo das Empresas Recicladoras)")
        print("5. Gerar Relatório")
        print("6. Sair")
        opcao = input("Escolha uma opção: ")

        #Cadastro das empresas
        if opcao == "1":
            sistema_cadastro_fornecedoras()

        #Validação do cadastro
        elif opcao == "2":
            sistema_cadastro_recicladoras()

        # Listagem de empresas
        elif opcao == "3":
            sistema_residuos()

        elif opcao == "4":
            sistema_recicladora()

        elif opcao == "5":
            gerar_pdf()

        #Saída
        elif opcao == "6":
            print("Encerrando o sistema... ")
            break

        else:
            print(" Opção inválida. Tente novamente.")

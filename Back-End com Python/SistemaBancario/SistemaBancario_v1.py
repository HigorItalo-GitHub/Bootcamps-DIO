"""

*** Programa que inmplementa um sistema bancário simples para registro diário de movientações financeiras básicas de um usuário ***

As operações disponíveis no sistema são: 
 - Depositar: Adição de valores positivos para a conta bancária

 - Sacar: Pemite a realização de um número pre-determinado de saques diarios (3), com um valor máximo
 também pré-definido (R$500,00). O sistema é capaz de alertar ao usuário se o limite de saques diários é 
 ultrapassado, apresentando o alerta em tela quando ocorre solicitação de saque nessa situação.

 - Visualizar extrato: Lista todos os depósitos e saques efetuados na conta, apresentando o saldo atual da conta.
 Em caso de não haverem sido realizadas movimentações na conta, uma mensagem informativa indicando esse situação é
 apresentada em tela quando a operação é solicitada.
"""

menu = """
===== SISTEMA BANCÁRIO =====
          
          Selecione uma das opções

[1] Realizar depósito
[2] Realizar saque
[3] Exibir extrato
[0] Sair

=============================================\n"""

saldo = 0
lista_de_depositos = list()
lista_de_saques = list()
limite_de_valor_de_saque = 500
extrato = 0
numero_de_saques = 0
LIMITE_DE_SAQUES = 3

while True:

    opcao = input(menu)

    if opcao == '1':
        deposito = input("OPCAO 1 SELECIONADA - REALIZAR DEPOSITO\nInforme o valor a ser depositado:\n")
        try:
            deposito = float(deposito)
            if deposito > 0:
                print(f"\n+++ Depósito no valor de R$ {deposito:.2f} realizado +++\nRetornando ao Menu inicial.")
                saldo += deposito
                lista_de_depositos.append(deposito)
                extrato += 1
            else: print(f"Valor informado ({deposito}) é inválido para depósito. Por favor, forneça um valor superior a zero para realizar depósitos.\nRetornando ao Menu inicial.")
        except:
            print(f"A informação fornecida ({deposito}) não corresponde a um valor numérico.\nPor favor, informe uma valor númérico superior a zero ao realizar depósitos.\nRetornando ao Menu Inicial.\n")
            
    elif opcao == '2':
        if numero_de_saques < LIMITE_DE_SAQUES:
            saque = input("OPCAO 2 SELECIONADA - REALIZAR SAQUE\nInforme o valor a sacar:\n")
            try:
                saque = float(saque)
                if saque > 0 and saque <= 500:
                    if saldo >= saque:
                        print(f"\n--- Saque no valor de R${saque:.2f} realizado ---\nRetornando ao Menu inicial.")
                        saldo -= saque
                        lista_de_saques.append(saque)
                        numero_de_saques +=1
                    else: print("Saque indisponível - saldo insuficiente para o valor de saque solicitado.\nRetornando ao Menu inicial.")
                else: print(f"Apenas saques com valor positivo e de no máximo R$ {limite_de_valor_de_saque:.2f} estão permitidos.\nRetornando ao Menu inicial.")
            except:
                print(f"A informação fornecida ({saque}) não corresponde a um valor numérico.\nPor favor, informe uma valor númérico superior a zero ao realizar saques.\nRetornando ao Menu inicial:\n")
        else: print(f"Saque indisponível - limite de saques de diários ({LIMITE_DE_SAQUES}) excedito.\nRetornando ao Menu inicial.")
         
    elif opcao == '3':
        print("OPCAO 3 SELECIONADA - EXIBIR EXTRATO DE MOVIMENTAÇÃO:\n")
        if extrato:
            print(f"""############# EXTRATO DO DIA ############""")
            print("Depósitos:")
            for d in lista_de_depositos:
                print(f"R$ {d:.2f}")
            print("Saques:")
            for s in lista_de_saques:
                print(f"R$ {s:.2f}")
            print(f"---------\nSaldo: {saldo}")
        else:
            print("\n *** Não foram realizadas movimentações.\nRetornando ao Menu inicial.***")
    elif opcao == '0':
        print("\n||| Encerrando. Obrigado pelo acesso! |||\n")
        break
    else:
        print("Opção invalida. Forneça uma das opções indicadas no Menu:")

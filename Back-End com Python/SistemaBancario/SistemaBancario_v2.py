"""

*** Programa que inmplementa um sistema bancário simples (versão 2) para 
registro diário de movientações financeiras básicas de um usuário.
A nova versão realiza as ações 'Criar Usuário (cliente) e Criar Conta Corrente.
Juntamente com as ações de saque, depósito e extrato, todas passam a ser implemetadas e excutadas a partir de
funções. ***

As operações disponíveis no sistema atual são:

- Criar Usuário: Cada usuario tem como dados: nome, data de nascimento, cpf e endereço;
o endereço de um usuário corresponde a uma string no formato "logradouro, nº - bairro - cidade/sigla do estado;
O CPF armazenado de um usuário deve constar apenas de numeros (sem pontos ou hifens, caso seguem fornecidos);
Não deve ser permitido cadastrar dois usuarios com mesmo CPF.

- Criar Conta Corrente: Uma conta tem como dados: nº da agência, nº da conta e usuário;
o nº das contas são gerados de forma sequencial, partindo de 1;
o nº da agencia é fixo e igual a "0001";
um usuário pode possuir mais de uma conta, porém cada conta possui um único usuario associado.

- Depositar: Adição de valores positivos para a conta bancária

- Sacar: Pemite a realização de um número pre-determinado de saques diarios (3), com um valor máximo
também pré-definido (R$500,00). O sistema é capaz de alertar ao usuário se o limite de saques diários é 
ultrapassado, apresentando o alerta em tela quando ocorre solicitação de saque nessa situação.

- Exibir Extrato: Lista todos os depósitos e saques efetuados na conta, apresentando o saldo atual da conta.
Em caso de não haverem sido realizadas movimentações na conta, uma mensagem informativa indicando esse situação é
apresentada em tela quando a operação é solicitada.
"""

menu = """
===== SISTEMA BANCÁRIO =====
          
          Selecione uma das opções

[1] Realizar Depósito
[2] Realizar Saque
[3] Exibir Extrato
[4] Criar Usuário
[5] Criar Conta Corrente
[6] Exibir Contas
[7] Exibir Usuários
[0] Sair

=============================================\n"""

saldo = 0
lista_de_depositos = list()
lista_de_saques = list()
limite_de_valor_de_saque = 500
flag_extrato = False
numero_de_saques = 0
LIMITE_DE_SAQUES = 3

usuarios = []
contas_correntes = []
contas_id = 0
agencia = "0001"

def Tomar_Digitos_CPF(cpf): # Função auxiliar; retorna os digitos de uma string associada a um número de CPF
    digitos_filtrados = filter(str.isdigit, cpf)
    return (''.join(digitos_filtrados))

def Criar_Usuario(nome, dados_data_de_nascimento, cpf, dados_endereco):

    data_de_nascimento_padronizada = f"{dados_data_de_nascimento[0]}/{dados_data_de_nascimento[1]}/{dados_data_de_nascimento[2]}"

    endereco_padronizado = f"{dados_endereco[0]}, {dados_endereco[1]} - {dados_endereco[2]} - {dados_endereco[3]}/{dados_endereco[4]}"

    usuarios.append({"usuario": nome, 
                     "data_de_nascimento": data_de_nascimento_padronizada, 
                     "CPF": cpf, 
                     "endereço": endereco_padronizado})
    
    print(f"""\n@@@ Novo cliente cadastrado! @@@\nDados do cliente:\n      Nome: {nome}\n      Data de nascimento: {data_de_nascimento_padronizada}\n      CPF: {cpf}\n      Endereço: {endereco_padronizado}""")
    print("\nRetornando ao Menu inicial.\n")

def Criar_Conta_Corrente(cpf_informado, numero_agencia):

    flag_usuario = None

    for individuo in usuarios:
        if individuo["CPF"] == cpf_informado:
            print(f"identificado cliente cadastrado para o CPF informado: {individuo["usuario"]}. Vinculando conta ao CPF informado...")
            flag_usuario = individuo
    
    if flag_usuario:
        
        global contas_id
        contas_id += 1

        nova_conta_id = contas_id

        contas_correntes.append({"agência": numero_agencia, 
                                "conta": nova_conta_id, 
                                "usuário": flag_usuario})
        print(f"""\n@@@ Nova conta cadastrada! @@@\nDados da conta:\n      Nº Agência: {numero_agencia}\n      Nº Conta: {nova_conta_id}\n      Usuário: {flag_usuario["usuario"]} (CPF: {flag_usuario["CPF"]})""")
        print("\nRetornando ao Menu inicial.\n")
    else:
        print(">>> CPF informado não consta entre usuários cadastros. Por favor, informe um CPF já cadastrado ou cadastre um novo usuario para o CPF informado. <<<\nRetornando ao Menu inicial.\n")

def Exibir_Contas():
    print(f"-.-.- Exibindo Contas Correntes Existentes (Total: {len(contas_correntes)}): -.-.-\n")
    if not contas_correntes:
        print("Não há contas correntes existentes no momento.\n")
    else:
        for conta_existente in contas_correntes:
            for chave, valor in conta_existente.items():
                if chave == 'usuário':
                    print(f"Usuário: {valor['usuario']} (CPF: {valor['CPF']})\n")
                else:
                    print(f"{chave}: {valor}\n")

def Exibir_Usuarios():
    if not usuarios:
        print("Não há clientes cadastrados no momento.")
    else:
        print(f"-.-.- Exibindo dados de clientes cadastrados (Total: {len(usuarios)}): -.-.-\n")
        for usuario_existente in usuarios:
            for chave, valor in usuario_existente.items():
                print(f"{chave}: {valor}\n")

def Depositar(saldo_disponivel, extrato, /):

    deposito = input("Informe o valor a ser depositado:\n")

    try:
        deposito = float(deposito)
        if deposito > 0:
            print(f"\n+++ Depósito no valor de R$ {deposito:.2f} realizado +++\nRetornando ao Menu inicial.")
            saldo_disponivel += deposito
            lista_de_depositos.append(deposito)
            extrato = True
        else: print(f"Valor informado ({deposito}) é inválido para depósito. Por favor, forneça um valor superior a zero para realizar depósitos.\nRetornando ao Menu inicial.")
    except:
        print(f"A informação fornecida ({deposito}) não corresponde a um valor numérico.\nPor favor, informe uma valor númérico superior a zero ao realizar depósitos.\nRetornando ao Menu Inicial.\n")
    
    return saldo_disponivel, extrato

def Sacar(*, numero_saques_efetuados, saldo_disponivel, extrato):

    valor_saque = input("Informe o valor a sacar:\n")

    try:
        saque = float(valor_saque)
        if saque > 0 and saque <= 500:
            if saldo_disponivel >= saque:
                print(f"\n--- Saque no valor de R${saque:.2f} realizado ---\nRetornando ao Menu inicial.")
                saldo_disponivel -= saque
                lista_de_saques.append(saque)
                numero_saques_efetuados +=1
                extrato = True
            else: print("Saque indisponível - saldo insuficiente para o valor de saque solicitado.\nRetornando ao Menu inicial.")
        else: print(f"Apenas saques com valor positivo e de no máximo R$ {LIMITE_DE_SAQUES:.2f} estão permitidos.\nRetornando ao Menu inicial.")
    except:
        print(f"A informação fornecida ({saque}) não corresponde a um valor numérico.\nPor favor, informe uma valor númérico superior a zero ao realizar saques.\nRetornando ao Menu inicial:\n")

    return numero_saques_efetuados, saldo_disponivel, extrato

def Emitir_Extrato(saldo_disponivel, / , *, status_extrato):

    if status_extrato:
        print(f"""############# EXTRATO DO DIA ############""")
        print("Depósitos:")
        for d in lista_de_depositos:
            print(f"R$ {d:.2f}")
        print("Saques:")
        for s in lista_de_saques:
            print(f"R$ {s:.2f}")
        print(f"---------\nSaldo: {saldo_disponivel}")
    else:
        print("\n *** Não foram realizadas movimentações.\nRetornando ao Menu inicial.***")

while True:

    opcao = input(menu)

    if opcao == '1':

        print("OPCAO 1 SELECIONADA - REALIZAR DEPOSITO")

        saldo, flag_extrato = Depositar(saldo, flag_extrato)
            
    elif opcao == '2':

        print("OPCAO 2 SELECIONADA - REALIZAR SAQUE\n")

        if numero_de_saques < LIMITE_DE_SAQUES:

            numero_de_saques, saldo, flag_extrato = Sacar(numero_saques_efetuados=numero_de_saques, saldo_disponivel=saldo, extrato=flag_extrato)
        
        else:
            
            print(f"Saque indisponível - limite de saques de diários ({LIMITE_DE_SAQUES}) excedito.\nRetornando ao Menu inicial.")
         
    elif opcao == '3':

        print("OPCAO 3 SELECIONADA - EXIBIR EXTRATO DE MOVIMENTAÇÃO:\n")

        Emitir_Extrato(saldo, status_extrato=flag_extrato)

    elif opcao == '4':
        
        print("OPCAO 4 SELECIONADA - CRIAR NOVO USUÁRIO:\n")

        novo_cpf = input("Informe número de CPF do usuário:\n")
        
        digitos_cpf = Tomar_Digitos_CPF(novo_cpf)

        if digitos_cpf in [individuo["CPF"] for individuo in usuarios]:
            print("CPF informado já consta nos registros de usuários cadastrados.\nRetornando ao Menu inicial.\n")
        else:
            novo_nome = input("Digite o nome completo do usuário:\n")
            novo_dia_nascimento = input("Informe dia de nascimento do usuário:\n")
            novo_mes_nascimento = input("Informe mês (numérico) de nascimento do usuário:\n")
            novo_ano_nascimento = input("informe ano (numérico, 4 digitos) de nascimento do usuário:\n")
            novo_endereco_logradouro = input("Informe logradouro (rua, avenida etc.) residencial do usuário:\n")
            novo_endereco_numero = input("Informe número residencial do usuário:\n")
            novo_endereco_bairro = input("Informe bairro do logradouro residencial do usuário:\n")
            novo_endereco_cidade = input("Informe cidade do logradouro residencial do usuário:\n")
            novo_endereco_estado = input("Informe estado do logradouro residencial do usuário:\n")

            Criar_Usuario(novo_nome, 
                          [novo_dia_nascimento, novo_mes_nascimento, novo_ano_nascimento], 
                          digitos_cpf, 
                          [novo_endereco_logradouro, novo_endereco_numero, 
                                novo_endereco_bairro, novo_endereco_cidade, novo_endereco_estado])

    elif opcao == '5':
        
        print("OPCAO 5 SELECIONADA - CRIAR NOVA CONTA CORRENTE:\n")

        cpf_para_conta = Tomar_Digitos_CPF(input("Informe CPF do usuário para a conta:\n"))
        
        Criar_Conta_Corrente(cpf_para_conta, agencia)
    
    elif opcao == '6':

        print("OPCAO 6 SELECIONADA - EXIBIR CONTAS:\n")

        Exibir_Contas()
    
    elif opcao == '7':

        print("OPCAO 7 SELECIONADA - EXIBIR USUÁRIOS:\n")

        Exibir_Usuarios()

    elif opcao == '0':
        print("\n||| Encerrando. Obrigado pelo acesso! |||\n")
        break

    else:
        print("Opção invalida. Forneça uma das opções indicadas no Menu:")

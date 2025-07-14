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

from abc import ABC, abstractmethod
from datetime import datetime

class Transacao(ABC):
    
    @property
    @abstractmethod
    def valor(self):
        pass
    
    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        transacao_realizada = conta.depositar(self.valor)
        
        if transacao_realizada:
            conta.historico.registrar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        transacao_realizada = conta.sacar(self.valor)
        
        if transacao_realizada:
            conta.historico.registrar_transacao(self)

class Historico:
    
    def __init__(self):
        self._transacoes = []
    
    @property
    def transacoes(self):
        return self._transacoes
    
    def registrar_transacao(self, transacao):
        self._transacoes.append(
            {"tipo": transacao.__class__.__name__,
             "valor": transacao.valor,
             "dia&horario": datetime.now().strftime("%d/%m/%Y %H:%M")}
        )

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
        
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def client(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self.saldo
        
        if valor > saldo:
            print("!!! Saque não realizado - valor solicitado excede saldo disponível. !!!")
        
        elif valor > 0:
            self._saldo -= valor
            print("--- Saque realizado com sucesso. ---")
            return True

        else:
            print("!!! Saque não realizado - valor para saque inválido. !!!")
        
        return False
    
    def depositar(self, valor):
        
        if valor > 0:
            self._saldo += valor
            print("+++ Depósito realizado com sucesso. +++")
        else:
            print("!!! Depósito não realizado - valor para depóstito inválido. !!!")
            return False

        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
    
    def sacar(self, valor):
        numero_de_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == "Saque"])
        
        if valor > self.limite:
            print(f"!!! Saque não realizado - valor solicitado excede o limite permitido (R$ {self.limite:.2f}). !!!\nRetornando ao Menu inicial.")
        
        elif numero_de_saques >= self.limite_saques:
            print(f"!!! Saque não realizado - limite de saques atingido ({self._limite_saques}).")
        
        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"Dados da Conta Corrente:\nNúmero: {self.numero}\nAgência: {self.agencia}\nCliente: {self.client.nome}"

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self._contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_de_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_de_nascimento = data_de_nascimento
    
    def __str__(self):
        return f"Nome: {self.nome}\nCPF: {self.cpf}\nNascimento: {self.data_de_nascimento}\nEndereço: {self.endereco}"

def busca_cliente(cpf, clientes):
    
    clientes_identificados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_identificados[0] if clientes_identificados else None

def busca_conta_0_cliente(cliente):
    
    if not cliente.contas:
        print("!!! Cliente informado não possui contas. !!!")
        return
    
    return cliente.contas[0]

def criar_conta_corrente(numero_da_conta, clientes, contas):
    
    cpf = input("Informe CPF do cliente:\n=>")
    cpf = tomar_digitos_cpf(cpf)
    
    cliente = busca_cliente(cpf, clientes)
    if not cliente:
        print("!!! Cliente não identificado entre usuários cadastrados.\nRetornando ao Menu incial.!!!\n")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_da_conta)
    
    contas.append(conta)
    
    cliente.contas.append(conta)
    
    print("$$$ Nova conta criada. $$$\nRetornando ao Menu inicial.\n")

def exibir_contas(contas):
    print(f"-.-.- Exibindo Contas Correntes Existentes (Total: {len(contas)}): -.-.-\n")
    if not contas:
        print("Não há contas correntes existentes no momento.\n")
    else:
        for conta_existente in contas:
            print("-." * 30)
            print(str(conta_existente))
        

def realizar_deposito(clientes):
    
    cpf = input("Informe CPF do cliente:\n=>")
    cpf = tomar_digitos_cpf(cpf)
    
    cliente = busca_cliente(cpf, clientes)
    
    if not cliente:
        print("!!! Cliente não identificado.\nRetornando ao Menu incial.!!!\n")
        return
    
    valor = float(input("Informe valor para depósito:\n=>"))
    
    transacao = Deposito(valor)
    
    conta = busca_conta_0_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def realizar_saque(clientes):
    
    cpf = input("Informe CPF do cliente:\n=>")
    cpf = tomar_digitos_cpf(cpf)
    
    cliente = busca_cliente(cpf, clientes)
    
    if not cliente:
        print("!!! Cliente não identificado.\nRetornando ao Menu incial.!!!\n")
        return
    
    valor = float(input("Informe valor para saque:\n=>"))
    
    transacao = Saque(valor)
    
    conta = busca_conta_0_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    
    cpf = input("Informe CPF do cliente:\n=>")
    cpf = tomar_digitos_cpf(cpf)
    
    cliente = busca_cliente(cpf, clientes)
    
    if not cliente:
        print("!!! Cliente não identificado.\nRetornando ao Menu incial.!!!\n")
        return

    conta = busca_conta_0_cliente(cliente)
    if not conta:
        return
    
    print(f"""############# EXTRATO DO DIA ############""")
    transacoes = conta.historico.transacoes
    extrato = ""
    if not transacoes:
        print("!!! Não foram realizadas transações nesta conta. !!!")
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao["dia&horario"]} - {transacao["tipo"]}: R${transacao["valor"]:.2f}"
    print(extrato)
    print(f"----------------------------------------------\nSaldo:\t\t\tR$ {conta.saldo:.2f}")
    print("#########################################")

def exibir_usuarios(usuarios):
    
    print(f"@-@-@ Exibindo Usuários cadastrados (Total: {len(usuarios)}) @-@-@")
    for usuario in usuarios:
        print("-*" * 30)
        print(str(usuario))

def criar_usuario(clientes):
    
    cpf = input("Informe CPF do cliente:\n=>")
    cpf = tomar_digitos_cpf(cpf)
    
    cliente = busca_cliente(cpf, clientes)
    
    if cliente:
        print("!!! CPF informado já consta nos registros de usuários cadastrados.\nRetornando ao Menu inicial.\n !!!")
        return
    novo_nome = input("Digite o nome completo do usuário:\n")
    novo_dia_nascimento = input("Informe dia de nascimento do usuário:\n")
    novo_mes_nascimento = input("Informe mês (numérico) de nascimento do usuário:\n")
    novo_ano_nascimento = input("informe ano (numérico, 4 digitos) de nascimento do usuário:\n")
    novo_endereco_logradouro = input("Informe logradouro (rua, avenida etc.) residencial do usuário:\n")
    novo_endereco_numero = input("Informe número residencial do usuário:\n")
    novo_endereco_bairro = input("Informe bairro do logradouro residencial do usuário:\n")
    novo_endereco_cidade = input("Informe cidade do logradouro residencial do usuário:\n")
    novo_endereco_estado = input("Informe estado do logradouro residencial do usuário:\n")
    
    data_de_nascimento_padronizada = f"{novo_dia_nascimento}/{novo_mes_nascimento}/{novo_ano_nascimento}"
    endereco_padronizado = f"{novo_endereco_logradouro}, {novo_endereco_numero} - {novo_endereco_bairro} - {novo_endereco_cidade}/{novo_endereco_estado}"
    
    cliente = PessoaFisica(cpf=cpf, nome=novo_nome, data_de_nascimento=data_de_nascimento_padronizada,endereco=endereco_padronizado)
    
    clientes.append(cliente)
    
    print(f"""\n@@@ Novo cliente cadastrado. @@@\nRetornando ao Menu inicial.\n""")
    
def tomar_digitos_cpf(cpf): # Função auxiliar; retorna os digitos de uma string associada a um número de CPF
    digitos_filtrados = filter(str.isdigit, cpf)
    return (''.join(digitos_filtrados))

def Menu():
    
    return input("""
    ============= SISTEMA BANCÁRIO ===============
            
            Selecione uma das opções

    [1] Realizar Depósito
    [2] Realizar Saque
    [3] Exibir Extrato
    [4] Criar Usuário
    [5] Criar Conta Corrente
    [6] Exibir Contas
    [7] Exibir Usuários
    [0] Sair

    =============================================\n=>""")

def main():
    clientes = []
    contas = []
    
    while True:
        
        opcao = Menu()
        
        if opcao == '1':
            print("OPCAO 1 SELECIONADA - REALIZAR DEPOSITO")
            realizar_deposito(clientes)
        
        elif opcao == '2':
            print("OPCAO 2 SELECIONADA - REALIZAR SAQUE")
            realizar_saque(clientes)
        
        elif opcao == '3':
            print("OPCAO 3 SELECIONADA - EXIBIR EXTRATO")
            exibir_extrato(clientes)
        
        elif opcao == '4':
            print("OPCAO 4 SELECIONADA - CRIAR USUÁRIO")
            criar_usuario(clientes)
        
        elif opcao == '5':
            print("OPCAO 5 SELECIONADA - CRIAR CONTA CORRENTE")
            conta_id = len(contas) + 1
            criar_conta_corrente(conta_id, clientes, contas)
        
        elif opcao == '6':
            print("OPCAO 6 SELECIONADA - EXIBIR CONTAS")
            exibir_contas(contas)
        
        elif opcao == '7':
            print("OPCAO 6 SELECIONADA - EXIBIR USUÁRIOS")
            exibir_usuarios(clientes)
        
        elif opcao == '0':
            print("\n||| Encerrando. Obrigado pelo acesso! |||\n")
            break
        
        else:
            print("Opção invalida. Forneça uma das opções indicadas no Menu:")

main()
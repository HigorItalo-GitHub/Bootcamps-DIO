"""

*** Programa que inmplementa um sistema bancário simples (versão 3) para 
registro diário de movientações financeiras básicas de um usuário.
A nova versão implementa as ações de 'Criar Usuário (cliente) e Criar Conta Corrente,
juntamente com as ações de saque e depósito, através do uso de classes, de maneira que
a instanciação dessas classes viabilizem e coordenem as ações associadas à cliente e contas
(saque, depósito e extrato de transações) desse sistema. ***

As classes implementadas são:

- Histórico: Classe responsável por registrar e armazenar as transações realizadas em uma conta.
> Armazena tipo, valor e data/hora de cada operação.
> A ser usada para gerar o extrato.

- Conta: Classe base que representa uma conta bancária genérica.
> Possui saldo, número, agência, cliente e histórico de transações.
> Apresenta métodos que permitem operações de depósito e saque.

- Conta Corrente: Classe que faz uso de herança a partir da classe Conta.
> Se constirui como um especialização da classe Conta, com limites de saque (valor e quantidade).
> Limita o valor individual dos saques e a quantidade por conta.
> Sobrescreve o método sacar.

- Transação: Classe abstrata que serve como interface para operações bancárias.
> Define que todas as transações devem ter uma propriedade valor (abstrata) e um método registrar(conta) (abstrato).

- Deposito: Classe que faz uso de herança a partir da classe Transação
> Representa uma operação de depósito bancário.
> Possui um valor e um método que executa o depósito e o registra no histórico da conta.

- Saque: classe que faz uso de herança a partir da classe Transação
> Representa uma operação de saque bancário.
> Possui um valor e um método que executa o saque e o registra no histórico da conta.

- Cliente: classe base que representa um cliente do banco.
> Possui atributos de endereço e uma lista de contas.
> Apresenta métodos que permitem realizar transações e adicionar contas.

- Pessoa Fisica: classe que faz uso de herança a partir de classe Cliente.
> Corresponde a um especialização da classe Cliente para pessoa física.
> Incluie os atributos: CPF, nome e data de nascimento.
"""

from abc import ABC, abstractmethod, abstractproperty
from datetime import datetime

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
        saldo = self._saldo
        
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
        self._limite = limite
        self._limite_saques = limite_saques
    
    def sacar(self, valor):
        numero_de_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == "Saque"])
        
        if valor > self.limite:
            print(f"!!! Saque não realizado - valor solicitado excede o limite permitido (R$ {self.limite:.2f}). !!!")
        
        elif numero_de_saques >= self._limite_saques:
            print(f"!!! Saque não realizado - limite de saques atingido ({self._limite_saques}).")
        
        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"Número: {self.numero}\nAgência: {self.agencia}\nCliente: {self.client.nome}"

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

class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []
    
    def realizar_transacao(self, Conta, Transacao):
        Transacao.registrar(Conta)
    
    def adicionar_conta(self, Conta):
        self._contas.append(Conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_de_nascimento, endereco):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_de_nascimento = data_de_nascimento
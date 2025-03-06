'''
v1:
Sistema de Banco.
Operações basicas: sacar, depositar e visualizar extrato.
Sistema irá utilizar apenas uma conta.
Depósitos serão armazenados em uma variável e exibidos no extrato.
O saque tem limite de 3 por dias e valor máxo de R$ 500,00.
Caso não tenha saldo, o saque será negado e informado.
Todos os aques devem ser armazenados em uma variável e exibidos no extrato.
O extrato lista todos os depositos e saques realizados na conta. No fim da listagem, deve ser exibido o saldo atual da conta.
Se o etrato estiver em branco, exibir a mensagem "Não foram realizadas movimentações".
Os valores devem ser exibidos usando o formado "R$ xxx.xx".

v2:
Limite de transações diárias (saques ou depósitos) aumentado para 10.
Informar que o usuário excedeu o número de transações permitidas para aquele dia.
'''

from datetime import datetime, time
import os

class Conta:
    """
    Uma classe representando uma conta bancária simples.

    Atributos:
        saldo (float): o saldo da conta.
        depositos (lista): uma lista de depósitos, cada um uma tupla de (data, valor).
        saques (lista): uma lista de saques, cada um uma tupla de (data, valor).
        limite_saques (int): o limite diário de saques.
        valor_maximo_saques (float): o valor máximo por saque.
    
    Métodos:
        __init__(): Inicializa um novo objeto Conta com valores padrão.
        depositar(self, valor): Deposita fundos na conta.
        sacar(self, valor): Sacar fundos da conta, se as condições forem atendidas.
        visualizar_extrato(self): Visualiza o extrato da conta.
    """
    def __init__(self):
        """
        Inicializa um novo objeto Conta com valores padrões.
        """
        self.saldo = 0
        self.depositos = []
        self.saques = []
        self.limite_transacoes = 10
        self.valor_maximo_saques = 500
        self.mascara_ptbr = "%d/%m/%Y %H:%M"

    def depositar(self, valor):
        """
        Deposita fundos na conta e subtrai valor para o limite diario de transações
        
        Args:
            valor (float): o valor a ser depositado.
        """
        if len(self.depositos + self.saques) < self.limite_transacoes:
            self.saldo += valor
            self.depositos.append((datetime.now().strftime(self.mascara_ptbr), valor))
            return True
        else:
            return False

    def sacar(self, valor):
        """
        Sacar fundos da conta, se as condições forem atendidas.
        Condições:
        1. O saldo da conta deve ser maior ou igual ao valor a ser sacado.
        2. O limite diário de saques deve ser atingido.
        3. O valor a ser sacado deve ser menor ou igual ao valor máximo por saque.

        Args:
            valor (float): o valor a ser sacado.

        Returns:
            bool: True se o saque foi bem-sucedido, False caso contrário.
        """
        if self.saldo >= valor and len(self.saques + self.depositos) < self.limite_transacoes and valor <= self.valor_maximo_saques:
            self.saldo -= valor
            self.saques.append((datetime.now().strftime(self.mascara_ptbr), valor))
            return True
        else:
            return False

    def visualizar_extrato(self):
        """
        Visualiza o extrato da conta.
        O extrato lista todos os depósitos e saques realizados na conta.
        No fim da listagem, exibe o saldo atual da conta.
        """
        if not self.depositos and not self.saques:
            print("Não foram realizadas movimentações")
        else:
            print("Extrato:")
            for deposito in self.depositos:
                print(f"Depósito: R$ {deposito[1]:.2f} em {deposito[0]}")
            for saque in self.saques:
                print(f"Saque: R$ {saque[1]:.2f} em {saque[0]}")
            print(f"Saldo atual: R$ {self.saldo:.2f}")

        input("Pressione Enter para continuar...")

def main():
    '''
    Função principal do programa.
    Exibe o menu de opções e realiza as operações escolhidas pelo usuário.
    '''
    conta = Conta()
    while True:
        print("\nMenu:")
        print("1. Depositar")
        print("2. Sacar")
        print("3. Visualizar extrato")
        print("4. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            valor = solicitar_valor("Digite o valor a ser depositado: ")
            if valor is not None:
                if conta.depositar(valor):
                    print("Depósito realizado com sucesso!")
                else:
                    print("Limite diário de transações atingido!")
        elif opcao == "2":
            valor = solicitar_valor("Digite o valor a ser sacado: ")
            if valor is not None:
                if conta.sacar(valor):
                    print("Saque realizado com sucesso!")
                else:
                    print("Saque negado! Verifique se o saldo é suficiente, se o limite diário de saques foi atingido ou se o valor do saque é maior que o permitido.")
        elif opcao == "3":
            conta.visualizar_extrato()
        elif opcao == "4":
            break
        else:
            print("Opção inválida!")

def solicitar_valor(mensagem):
    '''
    Solicita um valor numérico do usuário.

    Args:
        mensagem (str): a mensagem a ser exibida ao solicitar o valor.

    Returns:
        float: o valor numérico inserido pelo usuário.
    '''
    while True:
        try:
            valor = float(input(mensagem))
            return valor
        except ValueError:
            print("Por favor, insira um valor numérico válido.")
        except KeyboardInterrupt:
            print("\nSaindo...")
            time.sleep(1)
            os._exit(0)

if __name__ == "__main__":
    main()
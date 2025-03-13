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

v3:
Modificar o programa e adicionar funções para criar usuários e contas bancárias.
Um usuário deve ter um nome, data de nascimento, cpf e endereço.
O CPF deve ser verificado para não haver duplicatas.
Uma conta bancária deve ter uma agência, número da conta e usuário associado.
O número da conta deve ser sequencial e começar em 1.
A agência deve ser fixa em 0001.
'''

from datetime import datetime, time
import os

class Usuario:
    """
    Uma classe representando um usuário do banco.

    Atributos:
        nome (str): o nome do usuário.
        data_nascimento (str): a data de nascimento do usuário.
        cpf (str): o CPF do usuário.
        endereco (str): o endereço do usuário.
    """
    def __init__(self, nome, data_nascimento, cpf, endereco):
        """
        Inicializa um novo objeto Usuario.

        Args:
            nome (str): o nome do usuário.
            data_nascimento (str): a data de nascimento do usuário.
            cpf (str): o CPF do usuário.
            endereco (str): o endereço do usuário.
        """
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.endereco = endereco

class ContaBancaria:
    """
    Uma classe representando uma conta bancária.

    Atributos:
        agencia (str): o número da agência.
        numero_conta (int): o número da conta.
        usuario (Usuario): o usuário associado à conta.
        saldo (float): o saldo da conta.
        depositos (lista): uma lista de depósitos, cada um uma tupla de (data, valor).
        saques (lista): uma lista de saques, cada um uma tupla de (data, valor).
    """
    def __init__(self, agencia, numero_conta, usuario):
        """
        Inicializa um novo objeto ContaBancaria.

        Args:
            agencia (str): o número da agência.
            numero_conta (int): o número da conta.
            usuario (Usuario): o usuário associado à conta.
        """
        self.agencia = agencia
        self.numero_conta = numero_conta
        self.usuario = usuario
        self.saldo = 0
        self.depositos = []
        self.saques = []
        self.limite_transacoes = 10
        self.valor_maximo_saques = 500
        self.mascara_ptbr = "%d/%m/%Y %H:%M"

    def depositar(self, valor):
        """
        Deposita fundos na conta.

        Args:
            valor (float): o valor a ser depositado.

        Returns:
            bool: True se o depósito foi bem-sucedido, False caso contrário.
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

        Returns:
            None
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

class Conta:
    """
    Uma classe representando o sistema de contas bancárias.

    Atributos:
        usuarios (lista): uma lista de usuários cadastrados.
        contas (lista): uma lista de contas bancárias.
        numero_conta_sequencial (int): o número sequencial para novas contas.
        conta_atual (ContaBancaria): a conta atualmente acessada.
    """
    def __init__(self):
        """
        Inicializa um novo objeto Conta com valores padrões.
        """
        self.usuarios = []
        self.contas = []
        self.numero_conta_sequencial = 1
        self.conta_atual = None

    def criar_usuario(self):
        """
        Cria um novo usuário.
        É necessário informar o nome, data de nascimento, cpf e endereço.
        O CPF precisa ser checado, pois não podem haver duplicatas.

        Returns:
            Usuario: o novo usuário criado.
        """
        nome = input("Digite o nome do usuário: ")
        data_nascimento = input("Digite a data de nascimento (dd/mm/aaaa): ")
        cpf = input("Digite o CPF (apenas números): ")
        endereco = input("Digite o endereço (logradouro, número - bairro - cidade/sigla estado): ")

        # Verifica se o CPF já está cadastrado
        for usuario in self.usuarios:
            if usuario.cpf == cpf:
                print("Erro: CPF já cadastrado.")
                return None

        novo_usuario = Usuario(nome, data_nascimento, cpf, endereco)
        self.usuarios.append(novo_usuario)
        print("Usuário criado com sucesso!")
        return novo_usuario

    def criar_conta(self, usuario):
        """
        Cria uma conta bancária para o usuário e armazena em uma lista.
        A conta é composta por: agência, número da conta e usuário.
        O número da conta é sequencial e começa de 1.
        O número da agência é fixa em 0001.
        Um usuário pode ter mais de uma conta.

        Args:
            usuario (Usuario): o usuário associado à conta.

        Returns:
            ContaBancaria: a nova conta bancária criada.
        """
        agencia = "0001"
        numero_conta = self.numero_conta_sequencial
        nova_conta = ContaBancaria(agencia, numero_conta, usuario)
        self.contas.append(nova_conta)
        self.numero_conta_sequencial += 1
        print(f"Conta criada com sucesso! Número da conta: {numero_conta}")
        return nova_conta

    def acessar_conta(self, numero_conta):
        """
        Acessa uma conta bancária.

        Args:
            numero_conta (int): o número da conta a ser acessada.
        
        Returns:
            bool: True se a conta foi acessada com sucesso, False caso contrário.
        """
        for conta in self.contas:
            if conta.numero_conta == numero_conta:
                self.conta_atual = conta
                print(f"Conta {numero_conta} acessada com sucesso!")
                return True
        print("Erro: Conta não encontrada.")
        return False

def main():
    '''
    Função principal do programa.
    Exibe o menu de opções e realiza as operações escolhidas pelo usuário.
    '''
    sistema = Conta()
    while True:
        print("\nMenu:")
        print("1. Depositar")
        print("2. Sacar")
        print("3. Visualizar extrato")
        print("4. Criar usuário")
        print("5. Criar conta")
        print("6. Acessar conta")
        print("7. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            if sistema.conta_atual is None:
                print("Erro: Nenhuma conta acessada. Acesse uma conta primeiro.")
            else:
                valor = solicitar_valor("Digite o valor a ser depositado: ")
                if valor is not None:
                    if sistema.conta_atual.depositar(valor):
                        print("Depósito realizado com sucesso!")
                    else:
                        print("Limite diário de transações atingido!")
        elif opcao == "2":
            if sistema.conta_atual is None:
                print("Erro: Nenhuma conta acessada. Acesse uma conta primeiro.")
            else:
                valor = solicitar_valor("Digite o valor a ser sacado: ")
                if valor is not None:
                    if sistema.conta_atual.sacar(valor):
                        print("Saque realizado com sucesso!")
                    else:
                        print("Saque negado! Verifique se o saldo é suficiente, se o limite diário de saques foi atingido ou se o valor do saque é maior que o permitido.")
        elif opcao == "3":
            if sistema.conta_atual is None:
                print("Erro: Nenhuma conta acessada. Acesse uma conta primeiro.")
            else:
                sistema.conta_atual.visualizar_extrato()
        elif opcao == "4":
            sistema.criar_usuario()
        elif opcao == "5":
            if not sistema.usuarios:
                print("Erro: Nenhum usuário cadastrado. Crie um usuário primeiro.")
            else:
                cpf = input("Digite o CPF do usuário para criar a conta: ")
                usuario_encontrado = None
                for usuario in sistema.usuarios:
                    if usuario.cpf == cpf:
                        usuario_encontrado = usuario
                        break
                if usuario_encontrado:
                    sistema.criar_conta(usuario_encontrado)
                else:
                    print("Erro: Usuário não encontrado.")
        elif opcao == "6":
            numero_conta = input("Digite o número da conta para acessar: ")
            try:
                numero_conta = int(numero_conta)
                sistema.acessar_conta(numero_conta)
            except ValueError:
                print("Erro: Número da conta inválido.")
        elif opcao == "7":
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
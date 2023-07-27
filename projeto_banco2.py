import textwrap

def menu():
    menu_text = """\n
    ================ MENU ================
    [1]\tSacar
    [2]\tDepositar
    [3]\tExtrato
    [4]\tNova conta
    [5]\tListar contas
    [6]\tNovo usuário
    [0]\tSair
    => """
    return input(textwrap.dedent(menu_text))

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
            print("\n@@@ Seu saldo é insuficiente para realizar essa operação. @@@")
    elif excedeu_limite:
            print("\n@@@ O valor do saque excede o limite permitido para o seu tipo de conta. @@@")
    elif excedeu_saques:
            print("\n O número máximo de saques diários foi atingido. @@@")
    elif valor > 0:
            saldo -= valor
            numero_saques += 1
            extrato += f"Saque:\t\tR$ {valor:.2f} realizado.\n"
            print(f"Saque de R$ {valor:.2f} realizado.")
    else:
            print("@@@ Valor inválido. O valor do saque deve ser maior que zero. @@@")
    
    return saldo, extrato, numero_saques

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Deposito: R$ {valor:.2f}\n"
        print(f"\n=== Deposito de R$ {valor:.2f} realizado com sucesso! ===")
    else:
        print("\n@@@ Valor inválido. O valor depositado deve ser maior do que R$ 0,00. @@@")

    return saldo, extrato

def exibir_extrato(saldo, /, *, extrato):
    print("\n===================== Extrato ===============================================")
    print("Não foram realizadas movimentações na conta" if not extrato else extrato)
    print(f"\nSaldo disponivel em sua conta é de R$ {saldo:.2f}")
    print("===============================================================================")

def criar_novo_usuario(usuarios):
    cpf = input("Informe o CPF (somente números)")
    usuario = filtrar_usuario(cpf, usuarios)
    
    if usuario:
        print("\n@@@ Já existe um usuário com o CPF informado. @@@")
        return
    
    nome = input("Informe o seu nome completo: ")
    data_nascimento = input("Informe a sua data de nascimento, no formato (dd/mm/aaaa): ")
    endereco = input("Informe local de residência (logradouro, numero - bairro - cidade/sigla estado): ")

    usuarios.append({"nome":nome, "data_nascimento":data_nascimento, "cpf":cpf, "endereco":endereco})

    print("=== Usuário criado com sucesso! ===")

def filtrar_usuario(cpf, usuarios):
     usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
     return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_nova_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
         print("\n=== Conta criada com sucesso! ===")
         return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    
    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}        
        """
        print('=' * 100)
        print(textwrap.dedent(linha))
        
def main():
    LIMITE_SAQUES_DIARIOS = 3
    AGENCIA = "0001"
    saldo = 0
    extrato = ""
    limite_saque = 500
    saques_diarios = 0
    usuarios = []
    contas = []

    while True:
         
        opcao = menu()

        if opcao == "1":
            valor = float(input("Digite o valor que deseja sacar: "))

            saldo, extrato, saques_diarios = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite_saque,
                numero_saques=saques_diarios,
                limite_saques=LIMITE_SAQUES_DIARIOS,
            )             

        elif opcao == "2":
            valor = float(input("Digite o valor que deseja depositar: "))

            saldo, extrato = depositar(saldo, valor, extrato)
        
        elif opcao == "3":
            exibir_extrato(saldo, extrato=extrato)
    
        elif opcao == "4":
            numero_conta = len(contas) + 1
            conta = criar_nova_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)

        elif opcao == "5":
             listar_contas(contas)   

        elif opcao == "6":
            criar_novo_usuario(usuarios)       

        elif opcao == "0":
            print("Saindo do sistema...")
            print("Obrigado por utilizar nosso sistema, volte sempre!")
            break
        
        else:
            print("A opção escolhida é invalida, tente novamente.")

main()
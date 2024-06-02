# Segundo desafio DIO sistema bancário!

import os
import random
import datetime
import re

def main():
    VALOR_SEQUENCIAL_INICIAL_AGENCIA = "0001"
    continua_operacao = True
    qtd_saque_disponivel = 3
    lista_usuarios = []
    lista_contas = []
    
    limpar_terminal()
    print("Crie um usuário para acessar o sistema bancário!")
    input("Pressione alguma tecla para continuar...")
    usuario = criar_usuario(lista_usuarios, True)
    
    limpar_terminal()
    print("Crie uma conta com base no usuário para acessar o sistema bancário!")
    input("Pressione alguma tecla para continuar...")
    lista_contas = criar_conta(VALOR_SEQUENCIAL_INICIAL_AGENCIA, lista_contas, lista_usuarios, True)
    
    for conta in lista_contas:
        if usuario["CPF"] == conta["CPF"]:
            conta_usuario = conta
            break
    
    conta_usuario["Saldo"] = define_orcamento_inicial()

    while continua_operacao:
        limpar_terminal()
        print("""Seja bem vindo ao sistema Bancario!\n
O que deseja fazer?

1-Depósito
2-Saque
3-Extrato
4-Novo Usuário
5-Nova Conta
6-Listar Contas
7-Sair\n""")

        opcao = input()

        if opcao == "1" or opcao.lower() in ["depósito", "deposito"]:
            conta_usuario["Saldo"], conta_usuario["Extrato"] = deposito(conta_usuario["Saldo"], conta_usuario["Extrato"], lista_usuarios, lista_contas)
        elif opcao == "2" or opcao.lower() == "saque":
            conta_usuario["Saldo"], qtd_saque_disponivel, conta_usuario["Extrato"] = saque(saldo_disponivel=conta_usuario["Saldo"], qtd_saque_disponivel=qtd_saque_disponivel, atividades_conta=conta_usuario["Extrato"])
        elif opcao == "3" or opcao.lower() == "extrato":
            extrato(conta_usuario["Saldo"], atividades_conta=conta_usuario["Extrato"])
        elif opcao == "4" or opcao.lower() in ["usuario", "usuário", "novousuario", "novousuário"]:
            lista_usuarios = criar_usuario(lista_usuarios, False)
        elif opcao == "5" or opcao.lower() in ["conta", "novaconta"]:
            lista_contas = criar_conta(VALOR_SEQUENCIAL_INICIAL_AGENCIA, lista_contas, lista_usuarios)
        elif opcao == "6" or opcao.lower() in ["listarcontas", "listar"]:
            listar_contas(lista_contas)
        elif opcao == "7" or opcao.lower() == "sair":
            limpar_terminal()
            continua_operacao = False
            print("Saindo do sistema...")
            break
        else:
            print("\nOpção inválida!!!")
            input("Pressione alguma tecla para continuar...")
            continue

                    
def deposito(saldo_disponivel, atividades_conta, lista_usuarios, lista_contas, /):
    sair = False
    concluiu_deposito = False
    minha_conta = False
    
    while not sair:
        limpar_terminal()
        print("Você está na área de Depósito. Caso queira voltar ao menu digite a palavra \"sair\"\n")
        print("Você deseja depositar para você ou para outra pessoa ? \n\n1-para mim\n2-outra pessoa\n3-sair\n")
        pessoa = input()
    
        if pessoa == "1" or pessoa.lower() in ["para", "mim"]:
            minha_conta = True
        elif pessoa == "2" or pessoa.lower() in ["outra", "pessoa"]:
            minha_conta = False
            limpar_terminal()
            cpf_pessoa = input("Insira o CPF da pessoa que deseja fazer o depósito: ")
            
            if not filtra_usuario(lista_contas, cpf_pessoa, "cpf"):
                print("\nUsuário não encontrado!")
                input("Pressione alguma tecla para continuar...")
                sair = True
                break
            else:
                print("\nUsuário encontrado!")
                input("Pressione alguma tecla para continuar...")
        elif pessoa == "3" or pessoa.lower() in ["sair", "voltar"]:
            sair = True
            break
        else:
            print("\nValor inserido inválido!")
            input("Pressione alguma tecla para continuar...")
            continue
        
        while not sair:
            limpar_terminal()
            valor = str(input("Insira o valor que deseja depositar: "))

            if valor.lower() == "sair":
                sair = True
                break
            
            try:
                valor = float(valor)
            except:
                print("\nValor digitado inválido!")
                input("Pressione alguma tecla para continuar...")
                continue
            
            if valor <= 0 and not sair:
                limpar_terminal()
                mensagem = """O valor digitado é nulo ou negativo!
Deseja depositar outro valor ?

1-Sim
2-Não
\n"""

                sair = valida_continuar(mensagem, sair)
                continue
                    
            if valor > 0:
                break            
            
        while not sair:
            limpar_terminal()
            if minha_conta:
                saldo_atual = saldo_disponivel + valor
            else:
                saldo_atual = saldo_disponivel - valor
                        
                
            resposta = input(f"""Seu saldo atual: R${saldo_disponivel:.2f}
Valor após o depósito: R${saldo_atual:.2f}
Você deseja realizar um depósito no valor de R${valor:.2f} ?

1-Sim
2-Não
\n""")
            
            if resposta == "1" or resposta.lower() in ["sim", "s"]:
                atividades_conta += f"\nDepósito feito no valor de R${valor:.2f} retirado do seu saldo de R${saldo_disponivel:.2f} para {'a sua conta' if minha_conta else 'a conta de ' + nome_pessoa}. Seu saldo atual é de R${saldo_atual:.2f}.\n"
                saldo_disponivel = saldo_atual
                concluiu_deposito = True
                break
            elif resposta == "2" or resposta.lower() in ["nao", "não", "n"]:
                break
            else:
                print("Valor inserido inválido!")
                input("Pressione alguma tecla para continuar...")
           
        limpar_terminal()
        menasgem = f"""{'Depósito feito com sucesso!' if concluiu_deposito else 'Depósito cancelado!' } \n
Deseja realizar outro Depósito ?

1-Sim
2-Não\n"""
        
        sair = valida_continuar(menasgem, sair)
        break
    
    return saldo_disponivel, atividades_conta
    
    
def saque(*, saldo_disponivel, qtd_saque_disponivel, atividades_conta):
    concluiu_saque = False
    sair = False
    
    while not sair:
        if qtd_saque_disponivel == 0:
            limpar_terminal()
            print("Quantidade de saques excedidas hoje!!!")
            input("Pressione alguma tecla para continuar...")
            sair = True
            break
    
        limpar_terminal()
        print("Você está na área de Saque. Caso queira voltar ao menu digite a palavra \"sair\"")
        valor_saque = str(input("Insira o valor que deseja sacar: "))

        if valor_saque.lower() == "sair":
            sair = True
            break
                
        try:
            valor_saque = float(valor_saque)
        except:
            print("\nValor digitado não válido!")
            input("Pressione alguma tecla para continuar...")
            continue
        
        if valor_saque <= 0:
            limpar_terminal()
            print("Valor digitado é nulo ou negativo!")
            input("Pressione alguma tecla para continuar...")
            continue
        elif valor_saque > saldo_disponivel:
            limpar_terminal()
            print("Saldo menor que o valor digitado!")
            input("Pressione alguma tecla para continuar...")
            continue
        elif valor_saque > 500.00:
            limpar_terminal()
            print("Valor acima de R$500,00!")
            input("Pressione alguma tecla para continuar...")
            continue
    
        saldo_atual = saldo_disponivel - valor_saque
        
        while not sair:
            limpar_terminal()
            resposta = input(f"""Seu saldo atual: R${saldo_disponivel:.2f}
Valor após o saque: R${saldo_atual:.2f}
Você realmente deseja realizar um depósito no valor de R${valor_saque:.2f} ? 

1-Sim
2-Não
\n""")
        
            if resposta == "1" or resposta.lower() in["sim", "s"]:
                atividades_conta += f"\nSaque realizado no valor de {valor_saque:.2f} do seu saldo de {saldo_disponivel:.2f}. Seu saldo atual é de {saldo_atual:.2f}.\n"
                saldo_disponivel = saldo_atual
                qtd_saque_disponivel -= 1
                concluiu_saque = True
                break
            elif resposta == "2" or resposta.lower() in ["nao", "não", "n"]:
                break
            else:
                print("\nValor digitado não válido!")
                input("Pressione alguma tecla para continuar...")
        
        if not sair:            
            limpar_terminal()
            mensagem = (f"""{'Saque feito com sucesso!' if concluiu_saque else 'Saque cancelado!' } \n
Deseja realizar outro Saque ?

1-Sim
2-Não\n""")
            
            sair = valida_continuar(mensagem, sair)
                
    return saldo_disponivel, qtd_saque_disponivel, atividades_conta
        
        
def extrato(saldo_disponivel, /, *, atividades_conta):
    
    limpar_terminal()
    
    formatacao_extrato = "=======================EXTRATO=======================\n"
    
    if atividades_conta != "":
        formatacao_extrato += atividades_conta
    else:
        formatacao_extrato += "Não foram realizadas nenhuma movimentação."    
    
    formatacao_extrato += f"\nSaldo restante: R${saldo_disponivel:.2f}"
    
    formatacao_extrato += "\n===================================================="
    
    print(formatacao_extrato)
    input("\n\nPressione alguma tecla para continuar...")
    
    
def limpar_terminal():
    if os.name == "nt":
        os.system('cls')
    else:
        os.system('clear')
        
        
def define_orcamento_inicial():
    while True:
        limpar_terminal()
        print("Teste Sistema Bancário!")
        
        try:
            saldo_disponivel = float(input("Digite a quantia de saldo que deseja ter em sua conta teste: "))
            break
        except:
            print("Valor inserido inválido!")
            input("Pressione alguma tecla para continuar...")
            
    return saldo_disponivel


def valida_continuar(menasgem, sair):
    while True:
        limpar_terminal()
        print(menasgem)
        continuar = input()

        if continuar == "1" or continuar.lower() in ["s", "sim"]:
            break
        elif continuar == "2" or continuar.lower() in ["n", "não", "nao"]:
            sair = True
            break
        else:
            print("\nValor inserido inválido!")
            input("Pressione alguma tecla para continuar...")
            
    return sair
  
  
def criar_usuario(usuarios: list[object], tester=False):
    sair = False
    cancelou = False
    nome = ""
    cpf = ""
    data_nascimento = ""
    informacoes_pessoais = [["Nome", "Informe o nome completo: "], ["Data de nascimento", "Informe sua data de nascimento dd/mm/aaaa: "]]
    informacoes_endereco = []

    while not sair:
        limpar_terminal()
        cpf = input("Informe o CPF da conta: ")
        
        if cpf.lower() == "sair":
            sair = True
            cancelou = True
            break
        elif len(cpf) != 11:
            limpar_terminal()
            print("CPF inválido!")
            input("Pressione alguma tecla para continuar...")
            continue
        
        cpf = re.sub(r'\D', '', cpf)
        usuario_cadastado = filtra_usuario(usuarios, cpf, "CPF")

        if usuario_cadastado:
            limpar_terminal()

            mensagem = """Usuário com o CPF já cadastrado!
Deseja cadastrar outro usuário ?

1-Sim
2-Não
\n\n"""

            sair = valida_continuar(mensagem, sair)
            continue

        while not sair:
            limpar_terminal()
            nome = input(informacoes_pessoais[0][1])

            if nome == "" or contem_numero(nome) or len(nome) < 3:
                limpar_terminal()
                print("Valores inseridos inválidos!")
                input("Pressione alguma tecla para continuar...")
                continue
            elif nome == "sair":
                sair = True
                cancelou = True
                
            break
            
        while not sair:
            data_nascimento = input(informacoes_pessoais[1][1])
            
            if data_nascimento.lower() == "sair":
                sair = True
                cancelou = True
                continue
            else:
                data_nascimento = re.sub(r'\D', '', data_nascimento)
                
                if len(data_nascimento) == 8:
                    data_nascimento = data_nascimento[:2] + "/" + data_nascimento[2:4] + "/" + data_nascimento[4:]
                    
                    try:
                        datetime.datetime.strptime(data_nascimento, "%d/%m/%Y")
                        break
                    except:
                        limpar_terminal()
                        print("Valores inseridos inválidos!")
                        input("Pressione alguma tecla para continuar...")
                        continue
                else:
                    limpar_terminal()
                    print("Valores inseridos inválidos!")
                    input("Pressione alguma tecla para continuar...")
                    continue
        
        perguntas_endereco = [["Cidade: ", "Informe a cidade: "], ["Bairro: ", "Informe o bairro: "], ["Numero: ", "Informe o número: "], ["Estado: ", "Informe o estado: "], ["Logradouro: ", "Informe o logradouro: "]]
        
        while not sair:
            i = 0
            while i < len(perguntas_endereco):
                limpar_terminal()
                print("Informações de endereço\n ")
            
                resposta = input(perguntas_endereco[i][1])
                
                if resposta.lower() == "sair":
                    sair = True
                    cancelou = True
                    break
                elif i != 2:
                    if resposta == "" or contem_numero(resposta):
                        limpar_terminal()
                        print("Valores inseridos inválidos!")
                        input("Pressione alguma tecla para continuar...")
                        continue
                else:
                    try:
                        resposta = int(resposta)
                    except:
                        limpar_terminal()
                        print("Valores inseridos inválidos!")
                        input("Pressione alguma tecla para continuar...")
                        continue
                
                informacoes_endereco.append(f"{perguntas_endereco[i][0]}: {resposta}")
                i += 1
            break
                        
        if not sair:
            limpar_terminal()
            usuarios.append({"CPF": cpf, informacoes_pessoais[0][0]: nome, informacoes_endereco[1][0]: data_nascimento, "Endereco": informacoes_endereco})
            
            if not tester:
                mensagem = """
Usuário cadastrado com sucesso!
Deseja cadastrar outro usuário ?

1-Sim
2-Não
\n\n"""

                sair = valida_continuar(mensagem, sair)
                continue
            else:
                sair = True

    if cancelou and tester:
        os._exit(0)
    elif tester:
        return {"CPF": cpf, informacoes_pessoais[0][0]: nome, informacoes_pessoais[1][0]: data_nascimento, "Endereco": informacoes_endereco}
    else:
        return usuarios
    

def criar_conta(sequencial_agencia, contas: list[object], usuarios: list[object], tester=False):
    sair = False
    cancelou = False

    while not sair:
        limpar_terminal()
        print("Você está na área de criação de conta. Caso queira voltar ao menu digite a palavra \"sair\"")
        cpf = input("Informe o CPF do usuário que deseja criar a conta: ")

        if cpf.lower() == "sair":
            sair = True
            cancelou = True
            break
        else:
            cpf = re.sub(r'\D', '', cpf)
        
        if len(cpf) != 11:
            limpar_terminal()
            print("CPF inválido!")
            input("Pressione alguma tecla para continuar...")
            continue

        usuario_cadastrado = filtra_usuario(usuarios, cpf, "CPF")
        possui_conta = filtra_usuario(contas, cpf, "CPF")

        if not possui_conta and usuario_cadastrado:
            agencia = str(int(sequencial_agencia) + len(contas)).zfill(4)
            numero_conta = random.randint(1, 9999)
            saldo = 0.0
            
            numero_valido = False
            
            while not numero_valido:
                for conta in contas:
                    while conta["numero da conta"] == str(numero_conta).zfill(4):
                        numero_conta = random.randint(1, 9999)

                repete = False
                for conta in contas:
                    if conta["numero da conta"] == str(numero_conta).zfill(4):
                        repete = True
                        break
                        
                if not repete:
                    numero_valido = True
               
            contas.append({"Agencia": str(agencia).zfill(4), "Conta": str(numero_conta).zfill(4), "CPF": cpf, "Saldo": saldo, "Extrato": ""})
            print("Conta cadastrada com sucesso!")
            print(f"Agência: {agencia}\nConta: {numero_conta}\nCPF: {cpf}\nSaldo: R${saldo:.2f}")
            input("Pressione alguma tecla para continuar...")
            
        limpar_terminal()
        
        mensagem = ""
        
        if not tester:
            if possui_conta:
                mensagem = "Usuário já possui conta!"
            elif not usuario_cadastrado:
                mensagem = "Usuário não encontrado!"
            
                mensagem += f"""\nDeseja cadastrar uma conta para outro usuário ?

1- Sim
2-Não
\n\n"""

                sair = valida_continuar(mensagem, sair)
                continue
        elif not usuario_cadastrado:
            print("Usuário não encontrado!")
            input("Pressione alguma tecla para continuar...")
            continue
        else:
            sair = True

    if cancelou and tester:
        os._exit(0)

    return contas
            

def listar_contas(contas: list[object]):
    limpar_terminal()
    
    if len(contas) == 0:
        print("Nenhuma conta cadastrada!")
    else:
        print("====================LISTA DE CONTAS===================\n")
        
        for conta in contas:
            print(f"Agência: {conta['Agencia']}\nConta: {conta['Conta']}\nCPF: {conta['CPF']}\nSaldo: R${conta['Saldo']:.2f}")
            
        print("\n====================================================")
            
    input("\n\nPressione alguma tecla para continuar...")


def filtra_usuario(usuarios, dados_usuario, filtro):
    for usuario in usuarios:
        if usuario[filtro] == dados_usuario:
            return True
        
    return False
    
    
def contem_numero(palavra):
    return any(letra.isdigit() for letra in palavra)
            
            
main()
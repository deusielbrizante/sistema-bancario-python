# Desafio DIO sistema bancário!

import os

def main():
    continua_operacao = True
    saque_disponivel = 3
    atividades_conta = ""

    saldo_disponivel = define_orcamento_inicial()

    while continua_operacao:
        limpar_terminal()
        print("""Seja bem vindo ao sistema Bancario!\n
O que deseja fazer?

1-Depósito
2-Saque
3-Extrato
4-Sair\n""")

        opcao = input()

        if opcao == "1" or opcao.lower() in ["depósito", "deposito"]:
            saldo_disponivel, atividades_conta = deposito(saldo_disponivel, atividades_conta)
        elif opcao == "2" or opcao.lower() == "saque":
            saldo_disponivel, saque_disponivel, atividades_conta = saque(saldo_disponivel, saque_disponivel, atividades_conta)
        elif opcao == "3" or opcao.lower() == "extrato":
            atividades_conta, saldo_disponivel = extrato(atividades_conta, saldo_disponivel)
        elif opcao == "4" or opcao.lower() == "sair":
            limpar_terminal()
            continua_operacao = False
            print("Saindo do sistema...")
            break
        else:
            print("\nOpção inválida!!!")
            input("Pressione alguma tecla para continuar...")
            continue

                    
def deposito(saldo_disponivel, atividades_conta):    
    sair = False
    concluiu_deposito = False
    minha_conta = False
    
    while not sair:
        while True:
            limpar_terminal()
            print("Você deseja depositar para você ou para outra pessoa ? \n\n1-para mim\n2-outra pessoa\n3-sair\n")
            pessoa = input()
        
            if pessoa == "1" or pessoa.lower() in ["para", "mim"]:
                minha_conta = True
                break
            elif pessoa == "2" or pessoa.lower() in ["outra", "pessoa"]:
                minha_conta = False
                limpar_terminal()
                nome_pessoa = input("Insira o nome da pessoa que deseja fazer o depósito: ")
                break
            elif pessoa == "3" or pessoa.lower() in ["sair", "voltar"]:
                sair = True
                break
            else:
                print("\nValor inserido inválido!")
                input("Pressione alguma tecla para continuar...")
        
        while not sair:
            valor_valido = False
            
            while not valor_valido:
                try:
                    limpar_terminal()
                    print("Você está na área de Depósito. Caso queira voltar ao menu digite a palavra \"sair\"")
                    valor = input("Insira o valor que deseja depositar: ")

                    if valor.lower() == "sair":
                        sair = True
                        valor_valido = True
                    else:
                        valor = float(valor)
                        valor_valido = True
                except:
                    print("\nValor digitado inválido!")
                    input("Pressione alguma tecla para continuar...")
             
            if not sair:
                while valor <= 0:
                    limpar_terminal()
                    print("O valor digitado é nulo ou negativo!")
                    resposta = input("""Deseja depositar outro valor ?

1-Sim
2-Não
\n""")
                    
                    if resposta == "1" or resposta.lower() in ["sim", "s"]:
                        break
                    elif resposta == "2" or resposta.lower() in ["nao", "não", "n"]:
                        sair = True
                        break
                    else:
                        limpar_terminal()
                        print("Valor inserido inválido!")
                        input("Pressione alguma tecla para continuar...")
                        
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
    
        while not sair:            
            limpar_terminal()
            menasgem = (f"""{'Depósito feito com sucesso!' if concluiu_deposito else 'Depósito cancelado!' } \n
Deseja realizar outro Depósito ?

1-Sim
2-Não\n""")
            sair = valida_continuar(menasgem, sair)
            break
    
    return saldo_disponivel, atividades_conta
    
    
def saque(saldo_disponivel, saque_disponivel, atividades_conta):
    
    concluiu_saque = False
    sair = False
    
    while not sair:
        if saque_disponivel == 0:
            limpar_terminal()
            print("Quantidade de saques excedidas hoje!!!")
            input("Pressione alguma tecla para continuar...")
            sair = True
            return
    
        while not sair:
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
            
            while valor_saque <= 0:
                limpar_terminal()
                mensagem = ("""O valor digitado é nulo ou negativo!)
Deseja depositar outro valor ?

1-Sim
2-Não
\n""")
                sair = valida_continuar(mensagem,sair)
                break
            
            if valor_saque > 0:
                break
        
        if not sair:
            if valor_saque > saldo_disponivel:
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
                saque_disponivel -= 1
                concluiu_saque = True
                break
            elif resposta == "2" or resposta.lower() in ["nao", "não", "n"]:
                break
            else:
                print("\nValor digitado não válido!")
                input("Pressione alguma tecla para continuar...")
        
        while not sair:            
            limpar_terminal()
            mensagem = (f"""{'Saque feito com sucesso!' if concluiu_saque else 'Saque cancelado!' } \n
Deseja realizar outro Saque ?

1-Sim
2-Não\n""")
            sair = valida_continuar(mensagem, sair)
            break
                
    return saldo_disponivel, saque_disponivel, atividades_conta
        
        
def extrato(atividades_conta, saldo_disponivel):
    
    limpar_terminal()
    
    formatacao_extrato = "=======================EXTRATO=======================\n"
    
    if atividades_conta != "":
        formatacao_extrato += atividades_conta
    else:
        formatacao_extrato += "Não foram realizadas nenhuma movimentação."    
    
    formatacao_extrato += f"\nSaldo restante: R${saldo_disponivel:.2f}"
    
    print(formatacao_extrato)
    input("\n\nPressione alguma tecla para continuar...")
    
    return atividades_conta, saldo_disponivel
    
    
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
  
  
main()
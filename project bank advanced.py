from random import randint
from os import system

usuarios = []
usuario_atual = None

def criar_conta_corrente():
    agencia = randint(1000, 9999)
    numero = randint(1000000, 9999999)
    dv = randint(0, 9)
    conta = {
        "Agência": f"{agencia}",
        "Número da Conta": f"{numero}-{dv}",
        "Saldo": 0.0,
        "Extrato": [],
        "Saques Hoje": 0
    }
    return conta

def criar_usuario():
    global usuario_atual
    nome = input(
        "Digite o seu nome: "
        )
    idade = int(input(
        "Digite sua idade: "
        ))
    
    if idade < 18:
        print(
            "A idade mínima é de 18 anos."
            )
        return None

    data_de_nascimento = input(
        "Digite sua data de nascimento [xx/xx/xxxx]: "
        )
    
    cpf = input(
        "Digite seu CPF (apenas números): "
        )
    
    if len(cpf) != 11 or not cpf.isdigit():
        print(
            "CPF inválido. Deve conter exatamente 11 dígitos numéricos."
            )
        return None

    conta = criar_conta_corrente()

    usuario = {
        "Nome": nome,
        "Idade": idade,
        "Data de Nascimento": data_de_nascimento,
        "CPF": cpf,
        "Conta Bancária": conta,
    }

    print(
        "Usuário criado com sucesso!"
        )
    usuario_atual = usuario
    return usuario

def listar_usuarios():
    print(
        "\nUsuários cadastrados:"
        )
    for i, usuario in enumerate(usuarios):
        print(
            f"{i + 1}. {usuario['Nome']}"
            )

def trocar_usuario():
    listar_usuarios()
    escolha = int(input(
        "Escolha o número do usuário para usar: "
        )) - 1
    if 0 <= escolha < len(usuarios):
        global usuario_atual
        usuario_atual = usuarios[escolha]
        print(
            f"Usuário atual: {usuario_atual['Nome']}"
            )
    else:
        print(
            "Número inválido."
            )

def ver_usuario_atual():
    if usuario_atual:
        conta = usuario_atual["Conta Bancária"]
        print(
        f"\nInformações do usuário atual:\n"
        f"Nome: {usuario_atual['Nome']}\n"
        f"Idade: {usuario_atual['Idade']}\n"
        f"Data de Nascimento: {usuario_atual['Data de Nascimento']}\n"
        f"CPF: {usuario_atual['CPF']}\n"
        f"Agência: {conta['Agência']}\n"
        f"Número da Conta: {conta['Número da Conta']}\n"
        f"Saldo: R$ {conta['Saldo']:.2f}"
    )
    else:
        print(
            "Nenhum usuário selecionado."
            )

def deposito():
    if not usuario_atual:
        print(
            "Nenhum usuário selecionado."
            )
        return None

    try:
        valor = float(input(
            "Digite o valor que deseja depositar: "
            ))
        conta = usuario_atual["Conta Bancária"]
        saldo_antigo = conta["Saldo"]
        conta["Saldo"] += valor
        conta["Extrato"].append(
            f"Depósito - De R$ {saldo_antigo:.2f} para R$ {conta['Saldo']:.2f}"
            )
        print(
            f"Valor depositado: R$ {valor:.2f}"
            )
        
    except ValueError:
        print(
            "Digite um valor válido."
            )

def saque():
    if not usuario_atual:
        print(
            "Nenhum usuário selecionado."
            )
        return

    conta = usuario_atual["Conta Bancária"]

    if conta["Saques Hoje"] >= 3:
        print(
            "Limite diário de 3 saques atingido."
            )
        return

    try:
        valor = float(input(
            "Digite o valor que deseja sacar: "
            ))
        if valor > conta["Saldo"]:
            print(
                "Saldo insuficiente."
                )
            return

        saldo_antigo = conta["Saldo"]
        conta["Saldo"] -= valor
        conta["Saques Hoje"] += 1
        conta["Extrato"].append(
            f"Saque - De R$ {saldo_antigo:.2f} para R$ {conta['Saldo']:.2f}"
            )
        print(
            f"Valor sacado: R$ {valor:.2f}"
            )
        
    except ValueError:
        print(
            "Digite um valor válido."
            )

def extrato_ver():
    if not usuario_atual:
        print(
            "Nenhum usuário selecionado."
            )
        return

    conta = usuario_atual["Conta Bancária"]
    print(
        "\n====== EXTRATO ======"
        )
    if conta["Extrato"]:
        for operacao in conta["Extrato"]:
            print(operacao)
    else:
        print(
            "Nenhuma operação realizada."
            )
    print(
        f"Saldo atual: R$ {conta['Saldo']:.2f}"
        )
    print(
        "======================\n"
        )

def avancar_dia():
    for usuario in usuarios:
        usuario["Conta Bancária"]["Saques Hoje"] = 0
    print(
        "Novo dia iniciado. Limite de saques resetado '(3)' para todos os usuários."
        )

def fazer_pix():
    if not usuario_atual:
        print(
            "Nenhum usuário logado."
            )
        return

    listar_usuarios()
    escolha_usuario_pix = int(input(
        "Digite o número do usuário que receberá o Pix: "
        )) - 1

    if escolha_usuario_pix < 0 or escolha_usuario_pix >= len(usuarios):
        print(
            "Usuário inválido."
            )
        return

    destinatario = usuarios[escolha_usuario_pix]
    
    if destinatario == usuario_atual:
        print(
            "Você não pode enviar Pix para você mesmo."
            )
        return

    try:
        valor = float(input(
            "Digite o valor do Pix: "
            ))
        if valor <= 0:
            print(
                "Valor inválido."
                )
            return

        conta_origem = usuario_atual['Conta Bancária']
        conta_destino = destinatario['Conta Bancária']

        if valor > conta_origem['Saldo']:
            print(
                "Saldo insuficiente."
                )
            return

        conta_origem['Saldo'] -= valor
        conta_destino['Saldo'] += valor

        conta_origem['Extrato'].append(
            f"Pix enviado para {destinatario['Nome']} - R$ {valor:.2f}"
        )
        conta_destino['Extrato'].append(
            f"Pix recebido de {usuario_atual['Nome']} - R$ {valor:.2f}"
        )

        print(
            f"Pix de R$ {valor:.2f} enviado para {destinatario['Nome']} com sucesso."
            )

    except ValueError:
        print(
            "Valor inválido."
            )

while True:
    escolha = int(input(
        """
======== MENU - BANCO @#$ ========

1. Sacar
2. Depositar
3. Ver Extrato 
4. Avançar dia
5. Criar Conta
6. Listar Usuários
7. Trocar Usuário 
8. Ver informações do usuário atual
9. Fazer Pix para outro usuário cadastrado no banco
0. Sair

Escolha: """ ))

    if escolha == 1:
        saque()

    elif escolha == 2:
        deposito()

    elif escolha == 3:
        extrato_ver()

    elif escolha == 4:
        avancar_dia()

    elif escolha == 5:
        novo = criar_usuario()
        if novo:
            usuarios.append(novo)

    elif escolha == 6:
        listar_usuarios()

    elif escolha == 7:
        trocar_usuario()

    elif escolha == 8:
        ver_usuario_atual()

    elif escolha == 0:
        break

    elif escolha == 9: 
        fazer_pix()

    else:
        print(
            "Opção inválida."
            )

import hashlib
import time
import random
import requests
import sys
import os

# Nome do arquivo de status de mineração
STATUS_FILE_NAME = "mining_status.3txt"  # Modifique este nome conforme necessário

# Exibição da arte de texto no início
def show_art():
    art = """
######    ####    ######   ##   ##   ####    ##   ##  #######  ######
  ##  ##    ##     # ## #   ### ###    ##     ###  ##   ##   #   ##  ##
  ##  ##    ##       ##     #######    ##     #### ##   ## #     ##  ##
  #####     ##       ##     #######    ##     ## ####   ####     #####
  ##  ##    ##       ##     ## # ##    ##     ##  ###   ## #     ## ##
  ##  ##    ##       ##     ##   ##    ##     ##   ##   ##   #   ##  ##
 ######    ####     ####    ##   ##   ####    ##   ##  #######  #### ##
    """
    print(art)

# Função para verificar se a conexão com a internet está ativa
def check_internet_connection():
    try:
        # Tentativa de acessar o Google
        requests.get("http://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False

# Função para calcular o valor de BTC baseado no valor em reais
def calculate_btc_from_brl(amount_brl, btc_per_brl):
    return amount_brl * btc_per_brl

# Função para simular a mineração (Proof of Work)
def mine_block(difficulty, mining_time, reward_per_block):
    # "mining_time" é o tempo máximo para mineração (em segundos)
    print(f"Mineração iniciada com dificuldade {difficulty}... Tempo de mineração: {mining_time} segundos.")

    target = '0' * difficulty  # O número de zeros à esquerda do hash
    start_time = time.time()  # Início do tempo de mineração
    end_time = start_time + mining_time  # Define o tempo final
    btc_mined = 0  # Total de BTC minerado
    nonce = 0  # Contador de tentativas
    hashes_mined = 0  # Contador de hashes feitos

    # Enquanto o tempo de mineração não expirar
    while time.time() < end_time:
        # Criar um bloco com o nonce atual
        block_data = f"bloco_{nonce}_{random.randint(0, 100000)}"
        
        # Gerar o hash do bloco usando SHA256
        hash_result = hashlib.sha256(block_data.encode('utf-8')).hexdigest()
        hashes_mined += 1  # Aumenta o contador de hashes minerados

        # Verificar se o hash começa com a quantidade necessária de zeros
        if hash_result.startswith(target):
            print(f"\nBloco minerado! Hash encontrado: {hash_result}")
            btc_mined += reward_per_block  # Aumenta a recompensa pela mineração de um bloco
            print(f"BTC Minerado: {btc_mined:.8f} BTC")
        
        # Mostrar movimento no terminal enquanto minera
        sys.stdout.write("\rMinerando..." + "." * (int(time.time() * 5) % 4))  # Simula pontos movendo
        sys.stdout.flush()
        
        nonce += 1

    # Exibir as informações finais
    print("\n\nFim da mineração!")
    print(f"Total de hashes minerados: {hashes_mined}")
    return btc_mined

# Função para verificar se a mineração já foi realizada (arquivo de controle)
def check_if_mining_completed():
    if os.path.exists(STATUS_FILE_NAME):  # Usa o nome de arquivo configurado
        with open(STATUS_FILE_NAME, "r") as file:
            status = file.read().strip()
            if status == "esgotado":
                return True
    return False

# Função para marcar a mineração como esgotada
def mark_mining_as_completed():
    with open(STATUS_FILE_NAME, "w") as file:  # Usa o nome de arquivo configurado
        file.write("esgotado")

# Função principal para iniciar o processo de mineração
def main():
    # Verificar se a mineração já foi completada
    if check_if_mining_completed():
        print("Erro: Mineração esgotada. Não é possível minerar novamente.")
        return  # Encerra o programa se a mineração foi esgotada

    # Verificar conexão com a internet
    print("Verificando conexão com a internet...")
    if not check_internet_connection():
        print("Erro: Sem conexão com a internet. Certifique-se de que está conectado.")
        return  # Encerra o programa caso não haja internet

    # Exibe a arte de texto
    show_art()

    # Defina o valor em reais que você quer minerar
    amount_brl = 11  # Alterar este valor para o quanto você quer minerar (em reais)

    # Defina a cotação de 1 real para BTC
    btc_per_brl = 0.00000212  # Valor de 1 real em BTC

    # Calcular a quantidade de BTC que você quer minerar
    target_btc = calculate_btc_from_brl(amount_brl, btc_per_brl)

    # Defina a dificuldade de mineração, tempo de mineração e recompensa por bloco
    difficulty = 2  # Dificuldade (quantos zeros no começo do hash)
    mining_time = 660  # Tempo fixo de mineração em segundos (ajustável)
    reward_per_block = 0.0000020732087525647616  # Recompensa por bloco minerado (BTC)

    print("Iniciando o minerador de Bitcoin...\n")
    btc_mined = mine_block(difficulty, mining_time, reward_per_block)

    # Marcar a mineração como completada (esgotada)
    mark_mining_as_completed()

    # Exibir a quantidade de BTC minerado
    print(f"\nVocê minerou {btc_mined:.8f} BTC!")

if _name_ == "_main_":
    main()

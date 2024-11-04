import time
import random
import sys
import os
import socket
from threading import Thread

class Miner:
    def __init__(self, name):
        self.name = name
        self.balance_cents = self.load_balance()  # Carrega o saldo inicial
        self.btc_conversion_rate = 0.000001  # 1 centavo = 0,000001 BTC
        self.max_hourly_earning = 300  # limite de 300 centavos por hora
        self.earned_this_hour = 0  # ganho atual na hora
        self.start_time = time.time()  # Tempo de início da mineração
        self.running = True  # Controle para o loop de contagem

    def load_balance(self):
        if os.path.exists('saldo.txt'):
            with open('saldo.txt', 'r') as file:
                lines = file.readlines()
                if lines:
                    saldo_line = lines[0].strip().split(' ')[1].replace('R$', '')
                    return int(float(saldo_line) * 100)  # Converte para centavos
        return 0  # Saldo inicial se o arquivo não existir

    def update_balance(self, amount):
        self.balance_cents += amount
        self.earned_this_hour += amount
        self.save_balance()

    def save_balance(self):
        with open('saldo.txt', 'w') as file:
            file.write(f'Saldo: R${self.balance_cents / 100:.2f}\n')  # Armazena em reais
            file.write(f'Saldo em BTC: {self.balance_cents * self.btc_conversion_rate:.6f} BTC\n')  # BTC com 6 casas decimais
        print(f'\033[92mSaldo atualizado: R${self.balance_cents / 100:.2f} | {self.balance_cents * self.btc_conversion_rate:.6f} BTC\033[0m')

    def loading_animation(self, duration):
        spinner = ['|', '/', '-', '\\']
        end_time = time.time() + duration
        while time.time() < end_time and self.running:
            for symbol in spinner:
                sys.stdout.write(f'\r\033[93m{symbol} Processando...\033[0m')
                sys.stdout.flush()
                time.sleep(0.05)  # Tempo de espera bem reduzido

    def check_internet(self):
        try:
            socket.create_connection(("www.google.com", 80), timeout=5)
            return True
        except OSError:
            return False

    def display_uptime(self):
        uptime = time.time() - self.start_time
        hours, remainder = divmod(int(uptime), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def heavy_computation(self):
        """Função para simular um leve processamento."""
        # Simulação de um cálculo leve
        random_value = random.random() * random.randint(1, 10)
        return random_value  # Retorna um valor simples

    def earn_money(self):
        while self.running:
            if not self.check_internet():
                print("\033[91mConexão à internet perdida. A ferramenta será encerrada.\033[0m")
                self.running = False
                break  # Encerra o programa se a internet cair

            print(f"\r\033[96mTempo ligado: {self.display_uptime()} | Saldo: R${self.balance_cents / 100:.2f}\033[0m", end='')

            # Ganha entre 5 a 10 centavos a cada 2 a 3 minutos
            wait_time = random.choice([120, 180])  # 2 ou 3 minutos
            self.loading_animation(wait_time)  # Espera o tempo escolhido

            gain = random.randint(5, 10)  # Ganha entre 5 e 10 centavos
            if self.earned_this_hour + gain <= self.max_hourly_earning:
                self.update_balance(gain)  # Atualiza saldo se não ultrapassar o limite

            self.heavy_computation()  # Simula processamento leve após cada fase

            # Reinicia o contador de ganhos a cada hora
            if time.localtime().tm_min == 0 and time.localtime().tm_sec == 0:
                self.earned_this_hour = 0

    def start_mining(self):
        if not self.check_internet():
            print("\033[91mErro: Conexão à internet não detectada. Por favor, conecte-se à internet e tente novamente.\033[0m")
            return

        # Tela de carregamento
        print("\033[94mIniciando a mineração...\033[0m")
        time.sleep(1)  # Atraso para a tela de carregamento

        # Adicionando a arte de texto
        print("\033[94m"
              "███╗   ███╗██╗███╗   ██╗███████╗██████╗ \n"
              "████╗ ████║██║████╗  ██║██╔════╝██╔══██╗\n"
              "██╔████╔██║██║██╔██╗ ██║█████╗  ██████╔╝\n"
              "██║╚██╔╝██║██║██║╚██╗██║██╔══╝  ██╔══██╗\n"
              "██║ ╚═╝ ██║██║██║ ╚████║███████╗██║  ██║\n"
              "╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝\n"
              "                                        \033[0m")

        # Adicionando avisos e mensagens
        print("\033[91mAvisos e Mensagens:\033[0m")
        print("\033[91mAtenção: Verifique se sua máquina atende aos requisitos mínimos de hardware antes de iniciar a mineração.\033[0m")
        print("\033[91mLembrete: A mineração pode consumir muita energia. Esteja ciente dos custos operacionais e monitore o consumo.\033[0m")
        print("\033[91mAviso: As recompensas da mineração podem variar. Mantenha-se atualizado sobre as mudanças no protocolo Bitcoin.\033[0m")
        print("\033[91mNota: Esta ferramenta é destinada a usuários com experiência em criptomoedas. Utilize com responsabilidade.\033[0m")
        print("\033[91mDica: Considere unir-se a um pool de mineração para aumentar suas chances de sucesso e reduzir a variabilidade dos ganhos.\033[0m")
        print("\033[91mImportante: Qualquer tentativa de aplicar fraudes ou enganar fornecedores resultará no bloqueio imediato da sua conta, e o saldo disponível para saque não será liberado.\033[0m")

        print(f'\033[94m{self.name} começou a minerar... Saldo inicial: R${self.balance_cents / 100:.2f} | {self.balance_cents * self.btc_conversion_rate:.6f} BTC\033[0m')

        # Inicia o processo de ganhar dinheiro em uma thread separada
        mining_thread = Thread(target=self.earn_money)
        mining_thread.start()

        # Atualiza o tempo de atividade na thread principal
        while self.running:
            time.sleep(1)  # Atualiza a cada segundo

def main_menu():
    miner = Miner("Miner 1")
    
    while True:
        print("\n\033[96m=== Ferramenta de Mineração de Bitcoin ===\033[0m")
        print("\033[92m1. Iniciar mineração de Bitcoin\033[0m")
        print("\033[92m2. Consultar saldo\033[0m")
        print("\033[93m0. Sair\033[0m")
        
        choice = input("\n\033[94mDigite sua opção: \033[0m")

        if choice == '1':
            miner.start_mining()
        elif choice == '2':
            miner.save_balance()  # Exibe o saldo atual
        elif choice == '0':
            print("\033[91mSaindo da ferramenta...\033[0m")
            miner.running = False  # Para o loop de mineração
            break
        else:
            print("\033[91mOpção inválida. Tente novamente.\033[0m")

if __name__ == "__main__":
    main_menu()

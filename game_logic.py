import random
import subprocess
import logging

# Configuração do log
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

class Game:
    def __init__(self):
        self.board_size = 10  # Tabuleiro 10x10
        self.player_board = [[" " for _ in range(10)] for _ in range(10)]
        self.quantum_board = [[" " for _ in range(10)] for _ in range(10)]
        self.player_ships = []
        self.quantum_ships = []
        self.last_hit = None
        self.quantum_moves = []  # Lista de jogadas quânticas

    def quantum_attack(self):
        """ O computador quântico ataca usando os pontos convertidos do Quantum Job """
        logging.debug("Computador quântico atacando...")

        if not self.quantum_moves:
            logging.warning("Computador ficou sem jogadas!")
            return {"status": "miss", "message": "Computador ficou sem jogadas!"}

        move = self.quantum_moves.pop(0)
        x, y = move

        # 🔹 Log para verificar as coordenadas
        logging.debug(f"Ataque do Computador em ({x}, {y})")

        # 🔹 Verifica se está dentro dos limites (0 a 9)
        if not (0 <= x < 10 and 0 <= y < 10):
            logging.error(f"Coordenada inválida gerada pelo Quantum Job: ({x}, {y})")
            return {"status": "error", "message": f"Coordenada inválida ({x}, {y})"}

        # 🔹 Determina se o ataque acertou ou errou
        if self.player_board[y][x] == "S":
            self.player_board[y][x] = "X"
            logging.debug(f"Computador acertou um barco em ({x}, {y})!")
            return {"status": "hit", "x": x, "y": y, "message": "Computador acertou um barco!"}

        logging.debug(f"Computador errou em ({x}, {y}).")
        return {"status": "miss", "x": x, "y": y, "message": "Computador errou!"}

    def player_attack(self, coord):
        """ Processa o ataque do jogador no tabuleiro do computador quântico """
        logging.debug(f"🎯 Jogador atacando coordenada: {coord}")

        try:
            row = ord(coord[0].upper()) - ord("A")  # Converte letra para índice numérico
            col = int(coord[1:]) - 1  # Converte número da string para inteiro e ajusta para índice (0-9)
        except (IndexError, ValueError):
            logging.warning(f"⚠ Coordenada inválida: {coord}")
            return {"status": "error", "message": "Coordenada inválida"}

        # Verifica se está dentro dos limites
        if not (0 <= row < 10 and 0 <= col < 10):
            logging.warning(f"⚠ Coordenada fora do tabuleiro: {coord}")
            return {"status": "error", "message": "Ataque fora do tabuleiro"}

        if self.quantum_board[row][col] == "S":
            self.quantum_board[row][col] = "X"
            logging.debug(f"💥 Jogador acertou um navio em ({row}, {col})!")
            return {"status": "hit", "x": col, "y": row, "message": "Acertou um navio!"}
        
        self.quantum_board[row][col] = "O"
        logging.debug(f"❌ Jogador errou em ({row}, {col}).")
        return {"status": "miss", "x": col, "y": row, "message": "Errou!"}


    def setup_boards(self):
        """ Posiciona barcos aleatoriamente nos dois tabuleiros """
        logging.debug("Configurando tabuleiros...")

        self.player_ships = self.place_ships() # Gera posicao aleatoria para barcos
        self.quantum_ships = self.place_ships()  # 🔹 Certifique-se de que está atribuindo corretamente

        logging.debug(f"🚢 Coordenadas dos navios do jogador: {self.player_ships}")
        logging.debug(f"🚢 Coordenadas dos navios do computador quântico: {self.quantum_ships}")


        self.quantum_moves = self.get_quantum_moves()

        for (x, y) in self.player_ships:
            self.player_board[y][x] = "S"  # 🔹 Posiciona os navios do jogador

        for (x, y) in self.quantum_ships:  
            self.quantum_board[y][x] = "S"  # 🔹 Agora garante que os navios do CQ são colocados!
        
        logging.debug(f"🛠 Tabuleiro do jogador:\n{self.player_board}")
        logging.debug(f"🛠 Tabuleiro do computador quântico:\n{self.quantum_board}")

    def convert_quantum_move(self, binary_str):
        """ Converte string binária em coordenadas (x, y) dentro do tabuleiro """
        if len(binary_str) < self.board_size:
            logging.error(f"⚠ Erro: String binária muito curta! ({binary_str})")
            return None

        num_bits = len(binary_str) // 2  # Divide para X e Y

        x = int(binary_str[:num_bits], 2) % self.board_size  # Converte para decimal e mantém dentro do tabuleiro
        y = int(binary_str[num_bits:], 2) % self.board_size

        logging.debug(f"📌 Binário: {binary_str} → Coordenadas ({x}, {y})")
        return (x, y)

    def place_ships(self):
        """ Gera a posição aleatória dos 4 barcos """
        logging.debug("Gerando barcos aleatórios...")
        ship_sizes = [4, 3, 2, 1]  # Tamanhos dos barcos
        ships = []

        for size in ship_sizes:
            while True:
                x, y = random.randint(0, 9), random.randint(0, 9)
                direction = random.choice(["H", "V"])

                if self.valid_ship_placement(x, y, size, direction, ships):
                    for i in range(size):
                        ships.append((x + i, y) if direction == "H" else (x, y + i))
                    break

        logging.debug(f"Barcos gerados: {ships}")
        return ships

    def valid_ship_placement(self, x, y, size, direction, ships):
        """ Verifica se o barco pode ser colocado sem sair do tabuleiro """
        if direction == "H" and x + size > 10:
            return False
        if direction == "V" and y + size > 10:
            return False
        return all((x + i, y) not in ships if direction == "H" else (x, y + i) not in ships for i in range(size))

    def get_quantum_moves(self):
        """ Obtém os pontos aleatórios do Quantum Job e converte para coordenadas do tabuleiro """
        logging.debug("🔹 Executando quantum_job.py para gerar jogadas quânticas...")

        result = subprocess.run(['python3', 'quantum_job.py'], capture_output=True, text=True)
        output = result.stdout.strip()

        if not output:
            logging.error("⚠ Erro: quantum_job.py não retornou nenhuma saída!")
            return []

        logging.debug(f"📌 Saída bruta do Quantum Job:\n{output}")

        moves = []
        for line in output.split("\n"):
            coord = self.convert_quantum_move(line)  # 🔹 Converte usando a função da classe Game
            if coord is not None:
                moves.append(coord)

        if not moves:
            logging.warning("⚠ Nenhuma jogada válida foi gerada! Criando jogadas de backup.")
            moves = [(random.randint(0, 9), random.randint(0, 9)) for _ in range(10)]

        logging.debug(f"🎯 Jogadas quânticas finais: {moves}")
        return moves

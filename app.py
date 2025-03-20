from flask import Flask, jsonify, render_template, request
import subprocess
import importlib
import game_logic
import logging

importlib.reload(game_logic)
from game_logic import Game

# 🔹 Configurando logs
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")


app = Flask(__name__)

# Criando o jogo
game = Game()

# Rota para exibir o HTML
@app.route('/')
def index():
    return render_template('index.html')

# Rota para inicializar o tabuleiro
@app.route('/initialize_game', methods=['GET'])
def initialize_game():
    game.setup_boards()
    return jsonify({"message": "Tabuleiro gerado!", "player_board": game.player_board})

# Rota para buscar os pontos aleatórios do quantum job
@app.route('/get_quantum_moves', methods=['GET'])
def get_quantum_moves():
    quantum_moves = game.get_quantum_moves()
    return jsonify(quantum_moves)

@app.route('/player_attack', methods=['POST'])
def player_attack():
    data = request.get_json()
    coord = data.get("coord")

    logging.debug(f"Recebendo ataque do jogador: {coord}")

    player_result = game.player_attack(coord)
    quantum_result = game.quantum_attack()

    breakpoint()
    
    return jsonify({
        "player": player_result,
        "quantum": quantum_result
    })



# Rota para o computador quântico fazer um ataque
@app.route('/quantum_attack', methods=['GET'])
def quantum_attack(self):
    """ O computador quântico ataca usando os pontos aleatórios gerados """
    logging.debug("🤖 Computador quântico atacando...")

    if not self.quantum_moves:
        logging.warning("⚠ Computador ficou sem jogadas!")
        return {"status": "miss", "message": "Computador ficou sem jogadas!"}

    move = self.quantum_moves.pop(0)
    x, y = move

    logging.debug(f"💥 Ataque do Computador em ({x}, {y})")

    if self.player_board[y][x] == "S":
        self.player_board[y][x] = "X"
        logging.debug(f"💥 Computador acertou um navio do jogador em ({x}, {y})!")
        return {"status": "hit", "x": x, "y": y, "message": "Computador acertou um navio!"}

    self.player_board[y][x] = "O"  # 🔹 Marca um erro do computador
    logging.debug(f"❌ Computador errou em ({x}, {y}).")
    return {"status": "miss", "x": x, "y": y, "message": "Computador errou!"}  # ✅ Mensagem corrigida


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


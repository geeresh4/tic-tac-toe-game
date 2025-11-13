from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

# Store game states in memory (in production, use Redis or database)
games = {}

class TicTacToe:
    def __init__(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_mode = None
        self.game_over = False
        self.winner = None
        
    def reset(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        
    def make_move(self, row, col):
        if self.board[row][col] == '' and not self.game_over:
            self.board[row][col] = self.current_player
            if self.check_winner():
                self.game_over = True
                self.winner = self.current_player
            elif self.is_board_full():
                self.game_over = True
                self.winner = 'Tie'
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False
        
    def check_winner(self):
        # Check rows
        for row in self.board:
            if row[0] == row[1] == row[2] != '':
                return True
                
        # Check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != '':
                return True
                
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            return True
            
        return False
        
    def is_board_full(self):
        for row in self.board:
            if '' in row:
                return False
        return True
        
    def get_bot_move(self):
        # Try to win
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == '':
                    self.board[row][col] = 'O'
                    if self.check_winner():
                        self.board[row][col] = ''
                        return (row, col)
                    self.board[row][col] = ''
                    
        # Block player from winning
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == '':
                    self.board[row][col] = 'X'
                    if self.check_winner():
                        self.board[row][col] = ''
                        return (row, col)
                    self.board[row][col] = ''
                    
        # Take center if available
        if self.board[1][1] == '':
            return (1, 1)
            
        # Take corner if available
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        random.shuffle(corners)
        for row, col in corners:
            if self.board[row][col] == '':
                return (row, col)
                
        # Take any available space
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == '':
                    return (row, col)
                    
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/new-game', methods=['POST'])
def new_game():
    import uuid
    game_id = str(uuid.uuid4())
    games[game_id] = TicTacToe()
    return jsonify({'game_id': game_id})

@app.route('/api/make-move', methods=['POST'])
def make_move():
    data = request.json
    game_id = data.get('game_id')
    row = data.get('row')
    col = data.get('col')
    
    if game_id not in games:
        return jsonify({'error': 'Game not found'}), 404
        
    game = games[game_id]
    
    if game.make_move(row, col):
        result = {
            'board': game.board,
            'current_player': game.current_player,
            'game_over': game.game_over,
            'winner': game.winner
        }
        
        # Bot plays automatically if in bot mode
        if game.game_mode == 'bot' and not game.game_over and game.current_player == 'O':
            bot_move = game.get_bot_move()
            if bot_move:
                game.make_move(bot_move[0], bot_move[1])
                result['bot_move'] = {'row': bot_move[0], 'col': bot_move[1]}
        
        result['board'] = game.board
        result['current_player'] = game.current_player
        result['game_over'] = game.game_over
        result['winner'] = game.winner
        
        return jsonify(result)
    else:
        return jsonify({'error': 'Invalid move'}), 400

@app.route('/api/set-mode', methods=['POST'])
def set_mode():
    data = request.json
    game_id = data.get('game_id')
    mode = data.get('mode')
    
    if game_id not in games:
        return jsonify({'error': 'Game not found'}), 404
        
    games[game_id].game_mode = mode
    return jsonify({'status': 'success'})

@app.route('/api/reset', methods=['POST'])
def reset_game():
    data = request.json
    game_id = data.get('game_id')
    
    if game_id not in games:
        return jsonify({'error': 'Game not found'}), 404
        
    games[game_id].reset()
    return jsonify({
        'board': games[game_id].board,
        'current_player': games[game_id].current_player,
        'game_over': False,
        'winner': None
    })

@app.route('/api/game-state', methods=['POST'])
def get_game_state():
    data = request.json
    game_id = data.get('game_id')
    
    if game_id not in games:
        return jsonify({'error': 'Game not found'}), 404
        
    game = games[game_id]
    return jsonify({
        'board': game.board,
        'current_player': game.current_player,
        'game_over': game.game_over,
        'winner': game.winner,
        'game_mode': game.game_mode
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


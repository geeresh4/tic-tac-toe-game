import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 700
BOARD_SIZE = 3
CELL_SIZE = WIDTH // BOARD_SIZE
LINE_WIDTH = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
BLUE = (50, 150, 255)
GREEN = (50, 255, 100)
YELLOW = (255, 255, 100)
PURPLE = (200, 100, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)

# Fonts
FONT_LARGE = pygame.font.Font(None, 72)
FONT_MEDIUM = pygame.font.Font(None, 48)
FONT_SMALL = pygame.font.Font(None, 36)

class TicTacToe:
    def __init__(self):
        self.board = [['' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = 'X'
        self.game_mode = None  # 'bot' or 'friend'
        self.game_over = False
        self.winner = None
        self.celebration_particles = []
        self.celebration_timer = 0
        
    def reset(self):
        self.board = [['' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        self.celebration_particles = []
        self.celebration_timer = 0
        
    def make_move(self, row, col):
        if self.board[row][col] == '' and not self.game_over:
            self.board[row][col] = self.current_player
            if self.check_winner():
                self.game_over = True
                self.winner = self.current_player
                self.start_celebration()
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
        for col in range(BOARD_SIZE):
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
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board[row][col] == '':
                    self.board[row][col] = 'O'
                    if self.check_winner():
                        self.board[row][col] = ''
                        return (row, col)
                    self.board[row][col] = ''
                    
        # Block player from winning
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
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
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board[row][col] == '':
                    return (row, col)
                    
        return None
        
    def start_celebration(self):
        self.celebration_particles = []
        for _ in range(50):
            particle = {
                'x': WIDTH // 2,
                'y': HEIGHT // 2,
                'vx': random.uniform(-5, 5),
                'vy': random.uniform(-5, 5),
                'color': random.choice([RED, BLUE, GREEN, YELLOW, PURPLE]),
                'size': random.randint(3, 8)
            }
            self.celebration_particles.append(particle)
        self.celebration_timer = 180  # 3 seconds at 60 FPS

class GameUI:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Tic-Tac-Toe Game")
        self.clock = pygame.time.Clock()
        self.game = TicTacToe()
        self.state = 'menu'  # 'menu', 'mode_selection', 'playing', 'game_over'
        self.running = True
        
    def draw_menu(self):
        self.screen.fill(BLACK)
        title = FONT_LARGE.render("TIC-TAC-TOE", True, WHITE)
        title_rect = title.get_rect(center=(WIDTH//2, HEIGHT//2 - 100))
        self.screen.blit(title, title_rect)
        
        subtitle = FONT_MEDIUM.render("Press ENTER to Start", True, YELLOW)
        subtitle_rect = subtitle.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Decorative X and O
        for i in range(3):
            x_text = FONT_MEDIUM.render("X", True, RED)
            self.screen.blit(x_text, (50 + i*200, 50))
            o_text = FONT_MEDIUM.render("O", True, BLUE)
            self.screen.blit(o_text, (150 + i*200, 550))
            
    def draw_mode_selection(self):
        self.screen.fill(BLACK)
        title = FONT_MEDIUM.render("Select Game Mode", True, WHITE)
        title_rect = title.get_rect(center=(WIDTH//2, 150))
        self.screen.blit(title, title_rect)
        
        # Friend mode button
        friend_color = GREEN if self.game.game_mode == 'friend' else LIGHT_GRAY
        pygame.draw.rect(self.screen, friend_color, (150, 300, 300, 80), 0, 10)
        pygame.draw.rect(self.screen, WHITE, (150, 300, 300, 80), 3, 10)
        friend_text = FONT_MEDIUM.render("1. Play with Friend", True, BLACK)
        friend_rect = friend_text.get_rect(center=(WIDTH//2, 340))
        self.screen.blit(friend_text, friend_rect)
        
        # Bot mode button
        bot_color = GREEN if self.game.game_mode == 'bot' else LIGHT_GRAY
        pygame.draw.rect(self.screen, bot_color, (150, 420, 300, 80), 0, 10)
        pygame.draw.rect(self.screen, WHITE, (150, 420, 300, 80), 3, 10)
        bot_text = FONT_MEDIUM.render("2. Play with Bot", True, BLACK)
        bot_rect = bot_text.get_rect(center=(WIDTH//2, 460))
        self.screen.blit(bot_text, bot_rect)
        
        instruction = FONT_SMALL.render("Press 1 or 2 to select", True, YELLOW)
        inst_rect = instruction.get_rect(center=(WIDTH//2, 550))
        self.screen.blit(instruction, inst_rect)
        
    def draw_board(self):
        self.screen.fill(BLACK)
        
        # Draw grid lines
        for i in range(1, BOARD_SIZE):
            # Vertical lines
            pygame.draw.line(self.screen, WHITE, 
                           (i * CELL_SIZE, 0), 
                           (i * CELL_SIZE, WIDTH), 
                           LINE_WIDTH)
            # Horizontal lines
            pygame.draw.line(self.screen, WHITE, 
                           (0, i * CELL_SIZE), 
                           (WIDTH, i * CELL_SIZE), 
                           LINE_WIDTH)
                           
        # Draw X's and O's
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x = col * CELL_SIZE + CELL_SIZE // 2
                y = row * CELL_SIZE + CELL_SIZE // 2
                
                if self.game.board[row][col] == 'X':
                    # Draw X
                    offset = CELL_SIZE // 3
                    pygame.draw.line(self.screen, RED, 
                                   (x - offset, y - offset), 
                                   (x + offset, y + offset), 
                                   LINE_WIDTH)
                    pygame.draw.line(self.screen, RED, 
                                   (x - offset, y + offset), 
                                   (x + offset, y - offset), 
                                   LINE_WIDTH)
                elif self.game.board[row][col] == 'O':
                    # Draw O
                    radius = CELL_SIZE // 3
                    pygame.draw.circle(self.screen, BLUE, (x, y), radius, LINE_WIDTH)
                    
        # Draw current player indicator
        status_y = WIDTH + 20
        if not self.game.game_over:
            player_text = f"Current Player: {self.game.current_player}"
            player_color = RED if self.game.current_player == 'X' else BLUE
            status = FONT_MEDIUM.render(player_text, True, player_color)
            status_rect = status.get_rect(center=(WIDTH//2, status_y))
            self.screen.blit(status, status_rect)
            
            mode_text = f"Mode: {'Bot' if self.game.game_mode == 'bot' else 'Friend'}"
            mode_status = FONT_SMALL.render(mode_text, True, GRAY)
            mode_rect = mode_status.get_rect(center=(WIDTH//2, status_y + 40))
            self.screen.blit(mode_status, mode_rect)
        else:
            # Game over message
            if self.game.winner == 'Tie':
                result_text = "IT'S A TIE!"
                result_color = YELLOW
            else:
                result_text = f"PLAYER {self.game.winner} WINS!"
                result_color = GREEN if self.game.winner == 'X' else PURPLE
                
            result = FONT_LARGE.render(result_text, True, result_color)
            result_rect = result.get_rect(center=(WIDTH//2, status_y))
            self.screen.blit(result, result_rect)
            
            restart_text = FONT_SMALL.render("Press R to Restart or ESC for Menu", True, WHITE)
            restart_rect = restart_text.get_rect(center=(WIDTH//2, status_y + 50))
            self.screen.blit(restart_text, restart_rect)
            
        # Draw celebration particles
        if self.game.celebration_timer > 0:
            self.game.celebration_timer -= 1
            for particle in self.game.celebration_particles[:]:
                particle['x'] += particle['vx']
                particle['y'] += particle['vy']
                particle['vy'] += 0.2  # Gravity
                
                if 0 <= particle['x'] < WIDTH and 0 <= particle['y'] < HEIGHT:
                    pygame.draw.circle(self.screen, particle['color'], 
                                     (int(particle['x']), int(particle['y'])), 
                                     particle['size'])
                else:
                    self.game.celebration_particles.remove(particle)
                    
    def get_cell_from_pos(self, pos):
        x, y = pos
        if 0 <= x < WIDTH and 0 <= y < WIDTH:
            col = x // CELL_SIZE
            row = y // CELL_SIZE
            return (row, col)
        return None
        
    def handle_click(self, pos):
        if self.state == 'playing' and not self.game.game_over:
            cell = self.get_cell_from_pos(pos)
            if cell:
                row, col = cell
                if self.game.make_move(row, col):
                    # If playing with bot and game not over, bot plays automatically
                    if self.game.game_mode == 'bot' and not self.game.game_over:
                        pygame.time.wait(500)  # Small delay for better UX
                        bot_move = self.game.get_bot_move()
                        if bot_move:
                            self.game.make_move(bot_move[0], bot_move[1])
                            
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
                if event.type == pygame.KEYDOWN:
                    if self.state == 'menu':
                        if event.key == pygame.K_RETURN:
                            self.state = 'mode_selection'
                            
                    elif self.state == 'mode_selection':
                        if event.key == pygame.K_1:
                            self.game.game_mode = 'friend'
                            self.game.reset()
                            self.state = 'playing'
                        elif event.key == pygame.K_2:
                            self.game.game_mode = 'bot'
                            self.game.reset()
                            self.state = 'playing'
                            
                    elif self.state == 'playing':
                        if event.key == pygame.K_r and self.game.game_over:
                            self.game.reset()
                        elif event.key == pygame.K_ESCAPE:
                            self.state = 'menu'
                            
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        if self.state == 'playing':
                            self.handle_click(event.pos)
                        elif self.state == 'mode_selection':
                            # Handle button clicks
                            x, y = event.pos
                            if 150 <= x <= 450:
                                if 300 <= y <= 380:
                                    self.game.game_mode = 'friend'
                                    self.game.reset()
                                    self.state = 'playing'
                                elif 420 <= y <= 500:
                                    self.game.game_mode = 'bot'
                                    self.game.reset()
                                    self.state = 'playing'
                                    
            # Draw current state
            if self.state == 'menu':
                self.draw_menu()
            elif self.state == 'mode_selection':
                self.draw_mode_selection()
            elif self.state == 'playing':
                self.draw_board()
                
            pygame.display.flip()
            self.clock.tick(60)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = GameUI()
    game.run()


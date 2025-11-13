# Tic-Tac-Toe Game

A fully functional 2-player Tic-Tac-Toe game with user vs bot/friend modes, automatic bot moves, and celebration animations.

## Features

- **Two Game Modes**:
  - Play with Friend (local multiplayer)
  - Play with Bot (AI opponent)
  
- **Automatic Bot Moves**: The bot automatically plays after the user's move
- **Winner Detection**: Automatically detects winners or ties
- **Celebration Animation**: Full particle celebration when a player wins
- **User-Friendly Interface**: Clean GUI with pygame

## Installation

1. Install Python 3.7 or higher
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## How to Play

1. Run the game:
   ```bash
   python game.py
   ```

2. **Start Menu**: Press `ENTER` to start the game

3. **Select Mode**: 
   - Press `1` or click "Play with Friend" for local multiplayer
   - Press `2` or click "Play with Bot" to play against AI

4. **Gameplay**:
   - Click on any empty cell to place your mark (X or O)
   - Player X always starts first
   - In Bot mode, the bot automatically plays after your move
   - First player to get 3 in a row (horizontal, vertical, or diagonal) wins!

5. **Game Over**:
   - Winner is declared with a celebration animation
   - Press `R` to restart the game
   - Press `ESC` to return to the main menu

## Game Controls

- `ENTER`: Start game from main menu
- `1` or `2`: Select game mode
- `Mouse Click`: Make a move on the board
- `R`: Restart game (when game is over)
- `ESC`: Return to main menu

## Technical Details

- Built with Python and Pygame
- Uses smart AI algorithm for bot moves (tries to win, blocks player, strategic positioning)
- Particle system for winner celebrations
- Clean state management (menu → mode selection → playing → game over)

Enjoy playing!


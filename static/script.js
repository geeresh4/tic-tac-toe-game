let gameId = null;
let currentMode = null;

// Initialize game
async function initGame() {
    const response = await fetch('/api/new-game', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    });
    const data = await response.json();
    gameId = data.game_id;
}

// Start game - show mode selection
function startGame() {
    document.getElementById('menu-screen').classList.remove('active');
    document.getElementById('mode-screen').classList.add('active');
    initGame();
}

// Select game mode
async function selectMode(mode) {
    currentMode = mode;
    
    if (!gameId) {
        await initGame();
    }
    
    // Set mode on server
    await fetch('/api/set-mode', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            game_id: gameId,
            mode: mode
        })
    });
    
    document.getElementById('mode-screen').classList.remove('active');
    document.getElementById('game-screen').classList.add('active');
    document.getElementById('game-mode-text').textContent = `Mode: ${mode === 'bot' ? 'Bot' : 'Friend'}`;
    
    updateBoard();
}

// Make a move
async function makeMove(row, col) {
    if (!gameId) return;
    
    const cell = document.querySelector(`[data-row="${row}"][data-col="${col}"]`);
    if (cell.classList.contains('filled')) return;
    
    const response = await fetch('/api/make-move', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            game_id: gameId,
            row: row,
            col: col
        })
    });
    
    const data = await response.json();
    
    if (data.error) {
        console.error(data.error);
        return;
    }
    
    updateBoardFromData(data);
    
    // If bot made a move, update again
    if (data.bot_move) {
        setTimeout(() => {
            updateBoard();
        }, 500);
    }
}

// Update board from server data
async function updateBoardFromData(data) {
    const board = data.board;
    const currentPlayer = data.current_player;
    const gameOver = data.game_over;
    const winner = data.winner;
    
    // Update cells
    for (let row = 0; row < 3; row++) {
        for (let col = 0; col < 3; col++) {
            const cell = document.querySelector(`[data-row="${row}"][data-col="${col}"]`);
            cell.classList.remove('x', 'o', 'filled');
            
            if (board[row][col] === 'X') {
                cell.classList.add('x', 'filled');
            } else if (board[row][col] === 'O') {
                cell.classList.add('o', 'filled');
            }
        }
    }
    
    // Update current player display
    const currentPlayerEl = document.getElementById('current-player');
    if (!gameOver) {
        currentPlayerEl.innerHTML = `Current Player: <span style="color: ${currentPlayer === 'X' ? '#ff3333' : '#3399ff'}">${currentPlayer}</span>`;
    }
    
    // Handle game over
    if (gameOver) {
        const gameOverEl = document.getElementById('game-over');
        const winnerTextEl = document.getElementById('winner-text');
        gameOverEl.classList.remove('hidden');
        
        if (winner === 'Tie') {
            winnerTextEl.textContent = "IT'S A TIE!";
            winnerTextEl.className = 'winner-tie';
        } else {
            winnerTextEl.textContent = `PLAYER ${winner} WINS!`;
            winnerTextEl.className = winner === 'X' ? 'winner-x' : 'winner-o';
            startCelebration();
        }
        
        // Disable all cells
        document.querySelectorAll('.cell').forEach(cell => {
            cell.style.cursor = 'not-allowed';
        });
    }
}

// Update board from server
async function updateBoard() {
    if (!gameId) return;
    
    const response = await fetch('/api/game-state', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            game_id: gameId
        })
    });
    
    const data = await response.json();
    updateBoardFromData(data);
}

// Reset game
async function resetGame() {
    if (!gameId) {
        await initGame();
        return;
    }
    
    const response = await fetch('/api/reset', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            game_id: gameId
        })
    });
    
    const data = await response.json();
    
    // Clear board
    document.querySelectorAll('.cell').forEach(cell => {
        cell.classList.remove('x', 'o', 'filled');
        cell.style.cursor = 'pointer';
    });
    
    // Hide game over
    document.getElementById('game-over').classList.add('hidden');
    
    // Update board
    updateBoardFromData(data);
    
    // Re-enable cells
    document.querySelectorAll('.cell').forEach(cell => {
        cell.addEventListener('click', handleCellClick);
    });
}

// Back to menu
function backToMenu() {
    document.getElementById('game-screen').classList.remove('active');
    document.getElementById('menu-screen').classList.add('active');
    gameId = null;
    currentMode = null;
}

// Handle cell click
function handleCellClick(event) {
    const row = parseInt(event.currentTarget.dataset.row);
    const col = parseInt(event.currentTarget.dataset.col);
    makeMove(row, col);
}

// Add click listeners to cells
document.querySelectorAll('.cell').forEach(cell => {
    cell.addEventListener('click', handleCellClick);
});

// Keyboard controls
document.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && document.getElementById('menu-screen').classList.contains('active')) {
        startGame();
    } else if (e.key === '1' && document.getElementById('mode-screen').classList.contains('active')) {
        selectMode('friend');
    } else if (e.key === '2' && document.getElementById('mode-screen').classList.contains('active')) {
        selectMode('bot');
    } else if (e.key === 'r' && document.getElementById('game-screen').classList.contains('active')) {
        resetGame();
    } else if (e.key === 'Escape' && document.getElementById('game-screen').classList.contains('active')) {
        backToMenu();
    }
});

// Celebration animation
function startCelebration() {
    const celebration = document.getElementById('celebration');
    celebration.innerHTML = '';
    
    const colors = ['#ff3333', '#3399ff', '#33ff66', '#ffd700', '#ff33ff'];
    
    for (let i = 0; i < 50; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.top = Math.random() * 100 + '%';
        particle.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
        particle.style.animationDelay = Math.random() * 0.5 + 's';
        celebration.appendChild(particle);
    }
    
    // Clear particles after animation
    setTimeout(() => {
        celebration.innerHTML = '';
    }, 3000);
}


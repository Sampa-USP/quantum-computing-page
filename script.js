const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

function drawGrid() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (let i = 0; i <= 10; i++) {
        ctx.moveTo(i * 50, 0);
        ctx.lineTo(i * 50, 500);
        ctx.moveTo(0, i * 50);
        ctx.lineTo(500, i * 50);
    }
    ctx.stroke();
}

function drawShip(x, y) {
    ctx.fillStyle = "gray";  // 🔹 Barcos do jogador aparecem em cinza
    ctx.fillRect(x * 50, y * 50, 50, 50);
}

function drawQuantumAttack(x, y) {
    ctx.fillStyle = "blue";
    ctx.beginPath();
    ctx.arc(x * 50 + 25, y * 50 + 25, 10, 0, Math.PI * 2);
    ctx.fill();
}

function playerAttack() {
    const coord = document.getElementById("playerMove").value;
    fetch('/player_attack', {
        method: 'POST',
        body: JSON.stringify({ coord }),
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
        alert(data.player.message);

        if (data.quantum.status === "hit" || data.quantum.status === "miss") {
            drawQuantumAttack(data.quantum.x, data.quantum.y);
            alert(data.quantum.message);
        }
    });
}


function initializeGame() {
    fetch('/initialize_game')
        .then(response => response.json())
        .then(data => {
            drawGrid();
            data.player_board.forEach((row, y) => {
                row.forEach((cell, x) => {
                    if (cell === "S") drawShip(x, y);
                });
            });
        });
}

drawGrid();


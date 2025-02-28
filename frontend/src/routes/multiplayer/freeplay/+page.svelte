<script lang="ts">
    import { PUBLIC_API_BASE_URL } from '$env/static/public';
    import Alert from '$lib/Alert.svelte';
    import { User, resetGame, gameInfo } from "$lib/shared.svelte"
    import { io, Socket } from 'socket.io-client';
    import Board from '$lib/Board.svelte';
    import { page } from '$app/stores';

    const api_url = PUBLIC_API_BASE_URL || 'https://your-api.com/api/v1/';
    let boardComponent: any;
    let gameCode = $state("");
    let username = $state("");
    let showUsernameInput = $state(true);

    // Freeplay-specific types
    interface FreeplayGameStartData {
        code: string;
        symbols: { [username: string]: "X" | "O" };
    }

    interface FreeplayMoveData {
        code: string;
        move: [number, number];
        username: string;
        symbol: "X" | "O";
    }

    // Socket.io setup
    let socketioHostUrl = "http://localhost:5000";
    if (document.location.protocol === 'https:') {
        socketioHostUrl = document.location.hostname;
    }

    const socket: Socket = io(socketioHostUrl, {
        path: "/socket.io/",
        transports: ["websocket"]
    });

    // Game state
    let mySymbol: "X" | "O" = $state("X");
    let otherPlayer = $state("");
    let status = $state<"creating" | "waiting" | "playing" | "error">("creating");
    let errorMessage = $state("");

    // Extract code from URL
    $effect(() => {
        const params = new URLSearchParams(window.location.search);
        const urlCode = params.get('code');
        if (urlCode && urlCode !== gameCode) {
            gameCode = urlCode;
            status = "waiting";
            showUsernameInput = true;
        }
    });

    // Socket handlers
    socket.on('game_start_freeplay', (data: FreeplayGameStartData) => {
        status = "playing";
        const players = Object.keys(data.symbols);
        mySymbol = data.symbols[username];
        otherPlayer = players.find(name => name !== username) || "Opponent";
        resetGame();
    });

    socket.on('move_freeplay', (data: FreeplayMoveData) => {
        const [row, column] = data.move;
        boardComponent.makeProgrammaticMove(row, column, data.symbol);
    });

    socket.on('opponent_disconnected', (data) => {
        status = "error";
        errorMessage = `Opponent disconnected: ${data.message}`;
    });

    socket.on('freeplay_error', (data) => {
        if (data.message === "Room full") {
            errorMessage = "This game is already full";
            window.history.replaceState({}, '', '/freeplay');
            gameCode = "";
        } else {
            errorMessage = data.message;
        }
        status = "error";
    });

    // Game creation/joining logic
    async function createGame() {
        try {
            const response = await fetch(`${api_url}/freeplay/create`, { method: 'POST' });
            const data = await response.json();
            window.history.pushState({}, '', `/freeplay?code=${data.code}`);
            gameCode = data.code;
            status = "waiting";
        } catch (err) {
            status = "error";
            errorMessage = "Failed to create game";
        }
    }

    function joinGame() {
        if (!username.trim()) {
            errorMessage = "Please enter a username";
            return;
        }

        if (!/^\d{6}$/.test(gameCode)) {
            errorMessage = "Invalid game code format";
            return;
        }

        socket.emit('join_freeplay', {
            code: gameCode,
            username: username
        });

        showUsernameInput = false;

        // Add timeout for failed connection
        setTimeout(() => {
            if (status !== "playing") {
                status = "error";
                errorMessage = "Failed to connect to game";
            }
        }, 5000);
    }

    function handleMove(row: number, col: number, symbol: "X" | "O") {
        socket.emit('move_freeplay', {
            code: gameCode,
            move: [row, col],
            username: username,
            symbol: symbol
        });
    }

    function copyGameLink() {
        navigator.clipboard.writeText(window.location.href);
    }

    // Reconnection logic
    socket.on('connect', () => {
        if (gameCode && status === "playing") {
            socket.emit('rejoin_freeplay', {
                code: gameCode,
                username: username
            });
        }
    });
</script>

<div>
    <div style="max-width: 600px; margin: auto;">
        <h1>Freeplay Game</h1>

        {#if status === 'creating'}
            <div class="creation-panel">
                <button on:click={createGame}>Create New Game</button>
                <p>or</p>
                <div class="join-section">
                    <input
                        type="text"
                        bind:value={gameCode}
                        placeholder="Enter game code"
                        disabled={!showUsernameInput}
                    />
                    {#if showUsernameInput}
                        <input
                            type="text"
                            bind:value={username}
                            placeholder="Your username"
                        />
                        <button on:click={joinGame}>Join Game</button>
                    {/if}
                </div>
            </div>

        {:else if status === 'waiting'}
            <div class="waiting-panel">
                <h2>Game Code: {gameCode}</h2>
                <button on:click={copyGameLink}>📋 Copy Game Link</button>
                <div class="connection-status">
                    <div class="loading-spinner"></div>
                    <p>Waiting for opponent to join...</p>
                </div>
                {#if User.loggedIn}
                    <p class="hint">You can safely close this tab and return later</p>
                {/if}
            </div>

        {:else if status === 'playing'}
            <div class="game-panel">
                <h2>Playing against {otherPlayer}</h2>
                <Board
                    bind:this={boardComponent}
                    boardApiInfo={gameInfo.apiResponse}
                    mode="freeplay"
                    allowedPlayer={mySymbol}
                    onMove={handleMove}
                    opponentUsername={otherPlayer}
                />
            </div>

        {:else if status === 'error'}
            <div class="error-panel">
                <Alert>{errorMessage}</Alert>
                <button on:click={() => window.location.reload()}>Try Again</button>
            </div>
        {/if}
    </div>
</div>

<style>
    .creation-panel, .waiting-panel, .game-panel, .error-panel {
        text-align: center;
        padding: 2rem;
        background: #f5f5f5;
        border-radius: 8px;
        margin: 1rem 0;
    }

    input, button {
        margin: 0.5rem;
        padding: 0.5rem;
        border: 1px solid #ccc;
        border-radius: 4px;
    }

    button {
        background: #646cff;
        color: white;
        cursor: pointer;
    }

    .loading-spinner {
        width: 40px;
        height: 40px;
        border: 4px solid #f3f3f3;
        border-top: 4px solid #646cff;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 1rem auto;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    .hint {
        font-size: 0.9rem;
        color: #666;
        margin-top: 1rem;
    }

    .connection-status {
        margin-top: 1rem;
    }
</style>
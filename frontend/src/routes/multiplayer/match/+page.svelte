<script lang="ts">
    import { PUBLIC_API_BASE_URL } from '$env/static/public';
    import Alert from '$lib/Alert.svelte';
    import Login from '$lib/Login.svelte';
    import { User, resetGame, gameInfo } from "$lib/shared.svelte"
    import { io, Socket } from 'socket.io-client';
    import Board from '$lib/Board.svelte';
    const api_url = PUBLIC_API_BASE_URL || 'https://odevzdavani.tourdeapp.cz/mockbush/api/v1/';
    let boardComponent: any; //reference to call functions exported from that component
    interface MatchFoundData {
        opponent: string;
        room: string;
        symbol: "X" | "O"
    }

    interface GameStartData {
        room: string;
        symbols: {[username: string]: "X" | "O"}; //If I wanted, I could move [player: string]: "X" | "O" or [key: string]: string; to a seperate interface Symbols
    }

    interface MoveData {
       room: string;           // Room identifier
       move: [number, number]; // x, y coordinates
       username: string;       // Player's username
       symbol: "X" | "O";      // Player's symbol
    }

   interface OpponentDisconnectedData {
       message: string;    // Disconnect message
   }

    interface ServerToClientEvents {
        match_found: (data: MatchFoundData) => void,
        game_start: (data: GameStartData) => void,
        move: (data: MoveData) => void,
        opponent_disconnected: (data: OpponentDisconnectedData) => void
    }

    interface JoinData {
        username: string,
        room: string
    }

    interface ClientToServerEvents {
        join: (data: JoinData) => void,
        move: (data: MoveData) => void,
    }

    // Connection
    let socketioHostUrl = "http://localhost:5000";
    let isProduction = document.location.hostname.includes("tourde.app") || document.location.protocol == 'https:';
    console.log("isProduction", isProduction);
    if(isProduction){
        socketioHostUrl = document.location.hostname; //without 5000
        console.log("socketioHostUrl changed to", socketioHostUrl);
    }
    console.log("socketioHostUrl is", socketioHostUrl);
    const socket: Socket<ServerToClientEvents, ClientToServerEvents> = io(socketioHostUrl, { //for deploy **probably** document.location.hostname without the port
		path: "/socket.io/",
		transports: ["websocket"],
        query: {
            user_uuid: User.uuid
        }
    });
    const minutesPerPlayerPerGame = 8;
    let player1Time = $state(minutesPerPlayerPerGame * 60);
    let player2Time = $state(minutesPerPlayerPerGame * 60);
    let currentPlayerTimer = $state<"X" | "O">("X");
    let timerInterval = $state<number | null>(null);
    let gameActive = $state(false);

    function formatTime(seconds: number): string {
        const minutes = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${minutes}:${secs.toString().padStart(2, "0")}`;
    }

    function startTimer() {
        if (timerInterval) clearInterval(timerInterval);
        timerInterval = setInterval(() => {
            if (currentPlayerTimer === "X") {
                player1Time -= 1;
            } else {
                player2Time -= 1;
            }

            if (player1Time <= 0 || player2Time <= 0) {
                clearInterval(timerInterval!);
                const winner = currentPlayerTimer === "X" ? "O" : "X";
                socket.emit("timeout", { room, winner });
                gameActive = false;
            }
        }, 1000);
    }

    function switchTimer() {
        currentPlayerTimer = currentPlayerTimer === "X" ? "O" : "X";
        startTimer();
    }


    // Listen for events
    socket.on('match_found', (data: MatchFoundData) => {
        // Show invitation dialog
        console.log(`Match found from ${data.opponent} at room ${data.room}. I'm playing symbol ${data.symbol}`);
        socket.emit('join', {username: User.name, room: data.room});
    });

    let mySymbol: "X" | "O" = $state("X");
    let room = "";
    let otherPlayer = "";
    socket.on('game_start', (data: GameStartData) => {
        // Should be logged after 'join' is sent to server
        room = data.room;
        console.log(`Game starting in room ${data.room} between these two players:`, data);
        resetGame();
        mySymbol = data.symbols[User.name as string];
        otherPlayer = Object.keys(data.symbols).filter((value) => value != User.name)[0];
        console.log("other player is", otherPlayer);

        player1Time = 5 * 60;
        player2Time = 5 * 60;
        gameActive = true;
        currentPlayerTimer = "X";
        startTimer();
        
        status = "Game started";
    });

    socket.on('move', (data) => {
        // Update game board
        console.log(`Move at ${data.move} by ${data.username}`);
        const [row, column] = data.move;
        boardComponent.makeProgrammaticMove(row, column, data.symbol);
        currentPlayerTimer = data.symbol === "X" ? "O" : "X";
        startTimer();
    });

    socket.on('opponent_disconnected', (data) => {
        console.log("Opponent disconnected", data.message);
    });
    
    console.log("document location", document.location.hostname);
    
    
    /*Matchmaking API call section -------------------------------------------*/
    let status: "Initial" | "Game started" | "Added to matchmaking queue" = $state("Initial");
    let showError = $state(false);
    let errorMessage = $state("");
    async function addToMatchMakingQueue(){
        console.log("Making call to /matchmaking");
        const request = await fetch(`${api_url}/matchmaking`,
            {
                method: "POST",
                body: JSON.stringify({
                    uuid: User.uuid
                }),
                headers: {
                    "Content-Type": "application/json",
                }
            }
        );
        if(request.status == 404){
            showError = true;
            errorMessage = "Uživatel nenalezen. \n Zkuste se odhlásit a přihlásit znova"; //a tam uživateli povíme, že byl třeba zabanován
        }
        if(request.ok){
            const response = await request.json();
            console.log("Response from /matchmaking", response.message);
            status = response.message;
        }
    }

    //The point of this effect TO HANDLE THE LIFETIME OF REGISTERED LISTENERS
    //PREVIOUSLY, WHEN THE USER NAVIGATED AWAY, THOSE LISTENERS would STAY until CTRL SHIFT R
    $effect(() => {
        if(User.loggedIn){
            console.log("Calling addToMatchMakingQueue() from effect");
            addToMatchMakingQueue();
        }else{
            console.log("User not logged in => not calling  addToMatchMakingQueue()")
        }

        return () => {
            //should be called when navigating away - needed for SPA
            //removes the connection without a full reload
            //(the trying to reconnect logs when the user was on a different page after the local server was turned off annoyed me)
            //what happens on socketio on this route, should also stay on this route
            console.log("Disconnecting because the user navigated away");
            socket.disconnect();
        }
    });

    function onMove(rowIndex: number, columnIndex: number, naTahu: "X" | "O"){
        console.log(`detected move of ${naTahu} to ${rowIndex}, ${columnIndex} from local player to send to server`);
        socket.emit("move", {
            room: room,
            move: [rowIndex, columnIndex],
            username: (User.name as string), //TODO: mozna hodit vyjimu, kdyby nahodou tady User.name byl null //z localstorage siece User.name muze byt null, ale verim ze se to tady nestane (ze se uz nastavi z registrovaní / přihlášení)
            symbol: naTahu
        });
        switchTimer();
    }

    let showLoginPopup = $state(false);
    let showRegisterPopup = $state(false);
</script>

<div>
    <div style="max-width: 600px;margin: auto;">
        <h1>Hodnocená hra</h1>
        {#if status != "Game started"}
            <h2>Hra, v niž lze získat ELO. Spoluhráče vám přiřadíme :)</h2>
        {/if}
        {#if User.loggedIn}
            {#if status == "Added to matchmaking queue"}
                <p>Čeká se na spoluhráče...</p>
                <hr>
                <p>Hra nezačiná?</p>
                <button onclick={() => window.location.reload()}>Načíst znova</button>
            {:else if status == "Initial"}
                <p>Načítání...</p>
                <hr>
                <p>Hra nezačiná?</p>
                <button onclick={() => window.location.reload()}>Načíst znova</button>
            {:else if status == "Game started"}
                <div class="timers">
                    <div class="timer" class:active={currentPlayerTimer === mySymbol}>
                        <span>Váš čas: {formatTime(mySymbol === "X" ? player1Time : player2Time)}</span>
                    </div>
                    <div class="timer" class:active={currentPlayerTimer !== mySymbol}>
                        <span>Čas soupeře: {formatTime(mySymbol === "X" ? player2Time : player1Time)}</span>
                    </div>
                </div>
                <Board bind:this={boardComponent} boardApiInfo={gameInfo.apiResponse} mode="multiplayer" allowedPlayer={mySymbol} onMove={onMove} opponentUsername={otherPlayer}/>
            {/if}
        {:else}
            <hr>
            <div class="center">
                <h2>Pro tento typ hry je potřeba <button onclick={() => showLoginPopup = true}>Se přihlásit</button> </h2>
                <h2>Jinak si můžete zahrát <a href="../multiplayer/friendly">přátelskou (nehodnocenou) hru</a></h2>
                <h2>Nemáte účet? <button onclick={() => showRegisterPopup = true}>Registrovat</button></h2> 
            </div>
        {/if}
    </div>
</div>

{#if showError}
    <Alert bind:show={showError}>{errorMessage}</Alert>
{/if}

{#if showLoginPopup}
  <!-- it seems like window.location reload does not reload the page when called from components in Svelte -->
  <Login bind:show={showLoginPopup} reloadPageAfterSuccess={true}/>
{/if}

{#if showRegisterPopup}
    <!-- callbackAfterSuccess={() => window.location.reload()} -->
  <Login bind:show={showRegisterPopup} mode="register" reloadPageAfterSuccess={true}/>
{/if}

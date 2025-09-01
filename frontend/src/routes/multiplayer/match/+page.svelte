<script lang="ts">
    import { PUBLIC_API_BASE_URL } from '$env/static/public';
    import Alert from '$lib/Alert.svelte';
    import { User, resetGame, gameInfo } from "$lib/shared.svelte"
    import Board from '$lib/Board.svelte';
    import { beforeNavigate } from '$app/navigation';
    import { SocketHandler } from './socketHandler';

    const api_url = PUBLIC_API_BASE_URL || 'https://odevzdavani.tourdeapp.cz/mockbush/api/v1/';
    let boardComponent: any; //reference to call functions exported from that component
    let socketHandler: SocketHandler | undefined

    // Connection
    if(User.loggedIn){
        let socketioHostUrl = "http://localhost:5000";
        let isProduction = document.location.hostname.includes("tourde.app") || document.location.protocol == 'https:';
        console.log("isProduction", isProduction);
        if(isProduction){
            socketioHostUrl = document.location.hostname; //without 5000
            console.log("socketioHostUrl changed to", socketioHostUrl);
        }
        console.log("socketioHostUrl is", socketioHostUrl);

        socketHandler = new SocketHandler(
            socketioHostUrl,
            //callbacks for these server sent events
            {
                match_found(data){
                    return;
                },
                game_start(data){
                    if(User.name === null){
                        console.error("Cannot respond to gam_start when the user is null = logged out");
                        return;
                    }
                    // Should be logged after 'join' is sent to server
                    room = data.room;
                    console.log(`Game starting in room ${data.room} between these two players:`, data);
                    resetGame();
                    mySymbol = data.symbols[User.name];
                    otherPlayer = Object.keys(data.symbols).filter((value) => value != User.name)[0];
                    console.log("other player is", otherPlayer);

                    player1Time = 5 * 60;
                    player2Time = 5 * 60;
                    gameActive = true;
                    currentPlayerTimer = "X";
                    startTimer();
                    status = "Game started";
                },
                move(data){
                    // Update game board
                    console.log(`Move at ${data.move} by ${data.username}`);
                    const [row, column] = data.move;
                    boardComponent.makeProgrammaticMove(row, column, data.symbol);
                    currentPlayerTimer = data.symbol === "X" ? "O" : "X";
                    console.log("move event received", timerInterval);
                    //Do not start timer if it was stopped after win was detected
                    if(gameActive){
                        startTimer();
                    }
                },
                opponent_disconnected(data) {
                    console.log("Opponent disconnected", data.message);
                },
            }
        );

        //The point of this is TO HANDLE THE LIFETIME of socketio listeners
        //Before using beforeNavigate, WHEN THE USER NAVIGATED AWAY, THOSE socketio LISTENERS would STAY until CTRL SHIFT R (beause this is an SPA)
        beforeNavigate((navigation) => {
            if(navigation.to && navigation.to.url){
                //else it would differentiate between "/multiplayer/match" and "/multiplayer/match#", causing a disconnect
                if(!navigation.to.url.pathname.startsWith("/multiplayer/match")){
                    console.log("Disconnecting because the user navigated away to", navigation.to.url.pathname);
                    socketHandler!.disconnect(); 
                }  
            }
        });
    }
   
   
    const minutesPerPlayerPerGame = 8;
    let player1Time = $state(minutesPerPlayerPerGame * 60);
    let player2Time = $state(minutesPerPlayerPerGame * 60);
    let currentPlayerTimer = $state<"X" | "O">("X");
    let timerInterval = $state<number | NodeJS.Timeout | null>(null); //it is a number as this is not called in node.js context, but adding to appease TS
    let gameActive = $state(false);

    function formatTime(seconds: number): string {
        const minutes = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${minutes}:${secs.toString().padStart(2, "0")}`;
    }

    function startTimer() {
        console.log("old", timerInterval);
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
                socketHandler!.emit("timeout", { room, winner });
                gameActive = false;
            }
        }, 1000);
        console.log("new", timerInterval);
    }

    function switchTimer() {
        currentPlayerTimer = currentPlayerTimer === "X" ? "O" : "X";
        startTimer();
    }

    function stopTimer(){
        console.log("STOP TIMER RAN", timerInterval);
        clearInterval(timerInterval as number);
        gameActive = false;
    }

    let mySymbol: "X" | "O" = $state("X");
    let room = "";
    let otherPlayer = "";
    
    
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

    //The point of this effect is TO HANDLE THE LIFETIME of addToMatchmaking queue
    //Similarly beforeNavigate handles the lifetime of socketio events
    //All because this is an SPA
    $effect(() => {
        if(User.loggedIn){
            console.log("Calling addToMatchMakingQueue() from effect");
            addToMatchMakingQueue();
        }else{
            console.log("User not logged in => not calling  addToMatchMakingQueue()")
        }
    });

    function onMove(rowIndex: number, columnIndex: number, naTahu: "X" | "O"){
        if(!User.loggedIn){
            throw new Error("Move attempted while user not logged in");
        }
        console.log(`detected move of ${naTahu} to ${rowIndex}, ${columnIndex} from local player to send to server`);
        if(User.name === null){
            throw Error("Tady už určitě nesmí být User null, z funkce onMove, která posílá tah");
        }
        socketHandler!.emit("move", {
            room: room,
            move: [rowIndex, columnIndex],
            username: User.name,
            symbol: naTahu
        });
        switchTimer();
    }
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
                <Board bind:this={boardComponent} boardApiInfo={gameInfo.apiResponse} mode="multiplayer" allowedPlayer={mySymbol} onMove={onMove} opponentUsername={otherPlayer} onWin={stopTimer}/>
            {/if}
        {:else}
            <hr>
            <div class="center">
                <h2>Pro tento typ hry je potřeba <a data-sveltekit-reload href={`../login?returnURL=${encodeURIComponent("/multiplayer/match")}`}>Se přihlásit</a> </h2>
                <h2>Jinak si můžete zahrát <a data-sveltekit-reload href="../multiplayer/friendly">přátelskou (nehodnocenou) hru</a></h2>
                <h2>Nemáte účet? <a data-sveltekit-reload href={`../register?returnURL=${encodeURIComponent("/multiplayer/match")}`}>Registrovat</a></h2> 
            </div>
        {/if}
    </div>
</div>

{#if showError}
    <Alert bind:show={showError}>{errorMessage}</Alert>
{/if}

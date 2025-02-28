<script lang="ts">
    import { PUBLIC_API_BASE_URL } from '$env/static/public';
    import { io, Socket } from 'socket.io-client';
    import { freeplayCreatePost, freePlayGameObject, User, gameInfo } from "$lib/shared.svelte";
    import { page } from '$app/state';
    import Board from '$lib/Board.svelte';
    let gameCode = $derived(String(page.url).split("?code=")[1]);
    let isGameUrl = $derived(!!gameCode);

    $effect(() => {
        if(isGameUrl){
            socket.emit(`join_freeplay`, {
                code: gameCode,
                username: User.name
            });
        }
    });

    let socketioHostUrl = "http://localhost:5000";
    let isProduction = document.location.hostname.includes("tourde.app") || document.location.protocol == 'https:';
    console.log("isProduction", isProduction);
    if(isProduction){
        socketioHostUrl = document.location.hostname; //without 5000
        console.log("socketioHostUrl changed to", socketioHostUrl);
    }
    console.log("socketioHostUrl is", socketioHostUrl);
    //: Socket<ServerToClientEvents, ClientToServerEvents>
    const socket = io(socketioHostUrl, { //for deploy **probably** document.location.hostname without the port
		path: "/socket.io/",
		transports: ["websocket"],
        query: {
            user_uuid: User.uuid
        }
    });

    let stav = $state("");

    
    socket.on('waiting_for_opponent', (data) => {
        stav = "waiting";
    });

    let mySymbol: "X" | "O" = $state("X");
    socket.on(`game_start`, (data) => { 
        mySymbol = data.symbols[User.name as string];
        stav = "start";
    });

    let boardComponent: any;

    function onMove(rowIndex: number, columnIndex: number, naTahu: "X" | "O"){
        console.log(`detected move of ${naTahu} to ${rowIndex}, ${columnIndex} from local player to send to server`);
        if(User.name === null){
            throw Error("Tady už určitě nesmí být User null, z funkce onMove, která posílá tah");
        }
        socket.emit("move", {
            code: gameCode,
            move: [rowIndex, columnIndex],
            username: User.name,
            symbol: naTahu
        });
    }

    socket.on(`move`, (data) => { 
        const [row, column] = data.move;
        boardComponent.makeProgrammaticMove(row, column, data.symbol);
    });


</script>
<p>{isGameUrl}</p>
{#if User.loggedIn && !gameCode}
    <p>{gameCode}</p>
    <div class="center">
        <h2>Vytvoření Friendly hry</h2>
        <p>Vygenerujte si kód hry, který pak nasdílíte spoluhráči</p>
        {#if freePlayGameObject.loaded}
            <p>Kód je {freePlayGameObject.code}</p>
            <p>Na hru se připojte <a href="?code={freePlayGameObject.code}">odkazem</a>, který obsahuje kód. Tento odkaz je možné sdílet spoluhráči se stejným výsledkem jako sdílení kódu.</p>
        {/if}
        <button onclick={() => freeplayCreatePost()}>Vygenerovat kód</button>
    </div>
{:else}
    {#if stav == "waiting"}
        <p>Čeká se na spoluhráče...</p>
    {:else if stav == "start"}
        <Board bind:this={boardComponent} boardApiInfo={gameInfo.apiResponse} mode="multiplayer" allowedPlayer={mySymbol} onMove={onMove}/>
    {/if}
{/if}
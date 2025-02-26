<script lang="ts">
    import { PUBLIC_API_BASE_URL } from '$env/static/public';
    import Alert from '$lib/Alert.svelte';
    import { User } from "$lib/shared.svelte"
    import { onMount } from 'svelte';
    import { io, Socket } from 'socket.io-client';
    const api_url = PUBLIC_API_BASE_URL || 'https://odevzdavani.tourdeapp.cz/mockbush/api/v1/';
    
    interface MatchFoundData {
        opponent: string;
        room: string;
        symbol: "X" | "O"
    }

    interface GameStartData {
        room: string;
        symbols: {[username: string]: "X" | "O"}; //If I wanted, I could move [player: string]: "X" | "O" or [key: string]: string; to a seperate interface Symbols
    }

    interface ServerToClientEvents {
        match_found: (data: MatchFoundData) => void,
        game_start: (data: GameStartData) => void,
    }

    interface JoinData {
        username: string,
        room: string
    }

    interface ClientToServerEvents {
        join: (data: JoinData) => void,
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
    const socket = io(socketioHostUrl, { //for deploy **probably** document.location.hostname without the port
		path: "/socket.io/",
		transports: ["websocket"],
        query: {
            user_uuid: User.uuid
        }
    });

    // Listen for events
    socket.on('match_found', (data: MatchFoundData) => {
        // Show invitation dialog
        console.log(`Match found from ${data.opponent} at room ${data.room}. I'm playing symbol ${data.symbol}`);
        socket.emit('join', {username: data.opponent, room: data.room});
    });

    socket.on('game_invitation', (data) => {
        // Show invitation dialog
        console.log(`Invitation from ${data.challenger.username}`);
    });

    socket.on('game_start', (data: GameStartData) => {
        // Should be logged after 'join' is sent to server
        console.log(`Game starting in room ${data.room} between these two players:`, data);
    });

    socket.on('move', (data) => {
        // Update game board
        console.log(`Move at ${data.move} by ${data.username}`);
    });

    socket.on('opponent_disconnected', (data) => {
        console.log("Opponent disconnected", data.message);
    });
    
    console.log("document location", document.location.hostname);
    
    
    /*Matchmaking API call section -------------------------------------------*/
    let status = $state("Initial");
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
    onMount(addToMatchMakingQueue);
</script>

<div class="center">
    <h1>Hodnocená hra</h1>
    <h2>Hra, v niž lze získat ELO. Spoluhráče vám přiřadíme :)</h2>
    {#if status == "Added to matchmaking queue"}
        <p>Čeká se na spoluhráče...</p>
    {:else if status == "Initial"}
        <p>Načítání...</p>
    {/if}
</div>

{#if showError}
    <Alert bind:show={showError}>{errorMessage}</Alert>
{/if}

<script lang="ts">
    import { PUBLIC_API_BASE_URL } from '$env/static/public';
    import Alert from '$lib/Alert.svelte';
    import { User } from "$lib/shared.svelte"
    import { onMount } from 'svelte';
    import io from 'socket.io-client';
    const api_url = PUBLIC_API_BASE_URL || 'https://odevzdavani.tourdeapp.cz/mockbush/api/v1/';
    
    // Connection
    const socket = io("http://localhost:5000", { //for deploy **probably** document.location.hostname without the port
		path: "/socket.io/",
		transports: ["websocket"],
        query: {
            user_uuid: User.uuid
        }
    });

    // Listen for events
    socket.on('game_invitation', (data) => {
        // Show invitation dialog
        console.log(`Invitation from ${data.challenger.username}`);
    });

    socket.on('game_start', (data) => {
        // Initialize game board
        console.log(`Game starting in room ${data.room}`);
    });

    socket.on('move', (data) => {
        // Update game board
        console.log(`Move at ${data.move} by ${data.username}`);
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
            console.log("Respone from /matchmaking", response.message);
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

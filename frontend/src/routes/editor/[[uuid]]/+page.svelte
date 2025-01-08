<script>
    import { gameInfo, resetGame, fetchGame } from "$lib/shared.svelte";
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import BoardEditor from "$lib/BoardEditor.svelte";
    import { PUBLIC_API_BASE_URL } from '$env/static/public';
    const api_url = PUBLIC_API_BASE_URL || 'https://odevzdavani.tourdeapp.cz/mockbush/api/v1/';

    //TODO: ADD put request to update the game
    async function editPuzzle(){
        if($page.params.uuid){ //on /game/:uuid, editing an existing game
            const request = await fetch(`${api_url}/games/${$page.params.uuid}`, 
                {
                    method: "PUT",
                    body: JSON.stringify({
                        name: gameInfo.apiResponse.name,
                        board: gameInfo.apiResponse.board,
                        difficulty: gameInfo.apiResponse.difficulty,    
                    }),
                    headers: {
                        "Content-Type": "application/json",
                    }
                }
            );
            const data = await request.json();
            console.log("data", data)
        }else{
            throw new Error("Call createPuzzle first");
        }
    }

    let boardKey = 0;

    $effect(() => {

        const uuid = $page.params.uuid;
        console.log("slug changed to", uuid);
        boardKey++; // Force re-render
    
        if (!uuid) {
            // Reset to empty board when no UUID in URL
            resetGame();
        } else {
            // Fetch game data when UUID present
            fetchGame(uuid).then(data => {
                gameInfo.apiResponse = data;
                gameInfo.selected = true;
            });
        }
    });
</script>

<!-- <h1>Editor {gameInfo.apiResponse.name}</h1> -->

<div class="toolbar">
    <input type="text" bind:value={gameInfo.apiResponse.name}>
    <button onclick={editPuzzle}>Uložit</button>
</div>

{#if gameInfo.selected}
    <BoardEditor boardApiInfo={gameInfo.apiResponse}></BoardEditor>
{/if}


<style>
    .toolbar {
        display: flex;
        gap: 0.5em;
        height: 50px;
        width: fit-content;
        margin: 1rem auto;
    }
    .toolbar > input{
        padding: 0.5em;
        font-size: 2rem;
        width: 100%;
    }
</style>
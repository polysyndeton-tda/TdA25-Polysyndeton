<script>
    import { gameInfo, resetGame, fetchGame, editPuzzle } from "$lib/shared.svelte";
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import BoardEditor from "$lib/BoardEditor.svelte";
    import { PUBLIC_API_BASE_URL } from '$env/static/public';
    const api_url = PUBLIC_API_BASE_URL || 'https://odevzdavani.tourdeapp.cz/mockbush/api/v1/';

    let boardKey = 0;
    let errorMessage = $state("");
    
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
                console.log("data from editor fetch", data);
                gameInfo.apiResponse = data;
                gameInfo.selected = true;
            })
            .catch(err => {
                errorMessage = err;
            })
        }
    });
</script>

{#if gameInfo.selected}
    <div class="toolbar">
        <input type="text" bind:value={gameInfo.apiResponse.name}>
        <button onclick={() => editPuzzle($page.params.uuid)}>Uložit</button>
    </div>
    <BoardEditor boardApiInfo={gameInfo.apiResponse}></BoardEditor>
{/if}

{#if errorMessage}
    <h2 class="errorMessage">{errorMessage}</h2>
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
    .errorMessage{
        /* For \n in the error message to be rendered in HTML*/
        white-space: pre-wrap;
    }
</style>
<script>
    import { gameInfo, resetGame, fetchGame, editPuzzle } from "$lib/shared.svelte";
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import BoardEditor from "$lib/BoardEditor.svelte";
    import { PUBLIC_API_BASE_URL } from '$env/static/public';
    const api_url = PUBLIC_API_BASE_URL || 'https://odevzdavani.tourdeapp.cz/mockbush/api/v1/';

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


<div class="toolbar">
    <input type="text" bind:value={gameInfo.apiResponse.name}>
    <button onclick={() => editPuzzle($page.params.uuid)}>Uložit</button>
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
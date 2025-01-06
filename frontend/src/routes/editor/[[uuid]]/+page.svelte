<script>
    import { gameInfo, resetGame } from "$lib/shared.svelte";
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import BoardEditor from "$lib/BoardEditor.svelte";
    import { PUBLIC_API_BASE_URL } from '$env/static/public';

    async function fetchGame(uuid) {
        const api_url = PUBLIC_API_BASE_URL || 'https://odevzdavani.tourdeapp.cz/mockbush/api/v1/';
        const request = await fetch(`${api_url}/games/${uuid}`);
        const data = await request.json();
        return data;
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

{#if gameInfo.selected}
<BoardEditor boardApiInfo={gameInfo.apiResponse}></BoardEditor>
{/if}

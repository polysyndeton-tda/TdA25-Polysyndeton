<script>
    import { gameInfo, resetGame } from "$lib/shared.svelte";
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import BoardEditor from "$lib/BoardEditor.svelte";

    async function fetchGame(uuid) {
        const request = await fetch('https://odevzdavani.tourdeapp.cz/mockbush/api/v1/games/' + uuid);
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

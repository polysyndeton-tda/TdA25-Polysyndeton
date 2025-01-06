<script>
    import { gameInfo, resetGame } from "$lib/shared.svelte";
    import Board from "$lib/Board.svelte";
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import { PUBLIC_API_BASE_URL } from '$env/static/public';

    async function fetchGame(uuid) {
        const api_url = PUBLIC_API_BASE_URL || 'https://odevzdavani.tourdeapp.cz/mockbush/api/v1/';
        const request = await fetch(`${api_url}/games/${uuid}`);
        const data = await request.json();
        return data;
    }

    let boardKey = 0;
    let loaded = $state(false);

    $effect(() => {
        /*Does not react to further Game button clicks in the nav since $page.params.uuid stays the same
         => there needs to be a function in the nav onclick listener that explicitly resets the state => resetGame */
        const uuid = $page.params.uuid;
        console.log("slug changed to", uuid);
        //This fixes the "Game" link in the nav loading the /game page with an empty board (emptying the current one)
        //but it doesn't reset the "na tahu" and doesn't hide the victory message from last game => Board.svelte handles that using $derived and $effect
        boardKey++; // Force re-render
        
        if (!uuid) {
            // Reset to empty board when no UUID in URL
            resetGame();
            loaded = true;
        } else {
            // Fetch game data when UUID present
            fetchGame(uuid).then(data => {
                gameInfo.apiResponse = data;
                gameInfo.selected = true;
                loaded = true;
            });
        }
    });
</script>
<!-- 
Drawing conditionallly to avoid "TypeError: Cannot read properties of undefined (reading 'name')"
when apiResponse is undefined, and I'm reading name propety here -->
{#if loaded}
    {#if gameInfo.apiResponse.name}
        <h1>{gameInfo.apiResponse.name}</h1>
    {:else}
        <h1>Piškvorky</h1>
    {/if}

    <!-- TODO: pridat tlacitko ulozit (z prazdnych piskvorek do ulohy (je to v treti fazi)) -->

    {#if gameInfo.selected}
    <Board boardApiInfo={gameInfo.apiResponse}></Board>
    {/if}
{/if}
<script>
    import { gameInfo, resetGame } from "$lib/shared.svelte";
    import Board from "$lib/Board.svelte";
    import { onMount } from 'svelte';
    import { page } from '$app/stores';

    async function fetchGame(uuid) {
        const request = await fetch('https://odevzdavani.tourdeapp.cz/mockbush/api/v1/games/' + uuid);
        const data = await request.json();
        return data;
    }

    let boardKey = 0;

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
        } else {
            // Fetch game data when UUID present
            fetchGame(uuid).then(data => {
                gameInfo.apiResponse = data;
                gameInfo.selected = true;
            });
        }
    });

    //Not using this for now (it could speed up the navigation from the game picker a bit, since stuff from it is loaded already)
    //But is seems like its fast enough already (plus this does't react to the UUID in the URL changes right (without destroying the component and making a new one))
    //https://www.okupter.com/blog/sveltekit-window-is-not-defined => using onMount
    // onMount(async () => {
    //     let adress = window.location.href;
    //     if(!adress.endsWith("/game")){
    //         let uuid = adress.split("/").pop();
    //         // if(!(uuid in gameInfo.apiResponse)){ //upravit ten filtr
    //         //     fetchGame(uuid);
    //         // }
    //         gameInfo.apiResponse = await fetchGame(uuid);
    //         console.log($state.snapshot(gameInfo.apiResponse));
    //     }else{
    //         gameInfo.apiResponse = {};
    //         gameInfo.apiResponse.board = Array(15).fill().map(() => Array(15).fill("")); //2D array of "" 15x15
    //         gameInfo.selected = true;
    //     }
    // });
</script>

{#if gameInfo.apiResponse.name}
    <h1>{gameInfo.apiResponse.name}</h1>
{:else}
    <h1>Piškvorky</h1>
{/if}

<!-- TODO: pridat tlacitko ulozit (z prazdnych piskvorek do ulohy (je to v treti fazi)) -->

{#if gameInfo.selected}
<Board boardApiInfo={gameInfo.apiResponse}></Board>
{/if}

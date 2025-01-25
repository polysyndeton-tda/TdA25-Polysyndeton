<script>
    import { gameInfo, resetGame, fetchGame, editPuzzle, difficultyMapToEN, difficultyMapToCZ, wait } from "$lib/shared.svelte";
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import BoardEditor from "$lib/BoardEditor.svelte";
    import { PUBLIC_API_BASE_URL } from '$env/static/public';
    import Toast from "$lib/Toast.svelte";
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

    let saved = $state(false);
    async function saveChangesGUI(){
        const requestInfo = await editPuzzle($page.params.uuid);
        if(requestInfo.ok){
            saved = true;
            await wait(2000);
            saved = false;
        }
    }
</script>

{#if gameInfo.selected}
    <div class="toolbar">
        <input type="text" bind:value={gameInfo.apiResponse.name}>
        <select bind:value={() => difficultyMapToCZ[gameInfo.apiResponse.difficulty], /*get*/
                            (v) => gameInfo.apiResponse.difficulty = difficultyMapToEN[v] /*set*/}> 
            <!-- class="o" is a workaround for: https://stackoverflow.com/questions/4672960/change-css-font-family-for-separate-options-in-select-tag -->
            <option class="o">začátečník</option>
            <option class="o">jednoduchá</option>
            <option class="o">pokročilá</option>
            <option class="o">těžká</option>
            <option class="o">nejtěžší</option>
        </select>
        <button onclick={saveChangesGUI}>Uložit</button>
    </div>
    <BoardEditor boardApiInfo={gameInfo.apiResponse}></BoardEditor>
{/if}

{#if errorMessage}
    <h2 class="errorMessage center">{errorMessage}</h2>
{/if}

{#if saved}
    <Toast>Změny uloženy</Toast>
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

    select{
        font-size: 2rem;
        font-family: 'Dosis';
    }
    .o{
        font-family: 'Dosis';
    }
    .errorMessage{
        /* For \n in the error message to be rendered in HTML*/
        white-space: pre-wrap;
    }
</style>
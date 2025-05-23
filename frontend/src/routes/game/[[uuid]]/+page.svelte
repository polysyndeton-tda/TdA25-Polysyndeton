<script>
    import { gameInfo, resetGame, fetchGame, editPuzzle, wait } from "$lib/shared.svelte.ts";
    import Board from "$lib/Board.svelte";
    import { untrack } from 'svelte';
    import { page } from '$app/stores';
    import { PUBLIC_API_BASE_URL } from '$env/static/public';
    import SaveAsDialog from "$lib/SaveAsDialog.svelte";
    import { goto } from '$app/navigation';
    import Toast from "$lib/Toast.svelte";
    const api_url = PUBLIC_API_BASE_URL || 'https://odevzdavani.tourdeapp.cz/mockbush/api/v1/';
    
    let dialogState = $state({
        show: false,
        OKCallback: undefined //an async function
    });

    function openSaveAsDialog(callback){
        dialogState.show = true;
        dialogState.OKCallback = callback;
    }

    let created = $state(false);
    async function createPuzzle() { //createGameRecord
        if(!$page.params.uuid){ //on /game, creating a new game
            const request = await fetch(`${api_url}/games`, 
                {
                    method: "POST",
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
            if(request.ok){
                goto(`/game/${data.uuid}`);
                created = true;
                await wait(2000);
                created = false;
            }else if(request.status == 422){
                alert("Stav křižků neodpovídá stavu koleček nebo naopak");
            }
        }else{
            throw new Error("You're editing an existing game, use editPuzzle instead");
        }
    }

    let updated = $state(false);
    async function saveChangesGUI(){
        const requestInfo = await editPuzzle($page.params.uuid);
        if(requestInfo.ok){
            updated = true;
            await wait(2000);
            updated = false;
        }
    }
    
    let boardKey = 0;
    let loaded = $state(false);
    let errorMessage = $state("");

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
            console.log("reset to empty board when no uuid in url")
            resetGame();
            loaded = true;
        } else {
            // Fetch game data when UUID present
            untrack(() => {
                console.log("gameInfo is", $state.snapshot(gameInfo));
                if("apiResponse" in gameInfo){ //to avoid reading property of undefined
                    if(gameInfo.apiResponse.uuid == uuid){
                        loaded = true;
                        return;
                    }
                }
                
                fetchGame(uuid).then(data => {
                    console.log("game fetched fresh from server")
                    gameInfo.apiResponse = data;
                    gameInfo.selected = true;
                    loaded = true;
                })
                .catch(err =>{
                    errorMessage = err;
                });
            });
        }
    });
</script>

<!-- 
Drawing conditionallly to avoid "TypeError: Cannot read properties of undefined (reading 'name')"
when apiResponse is undefined, and I'm reading name propety here -->
<div class="center">
{#if loaded}
    <div>
        {#if gameInfo.apiResponse.name}
            <h1>{gameInfo.apiResponse.name}</h1>
        {:else}
            <h1>Piškvorky</h1>
        {/if}

        {#if $page.params.uuid}
            <button onclick={saveChangesGUI}>Uložit změny</button>
        {:else}
            <button onclick={() => openSaveAsDialog(createPuzzle)}>Uložit jako úlohu</button>
        {/if}
    </div>

    {#if gameInfo.selected}
        <Board mode="singleplayer" boardApiInfo={gameInfo.apiResponse}></Board>
    {/if}

{:else if errorMessage}
    <h2 class="errorMessage">{errorMessage}</h2>
{/if}

{#if dialogState.show}
    <SaveAsDialog bind:dialogState></SaveAsDialog>
{/if}

{#if created}
    <Toast>Úloha {gameInfo.apiResponse.name} uložena</Toast>
{/if}
{#if updated}
    <Toast>Změny uloženy</Toast>
{/if}
</div>
<style>
    .errorMessage{
        /* For \n in the error message to be rendered in HTML*/
        white-space: pre-wrap;
    }
</style>
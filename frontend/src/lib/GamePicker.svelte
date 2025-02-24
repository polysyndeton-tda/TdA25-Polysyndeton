<script lang="ts">
    import { gameInfo, deletePuzzle, gameStateToCZ, wait } from "$lib/shared.svelte.ts";
    import type { GamesGetApiResponse } from "$lib/shared.svelte";
    import { PUBLIC_API_BASE_URL } from '$env/static/public';
    import { onMount } from "svelte";
    import BoardPreview from "./BoardPreview.svelte";
    import Filter from "./Filter.svelte";
    import Toast from "./Toast.svelte";
    import GameStarRating from "./GameStarRating.svelte";
    import Confirm from "./Confirm.svelte";
    const api_url = PUBLIC_API_BASE_URL || 'https://odevzdavani.tourdeapp.cz/mockbush/api/v1/';

    let items: GamesGetApiResponse[] = $state([]);
    let loaded = $state(false);
    async function fetchAllGames(){
        //all games list
        const request = await fetch(`${api_url}/games`);
        const data: GamesGetApiResponse[] = await request.json();
        console.log(data);
        items = data;
        loaded = true;
    }

    let filterState: any = $state({
       used: false,
       filters: {
            difficulty: ["beginner", "easy", "medium", "hard", "extreme"], //list of difficulty value
            name: "",       //a name of one board
            date_filter: "" //"24h", "7d", "1m", "3m"
       } 
    });

    async function fetchAllGamesFiltered(parametr: any){
        const params = new URLSearchParams(filterState.filters);
        const response = await fetch(`${api_url}/filter?${params.toString()}`);
        const games = await response.json();
        items = games;
    }

    $effect(() => {
        //the filterState parameter here is only to make sure the effect runs when filterState changes
        fetchAllGamesFiltered(filterState);
    });

    onMount(fetchAllGames);
    type deletedPuzzleType = {
        confirmed: boolean,
        showDialog: boolean,
        game: GamesGetApiResponse
    }
    let deletedPuzzle: deletedPuzzleType = $state({
        confirmed: false,
        showDialog: false,
        game: {} as GamesGetApiResponse // as GamesGetApiResponse until I make better typed initialisation code (game sure is assigned before accessing in the "Smazat" button callback with `deletedPuzzle.game = game;` ) 
    });

    async function deletePuzzleFromGui(game: GamesGetApiResponse, uuid: string){
        let deleted = await deletePuzzle(uuid);
        if(deleted){
            deletedPuzzle.confirmed = true;
            console.log($state.snapshot(items));
            items = items.filter(t => t !== game);
            console.log($state.snapshot(items));
            wait(2600).then(()=> deletedPuzzle.confirmed = false);
        }
    }

    function setGameInfoForInstantLoad(index: number){
        console.log("entrar")
        gameInfo.apiResponse = items[index];
        gameInfo.selected = true;
    }

</script>

{#if loaded}
    <Filter bind:filterState ></Filter>
    <div class="all-container">
    <p class="infoFilter">
        Když ve filtru necháte v kategorii výběr prázdný, tak se filtr neaplikuje. 
        Tedy nechcete-li filtrovat podle obtížnosti, můžete vybrat buď všechny kategorie nebo žádnou.
        Nechcete-li filtrovat podle názvu, nechte políčko prázdné.
    </p>
    <br>
    {#if items.length == 0}
        {#if filterState.used}
            <p>Vaším filtrům neodpovídá žádná úloha</p>
        {:else}
            <p>Zatím žádné úlohy nebyly vytvořeny</p>
        {/if}
    {:else}
        <div class="games-container">
            {#each items as game, index (game)}
                <a id={"i" + index} href={"/game/"+ items[index].uuid} 
                 onmouseenter={() => setGameInfoForInstantLoad(index)}
                 ontouchstart={() => setGameInfoForInstantLoad(index)}
                 class="button holder" role="button" tabindex="0">
                 
                    <BoardPreview boardApiInfo={game}></BoardPreview>
                    <!-- right column -->
                    <div style="display: flex; justify-content:center;flex-grow: 1;width: 30vw;max-width: 225px;">
                    <div class="center">
                        <!-- href={"/game/"+ items[index].uuid} -->
                        <p class="btnlink title">{game.name}</p>
                        <GameStarRating difficulty={game.difficulty}/>
                        <p class="btnlink">Stav: {gameStateToCZ[game.gameState]}</p>
                        <hr>
                        <button class="button hasOwnClickHandler" 

                            ontouchstart={(e) => {
                                // as HTMLAnchorElement tells Typescript we are absolutely sure the element is there on the page
                                (document.getElementById("i" + index) as HTMLAnchorElement).href = "/editor/" + items[index].uuid;
                            }
                            }

                            ontouchend={(e) => {
                                (document.getElementById("i" + index) as HTMLAnchorElement).href = "/game/" + items[index].uuid;
                            }}

                            onmouseenter={(e)=> {
                                (document.getElementById("i" + index) as HTMLAnchorElement).href = "/editor/" + items[index].uuid;
                            }
                            }
                            onmouseleave={(e) => {
                                (document.getElementById("i" + index) as HTMLAnchorElement).href = "/game/" + items[index].uuid;
                            }
                            }
                            onmousedowncapture={(e) => {
                                e.preventDefault();
                                console.log(event.which);
                            }}

                            onkeydown={(e) => {
                                e.preventDefault();
                                if(e.key == "Enter"){
                                    (document.getElementById("i" + index) as HTMLAnchorElement).href = "/editor/" + items[index].uuid;
                                    (document.getElementById("i" + index) as HTMLAnchorElement).click();
                                }
                            
                        }}>Upravit</button>
                        <button class="hasOwnClickHandler" onclick={(e) => {
                            e.preventDefault(); //prevents from sending us to /game
                            deletedPuzzle.game = game;
                            deletedPuzzle.showDialog = true;
                        }}>Smazat</button>  
                    </div>
                    </div>
                </a>
            {/each}
        </div>
    {/if}
    </div>
{/if}

{#if deletedPuzzle.confirmed}
    <Toast>Úloha {deletedPuzzle.game.name} smazána</Toast>
{/if}

{#if deletedPuzzle.showDialog}
    <Confirm bind:show={deletedPuzzle.showDialog} 
    okCallback={() => deletePuzzleFromGui(deletedPuzzle.game, deletedPuzzle.game.uuid)}>Smazat úlohu "{deletedPuzzle.game.name}"?</Confirm>
{/if}

<style>
.all-container {
    display: flex;
    flex-direction: column;
    align-items: center;
}
.infoFilter{
    max-width: 500px;
    padding: 0 10px;
}
.button{
    display: block;
    border-radius: 8px;
    border: 1px solid transparent;
    padding: 0.6em 1.2em;
    font-size: 1.2rem;
    font-weight: 535;
    font-family: inherit;
    cursor: pointer;
    transition: border-color 0.25s;
    text-decoration: none;
    background-color: #f6f6f6;
    color: black;
}

.holder{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
}

.holder p{
    margin: 0;
}

.holder button{
    width: 100%;    
}

.btnlink{
    text-decoration: none;
    color: black;
    font-size: 1.2rem;
    letter-spacing: 0.5px;
}

.title{
    font-weight: bold;
    font-size: 1.3rem;
    text-decoration: underline;
    overflow-wrap: anywhere; /*For really long words => to avoid overflow (normally names are broken at spaces)*/
}

.button:hover {
  border-color: #0070BB; /*#646cff;*/ /*#535bf2;*/
}
.button:focus,
.button:focus-visible {
  outline: 4px auto -webkit-focus-ring-color;
}
.games-container{
    display: flex;
    flex-direction: column;
    gap: 5px;
    max-width: 100vw;
}

@media (prefers-color-scheme: dark) {
    .button {
        background-color: #1a1a1a;
        color: white;
    }
    .btnlink{
        color: white;
    }
}
</style>

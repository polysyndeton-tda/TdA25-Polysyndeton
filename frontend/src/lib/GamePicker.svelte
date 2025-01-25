<script>
    import { gameInfo, deletePuzzle, difficultyMapToCZ, difficultyMapToNumber, gameStateToCZ } from "./shared.svelte.js";
    import { PUBLIC_API_BASE_URL } from '$env/static/public';
    import { onMount } from "svelte";
    import BoardPreview from "./BoardPreview.svelte";
    import StarRating from 'svelte-star-rating';
    import Filter from "./Filter.svelte";
    import Toast from "./Toast.svelte";
    const api_url = PUBLIC_API_BASE_URL || 'https://odevzdavani.tourdeapp.cz/mockbush/api/v1/';

    const config = {
        emptyColor: 'hsl(240, 80%, 85%)',
        fullColor:  '#E31837',
        showText: false,
        size: 22,
    };
    const style = 'justify-content:center;padding: 10px 0 0 10px;'; //border: 1px solid firebrick;padding: 12px;';

    let items = $state([]);
    let loaded = $state(false);
    async function fetchAllGames(){
        //all games list
        const request = await fetch(`${api_url}/games`);
        const data = await request.json();
        console.log(data);
        items = data;
        loaded = true;
    }

    let filterState = $state({
       used: false,
       filters: {
            difficulty: ["beginner", "easy", "medium", "hard", "extreme"], //list of difficulty value
            name: "",       //a name of one board
            date_filter: "" //"24h", "7d", "1m", "3m"
       } 
    });

    async function fetchAllGamesFiltered(){
        const params = new URLSearchParams(filterState.filters);
        const response = await fetch(`${api_url}/filter?${params.toString()}`);
        const games = await response.json();
        items = games;
    }

    $effect(() => {
        fetchAllGamesFiltered(filterState);
    });

    onMount(fetchAllGames);

    function wait(ms) {
        if(ms > 0){
            return new Promise((resolve, reject) => {
                setTimeout(() => {
                    resolve(ms)
                }, ms )
            });
        }else{
			return;
		}
    }

    let confirmPuzzleDeleted = $state(false);
    let puzzleDeletedName = $state("");

    async function deletePuzzleFromGui(game, uuid){
        let deleted = await deletePuzzle(uuid);
        if(deleted){
            confirmPuzzleDeleted = true;
            puzzleDeletedName = game.name;
            console.log($state.snapshot(items));
            items = items.filter(t => t !== game);
            console.log($state.snapshot(items));
            wait(2600).then(()=> confirmPuzzleDeleted = false);
        }
    }

</script>

{#if loaded}
    <Filter bind:filterState ></Filter>

    <p class="infoFilter">
        Když ve filtru necháte v kategorii výběr prázdný, tak se filtr neaplikuje. 
        Tedy nechcete-li filtrovat podle obtížnosti, můžete vybrat buď všechny kategorie nebo žádnou.
        Nechcete-li filtrovat podle názvu, nechte políčko prázdné.
    </p>
    <br>
    {#if items.length == 0}
        <p>Zatím žádné úlohy nebyly vytvořeny</p>
    {:else}
        <div class="games-container">
            {#each items as game, index (game)}
                <a id={"i" + index} href={"/game/"+ items[index].uuid} class="button holder" role="button" tabindex="0">
                    <BoardPreview boardApiInfo={game}></BoardPreview>
                    <div style="display: flex; justify-content:center;flex-grow: 1;">
                    <div class="center">
                        <!-- href={"/game/"+ items[index].uuid} -->
                        <p class="btnlink title" onclick={ 
                            () => {
                                gameInfo.apiResponse = items[index];
                                gameInfo.selected = true;
                            }
                        }>{game.name}
                        </p>
                        <!-- instead of this, show a star<p class="btnlink">{difficultyMapToCZ[game.difficulty]}</p> -->
                        <div title={difficultyMapToCZ[game.difficulty]}><StarRating rating={difficultyMapToNumber[game.difficulty]} {config} {style} /></div>
                        <p class="btnlink">Stav: {gameStateToCZ[game.gameState]}</p>
                        <hr>
                        <button class="button hasOwnClickHandler" 

                            ontouchstart={(e) => {
                                document.getElementById("i" + index).href = "/editor/" + items[index].uuid;
                            }
                            }

                            ontouchend={(e) => {
                                document.getElementById("i" + index).href = "/game/" + items[index].uuid;
                            }}

                            onmouseenter={(e)=> {
                                document.getElementById("i" + index).href = "/editor/" + items[index].uuid;
                            }
                            }
                            onmouseleave={(e) => {
                                 document.getElementById("i" + index).href = "/game/" + items[index].uuid;
                            }
                            }
                            onmousedowncapture={(e) => {
                                e.preventDefault();
                                console.log(event.which);
                            }}

                            onkeydown={(e) => {
                                e.preventDefault();
                                if(e.key == "Enter"){
                                    document.getElementById("i" + index).href = "/editor/" + items[index].uuid;
                                    document.getElementById("i" + index).click();
                                }
                            
                        }}>Upravit</button>
                        <button class="hasOwnClickHandler" onclick={(e) => {
                            e.preventDefault(); //prevents from sending us to /game
                            deletePuzzleFromGui(game, game.uuid);
                        }}>Smazat</button>  
                    </div>
                    </div>
                </a>
            {/each}
        </div>
    {/if}
{/if}

{#if confirmPuzzleDeleted}
    <Toast>Úloha {puzzleDeletedName} smazána</Toast>
{/if}


<style>
.infoFilter{
    max-width: 500px;
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

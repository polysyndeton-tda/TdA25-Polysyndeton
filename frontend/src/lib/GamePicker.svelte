<script>
    import { gameInfo, deletePuzzle, difficultyMapToCZ, difficultyMapToNumber, gameStateToCZ } from "./shared.svelte.js";
    import { PUBLIC_API_BASE_URL } from '$env/static/public';
    import { onMount } from "svelte";
    import { goto } from '$app/navigation';
    import BoardPreview from "./BoardPreview.svelte";
    import StarRating from 'svelte-star-rating';
    import { eventNames } from "process";

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
        const api_url = PUBLIC_API_BASE_URL || 'https://odevzdavani.tourdeapp.cz/mockbush/api/v1/';
        const request = await fetch(`${api_url}/games`);
        const data = await request.json();
        console.log(data);
        items = data;
        loaded = true;
    }

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

    function navigateToGame(event, path, index){
        event.preventDefault();
        //needed to filter out events, so that the "Upravit" and "Smazat" buttons work (instead of sending us to /game)
        // if(event.target.classList.contains("hasOwnClickHandler")){
        //     event.preventDefault();
        //     return false;
        // } 
    }

    function buttonShield(event){
        event.preventDefault(); 
    }

</script>

{#if loaded}
    {#if items.length == 0}
        <p>Zatím žádné úlohy nebyly vytvořeny</p>
    {:else}
        <div class="games-container">
            {#each items as game, index (game)}
                <a id={"i" + index} href={"/game/"+ items[index].uuid} class="button holder" role="button" tabindex="0">
                    <BoardPreview boardApiInfo={game}></BoardPreview>
                    <div style="display: flex; justify-content:center;flex-grow: 1;">
                    <div>
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
    <div id="snackbar" class="show">Úloha {puzzleDeletedName} smazána</div>
{/if}


<style>
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


/* The snackbar - position it at the bottom and in the middle of the screen */
#snackbar {
  visibility: hidden; /* Hidden by default. Visible on click */
  min-width: 250px; /* Set a default minimum width */
  margin-left: -125px; /* Divide value of min-width by 2 */
  background-color: #333; /* Black background color */
  color: #fff; /* White text color */
  text-align: center; /* Centered text */
  border-radius: 2px; /* Rounded borders */
  padding: 16px; /* Padding */
  position: fixed; /* Sit on top of the screen */
  z-index: 1; /* Add a z-index if needed */
  left: 50%; /* Center the snackbar */
  bottom: 30px; /* 30px from the bottom */
}

/* Show the snackbar when clicking on a button (class added with JavaScript) */
#snackbar.show {
  visibility: visible; /* Show the snackbar */
  /* Add animation: Take 0.5 seconds to fade in and out the snackbar.
  However, delay the fade out process for 2.5 seconds */
  /* -webkit-animation: fadein 0.5s, fadeout 0.5s 2.5s; */
  animation: fadein 0.5s, fadeout 0.5s 2.5s;
}

/* Animations to fade the snackbar in and out */
@-webkit-keyframes fadein {
  from {bottom: 0; opacity: 0;}
  to {bottom: 30px; opacity: 1;}
}

@keyframes fadein {
  from {bottom: 0; opacity: 0;}
  to {bottom: 30px; opacity: 1;}
}

@-webkit-keyframes fadeout {
  from {bottom: 30px; opacity: 1;}
  to {bottom: 0; opacity: 0;}
}

@keyframes fadeout {
  from {bottom: 30px; opacity: 1;}
  to {bottom: 0; opacity: 0;}
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


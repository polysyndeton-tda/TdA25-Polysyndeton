<script>
    import { gameInfo, deletePuzzle } from "./shared.svelte.js";
    import { PUBLIC_API_BASE_URL } from '$env/static/public';
    import { onMount } from "svelte";

    let items = $state([]);
    let loaded = $state(false);
    async function fetchAllGames(){
        //all games list
        const api_url = PUBLIC_API_BASE_URL || 'https://odevzdavani.tourdeapp.cz/mockbush/api/v1/';
        const request = await fetch(`${api_url}/games`);
        const data = await request.json();
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

</script>

{#if loaded}
    {#if items.length == 0}
        <p>Zatím žádné úlohy nebyly vytvořeny</p>
    {:else}
        <div class="games-container">
            {#each items as game, index (game)}
                <span class="button holder">
                    <a class="btnlink" href={"./game/"+ items[index].uuid} onclick={
                        () => {
                            //JS won't let me do a gameInfo = items[index] assignment, as a gameInfo import is const 
                            gameInfo.apiResponse = items[index];
                            gameInfo.selected = true;
                        }
                    }
                    >
                    {game.name}
                    </a>
                    <a class="button" href={"./editor/" + items[index].uuid}>Edit</a>
                    <button onclick={() => {
                        deletePuzzleFromGui(game, game.uuid);
                    }}>Delete</button>
                </span>
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
}

.btnlink{
    text-decoration: none;
    color: black;
    font-size: 1.2rem;
    letter-spacing: 0.5px;
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


<script>
    import {gameInfo} from "./shared.svelte.js";
    async function fetchAllGames(){
        //all games list
        const request = await fetch('https://odevzdavani.tourdeapp.cz/mockbush/api/v1/games/');
        const data = await request.json();
        console.log(data);
        return data;
    }
  
</script>
  
{#await fetchAllGames()}
    <p>loading</p>
{:then items}
    <div class="games-container">
        {#each items as game, index}
            <button onclick={
                () => {
                    //JS won't let me do a gameInfo = items[index] assignment, as a gameInfo import is const 
                    gameInfo.apiResponse = items[index];
                    gameInfo.selected = true;
                    // gameInfo.selectedGameId = game.uuid;
                }
            }
            >
            {game.name}
            </button>
        {/each}
    </div>
{:catch error}
<p style="color: red">{error.message}</p>
{/await}


<style>
button{
    display: block;
}
.games-container{
    display: flex;
    flex-direction: column;
    gap: 5px;
}
</style>
<script>
    import { gameInfo } from "./shared.svelte.js";
    import { PUBLIC_API_BASE_URL } from '$env/static/public';
    async function fetchAllGames(){
        //all games list
        const api_url = PUBLIC_API_BASE_URL || 'https://odevzdavani.tourdeapp.cz/mockbush/api/v1/';
        const request = await fetch(`${api_url}/games`);
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
        </span>
        {/each}
    </div>
{:catch error}
<p style="color: red">{error.message}</p>
{/await}


<style>
.button{
    display: block;
    border-radius: 8px;
    border: 1px solid transparent;
    padding: 0.6em 1.2em;
    font-size: 1em;
    font-weight: 500;
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


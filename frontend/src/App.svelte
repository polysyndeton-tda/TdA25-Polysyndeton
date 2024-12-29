<script>
  let selectedGame = $state(false);
  let selectedGameId = $state("");
  async function fetchAllGames(){
    //all games list
    const request = await fetch('https://odevzdavani.tourdeapp.cz/mockbush/api/v1/games/');
    const data = await request.json();
    console.log(data);
    return data;
  }

</script>

<h1>Hello TdA</h1>

<!-- TODO: Find out how to wrap this each block in a div => asi to nejde, treba component -->
{#await fetchAllGames()}
  <p>loading</p>
{:then items}
{#each items as game}
  <button onclick={
    () => {
      selectedGame = true;
      selectedGameId = game.uuid;
    }
  }
  >
  {game.name}
  </button>
{/each}
{:catch error}
<p style="color: red">{error.message}</p>
{/await}


{#if selectedGame}
<p>Selected game {selectedGameId}</p>
{/if}


<style>
  button{
    display: block;
  }
</style>
<!-- <button onclick={main}>Start</button> -->




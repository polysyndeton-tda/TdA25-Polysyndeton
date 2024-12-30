<script>
  import Board from "./Board.svelte";
  import GamePicker from "./GamePicker.svelte";
  import {gameInfo} from "./shared.svelte.js";
  let beginNewGame = false;
</script>

<h1>Hello TdA</h1>

<!-- bylo by nice nakonfigurovat backend aby umel odpovedet na http://server-url.cz/game/{uuid}
      => tam proste staci naservovat taky tuto App.svelte stránku (co bude na /game), s parametrem uuid si poradim a rovnou nactu tu hru
-->
{#if !beginNewGame && !gameInfo.selected}
<h2>Uložené hry</h2>
<GamePicker></GamePicker>
<button onclick={()=> beginNewGame = true}>Začít novou hru</button>
{:else}
<!-- <Board boardApiInfo={gameInfo.apiResponse}></Board> -->
{/if}


{#if gameInfo.selected}
<button onclick={()=>{
  gameInfo.selected = false;
  beginNewGame = false;
}}>Back
</button>

<p>Selected game {gameInfo.apiResponse.uuid}</p>
<Board boardApiInfo={gameInfo.apiResponse}></Board>
{/if}

<script>
  import GamePicker from "./GamePicker.svelte";
  import {gameInfo} from "./shared.svelte.js";

</script>

<h1>Hello TdA</h1>

<GamePicker></GamePicker>

{#if gameInfo.selected}
<p>Selected game {gameInfo.selectedGameId}</p>
{/if}

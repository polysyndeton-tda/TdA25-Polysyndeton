  <script>
    import { gameInfo } from "$lib/shared.svelte";
    let { showDialog, dialogOKCallback } = $props();

    // document.querySelector("input").value = gameInfo.apiResponse.name;
    // document.querySelector("select").value = gameInfo.apiResponse.difficulty;

  </script>
  
  <div class="popup-container">
        <div class="popup">
            <h2>Save As</h2>
            <div>
                <input type="text" value={gameInfo.apiResponse.name}>
                <select value={gameInfo.apiResponse.difficulty}>
                    <option>beginner</option>
                    <option>easy</option>
                    <option>medium</option>
                    <option>hard</option>
                    <option>extreme</option>
                </select>
            </div>
            <div>
                <button onclick={
                    async () => {
                        /*
                        The gameInfo gets updated only on Save button, making Cancel easy

                        If we used bind:value in <input> and <select>, the values would update automatically 
                        (making undo = cancel here more difficult = previous value would have to be saved in a separate variable), 
                        and the Save button would only send them to the server,
                        */
                        gameInfo.apiResponse.name = document.querySelector("input").value;
                        gameInfo.apiResponse.difficulty = document.querySelector("select").value;
                        //the callback is an async function calling fetch, if await wasn't used we would have got race conditions.
                        await dialogOKCallback();
                    }
                }>OK</button>
                <button onclick={() => showDialog[0] = false}>Cancel</button>
            </div>
        </div>
</div>


<style>
    .popup-container{
        position: fixed;
        top: 0;
        height: 100%;
        width: 100%;
        display: flex;
        inset-inline-start: 0px;
        align-items: center;
        justify-content: center;
    }
    .popup{
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: #242424; 
        background-color: #101010;
        padding: 10px;
        display: flex;
        flex-direction: column;
        gap: 10px;
        border-radius: 8px;
        filter: drop-shadow(0 0 8px var(--menu-item-hover-color));

    }
    .popup > * > * {
        font-size: 1.5rem;
    }
</style>
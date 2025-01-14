  <script>
    import { gameInfo } from "$lib/shared.svelte";
    let { dialogState = $bindable() } = $props();
    function addFocus(node){
        node.select();
    }
  </script>
  
  <div class="popup-container">
        <div class="popup">
            <div class="title">
                <h2>Save As</h2>
                <div>
                    <input type="text" use:addFocus value={gameInfo.apiResponse.name}>
                    <select value={gameInfo.apiResponse.difficulty}>
                        <option>beginner</option>
                        <option>easy</option>
                        <option>medium</option>
                        <option>hard</option>
                        <option>extreme</option>
                    </select>
                </div>
            </div>
            <div>
                <button class="ok" onclick={
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
                        await dialogState.OKCallback();
                    }
                }>OK</button>
                <button onclick={() => dialogState.show = false}>Cancel</button>
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
        padding: 10px;
        display: flex;
        flex-direction: column;
        gap: 10px;
        border-radius: 8px;
        filter: drop-shadow(0 0 8px var(--menu-item-hover-color));

    }
    input, select{
        font-size: 1.5rem;
    }

    @media (prefers-color-scheme: light){
        h2{
            color: white;
        }
        .title{
            background-color: #0257a5;
            border-radius: 8px;
            padding: 10px;
        }
        .popup{
            background: #739bc5; /*#76aeea;*/
            padding: 0 0 10px 0;
            box-shadow: rgba(100, 100, 111, 1) 0px 7px 29px 0px;
        }
    }

    @media (prefers-color-scheme: dark){
        .popup{
            background-color: #101010; /*#242424*/
        }
    }
    /* fix from https://stackoverflow.com/questions/30282921/fixed-pop-up-div-gets-overlapped-by-keyboard */
    @media (max-width: 767px) {
        .popup-container {
            width: 100%;
            top: 10px;
            bottom: 0px;    
            overflow-y: auto;
            max-height: 100%;
        }
    }
</style>
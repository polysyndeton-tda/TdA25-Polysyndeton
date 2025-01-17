  <script>
    import { gameInfo, difficultyMapToEN, difficultyMapToCZ } from "$lib/shared.svelte";
    import { scale } from 'svelte/transition'
    let { dialogState = $bindable() } = $props();

    function addFocus(node){
        node.select();
    }

    async function save(){
    /*
        The gameInfo gets updated only on Save button, making Cancel easy

        If we used bind:value in <input> and <select>, the values would update automatically 
        (making undo = cancel here more difficult = previous value would have to be saved in a separate variable), 
        and the Save button would only send them to the server,
        */
        gameInfo.apiResponse.name = document.querySelector("input").value;
        gameInfo.apiResponse.difficulty = difficultyMapToEN[document.querySelector("select").value];
        //the callback is an async function calling fetch, if await wasn't used we would have got race conditions.
        await dialogState.OKCallback();
    }

    function close(){
        dialogState.show = false;
    }
  </script>
  
  <div in:scale={{ duration: 75}} out:scale={{ duration: 95}} class="popup-container">
        <div class="popup">
            <div class="title">
                <h2>Uložit jako</h2>
                <div class="contentBar">
                    <input type="text" onkeydown={e=> {
                        if(e.key == "Enter") save();
                        else if (e.key == "Escape") close();
                    }} use:addFocus value={gameInfo.apiResponse.name}>
                    <select value={difficultyMapToCZ[gameInfo.apiResponse.difficulty]}>
                        <option>začátečník</option>
                        <option>jednoduchá</option>
                        <option>pokročilá</option>
                        <option>těžká</option>
                        <option>nejtěžší</option>
                    </select>
                </div>
            </div>
            <div>
                <button class="ok" onclick={save}>OK</button>
                <button onclick={close}>Zrušit</button>
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
        display: flex;
        flex-direction: column;
        gap: 10px;
        border-radius: 8px;
        filter: drop-shadow(0 0 8px var(--menu-item-hover-color));
        padding: 0 0 10px 0;
    }
    .title{
        border-radius: 8px;
        padding: 10px;
    }

    .contentBar{
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        justify-content: center;
    }

    input{
        flex-grow: 1;
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
        }
        .popup{
            background: #739bc5; /*#76aeea;*/
            box-shadow: rgba(100, 100, 111, 1) 0px 7px 29px 0px;
        }
    }

    @media (prefers-color-scheme: dark){
        .title{
            background-color: #101010; /*#242424*/
        }
        .popup{
            background-color: #434343;
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
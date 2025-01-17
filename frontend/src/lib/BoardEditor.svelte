<script>
    import {untrack} from 'svelte';
    let { boardApiInfo } = $props();

    let name = $derived(boardApiInfo.name);
    $effect(() => {
        document.title = "Editor - " + name;
    });

    function count(array, item) {
        let count = 0;
        for (let row of array) {
            for (let elem of row) {
                if (item == elem) {
                    count++;
                }
            }
        }
        return count;
    }

    let selectedTool = $state("X");
    let cursorClass = $state("cursor-X");

    let lastMoved = "";
    let naTahu = $state("X");
    let isVictory = $state(false);
    let whoWon = $state("");
    let boardWonAlready = $state(false);

    let boardStatus = $state({
        "O": 0,
        "X": 0,
        "" : 0, //these are not shown
        "eraser": 0 //these are not shown, quick hack
    });

    let totalNumberOfMoves = $derived(boardStatus.X + boardStatus.O);

    let statusOK = $derived.by(() => {
        if(boardStatus.X != boardStatus.O && boardStatus.X != (boardStatus.O + 1)){
            if(boardStatus.X > boardStatus.O){
                return {ok: false, message: "Moc křížků!"};
            }else{
                return {ok: false, message: "Moc koleček!"};
            }
        }else{
            return {ok: true, message: "V pořádku"};
        }
    });

    let switchToolToNaTahuAutomatically = $state(false);
    $effect(() => {
        if(totalNumberOfMoves % 2 == 0){
            naTahu = "X";
        }else{
            naTahu = "O";
        }
        if(switchToolToNaTahuAutomatically){
            untrack(() => {
                /*If untrack wasn't used, the change of the tool would be blocked after a "Moc křížků!" or "Moc koleček!"
                situation when Přepínat se střídáním tahů (kromě gumy) is selected*/
                if(selectedTool != ""){
                    console.log("automatická změna toolu na " + selectedTool);
                    selectTool(naTahu);
                }
            });
        }
    });

    let uuid = $derived(boardApiInfo.uuid);
    $effect.pre(() => {
        console.log("reset", uuid);
        untrack(() => {
            lastMoved = "";
            naTahu = "X";
            isVictory = false;
            whoWon = "";
            boardWonAlready = false;
            reset();
            // checkIfBoardWonAlready();
        });
    });

    function reset(){
        console.log("co bylo v effectu  z editoru runuje");
        let numberOfCrosses = count(boardApiInfo.board, "X");
        let numberOfNoughts = count(boardApiInfo.board, "O");
        let numberOfMoves = numberOfCrosses + numberOfNoughts;
        boardStatus.X = numberOfCrosses;
        boardStatus.O = numberOfNoughts;
        if (numberOfMoves % 2 == 0) {
            lastMoved = "O";
            naTahu = "X";
        } else {
            lastMoved = "X";
            naTahu = "O";
        }
    }

    function placeItem(rowIndex, columnIndex) {
        let previous = boardApiInfo.board[rowIndex][columnIndex];
        if(previous == ""){
            console.log("empty", selectedTool);
        }else{
            console.log(previous, selectedTool)
        }
       
        if(previous == selectedTool){
            //no need to change counts of anything
        }else{
            boardStatus[previous] -= 1;
            boardStatus[selectedTool] += 1
        }
        boardApiInfo.board[rowIndex][columnIndex] = selectedTool;
        console.log("placeItem", selectedTool);
    }

    $inspect(selectedTool);
    $inspect(boardApiInfo);

    function selectTool(tool) {
        if(tool == "eraser"){
            selectedTool = "";
        }else{
            selectedTool = tool;
        }
        cursorClass = "cursor-" + tool;
    }
</script>

<div class="toolbar">
    <button aria-label="X tool" class="player X" class:selected={selectedTool === "X"}  onclick={() => selectTool("X")}>X</button>
    <button aria-label="O tool" class="player O" class:selected={selectedTool === "O"}  onclick={() => selectTool("O")}>O</button>
    <button aria-label="eraser tool" class="player eraser" class:selected={selectedTool === ""} onclick={() => selectTool("eraser")}>E</button> <!-- Eraser icon created by Hexagon075 - Flaticon -->
    <label><input type="checkbox" bind:checked={switchToolToNaTahuAutomatically}>Přepínat se střídáním tahů (kromě gumy)</label> <!-- Přepínat nástroj se střídáním tahů -->
</div>

<div class="gridContainer">
    <div class="grid {cursorClass}">
        {#each boardApiInfo.board as row, rowIndex}
            <div class="row">
                {#each row as field, columnIndex}
                    <div class="field {field}" role="button" tabindex="0" onclick={() => placeItem(rowIndex, columnIndex)}></div>
                {/each}
            </div>
        {/each}
    </div>
    <div class="boardStatusInfo">
        <div class="placedSymbolsInfo">
            <span>Umístěno: </span>
            <span><span class="player X">X</span>: {boardStatus.X}</span>
            <span><span class="player O">O</span>: {boardStatus.O}</span>
        </div>
        {#if statusOK.ok}
            <p>✅ {statusOK.message}</p>
        {:else}
            <p>❌ {statusOK.message}</p>
        {/if}
    </div>
</div>

<div class="center">
{#if !statusOK.ok}
    <h2 class="status warn">Taková hra nemůže nastat!</h2>
{:else}
    <h2 class="status"><span class="player {naTahu}">{naTahu}</span> na tahu</h2>
{/if}
</div>

<style>
    .status{
        font-size: xx-large;
        margin-top: 0;
    }
    .warn{
        text-decoration: 3px solid #e31837 underline;
    }
    p{
        /*For some reason needed for the ❌ in ❌ {statusOK.message} to render properly on Chromium (else it is black & white) */
        font-family: 'Dosis';
    }
    .boardStatusInfo{
        display: flex;
        gap: 10px;
        align-items: center;
        justify-content: space-between;
    }
    .boardStatusInfo span{
        font-size: xx-large;
        font-weight: 500;
    }
    .boardStatusInfo p{
        font-size: xx-large;
        font-weight: 535;
    }
    .placedSymbolsInfo{
        display: flex;
        gap: 10px;
    }
    .player{
        color: transparent;
        vertical-align: middle;
        font-size: xx-large;
    }

    .toolbar {
        display: flex;
        gap: 0.5em;
        height: 50px;
        width: fit-content;
        margin: 1rem auto;
    }

    .toolbar button.selected {
        outline: 3px solid #6495ed;
        outline-offset: 2px;
        border-radius: 4px;
    }

    label{
        font-size: 1.2rem;
        font-weight: 500;
        letter-spacing: 0.5px;
    }

    button{
        padding: 0.5em;
        background-size: 75% 75% !important;
    }

    .gridContainer{
        max-width: 500px;
        margin: 0 auto;
    }

    .grid {
        display: flex;
        flex-direction: column;
        gap: 1.5px;
        width: 100%;
        max-width: 500px;
        background: #6495ed80; /*#ffffff26*/
    }

    .grid.cursor-X {
        cursor: url(/X_modre_cursor.svg) 15 15, auto; 
    }
    
    .grid.cursor-O {
        cursor: url(/O_cervene_cursor.svg)  15 15, auto;
    }
    
    .grid.cursor-eraser {
        cursor: url(/eraser32.png) 10 25, auto;
    }

    .row {
        display: flex;
        flex-direction: row;
        gap: 1.5px;
    }
    .field {
        aspect-ratio: 1/1;
        width: calc(100% / 15);
        background-color: #F6F6F6;
    }
    .O {
        /*I didn't put the images in the ./static folder because when I did, I got an error: 
        The request url "/home/petr/Documents/tda/sveltekit experiment/my-app/static/X_modre.svg" is outside of Vite serving allow list.*/
        background-image: url(/O_cervene.svg);
        background-size: 85% 85%;
        background-repeat: no-repeat;
        background-position: center;
    }
    .X {
        background-image: url(/X_modre.svg); 
        background-size: 85% 85%;
        background-repeat: no-repeat;
        background-position: center;
    }
    .eraser{
        background-image: url(/eraser.png);
        /* color: #ff69b4; */
        background-size: 85% 85%;
        background-repeat: no-repeat;
        background-position: center;
    }

    @media (prefers-color-scheme: dark) {
       .field{
            background-color: black;
       }
    }
</style>
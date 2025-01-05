<script>
    let { boardApiInfo } = $props();

    let selectedTool = $state("X");
    let cursorClass = $state("cursor-X");


    function placeItem(rowIndex, columnIndex) {
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
    <input type="text" bind:value={boardApiInfo.name}>
    <button>Save</button>
</div>

<div class="toolbar">
    <button aria-label="X tool" class="player X" class:selected={selectedTool === "X"}  onclick={() => selectTool("X")}>X</button>
    <button aria-label="O tool" class="player O" class:selected={selectedTool === "O"}  onclick={() => selectTool("O")}>O</button>
    <button aria-label="eraser tool" class="player eraser" class:selected={selectedTool === ""} onclick={() => selectTool("eraser")}>E</button> <!-- Eraser icon created by Hexagon075 - Flaticon -->
</div>

<div class="grid {cursorClass}">
    {#each boardApiInfo.board as row, rowIndex}
        <div class="row">
            {#each row as field, columnIndex}
                <div class="field {field}" role="button" tabindex="0" onclick={() => placeItem(rowIndex, columnIndex)}></div>
            {/each}
        </div>
    {/each}
</div>


<style>
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

    .toolbar > input{
        padding: 0.5em;
        font-size: 2rem;
        width: 100%;
    }

    button{
        padding: 0.5em;
        background-size: 75% 75% !important;
    }

    .grid {
        display: flex;
        flex-direction: column;
        gap: 1.5px;
        width: 100%;
        max-width: 500px;
        background: #6495ed80; /*#ffffff26*/
        margin: 0 auto;
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
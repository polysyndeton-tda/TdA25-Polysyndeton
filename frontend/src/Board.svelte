<script>
    let { boardApiInfo } = $props();

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

    let lastMoved = ""; //$state(""); 
    let naTahu = $state("X");

    // Computes whose turn is it initially
    //To make it run after every move, it is needed to update lastMoved or naTahu $state variables elsewhere
    //$effect works in a way that it runs once on when the component mounts and then when the $state variables which are read from in its function, change elsewhere
    //If I change lastMoved or naTahu in the $effect function, it will not trigger the effect
    /*If I change let lastMoved = $state(""); declration to let lastMoved = "";, it will not trigger the effect, 
      because it is not a $state variable = not a reactive value = so it being read in if (lastMoved === "") does not cause the effect to run*/
    //The other thing being read inside which changes (on every move) is the boardApiInfo.board $props, but changes to props do not trigger the effect
    //So that is why the effect runs only in the beginning = because the $effect runs on the component's mount and lastMoved doesn't matter because it is not a reactive variable
    
    //In other words:
    // Why boardApiInfo.board updates don't trigger the effect:

    // boardApiInfo is a prop, not a $state variable
    // Changes to object properties (like board) aren't tracked by default
    // Would need $state(boardApiInfo) to track changes to its properties

    /* Why lastMoved would trigger if made reactive:
        - Direct $state variable
        - Read directly in the effect (reading is important for reactivity here = if it only wrote to it (without reading it), it wouldn't trigger the effect)
        - Changes to $state variables are tracked
    */

    //In other words, there is nothing except the component mount that would trigger the effect to run again
    /*
    $effect(() => {
        console.log("effect runuje");
        if (lastMoved === "") {                             // reads non-reactive lastMoved
            let numberOfCrosses = count(boardApiInfo.board, "X");   // reads prop
            let numberOfNoughts = count(boardApiInfo.board, "O");   // reads prop
            let numberOfMoves = numberOfCrosses + numberOfNoughts;
            if (numberOfMoves % 2 == 0) {
                lastMoved = "O";    // writes to non-reactive
                naTahu = "X";       // writes to reactive
            } else {
                lastMoved = "X";    // writes to non-reactive
                naTahu = "O";       // writes to reactive
            }
        }
    });
    */

    $effect(() => {
        console.log("effect runuje");
        // let currentPlayer = naTahu;
        // console.log(currentPlayer);
        if (lastMoved === "") {
            let numberOfCrosses = count(boardApiInfo.board, "X");
            let numberOfNoughts = count(boardApiInfo.board, "O");
            let numberOfMoves = numberOfCrosses + numberOfNoughts;
            if (numberOfMoves % 2 == 0) {
                lastMoved = "O";
                naTahu = "X";
            } else {
                lastMoved = "X";
                naTahu = "O";
            }
        } else {
            // console.log("else", lastMoved);
            // if (lastMoved === "X") {
            //     naTahu = "O";
            // } else {
            //     naTahu = "X";
            // }
        }
    });

    function handleMove(rowIndex, columnIndex) {
        boardApiInfo.board[rowIndex][columnIndex] = naTahu;
        lastMoved = naTahu;
        if (lastMoved === "X") {
            naTahu = "O";
        } else {
            naTahu = "X";
        }
        console.log("handleMove", naTahu);
    }

    $inspect(naTahu);
</script>

<p>{naTahu} na tahu</p>
<div class="grid">
    {#each boardApiInfo.board as row, rowIndex}
        <div class="row">
            {#each row as field, columnIndex}
                {#if field == ""}
                    <div class="field" role="button" onclick={() => handleMove(rowIndex, columnIndex)}></div>
                {:else if field == "X"}
                    <div class="field X"></div>
                {:else if field == "O"}
                    <div class="field O"></div>
                {/if}
            {/each}
        </div>
    {/each}
</div>

<style>
    .grid {
        display: flex;
        flex-direction: column;
        gap: 1.5px;
        width: 100%;
        max-width: 500px;
        background: #6495ed80; /*#ffffff26*/
        margin: 0 auto;
    }
    .row {
        display: flex;
        flex-direction: row;
        gap: 1.5px;
    }
    .field {
        aspect-ratio: 1/1;
        width: calc(100% / 15);
        background: black;
    }
    .O {
        background-image: url(./assets/O_cervene.svg);
        background-size: 85% 85%;
        background-repeat: no-repeat;
        background-position: center;
    }
    .X {
        background-image: url(./assets/X_modre.svg);
        background-size: 85% 85%;
        background-repeat: no-repeat;
        background-position: center;
    }
</style>
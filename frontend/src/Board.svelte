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

    let lastMoved = "";
    let naTahu = $state("X");

    //There is nothing except the component mount that would trigger the effect to run again => it runs once
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
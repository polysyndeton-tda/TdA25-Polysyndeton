<script>
    let {boardApiInfo} = $props();

    function count(array, item){
        let count = 0;
        // console.log($state.snapshot(row), item);
        for(let row of array){
            for(let elem of row){
                if(item == elem){
                    count++
                }
            }
        }
        return count;
    }

    let lastMoved = ""; // $state("");
    let naTahu = $derived.by(() =>{
        console.log("lastMoved", lastMoved)
        //when we don't know the last move, scan it in O(N)
        let numberOfCrosses = count(boardApiInfo.board, "X");
        let numberOfNoughts = count(boardApiInfo.board, "O"); //nought je anglicky kolecko :D
        let numberOfMoves = numberOfCrosses + numberOfNoughts;
        console.log("num moves", numberOfMoves);
        if(numberOfMoves % 2 == 0){
            lastMoved = "X";
            return "X";
        }else{
            lastMoved = "O";
            return "O";
        }
    });

    $inspect(naTahu);

</script>

<p>{naTahu} na tahu</p>
<div class="grid">
{#each boardApiInfo.board as row, rowIndex}
    <div class="row">
        {#each row as field, columnIndex }
            {#if field == ""}
                <div class="field" role="button" onclick={() => {
                    boardApiInfo.board[rowIndex][columnIndex] = naTahu;
                    console.log(naTahu);
                }} ></div>
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
    .grid{
        display: flex;
        flex-direction: column;
        gap: 1.5px;
        width: 100%;
        max-width: 500px;
        background: #6495ed80; /*#ffffff26*/
        margin: 0 auto;
    }
    .row{
        display: flex;
        flex-direction: row;
        gap: 1.5px;
    }
    .field{
        aspect-ratio: 1/1;
        width: calc(100% / 15);
        background: black;
    }
    .O{
        background-image: url(./assets/O_cervene.svg);
        background-size: 85% 85%;
        background-repeat: no-repeat;
        background-position: center; 
    }
    .X{
        background-image: url(./assets/X_modre.svg);
        background-size: 85% 85%;
        background-repeat: no-repeat;
        background-position: center; 
    }
</style>
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

    console.log("co bylo v effectu runuje");
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

    function checkVictory(rowIndex, columnIndex) {
        /*Checks if latest move on rowIndex, columnIndex is a winning one
        (made to be called from handleMove)
        */

        // board[0,0] is the north-west corner
        let matchedInDirection = {'n': 0, 'ne': 0, 'e': 0, 'se': 0, 's': 0, 'sw': 0, 'w': 0, 'nw': 0};

        //Checks in which directions out of directionsToLookAt, there are squares of the player who played this move
        //With every iteration, the directionsToLookAt for the next iteration
        //stays the same or gets smaller, depending on if there are relevant squares in that distance from (rowIndex, columnIndex)
        //All relevant square matches are put into matchedInDirection
        //To evaluate victory, values in opposite directions are added up
        //For victory of 5 items in a row, 4 items need to be found around
        let directionsToLookAt = new Set(['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']);
        for(let dist = 1; dist <= 4; dist++){
            let allPossiblePositions = {
                "n":    [rowIndex - dist, columnIndex, "n"],
                "ne":   [rowIndex - dist, columnIndex + dist, "ne"],
                "e":    [rowIndex, columnIndex + dist, "e"],
                "se":   [rowIndex + dist, columnIndex + dist, "se"],
                "s":    [rowIndex + dist, columnIndex, "s"],
                "sw":   [rowIndex + dist, columnIndex - dist, "sw"],
                "w":    [rowIndex, columnIndex - dist, "w"],
                "nw":   [rowIndex - dist, columnIndex -dist, "nw"]
            };

            //.keys() returns an iterator, which should have worked (and be lazily evaluated?) => for now a destructuring operator works
            let squaresInDirectionsToLookAt = [...directionsToLookAt.keys()].map((value) => {
                let [x,y, direction] = allPossiblePositions[value];
                /*  bounds checking is indeed necessary because if out of bounds the value is undefined 
                        => that can throw Uncaught TypeError: Cannot read properties of undefined (reading '2') 
                            when x is out bounds and y is 2 */
                if(0 <= x && x < 15 && 0 <= y && y < 15){
                    //when I don't return this, undefined is returned
                    return [boardApiInfo.board[x][y], direction];
                }
            });
           
            //squares of the same player who made this move
            let relevantSquares = squaresInDirectionsToLookAt.filter(e => {
                if(e == undefined) return false;
                let [value, direction] = e;
                if(value == naTahu) return true;
            });

            let relevantDirections = relevantSquares.map(e=> e[1]);
            directionsToLookAt = new Set(relevantDirections);

            relevantDirections.forEach((value)=> {
                matchedInDirection[value]++;
            });
        }
        console.log("result matchedInDirection", Object.entries(matchedInDirection));
        let lengths = [
            matchedInDirection["s"] + matchedInDirection["n"],
            matchedInDirection["ne"] + matchedInDirection["sw"],
            matchedInDirection["e"] + matchedInDirection["w"],
            matchedInDirection["se"] + matchedInDirection["nw"]
        ];
        console.log("is victory", lengths.some(v => v >= 4)); //vyhra muze byt >= 5 v rade (tedy jsme vedle tohoto tahu nasli alespon 4 pole s nim v lajne)
        return lengths.some(v => v >= 4);
    }

    let isVictory = $state(false);

    function handleMove(rowIndex, columnIndex) {
        if(isVictory){
            return;
        }
        boardApiInfo.board[rowIndex][columnIndex] = naTahu;
        lastMoved = naTahu;

        if (checkVictory(rowIndex, columnIndex, naTahu)) {
            console.log(`${naTahu} wins!`);
            isVictory = true;
            return;
        }
        if (lastMoved === "X") {
            naTahu = "O";
        } else {
            naTahu = "X";
        }
        console.log("handleMove", naTahu);
    }

    $inspect(naTahu);
</script>

<h2><span class="player {naTahu}">{naTahu}</span> na tahu</h2>
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

{#if isVictory}
    <h2 class="toast">Hráč <span class="player {naTahu}">{naTahu}</span> vyhrál!</h2>
{/if}

<style>
    .player{
        color: transparent;
        vertical-align: middle;
        font-size: xx-large;
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

    @media (prefers-color-scheme: dark) {
       .field{
            background-color: black;
       }
    }
</style>
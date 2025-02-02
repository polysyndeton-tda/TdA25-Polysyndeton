<script>
    import {untrack} from 'svelte';
    let { boardApiInfo } = $props();

    let name = $derived(boardApiInfo.name);
    $effect(() => {
        document.title = "Hra - " + name;
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

    let lastMoved = "";
    let naTahu = $state("X");
    let isVictory = $state(false);
    let whoWon = $state("");
    let boardWonAlready = $state(false);

    let uuid = $derived(boardApiInfo.uuid); //$page.params.uuid; doesn't work here
    $effect.pre(() => {
        console.log("board state reset due uuid changing", uuid);
        untrack(() => {
            lastMoved = "";
            naTahu = "X";
            isVictory = false;
            whoWon = "";
            boardWonAlready = false;
            reset();
            checkIfBoardWonAlready();
        });
    });
        
    
    function reset(){
        console.log("co bylo v effectu runuje");
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

    //a O(N) function to check if the game is already won (as in boards 86a55480-72b4-4302-a0ad-dba4b8409635 and ace938ba-ee31-485a-b58f-e1b397fa83ee on https://odevzdavani.tourdeapp.cz/mockbush/api/v1/games/)
    function checkIfBoardWonAlready(){
        for(let i = 0; i < 15; i++){
            for(let j = 0; j < 15; j++){
                let square = boardApiInfo.board[i][j];
                if(square == "X" || square == "O"){
                    if(checkVictory(i,j, square)){
                        boardWonAlready = true;
                        isVictory = true;
                        return;
                    }
                }
            }
        }
    }

    // quick O(1) function to check if the latest move is a winning one
    function checkVictory(rowIndex, columnIndex, player) {
        /*Checks if latest move on rowIndex, columnIndex is a winning one
        (made to be called from handleMove)
        */
        if(boardApiInfo.board[rowIndex][columnIndex] != player){
            return false;
        }

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
                if(value == player) return true;
            });

            let relevantDirections = relevantSquares.map(e=> e[1]);
            directionsToLookAt = new Set(relevantDirections);

            relevantDirections.forEach((value)=> {
                matchedInDirection[value]++;
            });
        }
        // console.log("result matchedInDirection", Object.entries(matchedInDirection));
        let lengths = [
            matchedInDirection["s"] + matchedInDirection["n"],
            matchedInDirection["ne"] + matchedInDirection["sw"],
            matchedInDirection["e"] + matchedInDirection["w"],
            matchedInDirection["se"] + matchedInDirection["nw"]
        ];
        let hasWon = lengths.some(v => v >= 4); //vyhra muze byt >= 5 v rade (tedy jsme vedle tohoto tahu nasli alespon 4 pole s nim v lajne)
        if(hasWon){
            whoWon = player; //for checkIfBoardWonAlready
        }
        return hasWon;
    }

    /* since a placed move is not overwritable here (as opposed to the editor),
    we only have to store a list of moves' coordinates and the value set (not the previous value) */
    let movesHistory = [];
    let moveIndex = $state(-1);

    function otherPlayer(player){
        if(moveIndex == -1){
            return "X";
        }
        if(player == "X"){
            return "O";
        }
        if(player == "O"){
            return "X";
        }
    }

    function undo(){
        const [rowIndex, columnIndex, value] = movesHistory[moveIndex];
        console.log(rowIndex, columnIndex, value);
        naTahu = value;
        boardApiInfo.board[rowIndex][columnIndex] = "";
        moveIndex--;
        isVictory = checkVictory(rowIndex, columnIndex, value);
    }

    function redo(){
        moveIndex++;
        const [rowIndex, columnIndex, value] = movesHistory[moveIndex];
        console.log(rowIndex, columnIndex, value);
        boardApiInfo.board[rowIndex][columnIndex] = value;
        isVictory = checkVictory(rowIndex, columnIndex, value);
        if(isVictory) return;
        naTahu = otherPlayer(value);
    }

    function handleMove(rowIndex, columnIndex) {
        if(-1 < moveIndex && moveIndex < movesHistory.length - 1){
            //the user pressed undo a couple of times, now presses redo, overwriting history of previous moves
            console.log("overwrite")
            movesHistory[moveIndex] = [rowIndex, columnIndex, naTahu];
        }else{
            //no redo possible ==  at the end of the list, new moves are being made
            console.log("new move")
            movesHistory.push([rowIndex, columnIndex, naTahu]);
        }
        
        console.log(movesHistory);
        moveIndex++;

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
<button disabled={moveIndex == -1} onclick={undo}>Undo</button>
<button disabled={moveIndex == movesHistory.length - 1} onclick={redo}>Redo</button>
<p>{moveIndex}</p>
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

{#if isVictory && !boardWonAlready}
    <h2 class="toast">Hráč <span class="player {naTahu}">{naTahu}</span> vyhrál!</h2>
{:else if isVictory && boardWonAlready}
    <h2 class="toast">Dorazila vyřešená úloha, hráč <span class="player {whoWon}">{whoWon}</span> vyhrál!</h2>
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

    @media (prefers-color-scheme: dark) {
       .field{
            background-color: black;
       }
    }
</style>

<!-- <img alt="n" src="{"./favicon.png"}"> -->
<script lang="ts">
    import {untrack} from 'svelte';
    import { updateElo, User, type BoardComponentInfo } from "$lib/shared.svelte";
    type BoardProps = {
        boardApiInfo: BoardComponentInfo,
        mode: "singleplayer" | "multiplayer", 
        allowedPlayer?: "X" | "O" //if mode is multiplayer, which player allow on this client
        onMove?: Function //like an event listener callback when the user makes a move (i.e. to send the move through sockets)
        opponentUsername?: string
    }
    let { boardApiInfo, mode, allowedPlayer, onMove, opponentUsername }: BoardProps = $props();

    //for delivering moves from the other player from api
    export function makeProgrammaticMove(rowIndex: number, columnIndex: number, symbol: "X" | "O"){
        if(mode == "singleplayer"){
            throw Error("Meant to be used on online multiplayer only");
        }
        //If the local user can play, he should, and a move from server cannot be forced
        if(allowedClickOnBoardOnThisClient){
            throw Error("Cannot force a move opponent from server now - the local player hasn't played yet");
        }
        if(symbol != naTahu){
            throw Error(`symbol ${symbol} is not in sync with who is supposed to play now ${naTahu}`)
        }
        console.log("programmatic move from server being made", rowIndex, columnIndex, symbol);
        boardApiInfo.board[rowIndex][columnIndex] = symbol;

        if(checkVictory(rowIndex, columnIndex, symbol)){
            console.log(`${symbol} wins!`);
            isVictory = true;
            if(User.name === null){
                throw Error("Z makeProgrammaticMove nemůže být User.name null");
            }
            if(opponentUsername === undefined){
                throw Error("Z makeProgrammaticMove nemůže být opponentUsername null");
            }
            updateElo(User.name, opponentUsername, false).catch(e => {
                console.error(e);
                //shouldn't happen at all, so this non fancy alert is sufficient
                alert(e);
            });
            return;
        }
        //change whose turn it is manually, because handleMove is not (AND SHOULD NOT BE) called here
        //handleMove would call the onMove event callback, that would send the move back to the other party
        if(naTahu == "O"){
            naTahu = "X";
        }else if(naTahu == "X"){
            naTahu = "O";
        }
    }

    //determines if the board can be written to from this user = if it is his turn in multiplayer (i.e. click on board)
    let allowedClickOnBoardOnThisClient = $derived.by(() => {
        if(mode == "multiplayer"){
            return naTahu == allowedPlayer;
        }else{
            //on singleplayer, the board is always writeable (until win, but that is handled by checkVictory)
            return true;
        }
    });

    let name = $derived(boardApiInfo.name);
    $effect(() => {
        document.title = "Hra - " + name;
    });

    function count(array: Array<Array<string>>, item: string) {
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
    let naTahu: "X" | "O" = $state("X");
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
        console.log("Part of reset: Determining naTahu based on the received board");
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
    type BoardSquare = "X" | "O" | "";
    // quick O(1) function to check if the latest move is a winning one
    function checkVictory(rowIndex: number, columnIndex: number, player: BoardSquare) {
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
        type Direction = 'n' | 'ne' | 'e' | 'se' | 's' | 'sw' | 'w' | 'nw';
        let directionsToLookAt: Set<Direction> = new Set(['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']);
        type Position = [number, number, Direction]; // [rowIndex, columnIndex, direction]
        for(let dist = 1; dist <= 4; dist++){
            let allPossiblePositions: Record<Direction, Position> = {
                "n":    [rowIndex - dist, columnIndex, "n"],
                "ne":   [rowIndex - dist, columnIndex + dist, "ne"],
                "e":    [rowIndex, columnIndex + dist, "e"],
                "se":   [rowIndex + dist, columnIndex + dist, "se"],
                "s":    [rowIndex + dist, columnIndex, "s"],
                "sw":   [rowIndex + dist, columnIndex - dist, "sw"],
                "w":    [rowIndex, columnIndex - dist, "w"],
                "nw":   [rowIndex - dist, columnIndex -dist, "nw"]
            };

            type DirectionTuple = [BoardSquare, Direction];

            //.keys() returns an iterator, which should have worked (and be lazily evaluated?) => for now a destructuring operator works
            let squaresInDirectionsToLookAt = [...directionsToLookAt.keys()].map((value) => {
                let [x,y, direction] = allPossiblePositions[value];
                /*  bounds checking is indeed necessary because if out of bounds the value is undefined 
                        => that can throw Uncaught TypeError: Cannot read properties of undefined (reading '2') 
                            when x is out bounds and y is 2 */
                if(0 <= x && x < 15 && 0 <= y && y < 15){
                    //when I don't return this, undefined is returned
                    return [boardApiInfo.board[x][y], direction] as DirectionTuple;
                }
            });
           
            //squares of the same player who made this move
            let relevantSquares = squaresInDirectionsToLookAt.filter(e => {
                if(e == undefined) return false;
                let [value, direction] = e;
                if(value == player) return true;
            });

            let relevantDirections: Array<Direction> = relevantSquares.map(e=> e[1]);
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

    function handleMove(rowIndex: number, columnIndex: number) {
        if(isVictory){
            return;
        }

        if(!allowedClickOnBoardOnThisClient){
            //blocks local user from making a move when it is not his turn
            return;
        }

        boardApiInfo.board[rowIndex][columnIndex] = naTahu;
        lastMoved = naTahu;

        if(onMove){
            onMove(rowIndex, columnIndex, naTahu);
        }

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
<!-- <p>{naTahu} {allowedPlayer} {allowedClickOnBoardOnThisClient}</p> -->

{#if isVictory && !boardWonAlready}
    <h2 class="toast">Hráč <span class="player {naTahu}">{naTahu}</span> vyhrál!</h2>
{:else if isVictory && boardWonAlready}
    <h2 class="toast">Dorazila vyřešená úloha, hráč <span class="player {whoWon}">{whoWon}</span> vyhrál!</h2>
{/if}

<h2 style="display: flex;justify-content: center;gap: 10px;">
    {#if mode == "multiplayer"}
    <div>
        Hrajete za <span class="player {allowedPlayer}">{allowedPlayer}</span>
    </div>
    |
    {/if}
    <div>
        Na tahu je <span class="player {naTahu}">{naTahu}</span>
    </div>
</h2>
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
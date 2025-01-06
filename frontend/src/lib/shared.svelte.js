//For global state like what game are we playing
export const gameInfo = $state({
    selected: false
});


export const resetGame = () => {
    console.log('resetting game from shared');
    gameInfo.selected = false;
    gameInfo.uuid = Date.now() //changing the uuid on empty game to trigger reset in Board.svelte
    gameInfo.apiResponse = {
        board: Array(15).fill().map(() => Array(15).fill("")),
        uuid: Date.now() //changing the uuid on empty game to trigger reset in Board.svelte

    };
    gameInfo.selected = true;
}
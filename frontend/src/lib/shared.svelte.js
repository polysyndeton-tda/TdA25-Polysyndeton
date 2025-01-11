import { PUBLIC_API_BASE_URL } from '$env/static/public';
const api_url = PUBLIC_API_BASE_URL || 'https://odevzdavani.tourdeapp.cz/mockbush/api/v1/';
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
        uuid: Date.now(), //changing the uuid on empty game to trigger reset in Board.svelte
        name: "nova hra",
        difficulty: "beginner"
    };
    gameInfo.selected = true;
}

export async function fetchGame(uuid) {
    const request = await fetch(`${api_url}/games/${uuid}`);
    const data = await request.json();
    return data;
}

export async function editPuzzle(uuid){
    //TODO: implement some other form of error checks when $page.params.uuid is not available here
    // => perhaps based on HTTP status code
    //(of course, this is not a .svelte file)
    //[vite-plugin-svelte-module] [plugin vite-plugin-svelte-module] src/lib/shared.svelte.js (31:26): src/lib/shared.svelte.js:31:26 Cannot reference store value outside a `.svelte` file
    // if($page.params.uuid){ //on /game/:uuid, editing an existing game
        const request = await fetch(`${api_url}/games/${uuid}`, 
            {
                method: "PUT",
                body: JSON.stringify({
                    name: gameInfo.apiResponse.name,
                    board: gameInfo.apiResponse.board,
                    difficulty: gameInfo.apiResponse.difficulty,    
                }),
                headers: {
                    "Content-Type": "application/json",
                }
            } 
        );
        const data = await request.json();
        console.log("editPuzzle response", data)
    // }else{
    //     throw new Error("Call createPuzzle first");
    // }
}

export async function deletePuzzle(uuid) {
    const request = await fetch(`${api_url}/games/${uuid}`,
        {
            method: 'DELETE',
            headers: {
              'Content-Type': 'text/plain;charset=UTF-8'
            }
        });
    if(request.ok){
        return true;
    }
    return false;
    //this path doesn't send any response
}
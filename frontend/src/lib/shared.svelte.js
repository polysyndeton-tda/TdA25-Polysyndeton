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
        name: "Nová hra piškvorek",
        difficulty: "beginner"
    };
    gameInfo.selected = true;
}

export async function fetchGame(uuid) {
    const request = await fetch(`${api_url}/games/${uuid}`);
    if(request.status == 404){
        throw Error("Úloha nebyla nalezena. \n Pravděpodobně je to proto, že byla smazána.");
    }
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
        console.log("editPuzzle response", data);
        if(request.status == 422){
            alert("Stav křižků neodpovídá stavu koleček nebo naopak.\n V tomto stavu není možné úlohu uložit");
        }
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

/*The levels of difficulty 
=Obtížnosti in Czech (začátečník, jednoduchá, pokročilá, těžká, nejtěžší)
In the UI in Czech, in the API in English*/
export const difficultyMapToEN = {
    "začátečník": "beginner",
    "jednoduchá": "easy",
    "pokročilá": "medium",
    "těžká": "hard",
    "nejtěžší": "extreme"
}

export const difficultyMapToCZ = {
    "beginner": "začátečník",
    "easy": "jednoduchá",
    "medium": "pokročilá",
    "hard": "těžká",
    "extreme": "nejtěžší"
}

export const difficultyMapToNumber = {
    "beginner": 1,
    "easy": 2,
    "medium": 3,
    "hard": 4,
    "extreme": 5
}

export const gameStateToCZ = {
    "opening": "Zahájení",
    "midgame": "Middle game", /*This English term was stated in the Commision, a Czech alternative would be Střední hra */
    "endgame": "Koncovka"
}

export const filterToEN = {
    "24 hodin": "24h",
    "7 dní": "7d",
    "3 měsíců": "3m",
    "1 měsíce": "1m",
    "neomezenou": ""
}

export const filterToCZ = {
    "24h": "24 hodin",
    "7d": "7 dní",
    "3m": "3 měsíců",
    "1m": "1 měsíce",
    "": "neomezenou"
}

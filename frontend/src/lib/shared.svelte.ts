import { PUBLIC_API_BASE_URL } from '$env/static/public';
const api_url = PUBLIC_API_BASE_URL || 'https://odevzdavani.tourdeapp.cz/mockbush/api/v1/';
//For global state like what game are we playing
type Difficulty = "beginner" | "easy" | "medium" | "hard" | "extreme";
type BoardCell = "X" | "O" | "";
type Board = BoardCell[][];

interface ApiResponse {
    board: Board;
    uuid: string;
    name: string;
    difficulty: Difficulty;
}

interface GameInfo {
    selected: boolean;
    uuid?: string;
    apiResponse?: ApiResponse;
}
export const gameInfo = $state<GameInfo>({
    selected: false
});

function assertApiResponse(apiResponse: ApiResponse | undefined): asserts apiResponse is ApiResponse {
    if (!apiResponse) {
        throw new Error("BIG ERROR: editPuzzle called before puzzle saved!");
    }
}

export const resetGame = () => {
    console.log('resetting game from shared');
    gameInfo.selected = false;
    gameInfo.uuid = String(Date.now()) //changing the uuid on empty game to trigger reset in Board.svelte
    gameInfo.apiResponse = {
        board: Array(15).fill().map(() => Array(15).fill("")),
        uuid: String(Date.now()), //changing the uuid on empty game to trigger reset in Board.svelte
        name: "Nová hra piškvorek",
        difficulty: "beginner"
    };
    gameInfo.selected = true;
}

export async function fetchGame(uuid: string) {
    const request = await fetch(`${api_url}/games/${uuid}`);
    if(request.status == 404){
        throw Error("Úloha nebyla nalezena. \n Pravděpodobně je to proto, že byla smazána.");
    }
    const data = await request.json();
    return data;
}

export async function editPuzzle(uuid: string){
    //TODO: implement some other form of error checks when $page.params.uuid is not available here
    //Done with this undefined check: 
    // page.params uuid is not available when the game hasn't been saved
    // and gameInfo.apiResponse is not available when the game hasn't been saved
    assertApiResponse(gameInfo.apiResponse);
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
        return request; //For GUI info on request (if succeeded)
    // }else{
    //     throw new Error("Call createPuzzle first");
    // }
}

export async function deletePuzzle(uuid: string) {
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

export function wait(ms: number) {
    if(ms > 0){
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                resolve(ms)
            }, ms )
        });
    }else{
        return;
    }
}

type UserChangeField = "password" | "email" | "username";
type RequireAtLeastOne<T> = { [K in keyof T]: Pick<T, K> }[keyof T]; //at least one property has to be there (if nothing is requested to change - what would be the point of the request)
type UserChange = RequireAtLeastOne<Record<UserChangeField, string>>;

interface UserProperties {
    uuid: string;
    username: string;
    email: string;
    elo: number;
    wins: number;
    draws: number;
    losses: number;
}

// Then make UserPostApiResponse extend it
interface UserPostApiResponse extends UserProperties {
    message?: string;  // for error responses
}

// Nullable version of UserProperties for the localstorage state
interface NullableUserProperties {
    uuid: string | null;
    username: string | null;
    email: string | null;
    elo: number | null;
    wins: number | null;
    draws: number | null;
    losses: number | null;
}

//this solution from https://www.reddit.com/r/sveltejs/comments/1d313ln/cannot_export_state_from_a_module_if_it_is/
class UserState implements Partial<NullableUserProperties>{
    //localStorage is not reactive
    // => so I made user methods a part of this class so values can be kept up to date manually (in login, logout)
    public token = localStorage.getItem("token");
    //wrapping this in $state() does not make it change when storage changes, 
    //but it is needed because name is displayed in UI
    //(else the UI (in +layout.svelte shows nothing):
    public name = $state<string | null>(localStorage.getItem("username"));
    public email: string | null = localStorage.getItem("email");
    //derived didnt work here, because token is not a $state() vriable (thats ok)
    public loggedIn = $state(this.token !== null);

    public uuid = localStorage.getItem("uuid");

    public isAdmin = localStorage.getItem("isAdmin");

    public elo = Number(localStorage.getItem("elo"));
    public wins = Number(localStorage.getItem("wins"));
    public draws = Number(localStorage.getItem("draws"));
    public losses = Number(localStorage.getItem("losses"));
    
    async login(username: string, password: string){
        const request = await fetch(`${api_url}/login`, 
            {
                method: "POST",
                body: JSON.stringify({
                    username: username,
                    password: password,
                }),
                headers: {
                    "Content-Type": "application/json",
                }
            } 
        );
        if(request.ok){
            this.loggedIn = true;
        }else{
            if(request.status == 404){
                throw Error("Takového uživatele neznáme. \n Zkontrolujte, zda jste v přihlašovacím jméně nenapsali překlep.");
            }
            if(request.status == 401){
                throw Error("Zkontrolujte, zda jste v hesle nenapsali překlep.");
            }
        }
        try{
            const response = await request.json();
            // console.log("response from login", response);
            localStorage.setItem("token", response.token);
            localStorage.setItem("username", username);
            localStorage.setItem("uuid", response.uuid);
            localStorage.setItem("isAdmin", response.is_admin);
            this.token = response.token;
        }catch(e){
            console.error(e);
        }
    }

    logout(){
        this.loggedIn = false;
        this.token = null;
        this.name = null;
        localStorage.clear();
    }

    async signUp(username: string, email: string, password: string){
        const request = await fetch(`${api_url}/users`, 
            {
                method: "POST",
                body: JSON.stringify({
                    username: username,
                    email: email,
                    password: password,
                    elo: 400
                }),
                headers: {
                    "Content-Type": "application/json",
                }
            } 
        );
        const data: UserPostApiResponse = await request.json();
        if(request.status == 409){
            if(data.message == "User with this username already exists"){
                throw Error("Toto uživatelské jméno již někdo používá. \n Zvolte jiné");
            }else if(data.message == "User with this email already exists"){
                throw Error("Tento email již nějaký účet používá. \n Zvolte jiný");
            }
        }
        if(request.status == 400){
            throw Error("Vyplňte prosím všechna pole formuláře.");
        }
        console.log("signUp response", data);
        type ValidKeys = Exclude<keyof UserProperties, 'username'>;
        //Setting this. state variables & localstorage from signup api response in a very demure type safe way
        //(Typescript shouted until I put all of these checks in)
        this.name = data.username;
        localStorage.setItem("username", this.name);
        for(const [key, value] of Object.entries(data)){
            if(key !== "username" && key !== "message"){
                const typedKey = key as ValidKeys;
                if (typedKey === 'uuid' || typedKey === 'email') {
                    (this[typedKey] as string) = String(value);
                } else {
                    (this[typedKey] as number) = Number(value);
                    
                }
                localStorage.setItem(typedKey, String(value));
            }
        }
        console.log("uuid", data.uuid);
        await this.login(username, password);
    }

    async delete(){
        const request = await fetch(`${api_url}/users/${this.uuid}`, {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${this.token}`
            }
        });
        if(request.status == 404){
            throw Error("Uživatel nenalezen \n Pravděpodobně už jste účet smazali. \n Pro ověření se zkuste odhlásit a přihlásit znova. Pokud to nepůjde, smazání účtu bylo úspěšné.");
        }
        if(request.ok){
            console.log("User deleted successfully");
            this.logout();
            return true;
        }
        return false;
    }

    async editUser(toChange: UserChange){
        console.log("Sending", JSON.stringify(toChange));
        const request = await fetch(`${api_url}/users/${this.uuid}`, {
            method: "PUT",
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${this.token}`
            },
            body: JSON.stringify(toChange),
        });
        const response = await request.json();
        if(request.ok){
            return true;
        }
        return false;
    }

    async changePassword(password: string){
        if(password == undefined){
            throw Error("Supply password string");
        }
        let changes = {"password": password}
        let ok = await this.editUser(changes);
        return ok;
    }
    async changeName(name: string){
        if(name == undefined || name == null){
            throw Error("Supply name string");
        }
        let changes = {"username": name}
        let ok = await this.editUser(changes);
        if(ok){
            this.name = name;
            localStorage.setItem("username", name);
            return true;
        }
        return false;
    }

    async changeEmail(email: string){
        if(name == undefined || name == null){
            throw Error("Supply name string");
        }
        let changes = {"email": email}
        let ok = await this.editUser(changes);
        return ok;
    }

    async getUsers(){
        const request = await fetch(`${api_url}/users`, {
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${this.token}`
            }
        }); //GET
        const response = await request.json(); //the only possible code in openapi is 200
        return response;
    }
}

export let User = new UserState();

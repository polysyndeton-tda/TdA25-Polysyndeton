import { io, Socket } from 'socket.io-client';
import { User } from "$lib/shared.svelte";

//_____Events defined to server and from server_____
interface ServerToClientEvents {
    match_found: (data: MatchFoundData) => void,
    game_start: (data: GameStartData) => void,
    move: (data: MoveData) => void,
    opponent_disconnected: (data: OpponentDisconnectedData) => void
}

interface ClientToServerEvents {
    join: (data: JoinData) => void,
    move: (data: MoveData) => void,
    timeout: (data: TimeoutData) => void,
}

//______________Each event's interface______________
interface MatchFoundData {
    opponent: string;
    room: string;
    symbol: "X" | "O"
}

interface GameStartData {
    room: string;
    symbols: {[username: string]: "X" | "O"}; //If I wanted, I could move [player: string]: "X" | "O" or [key: string]: string; to a seperate interface Symbols
}

interface MoveData {
    room: string;           // Room identifier
    move: [number, number]; // x, y coordinates
    username: string;       // Player's username
    symbol: "X" | "O";      // Player's symbol
}

interface OpponentDisconnectedData {
    message: string;    // Disconnect message
}

interface JoinData {
    username: string,
    room: string
}

interface TimeoutData {
    room: string;
    winner: "X" | "O";
}

//___________The socket class containing all socket.io interactions___________

export class SocketHandler {
    private socket: Socket<ServerToClientEvents, ClientToServerEvents>
    private allowUnregisteredUsers: boolean
    constructor(
        socketioServerURL: string,
        eventReceivedCallbacks: ServerToClientEvents,
        allowUnregisteredUsers: boolean = false,

    ){
        this.allowUnregisteredUsers = allowUnregisteredUsers;
        if((!User.uuid || !User.name) && !this.allowUnregisteredUsers){
            throw new Error("Trying to init socket connection with user not signed in when unregistered users are not allowed");
        }

        this.socket = io(socketioServerURL, { //for deploy **probably** document.location.hostname without the port
            path: "/socket.io/",
            transports: ["websocket"],
            query: {
                user_uuid: User.uuid
            }
        });

        //automatically connect
        this.socket.on('match_found', (data: MatchFoundData) => {
             if(!User.uuid || !User.name){
                throw new Error("Trying to respond to 'match_found' with user not signed in when unregistered users are not allowed");
            }
            //Now automatic join, maybe TODO: Show invitation dialog,
            console.log(`Match found from ${data.opponent} at room ${data.room}. I'm playing symbol ${data.symbol}`);
            this.socket.emit('join', {username: User.name, room: data.room});

            //And now call user defined callback, i. e. for some UI notification
            eventReceivedCallbacks['match_found'](data);
        });

        //For the rest of the server sent events, just call user callbacks
        this.socket.on('game_start', (data) => {
            eventReceivedCallbacks['game_start'](data);
        });

        this.socket.on('move', (data) => {
            eventReceivedCallbacks['move'](data);
        });

        this.socket.on('opponent_disconnected', (data) => {
            eventReceivedCallbacks['opponent_disconnected'](data);
        });
    }

    disconnect(){
        this.socket.disconnect();
    }

    emit<T extends keyof ClientToServerEvents>(
        type: T,
        //rest operator collects the possibly large list of parameters into options as an array
        ...options: Parameters<ClientToServerEvents[T]>
    ){
        //spread opeator takes that array and makes it a large list of parameters again
        this.socket.emit(type, ...options);
        console.info("emitting", type, options);
    }
}
<script lang="ts">
    import { io, Socket } from 'socket.io-client';
    import { User } from "$lib/shared.svelte";
    import { PUBLIC_API_BASE_URL } from '$env/static/public';
    const api_url = PUBLIC_API_BASE_URL || 'https://odevzdavani.tourdeapp.cz/mockbush/api/v1/';
    // Connection
    const socket = io("http://localhost:5000", { //for deploy **probably** document.location.hostname without the port
		path: "/socket.io/",
		transports: ["websocket"],
        query: {
            user_uuid: User.uuid
        }
    });

    interface GameInvitationData {
       room: string;           // Room identifier
       challenger: {
           uuid: string;       // Challenger's UUID
           username: string;   // Challenger's username
           elo: number;        // Challenger's ELO rating
       }
   }

    interface ServerToClientEvents {
        game_invitation: (data: GameInvitationData) => void,
    }

    socket.on('game_invitation', (data) => {
        // Show invitation dialog
        console.log(`Invitation from ${data.challenger.username}`);

        //for testing
        socket.emit('join_friendly', {
            username: data.challenger.username,
            room: data.room
        });

        socket.emit('accept_game', {
            room: data.room,
            username: data.challenger.username
        });
    });

    socket.on("game_accepted", (data) => {
        //for testing
        console.log("game accepted received");
    });

    

    socket.on("game_start", (data) => {
        //for testing
        console.log("game_start received");
    });

    

    let enteredName = $state("");

    async function friendlyPost(){
        const request = await fetch(`${api_url}/friendly`, {
            method: "POST",
            body: JSON.stringify({
                user_username: User.name,
                opponent_username: enteredName
            }),
            headers: {
                "Content-Type": "application/json",
            }
        });
    }
    

</script>



<div class="center">
    <h1>Nehodnocená hra</h1>
    <h2>Vyberte si svého spoluhráče</h2>

    <input bind:value={enteredName} type="text" placeholder="Jméno druhého hráče">
    <button onclick={async () => friendlyPost()}>Poslat pozvánku</button>
</div>


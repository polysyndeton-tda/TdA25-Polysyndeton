# Friendly Match Flow Documentation

## Overview

Friendly Match Flow:

1. Player 1 (inviter) sends a POST request to create a game invitation.
2. The backend generates a unique room ID and stores the session.
3. Player 1 shares the room ID with Player 2 (opponent).
4. Both players connect to the WebSocket room using the room ID.
5. Player 2 accepts the invitation, and the game starts automatically when both players join the room.

## API Endpoints

### 1. Create a Friendly Game Invitation

- **Endpoint**: `POST /api/v1/friendly`
- **Request Body**:
  ```json
  {
    "user_name": "Player1",
    "opponent_name": "Player2"
  }
  ```
- **Response**:
  ```json
  {
    "message": "Game invitation created",
    "room": "some-room-id"
  }
  ```
- **Purpose**: Creates a new friendly game session and returns a unique room ID.

### 2. Join a Friendly Game Room

- **WebSocket Event**: `join_friendly`
- **Payload**:
  ```json
  {
    "username": "Player1",
    "room": "some-room-id"
  }
  ```
- **Purpose**: Joins the WebSocket room for the friendly game.

### 3. Accept a Game Invitation

- **WebSocket Event**: `accept_game`
- **Payload**:
  ```json
  {
    "room": "some-room-id",
    "username": "Player2"
  }
  ```
- **Purpose**: Notifies the backend that the opponent has accepted the invitation.

### 4. Decline a Game Invitation

- **WebSocket Event**: `decline_game`
- **Payload**:
  ```json
  {
    "room": "some-room-id",
    "username": "Player2"
  }
  ```
- **Purpose**: Notifies the backend that the opponent has declined the invitation.

## Frontend Implementation

### 1. Create a Friendly Game Invitation

When Player 1 wants to invite Player 2, send a POST request to `/api/v1/friendly`:

```svelte
<script>
  let player1Name = "Player1";
  let player2Name = "Player2";
  let roomId = "";

  async function createFriendlyGame() {
    const response = await fetch("/api/v1/friendly", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_name: player1Name,
        opponent_name: player2Name,
      }),
    });

    const data = await response.json();
    roomId = data.room;
    console.log("Room ID:", roomId);
  }
</script>

<button on:click={createFriendlyGame}>Create Friendly Game</button>
```

### 2. Share the Room ID

Once the room ID is generated, share it with Player 2 (e.g., via a chat system or direct link).

### 3. Join the Friendly Game Room

Both players must join the WebSocket room using the room ID:

```svelte
<script>
  import { io } from "socket.io-client";

  let socket;
  let username = "Player1"; // or "Player2"
  let roomId = "some-room-id"; // Replace with the actual room ID

  function joinFriendlyRoom() {
    socket = io("http://localhost:5000"); // Replace with your backend URL
    socket.emit("join_friendly", { username, room: roomId });

    socket.on("game_start", (data) => {
      console.log("Game started!", data);
      // Handle game start logic (e.g., render the board)
    });

    socket.on("game_declined", (data) => {
      console.log("Game declined:", data);
      // Handle decline logic (e.g., show a message)
    });

    socket.on("error", (data) => {
      console.log("Error:", data.message);
      // Handle errors (e.g., invalid room or unauthorized access)
    });
  }
</script>

<button on:click={joinFriendlyRoom}>Join Friendly Room</button>
```

### 4. Accept or Decline the Invitation

Player 2 can accept or decline the invitation using WebSocket events:

```svelte
<script>
  function acceptGame() {
    socket.emit("accept_game", { room: roomId, username: "Player2" });
  }

  function declineGame() {
    socket.emit("decline_game", { room: roomId, username: "Player2" });
  }
</script>

<button on:click={acceptGame}>Accept Game</button>
<button on:click={declineGame}>Decline Game</button>
```

### 5. Handle Game Moves

Once the game starts, handle moves using the `move` event:

```svelte
<script>
  function makeMove(x, y) {
    socket.emit("move", {
      room: roomId,
      move: [x, y],
      username: "Player1",
      symbol: "X", // or "O"
    });
  }

  socket.on("move", (data) => {
    console.log("Opponent moved:", data);
    // Update the game board with the opponent's move
  });
</script>
```

## Example Flow

1. Player 1 creates a game invitation and gets a room ID.
2. Player 1 shares the room ID with Player 2.
3. Both players join the WebSocket room using the room ID.
4. Player 2 accepts the invitation.
5. The game starts, and both players can make moves.

## Error Handling

- If the room ID is invalid, the backend will emit an `error` event.
- If a player disconnects, the backend will emit an `opponent_disconnected` event.

## WebSocket Events

| Event | Description |
| --- | --- |
| `game_start` | Emitted when both players join the room. |
| `game_accepted` | Emitted when the opponent accepts the game. |
| `game_declined` | Emitted when the opponent declines the game. |
| `move` | Emitted when a player makes a move. |
| `opponent_disconnected` | Emitted when the opponent disconnects. |
| `error` | Emitted for invalid room or unauthorized access. |

## Testing the Flow

1. **Create a Game**:
   - Use the `createFriendlyGame` function to generate a room ID.

2. **Join the Room**:
   - Both players should join the room using the `join_friendly` event.

3. **Accept the Game**:
   - Player 2 should emit the `accept_game` event.

4. **Play the Game**:
   - Use the `move` event to handle game moves.

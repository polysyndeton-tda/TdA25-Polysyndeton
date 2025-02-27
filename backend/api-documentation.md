# Game API Documentation

## Overview
This document describes the API endpoints and WebSocket events for the multiplayer game system. The system supports both matchmaking and friendly matches.

## API Endpoints

### Matchmaking Request
Adds a user to the matchmaking queue.

```
POST /api/v1/matchmaking
```

**Request Body:**
```json
{
    "uuid": "player_uuid"
}
```

**Response:**
- Success (200):
```json
{
    "message": "Added to matchmaking queue"
}
```
- Error (404):
```json
{
    "message": "User not found"
}
```

### Friendly Match Request
Sends a game invitation to another player.

```
POST /api/v1/friendly
```

**Request Body:**
```json
{
    "user_username": "challenger_username",
    "opponent_username": "opponent_username"
}
```

**Response:**
- Success (200):
```json
{
    "message": "Game invitation sent",
    "room": "room_uuid1_uuid2"
}
```
- Error (404):
```json
{
    "message": "User not found"
}
```

## WebSocket Events

### Connection

To establish a WebSocket connection, include the user's UUID as a query parameter:
```javascript
const socket = io('ws://your-server', {
    query: {
        user_uuid: 'player_uuid'
    }
});
```

### Incoming Events (Server → Client)

1. **match_found**
   - Received when matchmaking finds an opponent
   ```typescript
   {
       room: string;       // Room identifier
       opponent: string;   // Opponent's UUID
       symbol: "X" | "O"   // what symbol am I playing with, not the opponent
   }
   ```

2. **game_invitation**
   - Received when another player sends a friendly match invitation
   ```typescript
   {
       room: string;           // Room identifier
       challenger: {
           uuid: string;       // Challenger's UUID
           username: string;   // Challenger's username
           elo: number;        // Challenger's ELO rating
       }
   }
   ```

3. **game_accepted**
   - Received when opponent accepts the game invitation
   ```typescript
   {
       room: string;       // Room identifier
       username: string;   // Username of accepting player
   }
   ```

4. **game_declined**
   - Received when opponent declines the game invitation
   ```typescript
   {
       room: string;       // Room identifier
       username: string;   // Username of declining player
   }
   ```

5. **game_start**
   - Received when both players have joined and the game can begin
   ```typescript
   {
       room: string;       // Room identifier
       symbols: {player.username: "X", otherPlayer.username: "O" }
   }
   ```
   This, but in more technical TypeScript terms:
   ```typescript
   {
        room: string;
        symbols: {[player: string]: "X" | "O"};
    }
   ```

6. **move**
   - Received when opponent makes a move
   ```typescript
   {
       room: string;       // Room identifier
       move: [number, number]; // x, y coordinates
       username: string;   // Player making the move
       symbol: "X" | "O";  // Player's symbol
   }
   ```

7. **opponent_disconnected**
   - Received when opponent disconnects from the game
   ```typescript
   {
       message: string;    // Disconnect message
   }
   ```

8. **already_connected**
    - Received when the user tries to connect to the game from a second device (for example has two tabs open during pairing)
      (Intended behaviour is to have the game on two frontends only)

### Outgoing Events (Client → Server)

1. **join**
   - Send when joining a matchmaking game
   ```typescript
   {
       username: string;   // Player's username
       room: string;      // Room identifier from match_found event
   }
   ```

2. **join_friendly**
   - Send when joining a friendly game
   ```typescript
   {
       username: string;   // Player's username
       room: string;      // Room identifier from game_invitation
   }
   ```

3. **accept_game**
   - Send to accept a friendly game invitation
   ```typescript
   {
       room: string;      // Room identifier
       username: string;  // Player's username
   }
   ```

4. **decline_game**
   - Send to decline a friendly game invitation
   ```typescript
   {
       room: string;      // Room identifier
       username: string;  // Player's username
   }
   ```

5. **move**
   - Send to make a move in the game
   ```typescript
   {
       room: string;           // Room identifier
       move: [number, number]; // x, y coordinates
       username: string;       // Player's username
       symbol: "X" | "O";      // Player's symbol
   }
   ```

## Typical Flow Examples

### Matchmaking Flow
1. Client sends POST to `/api/v1/matchmaking`
2. Client receives `match_found` event
3. Client sends `join` event
4. Client receives `game_start` event
5. Game begins with `move` events

### Friendly Match Flow
1. Challenger sends POST to `/api/v1/friendly`
2. Opponent receives `game_invitation` event
3. Both players send `join_friendly` event
4. Opponent sends either `accept_game` or `decline_game`
5. If accepted:
   - Both receive `game_accepted` event
   - Both receive `game_start` event
   - Game begins with `move` events
6. If declined:
   - Both receive `game_declined` event
   - Room is closed

## Implementation Example (Svelte)

```typescript
import io from 'socket.io-client';

// Connection
const socket = io('ws://your-server', {
    query: {
        user_uuid: 'player_uuid'
    }
});

// Listen for events
socket.on('game_invitation', (data) => {
    // Show invitation dialog
    console.log(`Invitation from ${data.challenger.username}`);
});

socket.on('game_start', (data) => {
    // Initialize game board
    console.log(`Game starting in room ${data.room}`);
});

socket.on('move', (data) => {
    // Update game board
    console.log(`Move at ${data.move} by ${data.username}`);
});

// Send events
function makeMove(x: number, y: number) {
    socket.emit('move', {
        room: currentRoom,
        move: [x, y],
        username: playerUsername,
        symbol: playerSymbol
    });
}

function acceptInvitation(room: string) {
    socket.emit('join_friendly', {
        username: playerUsername,
        room: room
    });
    
    socket.emit('accept_game', {
        room: room,
        username: playerUsername
    });
}
```

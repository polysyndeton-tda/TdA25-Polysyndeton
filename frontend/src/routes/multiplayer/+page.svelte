<div class="center">
    <h1>Multiplayer</h1>
    <div class="centerBox"> 
    <a class="button" href="multiplayer/friendly">Friendly hra</a>
    <a class="button" href="multiplayer/match">Kompetitivní hra</a>
    <a class="button" href="multiplayer/freeplay">Freeplay hra</a>
    </div>
</div>

<style>
.centerBox{
    display: flex;
    flex-direction: column;
    gap: 10px;
    max-width: 500px;
    margin: auto;
}
.button{
    display: block;
    border-radius: 8px;
    border: 1px solid transparent;
    padding: 0.6em 1.2em;
    font-size: 1.2rem;
    font-weight: 535;
    font-family: inherit;
    cursor: pointer;
    transition: border-color 0.25s;
    text-decoration: none;
    background-color: #f6f6f6;
    color: black;
}

.button:hover {
  border-color: #0070BB; /*#646cff;*/ /*#535bf2;*/
}
.button:focus,
.button:focus-visible {
  outline: 4px auto -webkit-focus-ring-color;
}

@media (prefers-color-scheme: dark) {
    .button {
        background-color: #1a1a1a;
        color: white;
    }
}

.timer.active {
    font-weight: bold;
    color: #f00;
}
</style>

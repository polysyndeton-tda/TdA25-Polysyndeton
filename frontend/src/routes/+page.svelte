<script>
    import Login from "$lib/Login.svelte";
    document.title = "TdA - Hlavní stránka";
    let showRegisterPopup = $state(false);
</script>

<div class="centerBox">
    <h1><span class="player X">X</span> Piškvorky <span class="player O">O</span></h1>
    <h2>🔥Vyrobené s láskou v Česku 🇨🇿</h2>
    <h3>Hrajte:</h3>
    <a class="button" href="/multiplayer">Online 🌐</a>
    <a class="button" href="/game">Lokálně s kamarádem 🙋‍♀️</a>
    <!-- <div class="register-wrapper">
        <button class="register" onclick={() => showRegisterPopup = true}>Registrovat již dnes!</button>
    </div> -->
</div>

{#if showRegisterPopup}
    <Login bind:show={showRegisterPopup} mode="register"/>
{/if}

<style>
/* The arrows */
.register-wrapper {
    margin-top: 20px;
    position: relative;
    display: inline-block;
}

.register-wrapper::before,
.register-wrapper::after {
    content: '';
    position: absolute;
    width: 30px;
    height: 30px;
    background: #ff6b6b;
    top: 50%;
    transform: translateY(-50%);
}

.register-wrapper::before {
    left: -50px;
    clip-path: polygon(100% 50%, 0 0, 0 100%);
}

.register-wrapper::after {
    right: -50px;
    clip-path: polygon(0 50%, 100% 0, 100% 100%);
}

/* The end of arrows */

.player{
    color: transparent;
    vertical-align: middle;
    font-size: xx-large;
}
.O {
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
.centerBox{
    display: flex;
    flex-direction: column;
    align-items: center;
}
.register{
    background-color: #E31837;
}
.register:hover{
    border-color: white;
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
    max-width: 500px;
    margin: 10px;
}

.button:hover {
  border-color: #0070BB;
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
@media (prefers-color-scheme: light) {
    .register{
        color: white;
    }
}
</style>
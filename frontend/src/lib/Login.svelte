<script lang="ts">
    import { scale, slide, fade } from 'svelte/transition';
    import { User } from '$lib/shared.svelte.ts';
    import Alert from './Alert.svelte';
    type LoginProps = {
        show?: boolean,
        mode?: "login" | "register",
        floating?: boolean,
        reloadPageAfterSuccess?: boolean
    }
    let {
        show = $bindable(),
        mode = $bindable("login"),
        floating = true,
        reloadPageAfterSuccess = false
    }: LoginProps = $props();

    let userNameField: HTMLInputElement;
    function addFocus(node: HTMLInputElement){
        node.select();
    }

    let email = $state("");
    let username = $state("");
    let password = $state("");
    let errorHappened = $state(false);
    let registerOrLoginError = $state("");

    function close(){
        show = false;
    }
</script>

{#snippet login(showCloseButton: boolean, showRegisterLink: boolean)}
    <div class="popup">
        <form>
            <div class="title">
                <div class="top-bar">
                    {#if mode == "login"}
                        <h2 in:fade>Přihlásit se</h2>
                    {:else}
                        <h2 in:fade>Registrovat</h2>
                    {/if} 
                    {#if showCloseButton}
                        <button aria-labelledby="Zavřít" onclick={close}><i class="fa-solid fa-xmark"></i></button>
                    {/if}
                </div>
                <table>
                    <tbody>
                        <tr>
                            <td>
                                <label for="username">Uživatelské jméno:</label>
                            </td>
                            <td>
                                <input use:addFocus bind:this={userNameField} bind:value={username} id="username" type="username">
                            </td>
                        </tr>
                        {#if mode == "register"}
                            <tr in:slide out:scale>
                                <td>
                                    <label for="email">E-mail:</label>
                                </td>
                                <td>
                                    <input bind:value={email} id="email" type="email">
                                </td>
                            </tr>
                        {/if}
                        <tr>
                            <td>
                                <label for="password">Heslo:</label>
                            </td>
                            <td>
                                <input bind:value={password} id="password" type="password">
                            </td>
                        </tr> 
                    </tbody>
                </table>
                {#if showRegisterLink}
                    {#if mode == "login"}
                        <p transition:slide>Ještě nemáte účet? <a href="javascript:void(0)" onclick={() => {
                            addFocus(userNameField);
                            mode = "register"}}> Registrovat</a></p>
                    {:else}
                        <p transition:slide>Již máte účet? <a href="javascript:void(0)" onclick={() => {
                            addFocus(userNameField);
                            mode = "login"}}>Přihlásit</a></p>
                    {/if}
                {/if}
            </div>
            <div class="button-area">
                {#if mode == "login"}
                    <button class="ok" onclick={() => {
                        User.login(username, password).catch(err => {
                            registerOrLoginError = err;
                            errorHappened = true;
                        })
                        .then(() => {
                            if(!errorHappened){
                                close();
                                if(reloadPageAfterSuccess){
                                    window.location.href = "/multiplayer/match";
                                }
                            }
                        });
                        User.name = username;
                        localStorage.setItem("username", username);
                        }}>Přihlásit</button>
                {:else}
                    <button class="ok" onclick={() => {
                        User.signUp(username, email, password).catch(err => {
                            errorHappened = true;
                            registerOrLoginError = err;                            
                        }).then(() => {
                            if(!errorHappened){
                                close();
                                if(reloadPageAfterSuccess){
                                    // window.location.reload();
                                    window.location.href = "/multiplayer/match";
                                }
                            };
                        });
                        }}>Registrovat</button>
                {/if}
            </div>
        </form>
    </div>
{/snippet}

{#if floating}
    <div transition:scale|global={{ duration: 300}} class="popup-container">
        {@render login(true, true)}
    </div>
{:else}
    <div style="display: flex;justify-content: center;">
        {@render login(false, true)}
    </div>
{/if}

{#if errorHappened}
    <Alert bind:show={errorHappened} okCallback={() => errorHappened = false}>{registerOrLoginError}</Alert>
{/if}

<style>
.popup-container{
    position: fixed;
    top: 0;
    height: 100%;
    width: 100%;
    display: flex;
    inset-inline-start: 0px;
    align-items: center;
    justify-content: center;
}
.popup{
    display: flex;
    justify-content: center;
    align-items: center;
    display: flex;
    flex-direction: column;
    gap: 10px;
    border-radius: 8px;
    filter: drop-shadow(0 0 8px var(--menu-item-hover-color));
    padding: 0 0 10px 0;
    width: 365px;
}
.title{
    border-radius: 8px;
    padding: 10px;
    width: 100%;
    box-sizing: border-box;
}

.top-bar{
    display: flex;
    justify-content: space-between;
    align-items: center;
}

h2{
    overflow-wrap: anywhere;
    max-width: 80vw;
    text-align: center;
    padding-left: 5px
}

table{
    border-collapse: separate;
    border-spacing: 10px 10px;
    margin: auto;
}

.button-area{
    text-align: center;
}

@media (prefers-color-scheme: light){
    h2, label, p{
        color: white;
    }
    p a{
        color: darkturquoise;
    }
    .title{
        background-color: #0257a5;
    }
    .popup{
        background: #739bc5; /*#76aeea;*/
        box-shadow: rgba(100, 100, 111, 1) 0px 7px 29px 0px;
    }
}

@media (prefers-color-scheme: dark){
    .title{
        background-color: #101010; /*#242424*/
    }
    .popup{
        background-color: #434343;
    }
}
/* fix from https://stackoverflow.com/questions/30282921/fixed-pop-up-div-gets-overlapped-by-keyboard */
@media (max-width: 767px) {
    .popup-container {
        width: 100%;
        top: 10px;
        bottom: 0px;    
        overflow-y: auto;
        max-height: 100%;
    }
}
</style>
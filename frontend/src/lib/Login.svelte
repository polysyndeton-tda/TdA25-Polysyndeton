<script lang="ts">
    import { scale, slide, fade } from 'svelte/transition';
    import { User } from '$lib/shared.svelte.ts';
    import Alert from './Alert.svelte';

    type LoginProps = {
        show?: boolean,
        mode?: "login" | "register",
        floating?: boolean,
        onSuccess?: Function,
    }
    let {
        show = $bindable(),
        mode = $bindable("login"),
        floating = true,
        onSuccess,
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
        <!-- 
        There was an implicit submission of a form going on.
        Basically although no button was made to specifically HTML submit the form,
        it was still being submitted the HTML way in addition to my JS fetch code.

        Basically two separate requests for POST http://localhost:5000/api/v1/login
        both HTTP 200 response,
        both with identical Request data and identical size (483 bytes, 741 bytes transferred)

        {"username":"Petr","password":"SG32#G)eXSGqf:G"}

        But of course different tokens in response (= a new one generated for every login API call)

        In Devtools, one of them had the initiator "fetch" 
        and the other one had a clickable link to "BBHbRatr.js:1 (fetch)" which revealed a stack frame: click handler => login => window.fetch

        More info on it: https://stackoverflow.com/questions/71133244/form-submitted-implicitly-even-when-there-are-other-input-element

        => since both works (HTTP 200, valid response with auth token),
        it may be possible to remove either:
            - login function with fetch call in JS
            - the form submit, with event.preventDefault()

        => removing the latter is preferred, as there is this bug: 
        
        Any URL query parameters are stripped after the form is submitted
        https://stackoverflow.com/questions/65973870/form-submission-for-get-strips-query-params
        It doesn't matter if those came from "name" attributes of the form
        or my idea of handling redirects from dedicated login/register pages back to the match page


        The only way I noticed this "implicit submission" was when I added the "name" attribute to an <input>
        in an attempt to make email autocomplete work (it of course doesn't - has nothing to do with that)

        => As a result query parameter pairs (name attribute value = input value) appeared in the document.href (not just any sort of form url)
           (because this is default for GET in forms, which is the default submission mode)
            => although network shows only POST submission? 
                =>  Maybe some SvelteKit magic going on with query params in the url
                    being added based on "name" attributes of inputs in the form (if any have the "name" attribute)
                    => if NO inputs have the "name" attribute than an "empty set of query parameters" could get appended
                           => which could manifest as ALL query params (from any sources, even if NONE were from the form) being removed upon form submission
        -->
        <form onsubmit={(event) => event.preventDefault()}>
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
                                <!-- name="username"  -->
                                <input use:addFocus bind:this={userNameField} bind:value={username} id="username" type="username">
                            </td>
                        </tr>
                        {#if mode == "register"}
                            <tr in:slide out:scale>
                                <td>
                                    <label for="email">E-mail:</label>
                                </td>
                                <td>
                                    <!-- name="email" -->
                                    <input autocomplete="email" bind:value={email} id="email" type="email">
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
                                if(onSuccess) onSuccess();
                            }
                        });
                        User.name = username;
                        localStorage.setItem("username", username);
                        }}>Přihlásit</button>
                {:else}

                    <!--
                    Before the form implicit submission removal (event.preventDefault() on the submit event),
                    this button removed the returnedURL query parameter from the URL and the redirect did not work
                    (by the time onSuccess was called it was null)
                    
                    <button>SURELY DOES NOTHING</button>

                    For more info, see previous commit a481f4cb3d9d1060d20cb2557ecd95ae4aea05a6
                    -->

                    <button class="ok" onclick={
                        () => {
                            User.signUp(username, email, password).catch(err => {
                                errorHappened = true;
                                registerOrLoginError = err;                            
                            }).then(() => {
                                if(!errorHappened){
                                    close();
                                    if(onSuccess) onSuccess();
                                };
                            });
                        }}    
                        >Registrovat
                    </button>
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
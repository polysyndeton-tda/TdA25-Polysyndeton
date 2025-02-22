<script lang="ts">
    import { User, wait } from "$lib/shared.svelte.ts";
    import Confirm from "$lib/Confirm.svelte";
    import Toast from "$lib/Toast.svelte";
    import Alert from "$lib/Alert.svelte";
    let showDeleteAccountPrompt = $state(false);
    let showDeleteConfirmation = $state(false);
    async function deleteUserGui(){
        try{
            let deleted = await User.delete();
            if(deleted){
                showDeleteConfirmation = true;
                User.logout();
                await wait(2600);
                showDeleteConfirmation = false;
            }
        }catch(err: any){
            console.error(err);
            showError = true;
            errorMessage = err.message;
        }
    }
    
    async function confirmUserDataChange(apiCall: Function, okMessage: string, failMessage: string){
        try{
            let ok = await apiCall();
            if(ok){
                toastMessage = okMessage;
            }else{
                toastMessage = failMessage;
            }
            showToast = true;
            await wait(2600);
            showToast = false;
        }catch(err: any){
            errorMessage = err;
            console.error(err);
            if((err.name == "TypeError" && err.message == "Failed to fetch") ||
                (err.name == "TypeError" && err.message == "NetworkError when attempting to fetch resource.")
            ){
                errorMessage = "Nejste připojeni k internetu.";
            }
            showError = true;
        }
    }

    let username = $state("");
    let password1 = $state("");
    let password2 = $state("");
    let email = $state("");
    let passwordsMatch = $derived(password1 == password2);
    let startedTyping = $derived(password1.length > 0 && password2.length > 0);

    let showToast = $state(false);
    let toastMessage = $state("");
    let showError = $state(false);
    let errorMessage = $state("");

</script>
{#if User.loggedIn}
    <div class="centerBox">
        <h1>Můj účet</h1>
        <h2>Úprava údajů:</h2>
        <details>
            <summary>Změnit Uživatelské jméno</summary>
            <label for="username">Zadejte svoje nové uživatelské jméno</label> <br>
            <input bind:value={username} id="username" type="text">
            {#if username === User.name}
                <p>Jméno, které jste napsali, se shoduje s vaším stávajícím jménem.</p>
            {/if}
            <button disabled={username === User.name} onclick={() => confirmUserDataChange(() => User.changeName(username), "Uživatelské jméno bylo změněno", "Nastala chyba. Zkuste to později.")}>Potvrdit</button>
        </details>
        <details>
            <summary>Změnit heslo</summary>
            <form autocomplete="off"></form>
            <label for="password">Zadejte svoje nové heslo&nbsp;&nbsp;</label> 
            <input bind:value={password1} class:ok={passwordsMatch && startedTyping} id="password" name="heslo" autocomplete="new-password" type="password"> <br> <br>
            <label for="password2">Ještě jednou pro kontrolu</label> 
            <input bind:value={password2} class:ok={passwordsMatch && startedTyping} id="password2" name="heslo2" autocomplete="new-password" type="password"> <br> <br>
            {#if passwordsMatch && startedTyping}
                <p>Shoduje se to, můžete to potvrdit :) ⬇️</p>
            {:else if startedTyping}
                <p>Hesla se neshodují!</p>
            {/if}
           
            <button 
            onclick={() => confirmUserDataChange(() => User.changePassword(password1), "Heslo bylo změneno", "Nastala chyba. Zkuste to později.")}
            disabled={!(passwordsMatch && startedTyping)}>Potvrdit</button>
        </details>
        <details>
            <summary>Změnit email</summary>
            <label for="email">Zadejte svoji novou emailovou adresu</label> <br>
            <input bind:value={email} id="email" type="email">
            <button onclick={() => confirmUserDataChange(() => User.changeEmail(email), "Emailová adresa byla změněna", "Nastala chyba. Zkuste to později.")}>Potvrdit</button>
        </details>
        <button onclick={() => showDeleteAccountPrompt = true}>Smazat účet</button>
    </div>
    
{:else}
    <h1 class="center">Pro zobrazení se přihlaste</h1>
{/if}

{#if showDeleteAccountPrompt}
    <Confirm bind:show={showDeleteAccountPrompt} okCallback={deleteUserGui}>Opravdu chcete smazat účet? Tato akce není vratná!</Confirm>
{/if}

{#if showDeleteConfirmation}
    <Toast>Účet smazán</Toast>
{/if}

{#if showToast}
    <Toast>{toastMessage}</Toast>
{/if}

{#if showError}
    <Alert bind:show={showError}>{errorMessage}</Alert>
{/if}

<style>
.ok{
    outline: 2px solid #00ff0078;
    border-radius: 4px;
}
.centerBox{
    margin: auto;
    max-width: 500px;
    width: 100%;
}
/* CSS from https://developer.mozilla.org/en-US/docs/Web/HTML/Element/summary */
details {
  border: 1px solid #aaa;
  border-radius: 4px;
  padding: 0.5em 0.5em 0;
  margin-bottom: 20px;
}

summary {
  font-weight: bold;
  margin: -0.5em -0.5em 0;
  padding: 0.5em;
  font-size: 1.2rem;
}

details[open] {
  padding: 0.5em;
}

details[open] summary {
  border-bottom: 1px solid #aaa;
  margin-bottom: 0.5em;
}

/* The same vertical margin as button's padding - to minimize layout shift when {#if username === User.name} block comes up
(If I put this into input padding, it would look weirdly "tall")*/
input{
    margin: 0.6rem auto;
}
</style>
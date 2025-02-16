<script>
    import { User, wait } from "$lib/shared.svelte";
    import Confirm from "$lib/Confirm.svelte";
    import Toast from "$lib/Toast.svelte";
    let showDeleteAccountPrompt = $state(false);
    let showDeleteConfirmation = $state(false);
    async function deleteUserGui(){
        let deleted = await User.delete();
        if(deleted){
            showDeleteConfirmation = true;
            User.logout();
            await wait(2600);
            showDeleteConfirmation = false;
        }
    }
</script>
{#if User.loggedIn}
    <div class="center">
        <button onclick={() => showDeleteAccountPrompt = true}>Smazat účet</button>
    </div>
    
{:else}
    <h1>Pro zobrazení se přihlaste</h1>
{/if}

{#if showDeleteAccountPrompt}
    <Confirm bind:show={showDeleteAccountPrompt} okCallback={deleteUserGui}>Opravdu chcete smazat účet? Tato akce není vratná!</Confirm>
{/if}

{#if showDeleteConfirmation}
    <Toast>Účet smazán</Toast>
{/if}
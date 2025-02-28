<script lang="ts">
    import { PUBLIC_API_BASE_URL } from '$env/static/public';
    import { freeplayCreatePost, freePlayGameObject, User } from "$lib/shared.svelte";
</script>
{#if User.loggedIn}
    <div class="center">
        <h2>Vytvoření Friendly hry</h2>
        <p>Vygenerujte si kód hry, který pak nasdílíte spoluhráči</p>
        {#if freePlayGameObject.loaded}
            <p>Kód je {freePlayGameObject.code}</p>
            <p>Na hru se připojte <a href="?code={freePlayGameObject.code}">odkazem</a>, který obsahuje kód</p>
        {/if}
        <button onclick={() => freeplayCreatePost()}>Vygenerovat kód</button>
    </div>
{/if}
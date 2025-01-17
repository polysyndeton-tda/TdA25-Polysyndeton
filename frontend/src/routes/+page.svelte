<script>
    import GamePicker from "$lib/GamePicker.svelte";
    document.title = "TdA - Úlohy";
</script>
<h1 class="center">Úlohy</h1>

<div class="container">
    <GamePicker></GamePicker>
</div>

<style>
    .container {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
</style>
<!-- <p>Visit <a href="https://svelte.dev/docs/kit">svelte.dev/docs/kit</a> to read the documentation</p>

<a href="./game/">about</a> -->
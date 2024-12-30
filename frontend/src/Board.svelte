<script>
    let {boardApiInfo} = $props();
</script>

<div class="grid">
{#each boardApiInfo.board as row}
    <div class="row">
        {#each row as field }
            {#if field == ""}
                <div class="field"></div>
            {:else if field == "X"}
                <div class="field X"></div>
            {:else if field == "O"}
                <div class="field O"></div>
            {/if}
        {/each}
    </div>
{/each}
</div>


<style>
    .grid{
        display: flex;
        flex-direction: column;
        gap: 1.5px;
        width: 100%;
        max-width: 500px;
        background: #6495ed80; /*#ffffff26*/
        margin: 0 auto;
    }
    .row{
        display: flex;
        flex-direction: row;
        gap: 1.5px;
    }
    .field{
        aspect-ratio: 1/1;
        width: calc(100% / 15);
        background: black;
    }
    .O{
        background-image: url(./assets/O_cervene.svg);
        background-size: 85% 85%;
        background-repeat: no-repeat;
        background-position: center; 
    }
    .X{
        background-image: url(./assets/X_modre.svg);
        background-size: 85% 85%;
        background-repeat: no-repeat;
        background-position: center; 
    }
</style>
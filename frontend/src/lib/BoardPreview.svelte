<script>
    let { boardApiInfo } = $props();
</script>

<div class="grid">
    {#each boardApiInfo.board as row, rowIndex}
        <div class="row">
            {#each row as field, columnIndex}
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
    .grid {
        display: flex;
        flex-direction: column;
        gap: 1.5px;
        /*changed from
        width: 225px;
        min-width: 225px;
        to this: (see commit 77731e557c317eeb60ba8542c761e099127b0721) */
        background: #6495ed80;
        width: 50vw;
        max-width: 225px;
    }
    .row {
        display: flex;
        flex-direction: row;
        gap: 1.5px;
    }
    .field {
        aspect-ratio: 1/1;
        width: calc(100% / 15);
        background-color: #F6F6F6;
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

    @media (prefers-color-scheme: dark) {
       .field{
            background-color: black;
       }
    }
</style>
<script>
    import { difficultyMapToCZ, filterToCZ, filterToEN } from "./shared.svelte.js";
    import { onMount, untrack } from "svelte";
    let { filterState = $bindable() } = $props();
    let difficultyLevelsSelected = $derived(filterState.filters.difficulty);
    console.log("init state", $state.snapshot(filterState.filters.difficulty))
    const allDifficultyLevels = ["beginner", "easy", "medium", "hard", "extreme"];
    let displayList = $state(Array(5).fill(false));
    onMount(() => {
        console.log("run")
        let a = difficultyLevelsSelected;
        for(const [index, value] of allDifficultyLevels.entries()){
            console.log(value, a, a.includes(value));
            if(a.includes(value)){
                displayList[index] = true;
            }else{
                displayList[index] = false;
            }
        }
    });
    //wanted to use filterState.filters.difficulty = $derived.by,
    //  but Svelte complained about invalid placement (yes, I know it is not a class field, come on)
    //So I had to come up with this...
    $effect(() => {
        console.log("ran")
        filterState.filters.difficulty = [];
        for(const [index, value] of displayList.entries()){
            console.log("e");
            untrack(() => {
                if(value == true){
                    filterState.filters.difficulty.push(allDifficultyLevels[index]);
                }
            });
        }
    });
</script>

<!--not possible to use function call in bind:
            an only bind to an Identifier or MemberExpression or a `{get, set}` pair
            https://svelte.dev/e/bind_invalid_expressionsvelte(bind_invalid_expression)
            src: https://github.com/sveltejs/svelte/issues/14341
            (difficulty level has at most 5 items, so it would have been OK)
             bind:checked={filterState.filters.difficulty.includes(difficultyLevel)} 
             
             => So, I came up with this onMount and $effect mess
             -->


<div class="filterContainer">
    <div>
        <h3>Obtížnost:</h3>
        {#each allDifficultyLevels as difficultyLevel, index}
            <label>
                <input type="checkbox" bind:checked={displayList[index]}>
                {difficultyMapToCZ[difficultyLevel]}
            </label>
            <br>
        {/each}
    </div>

    <div class="secondColumn">
        <label>
            <h3>Název hry: </h3>
            <input type="text" bind:value={filterState.filters.name}>
        </label>
        
        <label>

            <h3>Za dobu:</h3>
            <select onchange={(e) => {
                filterState.filters.date_filter = filterToEN[e.target.value];
            }}
            
            value={filterToCZ[filterState.filters.date_filter]}
            >
                <option>24 hodin</option>
                <option>7 dní</option>
                <option>1 měsíce</option>
                <option>3 měsíců</option>
                <option>neomezenou</option>
            </select>
        </label>
    </div>
</div>



<style>
    label, input, select{
        font-family: 'Dosis'; /*for select*/
        font-size: 1.2rem;
        letter-spacing: 0.5px;
        font-weight: 500;
    }
    .filterContainer{
        display: flex;
        align-items: baseline;
        gap: 25px;
        padding-bottom: 20px;
    }
    .secondColumn{
        display: flex; 
        flex-direction: column;
    }
    h3{
        font-size: 1.2rem;
        letter-spacing: 0.5px;
        font-weight: 700;
    }
</style>
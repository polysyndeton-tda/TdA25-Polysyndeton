<script>
    import { difficultyMapToCZ, filterToCZ, filterToEN } from "./shared.svelte.ts";
    import { onMount, untrack } from "svelte";
    let { filterState = $bindable() } = $props();

    let difficultyLevelsSelected = $derived(filterState.filters.difficulty);
    console.log("init state", $state.snapshot(filterState.filters.difficulty))

    const allDifficultyLevels = ["beginner", "easy", "medium", "hard", "extreme"];
    let displayList = $state(Array(5).fill(false));

    // `$derived(...)` can only be used as a variable declaration initializer or a class field
    // https://svelte.dev/e/state_invalid_placement
    //so this can't be: filterState.used = $derived(displayList.length)
    //so, $effect is it again...
    let used = $derived.by(() => {
        //all checkboxes checked or none checked
        let allDifficulitesPermitted = (filterState.filters.difficulty.length == allDifficultyLevels.length) || filterState.filters.difficulty.length == 0;
        if(  allDifficulitesPermitted
           && filterState.filters.name == ""
           && filterState.filters.date_filter == ""
        ){
            console.log("filter not active")
            return false;
        }
        console.log("filter active")
        return true;
    });

    $effect(() => {
        filterState.used = used;
    });

    onMount(() => {
        console.log("initialise displayList for checkboxes to use")
        let a = difficultyLevelsSelected;
        for(const [index, value] of allDifficultyLevels.entries()){
            // console.log(value, $state.snapshot(a), a.includes(value));
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
        console.log("build allowed difficulty list to send to API")
        filterState.filters.difficulty = [];
        for(const [index, value] of displayList.entries()){
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
        <fieldset> <!-- https://stackoverflow.com/questions/10469256/how-to-force-a-checkbox-and-text-on-the-same-line -->
        {#each allDifficultyLevels as difficultyLevel, index}
            <div style="display: inline;white-space: nowrap;">
                <label>
                    <input type="checkbox" bind:checked={displayList[index]}>
                    {difficultyMapToCZ[difficultyLevel]}
                </label>
            </div>
            <br>
        {/each}
        </fieldset>
    </div>

    <div class="secondColumn">
        <label>
            <h3>Název hry: </h3>
            <input class="textfield" type="text" bind:value={filterState.filters.name}>
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
    .textfield{
        min-width: 10ch;
        width: 95%;
        box-sizing: border-box;
    }
    .filterContainer{
        align-items: baseline;
        gap: 10px;
        padding-bottom: 20px;
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        /* 100% instead of 100vw because 
        Currently all browsers but Firefox incorrectly consider 100vw to be the entire page width,
        including vertical scroll bar, which can cause a horizontal scroll bar when overflow: auto is set
        https://caniuse.com/viewport-units
        https://stackoverflow.com/questions/23367345/100vw-causing-horizontal-overflow-but-only-if-more-than-one
        */
        width: 100%;
        margin: 0 auto;
        max-width: 500px;
        padding: 10px;
        box-sizing: border-box;
    }
    h3{
        font-size: 1.2rem;
        letter-spacing: 0.5px;
        font-weight: 700;
    }
</style>
<script>
    import { difficultyMapToCZ, difficultyMapToNumber } from "$lib/shared.svelte.ts";
    import StarRating from 'svelte-star-rating';
    let { difficulty } = $props(); //game.difficulty
    const config = {
        emptyColor: 'hsl(240, 80%, 85%)',
        fullColor:  '#E31837',
        showText: false,
        size: 22,
    };
    const style = 'justify-content:center;padding: 10px 0 0 10px;';
</script>
<!-- div title for tooltip on hover  -->
<div title={difficultyMapToCZ[difficulty]}><StarRating rating={difficultyMapToNumber[difficulty]} {config} {style} /></div>
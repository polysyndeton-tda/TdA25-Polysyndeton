<script>
    import { cubicOut } from 'svelte/easing';
    let { children } = $props();

    /*A replacement for the previous CSS animation as a Svelte animation (plays nicely with conditional rendering)*/
    
    // #snackbar.show {
    // visibility: visible; /* Show the snackbar */
    // /* Add animation: Take 0.5 seconds to fade in and out the snackbar.
    // However, delay the fade out process for 2.5 seconds */
    // animation: fadein 0.5s, fadeout 0.5s 2.5s;
    // }
    
    /*
      @keyframes fadein {
        from {bottom: 0; opacity: 0;}
        to {bottom: 30px; opacity: 1;}
      }

      @keyframes fadeout {
        from {bottom: 30px; opacity: 1;}
        to {bottom: 0; opacity: 0;}
      }
    
    */
    function slideAndFade(node, { duration = 400 }) {
        return {
            duration,
            css: (t) => {
            const eased = cubicOut(t);
            return `
                opacity: ${t};
                bottom: ${30 * eased}px;
            `;
            }
        };
    }
</script>

<div transition:slideAndFade|global id="snackbar">{@render children()}</div> <!-- class="show" -->


<style>
    /* The snackbar - position it at the bottom and in the middle of the screen */
    #snackbar {
        /*visibility:hidden removed with the change to svelte/easing (slideAndFade)*/
        /* visibility: hidden; Hidden by default. Visible on click */
        min-width: 250px; /* Set a default minimum width */
        margin-left: -125px; /* Divide value of min-width by 2 */
        background-color: #333; /* Black background color */
        color: #fff; /* White text color */
        text-align: center; /* Centered text */
        border-radius: 2px; /* Rounded borders */
        padding: 16px; /* Padding */
        position: fixed; /* Sit on top of the screen */
        z-index: 1; /* Add a z-index if needed */
        left: 50%; /* Center the snackbar */
        bottom: 30px; /* 30px from the bottom */
        font-size: 1.2rem;
    }
</style>
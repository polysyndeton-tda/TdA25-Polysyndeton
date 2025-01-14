<script>
    import { gameInfo, resetGame } from '$lib/shared.svelte';

	let { children } = $props();
</script>

<nav>
  <!-- smarter linking needed = because ./ goes up a folder both on page/ and on page/uuid   => sometimes it goes up only to page/ -->
   <!-- snad to je dost chytry, aby to pochopilo, ze / ma byt na nas root pokud bude stranka hostovana na /nejaka-podstranka/ -->
    <!-- stejne tak s /game kdyz to bude /nejaka-podstranka/game -->
  <!-- TODO: Fix Think different text and Game text to be aligned vertically -->
	<a aria-label="Think different academy homepage" href="/">
    <picture>
      <!-- User prefers light mode: -->
      <source srcset="/Think-different-Academy_LOGO_oficialni-bile.svg" media="(prefers-color-scheme: light)"/>
    
      <!-- User prefers dark mode: -->
      <source srcset="/Think-different-Academy_LOGO_oficialni_1_dark-mode.svg"  media="(prefers-color-scheme: dark)"/>
    
      <!-- User has no color preference: -->
      <img alt="Think different academy logo" src="Think-different-Academy_LOGO_oficialni-cerne.svg"/>
    </picture>
  </a>
	<a class="menuItem" href="/game" onclick={resetGame}>Nová hra</a>
</nav>

<div id="app">
{@render children()}
</div>

<style>
  :root {
      --menu-item-hover-color: white;
      --tda-logo-hover-color: #cbd0d69c; /*#171515c7;*/
  }

  @media (prefers-color-scheme: dark) {
    :root {
      --menu-item-hover-color: #0070bb; 
      --tda-logo-hover-color: goldenrod;
    }
  }

  nav{
    padding-top: 8px;
    /*padding-bottom: 18px;*/
  }

  /*The light bulb lighting up effect on hover */
  nav img {
    transition: filter 0.2s ease-in-out;
  }

  nav img:hover {
    filter: drop-shadow(0 0 8px var(--tda-logo-hover-color)); /*rgba(216, 178, 25, 0.6)*/
  }


  /*A cool underline effect when hovering on links*/
  .menuItem {
    font-weight: 700;
    color: white; /*#646cff #535bf2*/
    text-decoration: inherit;
  }
  .menuItem {
    position: relative;
    text-decoration: none;
  }
  
  .menuItem::after {
    content: '';
    position: absolute;
    width: 100%;
    transform: scaleX(0);
    height: 2px;
    bottom: 0;
    left: 0;
    background-color: var(--menu-item-hover-color);
    transform-origin: bottom right;
    transition: transform 0.25s ease-out;
  }
  
  .menuItem:hover::after {
    transform: scaleX(1);
    transform-origin: bottom left;
  }
  .menuItem:hover::after {
    transform: scaleX(1);
    transform-origin: bottom left;
  }
  
  .menuItem::after {
    content: '';
    position: absolute;
    width: 100%;
    transform: scaleX(0);
    height: 2px;
    bottom: 0;
    left: 0;
    background-color: var(--menu-item-hover-color);
    transform-origin: bottom left;
    transition: transform 0.25s ease-out;
  }

</style>
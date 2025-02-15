<script>
  import Login from '$lib/Login.svelte';
  import { gameInfo, resetGame, User } from '$lib/shared.svelte';
	let { children } = $props();
  let showLoginPopup = $state(false);

  let isDropdownOpen = $state(false);

  function toggleDropdown(){
    isDropdownOpen = !isDropdownOpen;
  }

  const handleClickOutside = (e) => {
    //check to make it so clicks inside the dropdown don't necessarily close it
    if (!e.target.closest('.dropdown')) {
      isDropdownOpen = false;
    }
  }
</script>
<link rel="stylesheet"  href="/fontawesome/css/all.css">
<svelte:window on:click={handleClickOutside}/>
<nav>
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

  <!-- The login button and menu -->
  {#if !User.loggedIn}
    <button onclick={() => showLoginPopup = true} class="right">Přihlásit se</button>
  {:else}
    <div class="dropdown right">
      <button onclick={toggleDropdown}> <i class="fa-solid fa-user"></i> {User.name}</button>
      {#if isDropdownOpen}
        <div class="dropdown-menu">
          <button onclick={() => {
            User.logout();
            isDropdownOpen = false;
          }}>Odhlásit</button>
        </div>
      {/if}
    </div>
  {/if}
</nav>

<div id="app">
{@render children()}
</div>

{#if showLoginPopup}
  <Login bind:show={showLoginPopup}/>
{/if}

<style>
  :root {
      --menu-item-hover-color: white;
      --tda-logo-hover-color: #cbd0d69c; /*#171515c7;*/
      --dropdown-bgcolor: #0257a5;
  }

  nav{
    display: flex;
    gap: 26px;
    font-size: 1.3rem;
    height: 90px;
    color: white;
    align-items: center;
    padding-top: 8px;
    padding-left: 10px;
    padding-right: 10px;
  }

  nav img {
      min-width: 200px;
      width: auto;
      object-fit: contain;
      padding: 5px;
      translate: 0 10px;
      /*The light bulb lighting up effect on hover */
      transition: filter 0.2s ease-in-out;
  }

  nav img:hover {
    filter: drop-shadow(0 0 8px var(--tda-logo-hover-color)); /*rgba(216, 178, 25, 0.6)*/
  }

  nav .right{
    margin-left: auto;
  }

  nav a:first-of-type {
    padding-left: 16px;
    /* Add this to ensure proper link sizing */
    display: flex;  
    align-items: center;
    color: white;
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

  .dropdown-menu {
    position: absolute;
    right: 0;
    min-width: 160px;
    text-align: center;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    padding-top: 10px;
    padding-bottom: 10px;
    margin-top: 5px;
    background-color: var(--dropdown-bgcolor);
  }

  @media (prefers-color-scheme: dark) {
    :root {
      --menu-item-hover-color: #0070bb; 
      --tda-logo-hover-color: goldenrod;
    }
    .dropdown-menu{
      --dropdown-bgcolor: #43414196;
      box-shadow: 0 2px 5px #b1b0b091;
    }
  }
</style>
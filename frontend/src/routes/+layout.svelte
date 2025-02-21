<script lang="ts">
	import '../app.css';
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
<link rel="stylesheet" href="/fontawesome/css/all.css">

<svelte:window on:click={handleClickOutside}/>
<nav>
	<!-- TODO: Fix Think different text and Game text to be aligned vertically -->
	<a aria-label="Think different academy homepage" href="/">
	  <picture style="display: flex;">
		<!-- User prefers light mode: -->
		<source srcset="/Think-different-Academy_LOGO_oficialni-bile.svg" media="(prefers-color-scheme: light)"/>
	  
		<!-- User prefers dark mode: -->
		<source srcset="/Think-different-Academy_LOGO_oficialni_1_dark-mode.svg"  media="(prefers-color-scheme: dark)"/>
	  
		<!-- User has no color preference: -->
		<img alt="Think different academy logo" src="Think-different-Academy_LOGO_oficialni-cerne.svg"/>
	  </picture>
	</a>
	<!-- <a class="menuItem" href="/game" onclick={resetGame}>Nová hra</a> -->
  
	<!-- The login button and menu -->
	{#if !User.loggedIn}
	  <button onclick={() => showLoginPopup = true} class="right">Přihlásit se</button>
	{:else}
	  <div class="dropdown right">
		<button onclick={toggleDropdown}> <i class="fa-solid fa-user"></i> {User.name}</button>
		{#if isDropdownOpen}
		  <div class="dropdown-menu">
			<a onclick={() => isDropdownOpen = false} class="button" href="/my-profile"><i class="fa-solid fa-gear"></i> Můj profil</a>
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
<br>
<footer class="center">© Think Different Academy 2025 | <a href="/gdpr">Prohlášení o ochraně osobních údajů (GDPR)</a> |  <a href="/contacts">Kontakty</a> </footer>

{#if showLoginPopup}
  <Login bind:show={showLoginPopup}/>
{/if}

<style>
  footer a{
    color: unset;
  }
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
    color: black;
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

    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
  }

  .button{
    display: block;
    border-radius: 8px;
    border: 1px solid transparent;
    padding: 0.6em 1.2em;
    font-size: 1.2rem;
    font-weight: 535;
    font-family: inherit;
    cursor: pointer;
    transition: border-color 0.25s;
    text-decoration: none;
    background-color: #f6f6f6;
    color: black;
    width: fit-content;
    /* for font awesome which makes it a flex container but doesn't add gap */
    gap: 5px;
  }
  button:hover {
    border-color: #0070BB; /*#646cff;*/ /*#535bf2;*/
  }
  .button:focus,
  .button:focus-visible {
    outline: 4px auto -webkit-focus-ring-color;
  }

  @media (prefers-color-scheme: light) {
    /*In light theme in blue header nav => lighter than other light theme buttons
    In dark theme the header nav is transparent => inherit from global button styles*/
    .dropdown button{
      background-color: #f6f6f6;
    }
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

    .button {
        background-color: #1a1a1a;
        color: white;
    }
    nav a:first-of-type {
      color: white;
    }
  }
</style>
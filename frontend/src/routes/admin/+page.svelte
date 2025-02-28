	
<script lang="ts">
    import DataTable from "./data-table.svelte";
    import * as ContextMenu from "$lib/components/ui/context-menu/index.js";
    import { columns } from "./columns.js";
    import { onMount } from "svelte";
    import { classList } from "$lib/classList";
    import { User } from "$lib/shared.svelte.ts";

    type UserAPI = {
        uuid: string;
        createdAt: string;
        username: string;
        email: string;
        elo: number;
        wins: number;
        draws: number;
        losses: number;
    };
 
    let data : UserAPI[] | undefined = $state();
    let loaded = $state(false);
  
  async function load() {
    data = await User.getUsers();
    console.log("data from db", $state.snapshot(data));
    //Convert all numerical values to strings
    data.map((object) => {
        // type NumericalKeys = keyof Pick<UserAPI, 'elo' | 'wins' | 'draws' | 'losses'>;
        const keysWithNumericalValues = ["elo", "wins", "draws", "losses"] as const; //const keysWithNumericalValues: (keyof UserAPI)[] : NumericalKeys[]
        for(let key of Object.keys(object) as Array<keyof UserAPI>){
            if(keysWithNumericalValues.includes(key as typeof keysWithNumericalValues[number])){
                (object[key] as string) = String(object[key]);
            }
        }
        console.log($state.snapshot(object));
        return object;
    });
    loaded = true;
  }
  onMount(load);
 

  //as these two variables are not used in any templating, I believe the warnings are not relevant
  let table: any; //reference to the table, not supposed to be reactive
  let selected: { //bound state from the table (there is an $effect inside updating this) = it is reactive although svelte complains
    property: true
  };

  let deletedUsersToBeSentToServer = [];

  function deleteUsers(){
    console.log("delete", $state.snapshot(selected));

    let rows = new Set(Object.keys(selected).map(Number));

    //To build deletedUsersToBeSentToServer either traverse array twice with 2 filter calls
    deletedUsersToBeSentToServer = data
        .filter((_, index) => rows.has(index))
        .map(user => user.uuid);
    
    data = data.filter((_, index) => !rows.has(index));
    //Or do it with a for loop and data = [...data] to trigger reactivity
 
    console.log(deletedUsersToBeSentToServer, $state.snapshot(data));
    table.toggleAllPageRowsSelected(false);
  }
  
</script>
<!-- adds the admin class to body on this page => which right now tells to turn off dark theme -->
<svelte:body use:classList={"admin"} />

<!-- to avoid errors about data being undefined => render only after data was fetched -->
{#if User.loggedIn && User.isAdmin}
    {#if loaded} 
         <!-- to enable tailwind for this shadcn component, while keeping tailwind off everywhere else -->
        <div data-admin="true" class="twp">
        <ContextMenu.Root>
            <ContextMenu.Trigger><DataTable classesToSet="w-[calc(100%-10px)] m-auto" bind:tableReference={table} bind:selectedRows={selected} {data} {columns} /></ContextMenu.Trigger>
            <ContextMenu.Content>
            <ContextMenu.Item onclick={deleteUsers}>Smazat</ContextMenu.Item>
            <ContextMenu.Item>Editovat</ContextMenu.Item>
            </ContextMenu.Content>
        </ContextMenu.Root>
        </div>
    {/if}
{:else}
    <h2 style="text-align:center">Pro přístup do Správy uživatelů (=Administrátorského panelu) je potřeba se <a href="../login">přihlásit</a> administrátorským účtem</h2>
{/if}

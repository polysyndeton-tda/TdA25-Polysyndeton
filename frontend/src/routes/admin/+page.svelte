	
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
  let bannedUsersToBeSentToServer = [];
  let usersToEdit = [];

  async function deleteUsers() {
    console.log("delete", $state.snapshot(selected));

    let rows = new Set(Object.keys(selected).map(Number));

    deletedUsersToBeSentToServer = data
      .filter((_, index) => rows.has(index))
      .map(user => user.uuid);

    data = data.filter((_, index) => !rows.has(index));

    console.log("Users to delete:", deletedUsersToBeSentToServer);
    console.log("Updated data:", $state.snapshot(data));

    table.toggleAllPageRowsSelected(false);

    for (const uuid of deletedUsersToBeSentToServer) {
      try {
        console.log(`Sending DELETE request for user ${uuid}...`);
        const response = await fetch(`/api/v1/users/${uuid}`, {
          method: 'DELETE',
        });

        console.log(`Response for user ${uuid}:`, response);

        if (response.ok) {
          if (response.status === 204) {
            console.log(`User ${uuid} deleted successfully.`);
          } else {
            const result = await response.json();
            console.log(`User ${uuid} deleted successfully:`, result.message);
          }
        } else {
          console.error(`Failed to delete user ${uuid}:`, response.statusText);
        }
      } catch (error) {
        console.error(`Error deleting user ${uuid}:`, error);
      }
    }
  }

  async function editUser() {
    console.log("edit", $state.snapshot(selected));

    let rows = new Set(Object.keys(selected).map(Number));

    usersToEdit = data
      .filter((_, index) => rows.has(index))
      .map(user => user.uuid);

    if (usersToEdit.length !== 1) {
      alert("Please select exactly one user to edit.");
      return;
    }

    const uuid = usersToEdit[0];

    const newUsername = prompt("Enter new username:");
    const newEmail = prompt("Enter new email:");
    const newElo = prompt("Enter new Elo:");

    if (!newUsername || !newEmail || !newElo) {
      alert("All fields are required.");
      return;
    }

    const updatedData = {
      username: newUsername,
      email: newEmail,
      elo: newElo,
    };

    try {
      const response = await fetch(`/api/v1/users/${uuid}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(updatedData),
      });

      if (response.ok) {
        const result = await response.json();
        console.log(`User ${uuid} updated successfully:`, result);

        const updatedUserIndex = data.findIndex(user => user.uuid === uuid);
        if (updatedUserIndex !== -1) {
          data[updatedUserIndex] = { ...data[updatedUserIndex], ...updatedData };
          console.log("Updated data:", $state.snapshot(data));
        }

        alert("User updated successfully!");
      } else {
        const error = await response.json();
        console.error(`Failed to update user ${uuid}:`, error.message);
        alert(`Failed to update user: ${error.message}`);
      }
    } catch (error) {
      console.error(`Error updating user ${uuid}:`, error);
      alert("An error occurred while updating the user.");
    }
  }

  async function banUsers() {
    console.log("ban", $state.snapshot(selected));

    let rows = new Set(Object.keys(selected).map(Number));

    bannedUsersToBeSentToServer = data
        .filter((_, index) => rows.has(index))
        .map(user => user.uuid);

    data = data.filter((_, index) => !rows.has(index));

    console.log(bannedUsersToBeSentToServer, $state.snapshot(data));

    table.toggleAllPageRowsSelected(false);

    for (const uuid of bannedUsersToBeSentToServer) {
        try {
        const response = await fetch('/api/v1/ban', {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json',
            },
            body: JSON.stringify({ uuid: uuid }),
        });

          if (response.ok) {
            const result = await response.json();
            console.log(`User ${uuid} banned successfully:`, result.message);
        } else {
            console.error(`Failed to ban user ${uuid}:`, response.statusText);
        }
        } catch (error) {
        console.error(`Error banning user ${uuid}:`, error);
        }
    }
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
            <ContextMenu.Item onclick={editUser}>Edit</ContextMenu.Item>
            <ContextMenu.Item onclick={banUsers}>Ban</ContextMenu.Item>
            </ContextMenu.Content>
        </ContextMenu.Root>
        </div>
    {/if}
{:else}
    <h2 style="text-align:center">Pro přístup do Správy uživatelů (=Administrátorského panelu) je potřeba se <a href="../login">přihlásit</a> administrátorským účtem</h2>
{/if}

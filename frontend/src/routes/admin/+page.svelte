<script>
    import Login from "$lib/Login.svelte";
    import { User, getUsers } from "$lib/shared.svelte.js";
    import { onMount } from "svelte";

    let users = $state();
    let loaded = $state(false);

    async function load(){
        users = await getUsers();
        console.log("users", users);
        loaded = true;
    }

    onMount(load);
</script>


<div class="centerBox">
    <h1>Admin</h1>    

    {#if User.loggedIn}
        {#if loaded}
        <table>
            <tbody> 
                <tr>
                    <th>Vytvořen:</th>
                    <th>Jméno:</th>
                    <th>Email:</th>
                    <th>ELO:</th>
                    <th>Výhry:</th>
                </tr>
                {#each users as user}
                    <tr>
                        <td>{user.createdAt}</td>
                        <td>{user.username}</td>
                        <td>{user.email}</td>
                        <td>{user.elo}</td>
                        <td>{user.wins}</td>
                    </tr>
                {/each}
            </tbody>
        </table>
        {/if}
    {:else}
        <Login floating={false} mode="login"/>
    {/if}
</div>
<style>
   .centerBox{
    display: flex;
    flex-direction: column;
    align-items: center;
   }
</style>
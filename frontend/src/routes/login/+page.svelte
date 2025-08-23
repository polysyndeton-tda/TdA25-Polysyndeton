<script>
    import Login from "$lib/Login.svelte";
    import { page } from '$app/state';
    function redirectIfInURL(){
        let redirect = page.url.searchParams.get("returnURL");
        console.log("page search (=query) params are", redirect, page.url.searchParams);
        if(redirect){
            console.log("Redirect to:", redirect);
            window.location.href = redirect;
        }
    }
</script>

<Login floating={false} onSuccess={redirectIfInURL}/>
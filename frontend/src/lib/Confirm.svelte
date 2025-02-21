<script>
    import { scale } from 'svelte/transition';
    let { show = $bindable(), children, okCallback } = $props();

    function addFocus(node){
        node.focus();
    }

    function confirm(){
        okCallback();
        close();
    }

    function close(){
        show = false;
    }
</script>

<div in:scale={{ duration: 75}} out:scale={{ duration: 95}} class="popup-container">
    <div class="popup">
        <div class="title">
            <h2>{@render children()}</h2>
        </div>
        <div>
            <button class="ok" use:addFocus onclick={confirm}>OK</button>
            <button onclick={close}>Zrušit</button>
        </div>
    </div>
</div>


<style>
.popup-container{
    position: fixed;
    top: 0;
    height: 100%;
    width: 100%;
    display: flex;
    inset-inline-start: 0px;
    align-items: center;
    justify-content: center;
}
.popup{
    display: flex;
    justify-content: center;
    align-items: center;
    display: flex;
    flex-direction: column;
    gap: 10px;
    border-radius: 8px;
    filter: drop-shadow(0 0 8px var(--menu-item-hover-color));
    padding: 0 0 10px 0;
}
.title{
    border-radius: 8px;
    padding: 10px;
}

h2{
    overflow-wrap: anywhere;
    max-width: 80vw;
}

@media (prefers-color-scheme: light){
    h2{
        color: white;
    }
    .title{
        background-color: #0257a5;
    }
    .popup{
        background: #739bc5; /*#76aeea;*/
        box-shadow: rgba(100, 100, 111, 1) 0px 7px 29px 0px;
    }
}

@media (prefers-color-scheme: dark){
    .title{
        background-color: #101010; /*#242424*/
    }
    .popup{
        background-color: #434343;
    }
}
/* fix from https://stackoverflow.com/questions/30282921/fixed-pop-up-div-gets-overlapped-by-keyboard */
@media (max-width: 767px) {
    .popup-container {
        width: 100%;
        top: 10px;
        bottom: 0px;    
        overflow-y: auto;
        max-height: 100%;
    }
}
</style>
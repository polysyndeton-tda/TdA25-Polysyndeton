<script>
    import { scale } from 'svelte/transition';
    let { show = $bindable(), okCallback} = $props();

    function addFocus(node){
        node.select();
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
            <div class="top-bar">
                <h2>Přihlásit se</h2> <button aria-labelledby="close" onclick={close}><i class="fa-solid fa-xmark"></i></button>
            </div>
            <table>
                <tbody>
                    <tr>
                        <td>
                            <label for="email">E-mail:</label>
                        </td>
                        <td>
                            <input use:addFocus id="email" type="email">
                        </td>
                    </tr>

                    <tr>
                        <td>
                            <label for="password">Heslo:</label>
                        </td>
                        <td>
                            <input id="password" type="password">
                        </td>
                    </tr>
                    
                </tbody>
            </table>
            <p>Ještě nemáte účet? <a href="javascript:void(0);">Registrovat</a></p>
        </div>
        <div class="button-area">
            <button class="ok" onclick={confirm}>Přihlásit</button>
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
    width: 365px;
}
.title{
    border-radius: 8px;
    padding: 10px;
    width: 100%;
    box-sizing: border-box;
}

.top-bar{
    display: flex;
    justify-content: space-between;
    align-items: center;
}

h2{
    overflow-wrap: anywhere;
    max-width: 80vw;
    text-align: center;
    padding-left: 5px
}

table{
    border-collapse: separate;
    border-spacing: 10px 10px;
    margin: auto;
}

label, input{
    font-size: 1.2rem;
}

.button-area{
    text-align: center;
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
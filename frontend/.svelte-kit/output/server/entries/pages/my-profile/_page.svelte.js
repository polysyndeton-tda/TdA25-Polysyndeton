import { f as copy_payload, g as assign_payload, e as pop, p as push, I as attr, J as stringify } from "../../../chunks/index.js";
import { U as User } from "../../../chunks/shared.svelte.js";
/* empty css                                                    */
/* empty css                                                  */
/* empty css                                                  */
function _page($$payload, $$props) {
  push();
  let username = "";
  let password1 = "";
  let password2 = "";
  let email = "";
  let startedTyping = password1.length > 0 && password2.length > 0;
  let $$settled = true;
  let $$inner_payload;
  function $$render_inner($$payload2) {
    if (User.loggedIn) {
      $$payload2.out += "<!--[-->";
      $$payload2.out += `<div class="centerBox svelte-ialfom"><h1>Můj účet</h1> <h2>Úprava údajů:</h2> <details class="svelte-ialfom"><summary class="svelte-ialfom">Změnit Uživatelské jméno</summary> <label for="username">Zadejte svoje nové uživatelské jméno</label> <br> <input${attr("value", username)} id="username" type="text"> <button>Potvrdit</button></details> <details class="svelte-ialfom"><summary class="svelte-ialfom">Změnit heslo</summary> <form autocomplete="off"></form> <label for="password">Zadejte svoje nové heslo  </label> <input${attr("value", password1)} id="password" name="heslo" autocomplete="new-password" type="password"${attr("class", `svelte-ialfom ${stringify([startedTyping ? "ok" : ""].filter(Boolean).join(" "))}`)}> <br> <br> <label for="password2">Ještě jednou pro kontrolu</label> <input${attr("value", password2)} id="password2" name="heslo2" autocomplete="new-password" type="password"${attr("class", `svelte-ialfom ${stringify([startedTyping ? "ok" : ""].filter(Boolean).join(" "))}`)}> <br> <br> `;
      if (startedTyping) {
        $$payload2.out += "<!--[-->";
        $$payload2.out += `<p>Shoduje se to, můžete to potvrdit :) ⬇️</p>`;
      } else {
        $$payload2.out += "<!--[!-->";
        if (startedTyping) {
          $$payload2.out += "<!--[-->";
          $$payload2.out += `<p>Hesla se neshodují!</p>`;
        } else {
          $$payload2.out += "<!--[!-->";
        }
        $$payload2.out += `<!--]-->`;
      }
      $$payload2.out += `<!--]--> <button${attr("disabled", !startedTyping, true)}>Potvrdit</button></details> <details class="svelte-ialfom"><summary class="svelte-ialfom">Změnit email</summary> <label for="email">Zadejte svoji novou emailovou adresu</label> <br> <input${attr("value", email)} id="email" type="email"> <button>Potvrdit</button></details> <button>Smazat účet</button></div>`;
    } else {
      $$payload2.out += "<!--[!-->";
      $$payload2.out += `<h1 class="center">Pro zobrazení se přihlaste</h1>`;
    }
    $$payload2.out += `<!--]--> `;
    {
      $$payload2.out += "<!--[!-->";
    }
    $$payload2.out += `<!--]--> `;
    {
      $$payload2.out += "<!--[!-->";
    }
    $$payload2.out += `<!--]--> `;
    {
      $$payload2.out += "<!--[!-->";
    }
    $$payload2.out += `<!--]--> `;
    {
      $$payload2.out += "<!--[!-->";
    }
    $$payload2.out += `<!--]-->`;
  }
  do {
    $$settled = true;
    $$inner_payload = copy_payload($$payload);
    $$render_inner($$inner_payload);
  } while (!$$settled);
  assign_payload($$payload, $$inner_payload);
  pop();
}
export {
  _page as default
};

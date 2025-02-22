import { f as copy_payload, g as assign_payload } from "../../chunks/index.js";
/* empty css                                               */
/* empty css                                               */
function _page($$payload) {
  document.title = "TdA - Hlavní stránka";
  let $$settled = true;
  let $$inner_payload;
  function $$render_inner($$payload2) {
    $$payload2.out += `<div class="centerBox svelte-1p8pvvf"><h1><span class="player X svelte-1p8pvvf">X</span> Piškvorky <span class="player O svelte-1p8pvvf">O</span></h1> <h2>🔥Vyrobené s láskou v Česku 🇨🇿</h2> <h3>Hrajte:</h3> <a class="button svelte-1p8pvvf" href="/multiplayer">Online 🌐</a> <a class="button svelte-1p8pvvf" href="/game">Lokálně s kamarádem 🙋‍♀️</a></div> `;
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
}
export {
  _page as default
};

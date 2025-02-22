import { f as copy_payload, g as assign_payload, e as pop, h as escape_html, p as push } from "../../chunks/index.js";
import { U as User } from "../../chunks/shared.svelte.js";
/* empty css                                               */
/* empty css                                               */
function _layout($$payload, $$props) {
  push();
  let { children } = $$props;
  let $$settled = true;
  let $$inner_payload;
  function $$render_inner($$payload2) {
    $$payload2.out += `<link rel="stylesheet" href="/fontawesome/css/all.css"> <nav class="svelte-1fa5r32"><a aria-label="Think different academy homepage" href="/" class="svelte-1fa5r32"><picture style="display: flex;"><source srcset="/Think-different-Academy_LOGO_oficialni-bile.svg" media="(prefers-color-scheme: light)"> <source srcset="/Think-different-Academy_LOGO_oficialni_1_dark-mode.svg" media="(prefers-color-scheme: dark)"> <img alt="Think different academy logo" src="Think-different-Academy_LOGO_oficialni-cerne.svg" class="svelte-1fa5r32"></picture></a>  `;
    if (!User.loggedIn) {
      $$payload2.out += "<!--[-->";
      $$payload2.out += `<button class="right svelte-1fa5r32">Přihlásit se</button>`;
    } else {
      $$payload2.out += "<!--[!-->";
      $$payload2.out += `<div class="dropdown right svelte-1fa5r32"><button class="svelte-1fa5r32"><i class="fa-solid fa-user"></i> ${escape_html(User.name)}</button> `;
      {
        $$payload2.out += "<!--[!-->";
      }
      $$payload2.out += `<!--]--></div>`;
    }
    $$payload2.out += `<!--]--></nav> <div id="app">`;
    children($$payload2);
    $$payload2.out += `<!----></div> <br> <footer class="center svelte-1fa5r32">© Think Different Academy 2025 | <a href="/gdpr" class="svelte-1fa5r32">Prohlášení o ochraně osobních údajů (GDPR)</a> | <a href="/contacts" class="svelte-1fa5r32">Kontakty</a></footer> `;
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
  _layout as default
};

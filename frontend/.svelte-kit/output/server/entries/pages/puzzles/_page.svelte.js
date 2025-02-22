import "clsx";
import { f as copy_payload, g as assign_payload, e as pop, p as push } from "../../../chunks/index.js";
/* empty css                                                  */
/* empty css                                                    */
function GamePicker($$payload, $$props) {
  push();
  let $$settled = true;
  let $$inner_payload;
  function $$render_inner($$payload2) {
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
function _page($$payload) {
  document.title = "TdA - Úlohy";
  $$payload.out += `<h1 class="center">Úlohy</h1> `;
  GamePicker($$payload);
  $$payload.out += `<!---->`;
}
export {
  _page as default
};

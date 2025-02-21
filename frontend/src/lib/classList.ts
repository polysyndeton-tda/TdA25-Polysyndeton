import type { Action } from "svelte/action";
// https://github.com/sveltejs/svelte/issues/3105
export const classList: Action<Element, string | string[]> = (node, classes) => {
  const tokens = Array.isArray(classes) ? classes : [classes];
  node.classList.add(...tokens);

  return {
    destroy() {
      node.classList.remove(...tokens);
    },
  };
};
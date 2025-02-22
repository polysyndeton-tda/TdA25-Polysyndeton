

export const index = 8;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/multiplayer/_page.svelte.js')).default;
export const imports = ["_app/immutable/nodes/8.HJ_jm8f3.js","_app/immutable/chunks/Ba07GB51.js","_app/immutable/chunks/DcSgunAn.js","_app/immutable/chunks/dQE67XWY.js"];
export const stylesheets = [];
export const fonts = [];

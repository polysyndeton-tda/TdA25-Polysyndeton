export const manifest = (() => {
function __memo(fn) {
	let value;
	return () => value ??= (value = fn());
}

return {
	appDir: "_app",
	appPath: "_app",
	assets: new Set(["Dosis-VariableFont_wght.ttf","O_cervene.svg","O_cervene_cursor.svg","Think-different-Academy_LOGO_oficialni-bile.svg","Think-different-Academy_LOGO_oficialni-cerne.svg","Think-different-Academy_LOGO_oficialni_1_dark-mode.svg","X_modre.svg","X_modre_cursor.svg","app.css","eraser.png","eraser32.png","favicon.png","fontawesome/css/all.css","fontawesome/webfonts/fa-brands-400.ttf","fontawesome/webfonts/fa-brands-400.woff2","fontawesome/webfonts/fa-regular-400.ttf","fontawesome/webfonts/fa-regular-400.woff2","fontawesome/webfonts/fa-solid-900.ttf","fontawesome/webfonts/fa-solid-900.woff2","fontawesome/webfonts/fa-v4compatibility.ttf","fontawesome/webfonts/fa-v4compatibility.woff2"]),
	mimeTypes: {".ttf":"font/ttf",".svg":"image/svg+xml",".css":"text/css",".png":"image/png",".woff2":"font/woff2"},
	_: {
		client: {start:"_app/immutable/entry/start.BU4pOokq.js",app:"_app/immutable/entry/app.Ds5Tl-oz.js",imports:["_app/immutable/entry/start.BU4pOokq.js","_app/immutable/chunks/ylLvelAk.js","_app/immutable/chunks/DcSgunAn.js","_app/immutable/chunks/DM6u0xJB.js","_app/immutable/chunks/y0YWbF4N.js","_app/immutable/entry/app.Ds5Tl-oz.js","_app/immutable/chunks/DcSgunAn.js","_app/immutable/chunks/BK38orX7.js","_app/immutable/chunks/Ba07GB51.js","_app/immutable/chunks/D_PpuvHk.js","_app/immutable/chunks/DM6u0xJB.js","_app/immutable/chunks/wFZPIAkx.js","_app/immutable/chunks/CxjwhJnB.js","_app/immutable/chunks/y0YWbF4N.js"],stylesheets:[],fonts:[],uses_env_dynamic_public:false},
		nodes: [
			__memo(() => import('./nodes/0.js')),
			__memo(() => import('./nodes/1.js')),
			__memo(() => import('./nodes/2.js')),
			__memo(() => import('./nodes/3.js')),
			__memo(() => import('./nodes/4.js')),
			__memo(() => import('./nodes/5.js')),
			__memo(() => import('./nodes/6.js')),
			__memo(() => import('./nodes/7.js')),
			__memo(() => import('./nodes/8.js')),
			__memo(() => import('./nodes/9.js')),
			__memo(() => import('./nodes/10.js'))
		],
		routes: [
			{
				id: "/",
				pattern: /^\/$/,
				params: [],
				page: { layouts: [0,], errors: [1,], leaf: 2 },
				endpoint: null
			},
			{
				id: "/admin",
				pattern: /^\/admin\/?$/,
				params: [],
				page: { layouts: [0,], errors: [1,], leaf: 3 },
				endpoint: null
			},
			{
				id: "/contacts",
				pattern: /^\/contacts\/?$/,
				params: [],
				page: { layouts: [0,], errors: [1,], leaf: 4 },
				endpoint: null
			},
			{
				id: "/editor/[[uuid]]",
				pattern: /^\/editor(?:\/([^/]+))?\/?$/,
				params: [{"name":"uuid","optional":true,"rest":false,"chained":true}],
				page: { layouts: [0,], errors: [1,], leaf: 5 },
				endpoint: null
			},
			{
				id: "/game/[[uuid]]",
				pattern: /^\/game(?:\/([^/]+))?\/?$/,
				params: [{"name":"uuid","optional":true,"rest":false,"chained":true}],
				page: { layouts: [0,], errors: [1,], leaf: 6 },
				endpoint: null
			},
			{
				id: "/gdpr",
				pattern: /^\/gdpr\/?$/,
				params: [],
				page: { layouts: [0,], errors: [1,], leaf: 7 },
				endpoint: null
			},
			{
				id: "/multiplayer",
				pattern: /^\/multiplayer\/?$/,
				params: [],
				page: { layouts: [0,], errors: [1,], leaf: 8 },
				endpoint: null
			},
			{
				id: "/my-profile",
				pattern: /^\/my-profile\/?$/,
				params: [],
				page: { layouts: [0,], errors: [1,], leaf: 9 },
				endpoint: null
			},
			{
				id: "/puzzles",
				pattern: /^\/puzzles\/?$/,
				params: [],
				page: { layouts: [0,], errors: [1,], leaf: 10 },
				endpoint: null
			}
		],
		prerendered_routes: new Set([]),
		matchers: async () => {
			
			return {  };
		},
		server_assets: {}
	}
}
})();

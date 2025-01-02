import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

export default {
  plugins: [svelte()],
  base: '/static/',  // This assumes Flask will serve static files from the /static/ folder
  build: {
    outDir: 'dist', // Output the build to the backend's static folder
  },
};


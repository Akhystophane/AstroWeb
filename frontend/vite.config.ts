import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react-swc';
import svgr from 'vite-plugin-svgr';

export default defineConfig({
  plugins: [react(), svgr()],
  build: {
    assetsDir: 'assets', // Assurez-vous que les fichiers sont dans le dossier `assets`
    rollupOptions: {
      output: {
        assetFileNames: 'assets/[name][extname]'  // Conserve le nom des fichiers sans hash
      }
    }
  }
});

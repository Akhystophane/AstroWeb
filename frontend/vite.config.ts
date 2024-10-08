import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react-swc';
import svgr from 'vite-plugin-svgr';

export default defineConfig(({ command, mode }) => {
  return {
    plugins: [react(), svgr()],
    base: mode === 'development' ? '/' : '/static/',  // Définit le chemin de base en fonction du mode
    build: {
      outDir: 'dist',  // Dossier de sortie du build
      assetsDir: 'assets',  // Dossier où seront placés les assets
      rollupOptions: {
        output: {
          // Préserve la structure des dossiers et les noms de fichiers
          assetFileNames: ({ name }) => {
            return 'assets/[name][extname]';  // Conserve le nom du fichier et son extension
          },
        },
      },
    },
  };
});


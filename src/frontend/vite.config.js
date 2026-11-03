import { fileURLToPath } from "node:url";
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

const outputDirectory = fileURLToPath(new URL("../app/api/static/", import.meta.url));

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/documents": "http://localhost:8000",
      "/ingest": "http://localhost:8000",
      "/query": "http://localhost:8000",
    },
  },
  build: {
    outDir: outputDirectory,
    emptyOutDir: true,
  },
});

import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/analyze": "http://localhost:8000",
      "/analysis": "http://localhost:8000",
      "/health": "http://localhost:8000",
      "/history": "http://localhost:8000",
    },
  },
});

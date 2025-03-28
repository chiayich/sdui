import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { resolve } from "path";

// 从环境变量获取端口，默认为5173
const frontendPort = parseInt(process.env.FRONTEND_PORT || "5173");
const backendPort = parseInt(process.env.BACKEND_PORT || "8000");

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      "@": resolve(__dirname, "src"),
    },
  },
  server: {
    host: "0.0.0.0",
    port: frontendPort,
    strictPort: true,
    watch: {
      usePolling: true,
    },
    cors: true,
    hmr: {
      host: "0.0.0.0",
      port: frontendPort,
      clientPort: frontendPort,
    },
    proxy: {
      "/api": {
        target: `http://localhost:${backendPort}`,
        changeOrigin: true,
        rewrite: (path) => path,
        configure: (proxy, _options) => {
          proxy.on("error", (err, _req, _res) => {
            console.log("proxy error", err);
          });
          proxy.on("proxyReq", (proxyReq, req, _res) => {
            console.log("Sending Request:", req.method, req.url);
          });
          proxy.on("proxyRes", (proxyRes, req, _res) => {
            console.log("Received Response:", proxyRes.statusCode, req.url);
          });
        },
      },
    },
  },
});

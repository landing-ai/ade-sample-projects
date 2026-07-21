import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    environment: "node",
    // e2e specs run under Playwright (`npm run e2e`), not vitest.
    exclude: ["node_modules/**", "e2e/**", ".next/**"],
  },
});

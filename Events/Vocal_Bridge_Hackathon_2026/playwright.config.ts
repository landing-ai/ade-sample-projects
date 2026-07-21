import { defineConfig } from "@playwright/test";

// E2E happy-path. Precondition: the fixture policy is already extracted (DB warm)
// and an LLM provider is reachable. Run: `npm run e2e`.
export default defineConfig({
  testDir: "./e2e",
  timeout: 120_000,
  fullyParallel: false,
  use: { baseURL: "http://localhost:3000" },
  projects: [{ name: "chromium", use: { browserName: "chromium" } }],
  webServer: {
    command: "npm run dev",
    port: 3000,
    reuseExistingServer: true,
    timeout: 120_000,
  },
});

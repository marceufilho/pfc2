import { defineConfig } from "@playwright/test";

// End-to-end tests run against the built site, served under the same base path as GitHub Pages.
export default defineConfig({
  testDir: "tests",
  timeout: 180_000,
  retries: 0,
  use: { baseURL: "http://localhost:4392/pfc2/" },
  webServer: {
    command: "pnpm exec astro preview --port 4392 --ignore-lock",
    url: "http://localhost:4392/pfc2/",
    reuseExistingServer: false,
    timeout: 60_000,
  },
});

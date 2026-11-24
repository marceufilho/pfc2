import { defineConfig } from "astro/config";
import starlight from "@astrojs/starlight";

// Project site on GitHub Pages: every URL lives under /pfc2/. Change `site` and `base` if the repository
// is published under another owner or name.
export default defineConfig({
  site: "https://marceufilho.github.io",
  base: "/pfc2",
  trailingSlash: "always",
  integrations: [
    starlight({
      title: "PFC2",
      description: "A small proved subset of C: contracts, laws, a playground and a replayable proof file.",
      customCss: ["./src/styles/pfc.css"],
      lastUpdated: false,
      sidebar: [
        { label: "Home", link: "/" },
        { label: "Playground", link: "/playground/" },
        { label: "A lock with one combination", link: "/lock/" },
        { label: "A game you cannot win", link: "/game/" },
        { label: "Examples", link: "/examples/" },
        { label: "Documentation", items: [{ autogenerate: { directory: "docs" } }] },
      ],
    }),
  ],
});

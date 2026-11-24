import { defineCollection } from "astro:content";
import { docsLoader } from "@astrojs/starlight/loaders";
import { docsSchema } from "@astrojs/starlight/schema";
import { z } from "astro/zod";

export const collections = {
  docs: defineCollection({
    loader: docsLoader(),
    schema: docsSchema({
      extend: z.object({
        // Pages ported from the paper name the LaTeX section they follow and its digest at porting time.
        source: z.string().optional(),
        source_sha256: z.string().optional(),
      }),
    }),
  }),
};

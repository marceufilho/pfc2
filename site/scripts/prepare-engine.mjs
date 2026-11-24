// Copies the Pyodide runtime from node_modules and the lock file into public/engine, then fetches the
// pinned wheels. Everything the browser engine loads is then served by the site itself.
import { execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const site = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const lock = JSON.parse(fs.readFileSync(path.join(site, "engine.lock.json"), "utf8"));
const source = path.join(site, "node_modules/pyodide");
const installed = JSON.parse(fs.readFileSync(path.join(source, "package.json"), "utf8")).version;
if (installed !== lock.pyodide) {
  console.error(`pyodide ${installed} is installed but engine.lock.json names ${lock.pyodide}`);
  process.exit(1);
}
const target = path.join(site, "public/engine/pyodide");
fs.mkdirSync(target, { recursive: true });
for (const file of ["pyodide.mjs", "pyodide.asm.mjs", "pyodide.asm.wasm", "python_stdlib.zip", "pyodide-lock.json"]) {
  fs.copyFileSync(path.join(source, file), path.join(target, file));
}
fs.copyFileSync(path.join(site, "engine.lock.json"), path.join(site, "public/engine/engine.lock.json"));
execFileSync(process.execPath, [path.join(site, "scripts/fetch-engine.mjs")], { stdio: "inherit" });
if (!fs.existsSync(path.join(site, "public/engine/pfc2-bundle.json"))) {
  console.error("public/engine/pfc2-bundle.json is missing; run `make site-data` from the repository root");
  process.exit(1);
}

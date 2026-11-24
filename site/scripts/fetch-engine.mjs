// Downloads the wheels named in engine.lock.json into public/engine/wheels and verifies each digest.
// Existing files with the right digest are kept; a wrong digest is an error, never a silent replacement.
import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const site = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const lock = JSON.parse(fs.readFileSync(path.join(site, "engine.lock.json"), "utf8"));
const target = path.join(site, "public/engine/wheels");
fs.mkdirSync(target, { recursive: true });
const digest = (bytes) => crypto.createHash("sha256").update(bytes).digest("hex");

for (const wheel of lock.wheels) {
  const file = path.join(target, wheel.file);
  if (fs.existsSync(file)) {
    if (digest(fs.readFileSync(file)) !== wheel.sha256) {
      console.error(`${wheel.file}: digest differs from engine.lock.json; remove the file and retry`);
      process.exit(1);
    }
    console.log(`${wheel.file}: present`);
    continue;
  }
  const response = await fetch(wheel.url);
  if (!response.ok) {
    console.error(`${wheel.file}: download failed with HTTP ${response.status}`);
    process.exit(1);
  }
  const bytes = Buffer.from(await response.arrayBuffer());
  if (digest(bytes) !== wheel.sha256) {
    console.error(`${wheel.file}: downloaded digest differs from engine.lock.json`);
    process.exit(1);
  }
  fs.writeFileSync(file, bytes);
  console.log(`${wheel.file}: downloaded and verified`);
}

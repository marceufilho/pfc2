// Web Worker hosting the PFC2 checker: Pyodide, the pinned wheels and the PFC2 sources of this repository.
// One request at a time; the page cancels by terminating the worker.
import { loadPyodide } from "./pyodide/pyodide.mjs";

const base = new URL(".", self.location.href);
let engine = null;

async function start() {
  const progress = (stage) => self.postMessage({ type: "progress", stage });
  progress("runtime");
  const pyodide = await loadPyodide({ indexURL: new URL("pyodide/", base).href });
  const lock = await (await fetch(new URL("engine.lock.json", base))).json();
  progress("solver");
  for (const wheel of lock.wheels) {
    await pyodide.loadPackage(new URL("wheels/" + wheel.file, base).href, { messageCallback: () => {} });
  }
  progress("checker");
  const bundle = await (await fetch(new URL("pfc2-bundle.json", base))).json();
  for (const [name, text] of Object.entries(bundle.files)) {
    const file = "/app/" + name;
    pyodide.FS.mkdirTree(file.slice(0, file.lastIndexOf("/")));
    pyodide.FS.writeFile(file, text);
  }
  pyodide.runPython(`
import sys, json
sys.path.insert(0, "/app")
from pfc2 import web

def run(payload):
    request = json.loads(payload)
    result = web.analyze(
        request["source"],
        name=request.get("name", "program.c"),
        level=request.get("level", "full"),
        timeout_ms=int(request.get("timeout_ms", web.DEFAULT_TIMEOUT_MS)),
    )
    return json.dumps({"result": result, "summary": web.summary(result)})
`);
  return { run: pyodide.globals.get("run"), files: Object.keys(bundle.files).length };
}

self.onmessage = async (event) => {
  const { id, request } = event.data;
  try {
    if (!engine) {
      engine = await start();
      self.postMessage({ type: "ready", files: engine.files });
    }
    if (request) self.postMessage({ type: "result", id, payload: engine.run(JSON.stringify(request)) });
  } catch (error) {
    self.postMessage({ type: "error", id, message: String(error && error.message ? error.message : error) });
  }
};

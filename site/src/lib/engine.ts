// Page-side handle of the checker worker: lazy start, one request at a time, cancellation by termination.
export interface EngineRequest {
  source: string;
  name?: string;
  level?: "full" | "memory";
  timeout_ms?: number;
}
export interface EngineReply {
  result: any;
  summary: any;
}
type Progress = (stage: string) => void;

const WATCHDOG_MS = 120_000;
let worker: Worker | null = null;
let pending: { id: number; resolve: (reply: EngineReply) => void; reject: (error: Error) => void } | null = null;
let counter = 0;
const listeners: Progress[] = [];

function spawn(): Worker {
  const base = import.meta.env.BASE_URL.replace(/\/?$/, "/");
  const created = new Worker(`${base}engine/worker.js`, { type: "module" });
  created.onmessage = (event) => {
    const message = event.data;
    if (message.type === "progress") listeners.forEach((listener) => listener(message.stage));
    else if (message.type === "ready") listeners.forEach((listener) => listener("ready"));
    else if (pending && message.id === pending.id) {
      const current = pending;
      pending = null;
      if (message.type === "result") current.resolve(JSON.parse(message.payload));
      else current.reject(new Error(message.message));
    }
  };
  created.onerror = (event) => {
    const current = pending;
    pending = null;
    worker = null;
    current?.reject(new Error(event.message || "the checker could not be loaded"));
  };
  return created;
}

export function onProgress(listener: Progress): void {
  listeners.push(listener);
}

export function cancel(): void {
  worker?.terminate();
  worker = null;
  const current = pending;
  pending = null;
  current?.reject(new Error("cancelled"));
}

export function analyze(request: EngineRequest): Promise<EngineReply> {
  if (pending) return Promise.reject(new Error("a check is already running"));
  worker ??= spawn();
  const id = ++counter;
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => {
      if (pending?.id === id) {
        cancel();
        reject(new Error("timed out; the checker was restarted"));
      }
    }, WATCHDOG_MS);
    pending = {
      id,
      resolve: (reply) => (clearTimeout(timer), resolve(reply)),
      reject: (error) => (clearTimeout(timer), reject(error)),
    };
    worker!.postMessage({ id, request });
  });
}

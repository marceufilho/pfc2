// A four-key lock. Whether a combination opens it is looked up in the list produced by running the compiled
// program on all 10,000 digit combinations (tools/site_data.py). This file contains no copy of the lock's rule.
import { dataUrl, pageUrl } from "./paths";

interface Program {
  id: string;
  path: string;
  source: string;
  accepted: boolean;
  certified_c?: boolean;
  obligations: number;
  proved: number;
  laws: number;
  tried?: number;
  openers?: string[];
  refusal: { line: number; column: number; meaning: string; goal: string }[];
}

const escape = (text: string): string =>
  text.replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]!);

export async function mount(root: HTMLElement): Promise<void> {
  if (root.dataset.mounted) return;
  root.dataset.mounted = "1";
  const { programs }: { programs: Program[] } = await (await fetch(dataUrl("showcase.json"))).json();
  const variants = {
    proved: programs.find((p) => p.path === "lock/lock.c")!,
    sloppy: programs.find((p) => p.path === "wrong/lock_copy_paste.c")!,
  };
  let which: keyof typeof variants = "proved";
  root.innerHTML = `
    <div class="panel">
      <div class="keys">${[0, 1, 2, 3].map((i) => `<input inputmode="numeric" maxlength="1" value="0" aria-label="key ${i + 1}">`).join("")}</div>
      <p class="state" role="status"></p>
      <div class="controls"><button class="primary swap"></button><button class="all">Try all 10,000</button></div>
    </div>
    <div class="verdict"></div>
    <details class="rules" open><summary>The program that is the lock</summary><pre></pre></details>`;
  const inputs = [...root.querySelectorAll<HTMLInputElement>(".keys input")];
  const state = root.querySelector<HTMLElement>(".state")!;
  const verdict = root.querySelector<HTMLElement>(".verdict")!;
  const swap = root.querySelector<HTMLButtonElement>(".swap")!;
  const pre = root.querySelector<HTMLElement>(".rules pre")!;

  const draw = (): void => {
    const lock = variants[which];
    const combination = inputs.map((input) => (/^[0-9]$/.test(input.value) ? input.value : "0")).join("");
    const open = lock.openers!.includes(combination);
    state.textContent = open ? `${combination}: open` : `${combination}: closed`;
    state.className = `state ${open ? "open" : "closed"}`;
  };
  const describe = (): void => {
    const lock = variants[which];
    const link = `<a href="${pageUrl("playground/")}#example=${lock.id}">Check this program yourself</a>`;
    swap.textContent = which === "proved" ? "Use the sloppy lock" : "Use the proved lock";
    pre.textContent = lock.source;
    verdict.innerHTML = lock.accepted
      ? `<p class="ok"><strong>Certified.</strong> ${lock.proved} of ${lock.obligations} obligations proved, ${lock.laws} laws among them: the combination opens the lock, and nothing else does. ${link}</p>`
      : `<p class="bad"><strong>Refused.</strong> ${escape(lock.refusal[0]!.meaning)} at line ${lock.refusal[0]!.line}: it cannot prove <code>${escape(lock.refusal[0]!.goal)}</code>. Press <em>Try all 10,000</em> for combinations that should not open it. ${link}</p>`;
    draw();
  };
  inputs.forEach((input, index) =>
    input.addEventListener("input", () => {
      input.value = input.value.replace(/[^0-9]/g, "").slice(-1);
      if (input.value && index < 3) inputs[index + 1]!.focus();
      draw();
    }),
  );
  swap.addEventListener("click", () => {
    which = which === "proved" ? "sloppy" : "proved";
    describe();
  });
  root.querySelector<HTMLButtonElement>(".all")!.addEventListener("click", () => {
    const lock = variants[which];
    const from = lock.certified_c ? "the certified C" : "the source compiled as plain C (a refused program releases no C)";
    state.textContent = `${lock.tried!.toLocaleString("en")} combinations were run through ${from} when this site was built: ${lock.openers!.length} open it (${lock.openers!.join(", ")}).`;
    state.className = "state";
  });
  describe();
}

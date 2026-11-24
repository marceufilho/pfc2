// Capture the flag. Every move is looked up in a table produced by running the compiled rules
// (tools/site_data.py); this file draws the board and reads keys. It contains no copy of the rules.
import { dataUrl, pageUrl } from "./paths";

interface Variant {
  example: string;
  source: string;
  accepted: boolean;
  certified_c: boolean;
  obligations: number;
  proved: number;
  refusal: { line: number; column: number; meaning: string }[];
  table: number[][][][];
  shortest_win: number[] | null;
}
interface Game {
  width: number;
  height: number;
  start: [number, number];
  flag: [number, number];
  wall_column: number;
  variants: { wall: Variant; open: Variant };
}

// Moves, as in the C program: 0 up, 1 down, 2 left, 3 right.
const KEYS: Record<string, number> = {
  ArrowUp: 0, ArrowDown: 1, ArrowLeft: 2, ArrowRight: 3,
  w: 0, s: 1, a: 2, d: 3,
};
const ARROWS = ["↑", "↓", "←", "→"];
const escape = (text: string): string =>
  text.replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]!);

export async function mount(root: HTMLElement): Promise<void> {
  if (root.dataset.mounted) return;
  root.dataset.mounted = "1";
  const game: Game = await (await fetch(dataUrl("game.json"))).json();
  let walled = true;
  let position: [number, number] = [...game.start];
  let moves = 0;
  let replay: number | undefined;

  root.innerHTML = `
    <div class="board" tabindex="0" role="application" aria-label="Game board. Use the arrow keys to move."></div>
    <div class="side">
      <div class="controls">
        <button class="toggle primary"></button>
        <button class="reset">Start again</button>
        <button class="solve" hidden>Show a winning play</button>
      </div>
      <div class="pad" aria-label="Move">
        <button data-move="0" aria-label="Up">↑</button>
        <div><button data-move="2" aria-label="Left">←</button><button data-move="1" aria-label="Down">↓</button><button data-move="3" aria-label="Right">→</button></div>
      </div>
      <p class="moves muted"></p>
      <div class="verdict" role="status"></div>
    </div>
    <details class="rules" open>
      <summary>The rules: the whole program</summary>
      <p class="muted file"></p>
      <pre class="source"></pre>
    </details>`;
  const $ = <T extends HTMLElement>(selector: string) => root.querySelector<T>(selector)!;
  const board = $(".board");
  board.style.gridTemplateColumns = `repeat(${game.width}, 1fr)`;
  const variant = () => (walled ? game.variants.wall : game.variants.open);
  const won = () => position[0] === game.flag[0] && position[1] === game.flag[1];

  function draw(): void {
    let cells = "";
    for (let y = 0; y < game.height; y++) {
      for (let x = 0; x < game.width; x++) {
        const wall = walled && x === game.wall_column;
        const here = position[0] === x && position[1] === y;
        const flag = game.flag[0] === x && game.flag[1] === y;
        const kind = wall ? "wall" : here && flag ? "player flag won" : here ? "player" : flag ? "flag" : "";
        cells += `<div class="cell ${kind}" data-x="${x}" data-y="${y}">${wall ? "" : here ? "●" : flag ? "⚑" : ""}</div>`;
      }
    }
    board.innerHTML = cells;
    board.dataset.x = String(position[0]);
    board.dataset.y = String(position[1]);
    $(".toggle").textContent = walled ? "Remove the wall" : "Put the wall back";
    $(".solve").hidden = walled;
    $(".moves").textContent = `Moves: ${moves}`;
    const v = variant();
    const link = `<a href="${pageUrl("playground/")}#example=${v.example}">Check this program yourself</a>`;
    const source = v.certified_c
      ? "Your moves are computed by the certified C that PFC2 released for this program."
      : "PFC2 released no C for this program, so your moves are computed by the same source compiled as ordinary C.";
    let text: string;
    if (v.accepted) {
      text = `<p class="ok"><strong>Proved: this game cannot be won.</strong> ${v.proved} of ${v.obligations} obligations hold for every sequence of moves, of any length. You can try anyway.</p>`;
    } else {
      const first = v.refusal[0];
      text = `<p class="bad"><strong>The proof is refused.</strong> ${v.proved} of ${v.obligations} obligations hold; at line ${first?.line} PFC2 reports: “${first?.meaning}”. Without the wall, the claim “nobody ever wins” is false, so nothing is certified.</p>`;
      if (won()) text += `<p class="win"><strong>You captured the flag in ${moves} moves.</strong> This is a play the refused proof said could exist.</p>`;
    }
    $(".verdict").innerHTML = `${text}<p class="muted">${source} ${link}.</p>`;
    // The program the checker judged, with the lines that differ between the two variants marked.
    const other = (walled ? game.variants.open : game.variants.wall).source.split("\n");
    const mine = v.source.replace(/\n$/, "").split("\n");
    const changed = mine.length === other.length || mine.length + 1 === other.length;
    $(".file").textContent = `examples/${v.example}.c` + (changed ? " — the marked lines are the only difference from the other variant" : "");
    $(".source").innerHTML = mine
      .map((line, index) => `<span class="${changed && line !== other[index] ? "changed" : ""}">${escape(line) || " "}</span>`)
      .join("");
  }

  function move(direction: number): void {
    if (won()) return;
    const next = variant().table[position[0]]![position[1]]![direction]!;
    position = [next[0]!, next[1]!];
    moves += 1;
    draw();
  }

  function reset(): void {
    clearInterval(replay);
    position = [...game.start];
    moves = 0;
    draw();
  }

  board.addEventListener("keydown", (event) => {
    const direction = KEYS[event.key];
    if (direction === undefined) return;
    event.preventDefault();
    move(direction);
  });
  root.querySelectorAll<HTMLButtonElement>("[data-move]").forEach((button) =>
    button.addEventListener("click", () => (move(Number(button.dataset.move)), board.focus())),
  );
  $(".toggle").addEventListener("click", () => ((walled = !walled), reset(), board.focus()));
  $(".reset").addEventListener("click", () => (reset(), board.focus()));
  $(".solve").addEventListener("click", () => {
    const play = variant().shortest_win;
    if (!play) return;
    reset();
    let step = 0;
    replay = window.setInterval(() => {
      if (step >= play.length) return clearInterval(replay);
      move(play[step++]!);
    }, 220);
  });
  $(".solve").title = `Found by trying every square: ${(game.variants.open.shortest_win ?? []).map((m) => ARROWS[m]).join(" ")}`;
  draw();
}

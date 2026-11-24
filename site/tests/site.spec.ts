import { expect, test } from "@playwright/test";

// Expectations are hand-derived from the example programs (examples/examples.json), not read from the checker.
test("count is certified in the browser and loses its proof without its precondition", async ({ page }) => {
  const errors: string[] = [];
  page.on("pageerror", (error) => errors.push(error.message));
  await page.goto("playground/");
  const playground = page.locator(".pfc-playground");
  await expect(playground.locator(".program")).toHaveValue("01_count/count");
  await playground.locator("button.run").click();
  await expect(playground.locator(".chips")).toContainText("certified (full)", { timeout: 150_000 });
  await expect(playground.locator(".chips")).toContainText("obligations proved: 6/6");
  await expect(playground.locator(".body")).toContainText("((0 <= i) && (i <= n))");
  await playground.locator('[data-tab="c"]').click();
  await expect(playground.locator(".body pre")).toContainText("long count(long n)");
  await expect(playground.locator(".body pre")).not.toContainText("counting_to_n_gives_n");

  await playground.locator(".experiment").selectOption({ label: "Remove every requires(...)" });
  await expect(playground.locator(".state")).toContainText("not certified", { timeout: 60_000 });
  await playground.locator('[data-tab="c"]').click();
  await expect(playground.locator(".body")).toContainText("A refused program releases no C.");
  expect(errors).toEqual([]);
});

test("a wrong program is refused at its line, underlined in the editor, and sum needs the memory level", async ({ page }) => {
  await page.goto("playground/");
  const playground = page.locator(".pfc-playground");
  await playground.locator(".program").selectOption("wrong/off_by_one");
  await playground.locator("button.run").click();
  await expect(playground.locator(".chips")).toContainText("not certified (full)", { timeout: 150_000 });
  await expect(playground.locator(".body table")).toContainText("this index may be outside the array");
  await expect(playground.locator(".body table")).toContainText("7:9");
  await expect(playground.locator(".cm-lintRange-error")).toHaveCount(2); // The write and the counter's overflow.

  await playground.locator(".program").selectOption("03_sum/sum");
  await expect(playground.locator(".level")).toHaveValue("memory");
  await playground.locator("button.run").click();
  await expect(playground.locator(".chips")).toContainText("certified (memory)", { timeout: 60_000 });
  await expect(playground.locator(".body")).toContainText("Overflow traps kept");
  await expect(playground.locator(".cm-lintRange-warning")).toHaveCount(1);
  await playground.locator(".level").selectOption("full");
  await playground.locator("button.run").click();
  await expect(playground.locator(".chips")).toContainText("not certified (full)", { timeout: 60_000 });
});

test("an impossible contract on a declared function is refused", async ({ page }) => {
  await page.goto("playground/#example=wrong/contradictory_extern");
  const playground = page.locator(".pfc-playground");
  await expect(playground.locator(".program")).toHaveValue("wrong/contradictory_extern");
  await playground.locator("button.run").click();
  await expect(playground.locator(".body")).toContainText("the contract of sensor cannot be satisfied", { timeout: 150_000 });
});

test("a shared link reopens the same program", async ({ page }) => {
  await page.goto("playground/");
  const playground = page.locator(".pfc-playground");
  await playground.locator(".program").selectOption("07_countdown/countdown");
  await playground.locator("button.share").click();
  const url = page.url();
  expect(url).toContain("#level=full&src=");
  await page.goto("about:blank");
  await page.goto(url);
  await expect(page.locator(".pfc-playground .cm-content")).toContainText("decreases(left)");
});

test("the documentation, the comparison page and the examples gallery are published", async ({ page }) => {
  await page.goto("docs/");
  await expect(page.locator("h1")).toHaveText("Documentation");
  await page.goto("docs/02-language/");
  await expect(page.locator("main")).toContainText("The words PFC2 adds");
  await page.goto("docs/10-pfc-and-pfc2/");
  await expect(page.locator("main")).toContainText("What PFC has that PFC2 does not");
  await page.goto("examples/");
  await expect(page.locator("main")).toContainText("05_binary_search/binary_search");
  await page.locator('a[href*="#example=05_binary_search/binary_search"]').click();
  await expect(page.locator(".pfc-playground .program")).toHaveValue("05_binary_search/binary_search");
});

test("the browser agrees with the native run on every example", async ({ page }) => {
  test.setTimeout(300_000);
  await page.goto("playground/");
  const playground = page.locator(".pfc-playground");
  const programs: { id: string; reference: unknown }[] = await page.evaluate(async () => {
    const response = await fetch(new URL("../data/programs.json", location.href));
    return (await response.json()).programs;
  });
  expect(programs.length).toBe(32); // The examples listed in examples/examples.json.
  await page.evaluate(() => {
    (window as any).summaries = [];
    document.addEventListener("pfc2-result", (event) => (window as any).summaries.push((event as CustomEvent).detail.summary));
  });
  const canonical = (value: unknown): string =>
    JSON.stringify(value, (_, item) =>
      item && typeof item === "object" && !Array.isArray(item)
        ? Object.fromEntries(Object.keys(item).sort().map((key) => [key, item[key]]))
        : item,
    );
  for (const [index, program] of programs.entries()) {
    await playground.locator(".program").selectOption(program.id);
    await playground.locator("button.run").click();
    await page.waitForFunction((count) => (window as any).summaries.length === count, index + 1, { timeout: 150_000 });
    const actual = await page.evaluate((position) => (window as any).summaries[position], index);
    expect(canonical(actual), program.id).toBe(canonical(program.reference));
  }
});

test("the game cannot be won with the wall and can be won without it", async ({ page }) => {
  await page.goto("game/");
  const game = page.locator(".flag-game");
  const board = game.locator(".board");
  await expect(game.locator(".verdict")).toContainText("Proved: this game cannot be won");
  await expect(game.locator(".verdict")).toContainText("40 of 40 obligations");
  await board.focus();
  for (let i = 0; i < 10; i++) await page.keyboard.press("ArrowRight");
  // Hand-read from flag.c: the wall is column 4, so the player stops in column 3 on its starting row.
  await expect(board).toHaveAttribute("data-x", "3");
  await expect(board).toHaveAttribute("data-y", "2");
  await expect(game.locator(".cell.wall")).toHaveCount(5);

  await expect(game.locator(".rules pre")).toContainText("#define WALL 4");
  await expect(game.locator(".rules pre")).toContainText("law nobody_ever_wins");

  await game.locator("button.toggle").click();
  await expect(game.locator(".rules pre .changed").filter({ hasText: "#define WALL 99" })).toHaveCount(1);
  await expect(game.locator(".verdict")).toContainText("The proof is refused");
  await expect(game.locator(".verdict")).toContainText("an iteration may break the loop invariant");
  await expect(game.locator(".cell.wall")).toHaveCount(0);
  await board.focus();
  for (let i = 0; i < 7; i++) await page.keyboard.press("ArrowRight");
  await expect(game.locator(".verdict")).toContainText("You captured the flag in 7 moves");
  await page.keyboard.press("ArrowLeft"); // The game is over: the player stays on the flag.
  await expect(board).toHaveAttribute("data-x", "7");

  await game.locator("button.toggle").click();
  await expect(game.locator(".verdict")).toContainText("Proved: this game cannot be won");
  await expect(board).toHaveAttribute("data-x", "0");
});

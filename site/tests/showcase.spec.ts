import { expect, test } from "@playwright/test";

test("the front page shows the midpoint refused and certified, from the stored results", async ({ page }) => {
  await page.goto("");
  const main = page.locator("main");
  await expect(main).toContainText("return (lo + hi) / 2;");
  await expect(main).toContainText("this arithmetic may overflow at line 8");
  await expect(main).toContainText("return lo + (hi - lo) / 2;");
  await expect(main).toContainText("5 of 5 obligations proved"); // Hand-read from `pfc2 check showcase/midpoint/midpoint.c`.
  const playground = page.locator(".pfc-playground");
  await expect(playground.locator(".program")).toHaveValue("showcase/midpoint/midpoint_wrong");
  await playground.locator("button.run").click();
  await expect(playground.locator(".chips")).toContainText("not certified (full)", { timeout: 150_000 });
});

test("the lock opens for one combination when proved and for ten when sloppy", async ({ page }) => {
  await page.goto("lock/");
  const lock = page.locator(".pfc-lock");
  const keys = lock.locator(".keys input");
  await expect(lock.locator(".verdict")).toContainText("Certified. 55 of 55 obligations proved, 2 laws");
  await expect(lock.locator(".state")).toContainText("0000: closed");
  for (const [index, key] of ["3", "1", "4", "1"].entries()) await keys.nth(index).fill(key);
  await expect(lock.locator(".state")).toContainText("3141: open");
  await keys.nth(3).fill("7");
  await expect(lock.locator(".state")).toContainText("3147: closed");
  await lock.locator("button.all").click();
  await expect(lock.locator(".state")).toContainText("1 open it (3141)");
  await expect(lock.locator(".rules pre")).toContainText("law only_one_combination");
  await expect(lock.locator(".rules pre")).toContainText("invariant(n == 4");

  await lock.locator("button.swap").click();
  await expect(lock.locator(".verdict")).toContainText("Refused.");
  await expect(lock.locator(".verdict")).toContainText("at line 13");
  await expect(lock.locator(".state")).toContainText("3147: open"); // The slip: the fourth key is never read.
  await lock.locator("button.all").click();
  await expect(lock.locator(".state")).toContainText("10 open it");
  await expect(lock.locator(".state")).toContainText("plain C");
});

test("every showcase program gets in the browser the result of its native run", async ({ page }) => {
  const { programs } = await (await page.request.get("data/showcase.json")).json();
  await page.goto("playground/");
  const playground = page.locator(".pfc-playground");
  for (const program of programs) {
    await playground.locator(".program").selectOption(program.id);
    await playground.locator("button.run").click();
    const expected = program.accepted ? `certified (${program.level})` : "not certified";
    await expect(playground.locator(".chips"), program.id).toContainText(expected, { timeout: 150_000 });
  }
});

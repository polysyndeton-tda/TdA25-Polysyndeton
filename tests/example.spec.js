// @ts-check
const { test, expect } = require('@playwright/test');

test('display 404 error page', async ({ page }) => {
  //go to a guaranteed non existing page (the page has game/uuid normally, so pass this "randomText" to avoid paranoia of collisions)
  //(the validity of the uuid is not tested on the backend, what is tested is if a game under this string exists in the db => it does not so 404 )
  await page.goto('http://127.0.0.1:5000/game/randomtext');
  await expect(page.locator(".errorMessage")).toHaveText("Error: Úloha nebyla nalezena. \n Pravděpodobně je to proto, že byla smazána.");
  await page.goto('http://127.0.0.1:5000/editor/randomtext');
  await expect(page.locator(".errorMessage")).toHaveText("Error: Úloha nebyla nalezena. \n Pravděpodobně je to proto, že byla smazána.");
});

// test('get started link', async ({ page }) => {
//   await page.goto('https://playwright.dev/');

//   // Click the get started link.
//   await page.getByRole('link', { name: 'Get started' }).click();

//   // Expects page to have a heading with the name of Installation.
//   await expect(page.getByRole('heading', { name: 'Installation' })).toBeVisible();
// });

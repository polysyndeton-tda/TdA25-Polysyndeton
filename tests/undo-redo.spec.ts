import { test, expect } from '@playwright/test';

test('Undo redo 1', async ({ page }) => {
  await page.goto('http://127.0.0.1:5000/game');
  //making any three moves on the board
  await page.locator('.row:nth-child(8) > .field:nth-child(5)').click();

  /*fails in Webkit (Playwright, Safari) with "" 
  Real life workaround: go to http://127.0.0.1:5000 first, from there click on "Nová hra" (instead of going to this page directly)
  Locator: locator('.row:nth-child(8) > .field:nth-child(5)')
  Expected pattern: /X/
  Received string:  ""

  When this, the line in question, gets commented out:
  */
  // await expect(page.locator('.row:nth-child(8) > .field:nth-child(5)')).toHaveClass(/X/);
  //and there is another .click() on the game square, it gets:
  //   Error: locator.click: Target page, context or browser has been closed
  // Call log:
  //   - waiting for locator('.row:nth-child(9) > .field:nth-child(5)')

  //Again, only on Webkit

  //The real-life analogy of this test, going to http://127.0.0.1:5000/game in Epiphany 46, and clicking the field **once** freezes it
  //Other browsers are fine

  await page.locator('.row:nth-child(9) > .field:nth-child(5)').click();
  await page.locator('.row:nth-child(10) > .field:nth-child(5)').click();
  // //undoing the third and second move
  // await page.getByRole('button', { name: 'Undo' }).click();
  // await page.getByRole('button', { name: 'Undo' }).click();
  // //making a different move, overwriting the second one in history
  // await page.locator('.row:nth-child(2) > .field:nth-child(9)').click();
  //make sure the redo button is disabled, because we don't the NON overwritten third move to show
  // await expect(page.getByRole('button', { name: 'Redo' })).toBeDisabled();
});
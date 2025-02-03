import { test, expect } from '@playwright/test';

test('Undo redo 1', async ({ page }) => {
  await page.goto('http://127.0.0.1:5000/game');
  //making any three moves on the board
  await page.locator('.row:nth-child(8) > .field:nth-child(5)').click();
  await expect(page.locator('.row:nth-child(8) > .field:nth-child(5)')).toHaveClass(/X/);
  // await page.locator('.row:nth-child(9) > .field:nth-child(5)').click();
  // await page.locator('.row:nth-child(10) > .field:nth-child(5)').click();
  // //undoing the third and second move
  // await page.getByRole('button', { name: 'Undo' }).click();
  // await page.getByRole('button', { name: 'Undo' }).click();
  // //making a different move, overwriting the second one in history
  // await page.locator('.row:nth-child(2) > .field:nth-child(9)').click();
  //make sure the redo button is disabled, because we don't the NON overwritten third move to show
  // await expect(page.getByRole('button', { name: 'Redo' })).toBeDisabled();
});
import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
  await page.goto('http://127.0.0.1:5000/');
  await page.getByRole('link', { name: 'Nová hra' }).click();
  //4 tahy na herní desce
  await page.locator('.row:nth-child(3) > .field:nth-child(7)').click();
  await page.locator('.row:nth-child(3) > .field:nth-child(8)').click();
  await page.locator('.row:nth-child(3) > .field:nth-child(9)').click();
  await page.locator('.row:nth-child(3) > .field:nth-child(10)').click();
  //3 undo akce
  await page.getByRole('button', { name: 'Undo' }).click();
  await page.getByRole('button', { name: 'Undo' }).click();
  await page.getByRole('button', { name: 'Undo' }).click();
  //2 tahy někam jinam (2 ze 4 tahů overwritten)
  await page.locator('.row:nth-child(2) > .field:nth-child(4)').click();
  await page.locator('.row:nth-child(2) > .field:nth-child(3)').click();
  //Teď by mělo být redo tlačítko zakázané (z user pohledu ted mame jakoby posledni tah (uživatele nezajímá implementace, kde ještě jsou nepřepsané pův. tahy za))
  await expect(page.getByRole('button', { name: 'Redo' })).toBeDisabled();
  //Teď undo, tedy od posledního zahraného tahu dozadu
  await page.getByRole('button', { name: 'Undo' }).click();
  //takže Redo by měla být zase legální akce
  await expect(page.getByRole('button', { name: 'Redo' })).toBeEnabled();
  //Teď jsme pro uživatele zase na konci toho stacku 
  await page.getByRole('button', { name: 'Redo' }).click();
  await expect(page.getByRole('button', { name: 'Redo' })).toBeDisabled();

  await page.getByRole('button', { name: 'Undo' }).click();
  await page.getByRole('button', { name: 'Undo' }).click();
  await page.getByRole('button', { name: 'Undo' }).click();

  //Test the board is empty now (není to těžiště toho testu, jen tak pro jistotu)
  for(let row = 1; row < 16; row++){ //if document.querySelectorAll is available here, that would be nicer
    for(let column = 1; column < 16; column++){
      await expect(page.locator(`.row:nth-child(${row}) > .field:nth-child(${column})`)).not.toHaveClass(/X|O/);
    }
  }
});
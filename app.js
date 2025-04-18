const fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(...args));
const cheerio = require('cheerio');
const { ipcMain } = require('electron');

const { app, BrowserWindow } = require('electron/main')
const path = require('node:path')

function createWindow () {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false
    }
  })

  win.loadFile('public/index.html')
}

app.whenReady().then(() => {
  createWindow()

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow()
    }
  })
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

ipcMain.on('searchGames', async (event, query) => {
  try {
    const searchUrl = `https://steamrip.com/?s=${query.replace(/ /g, '+')}`;
    const response = await fetch(searchUrl);

    if (!response.ok) {
      console.error(`Erreur HTTP: ${response.status}`);
      event.reply('searchResults', []); // On répond quand même pour éviter de bloquer le renderer
      return;
    }

    const html = await response.text();
    const $ = cheerio.load(html);

    const results = [];

    $('a.all-over-thumb-link').each((_, el) => {
      const title = $(el).find('span').text().trim();
      const href = $(el).attr('href');
      results.push({ title, href: 'https://steamrip.com/' + href });
    });
    

    event.reply('searchResults', results);
  } catch (error) {
    console.error('Erreur:', error);
    event.reply('searchResults', []);
  }
});
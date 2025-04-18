const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('api', {
  searchGames: (query) => {
    ipcRenderer.send('searchGames', query);
  },
  onResults: (callback) => {
    ipcRenderer.on('searchResults', (event, results) => callback(results));
  }
});

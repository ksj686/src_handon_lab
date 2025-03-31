const { app, BrowserWindow, ipcMain } = require('electron');
const { PythonShell } = require('python-shell');
const path = require('path');

function createWindow() {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),  // optional, not used in this example
      nodeIntegration: true,
      contextIsolation: false
    }
  });

  win.loadFile('index.html');
}

// Python 스크립트 실행
ipcMain.on('run-python', (event, inputDate) => {
  const options = {
    mode: 'text',
    pythonPath: 'C:/labs_python/.venv/Scripts/python.exe',  // 시스템에 설치된 Python 경로
    scriptPath: __dirname,
    args: [inputDate]  // 입력받은 날짜를 Python 스크립트에 전달
  };

  // Python 스크립트 실행
  PythonShell.run('bigtech.py', options)
    .then(result => {
      // Python 스크립트 실행 후 결과 처리
      event.reply('python-output', `Python Script Output:\n${result.join('\n')}`);
    })
    .catch(err => {
      // 오류 처리
      console.error('Error executing Python script:', err);
      event.reply('python-output', `Error: ${err.message}`);
    });
});

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});

export const STORAGE_KEYS = {
    FOLDERS: 'folders',
    EMAILS: 'emails',
    DARK_MODE: 'darkMode',
    USER: 'user'
  };
  
  export function saveData(key, value) {
    localStorage.setItem(key, JSON.stringify(value));
  }
  
  export function loadData(key, defaultValue = []) {
    const data = localStorage.getItem(key);
    return data ? JSON.parse(data) : defaultValue;
  }
  
  export function initializeDefaultFolders() {
    const defaultFolders = ['Gmail', 'Outlook', 'Yahoo'];
    let folders = loadData(STORAGE_KEYS.FOLDERS, []);
    defaultFolders.forEach(folder => {
      if (!folders.includes(folder)) {
        folders.push(folder);
      }
    });
    saveData(STORAGE_KEYS.FOLDERS, folders);
  }
  
export function saveBoolean(key, value) {
  localStorage.setItem(key, value ? 'true' : 'false');
}

export function loadBoolean(key, defaultValue = false) {
  const value = localStorage.getItem(key);
  return value === null ? defaultValue : value === 'true';
}

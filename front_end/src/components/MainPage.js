// src/components/MainPage.js
import React, { useEffect, useState } from 'react';
import Navbar from './Navbar';
import { loadData, STORAGE_KEYS, saveData } from '../utils/storage';

function MainPage({ onLogout, onFolderSelect }) {
  const [folders, setFolders] = useState([]);

  useEffect(() => {
    const loadedFolders = loadData(STORAGE_KEYS.FOLDERS, []);
    setFolders(loadedFolders);
  }, []);

  const handleCreateFolder = () => {
    const folderName = prompt('Enter new folder name');
    if (folderName) {
      const updatedFolders = [...folders, folderName];
      saveData(STORAGE_KEYS.FOLDERS, updatedFolders);
      setFolders(updatedFolders);
    }
  };

  return (
    <>
      <Navbar onLogout={onLogout} />
      <div className="container">
        <h1>My Folders</h1>
        <button onClick={handleCreateFolder}>Create New Folder</button>
        <div id="folder-list">
          {folders.map((folder, index) => (
            <button
              key={index}
              className="secondary folder-btn"
              onClick={() => onFolderSelect(folder)}
            >
              {folder}
            </button>
          ))}
        </div>
      </div>
    </>
  );
}

export default MainPage;

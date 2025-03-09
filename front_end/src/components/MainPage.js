// src/components/MainPage.js
import React, { useEffect, useState } from 'react';
import Navbar from './NavBar';

function MainPage({ onLogout, onFolderSelect }) {
  const [folders, setFolders] = useState([]);

  useEffect(() => {
    async function fetchCategories() {
      try {
        const response = await fetch('http://127.0.0.1:5000/update-emails');
        const categorizedEmails = await response.json();
        setFolders(Object.keys(categorizedEmails));
      } catch (error) {
        console.error('Error fetching categories:', error);
      }
    }
    fetchCategories();
  }, []);

  const handleSortEmails = async () => {
    await fetch('http://127.0.0.1:5000/update-emails');
    alert("Emails sorted successfully!");
  };

  return (
    <>
      <Navbar onLogout={onLogout} />
      <div className="container">
        <h1>Email Categories</h1>
        <button onClick={handleSortEmails}>Sort Emails</button>
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

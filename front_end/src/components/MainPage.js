import React, { useState } from 'react';
import Navbar from './NavBar';

const defaultFolders = ['Personal', 'Promotional', 'Urgent', 'Work']; // Replace with your preferred default folders

function MainPage({ onLogout, onFolderSelect }) {
  const [folders, setFolders] = useState(defaultFolders);

  const handleSortEmails = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/update-emails');
      const categorizedEmails = await response.json();
      setFolders(Object.keys(categorizedEmails));
      alert("Emails sorted successfully!");
    } catch (error) {
      console.error("Error sorting emails:", error);
    }
  };

  return (
    <>
      <Navbar onLogout={onLogout} />
      <div className="container">
        <h1 className='title'>Email Categories</h1>
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

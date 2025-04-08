import React, { useState, useEffect } from 'react';
import Navbar from './NavBar';
import { saveData, loadData, STORAGE_KEYS } from '../utils/storage';

function MainPage({ onLogout, onFolderSelect }) {
  const [folders, setFolders] = useState([]);
  const [emailCounts, setEmailCounts] = useState({});
  const [loading, setLoading] = useState(false);

  const defaultFolders = ['Personal', 'Promotional', 'Urgent', 'Work'];

  const updateFolderUI = (emailsObj) => {
    const dynamicFolders = Object.keys(emailsObj);
    const mergedFolders = Array.from(new Set([...defaultFolders, ...dynamicFolders]));
    setFolders(mergedFolders);

    const counts = {};
    mergedFolders.forEach(folder => {
      counts[folder] = emailsObj[folder]?.length || 0;
    });
    setEmailCounts(counts);
  };

  useEffect(() => {
    const storedEmails = loadData(STORAGE_KEYS.EMAILS, {});
    console.log("🔍 STORED EMAILS:", storedEmails);
    updateFolderUI(storedEmails);
  }, []);

  const handleSortEmails = async () => {
    const user = loadData(STORAGE_KEYS.USER, {});
    if (!user.email) {
      alert("User not logged in.");
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(
        `http://127.0.0.1:5000/update-emails?email=${encodeURIComponent(user.email)}`
      );
      const categorizedEmails = await response.json();

      console.log("🚀 RESPONSE FROM BACKEND:", categorizedEmails);

      if (categorizedEmails.error) {
        alert(`Error: ${categorizedEmails.error}`);
        return;
      }

      saveData(STORAGE_KEYS.EMAILS, categorizedEmails);
      updateFolderUI(categorizedEmails); // ✅ refresh folders + counts
      alert("Emails sorted successfully!");
    } catch (error) {
      console.error("Error sorting emails:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Navbar onLogout={onLogout} />

      {loading && (
        <div className="loading-overlay">
          <div className="spinner" />
          <p>Sorting emails, please wait...</p>
        </div>
      )}

      <div className="container">
        <h1 className="title">Email Categories</h1>
        <button onClick={handleSortEmails}>Sort Emails</button>

        <div id="folder-list">
          {folders.length > 0 ? (
            folders.map((folder, index) => (
              <button
                key={index}
                className="secondary folder-btn"
                onClick={() => onFolderSelect(folder)}
              >
                {folder} ({emailCounts[folder] || 0})
              </button>
            ))
          ) : (
            <p>No folders available.</p>
          )}
        </div>
      </div>
    </>
  );
}

export default MainPage;

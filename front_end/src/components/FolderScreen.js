import React, { useEffect, useState } from 'react';
import Navbar from './Navbar';
import { loadData, STORAGE_KEYS } from '../utils/storage';
import { updateEmails } from '../utils/email';
import EmailCard from './EmailCard';

function FolderScreen({ folder, onBack, onLogout }) {
  const [emails, setEmails] = useState([]);

  // Load emails for the folder when this screen mounts.
  useEffect(() => {
    if (folder === 'Gmail') {
      const folderEmails = loadData(STORAGE_KEYS.EMAILS, []);
      setEmails(folderEmails);
    } else {
      setEmails([]);
    }
  }, [folder]);

  const handleUpdateEmails = async () => {
    await updateEmails();
    const updatedEmails = loadData(STORAGE_KEYS.EMAILS, []);
    if (folder === 'Gmail') {
      setEmails(updatedEmails);
    }
    alert('Emails updated successfully!');
  };

  return (
    <>
      <Navbar onLogout={onLogout} />
      <div className="container">
        <h1>{folder}</h1>
        <button onClick={handleUpdateEmails}>Update Emails</button>
        <div id="email-list">
          {folder === 'Gmail' && emails.length > 0 ? (
            emails.map((email, index) => (
              <EmailCard key={index} email={email} />
            ))
          ) : (
            <p>No emails available in {folder}.</p>
          )}
        </div>
        <button className="secondary" onClick={onBack}>
          Back
        </button>
      </div>
    </>
  );
}

export default FolderScreen;

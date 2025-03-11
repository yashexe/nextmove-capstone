import React, { useEffect, useState } from 'react';
import Navbar from './NavBar';
import { updateEmails } from '../utils/email';
import EmailCard from './EmailCard';

function FolderScreen({ folder, onBack, onLogout }) {
  const [emails, setEmails] = useState([]);

  useEffect(() => {
<<<<<<< HEAD
    // Fetch and display categorized emails
    async function fetchEmails() {
      try {
        const response = await fetch('http://127.0.0.1:5000/update-emails');
        const categorizedEmails = await response.json();
        setEmails(categorizedEmails[folder] || []);
      } catch (error) {
        console.error('Error fetching emails:', error);
      }
=======
    if (folder === 'Gmail') {
      const folderEmails = loadData(STORAGE_KEYS.EMAILS, []);
      setEmails(folderEmails);
    } else {
      setEmails([]);
>>>>>>> fc2f95b9cd2ad2f294f905c6aaf6ada048170ab6
    }
    fetchEmails();
  }, [folder]);

  return (
    <>
      <Navbar onLogout={onLogout} />
      <div className="container">
        <h1>{folder}</h1>
        <button onClick={() => updateEmails()}>Sort Emails</button>
        <div id="email-list">
          {emails.length > 0 ? (
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

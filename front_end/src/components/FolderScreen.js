import React, { useEffect, useState } from 'react';
import Navbar from './NavBar';
import EmailCard from './EmailCard';

function FolderScreen({ folder, onBack, onLogout }) {
  const [emails, setEmails] = useState([]);

  useEffect(() => {
    async function fetchEmails() {
      try {
        const response = await fetch('http://127.0.0.1:5000/update-emails');
        const categorizedEmails = await response.json();
        setEmails(categorizedEmails[folder] || []);
      } catch (error) {
        console.error('Error fetching emails:', error);
      }
    }
    fetchEmails();
  }, [folder]);

  return (
    <>
      <Navbar onLogout={onLogout} />
      <div className="container">
        <h1>{folder}</h1>
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

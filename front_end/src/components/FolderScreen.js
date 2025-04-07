import React, { useEffect, useState } from 'react';
import Navbar from './NavBar';
import EmailCard from './EmailCard';
import { loadEmails } from '../utils/email';

function FolderScreen({ folder, onBack, onLogout }) {
  const [emails, setEmails] = useState([]);

  useEffect(() => {
    const categorizedEmails = loadEmails();  // load from local storage
    setEmails(categorizedEmails[folder] || []);
  }, [folder]);  

  return (
    <>
      <Navbar onLogout={onLogout} />
      <div className="container">
        <h1 className='title'>{folder}</h1>
        <div id="email-list">
          {emails.length > 0 ? (
            emails.map((email, index) => (
              <EmailCard
                key={index}
                email={email}
                subject={email.subject}
                from={email.from}
                category={email.category}
                body={email.body} />
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

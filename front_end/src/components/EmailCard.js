import React from 'react';

function EmailCard({ email }) {
  const { from, subject } = email;
  return (
    <div className="email-card">
      <div className="card-header">
        <strong>From:</strong> {from}
      </div>
      <div className="card-subject">
        <strong>Subject:</strong> {subject}
      </div>
    </div>
  );
}

export default EmailCard;

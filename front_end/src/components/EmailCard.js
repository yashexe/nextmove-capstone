import React, { useState } from 'react';

function EmailCard({ subject, from, category, body, currentFolder, gmail_id }) {
  const [expanded, setExpanded] = useState(false);
  const showCategory = category?.toLowerCase() !== currentFolder?.toLowerCase();
  console.log("gmail_id:", gmail_id);

  return (
    <div className="email-card" onClick={() => setExpanded(!expanded)}>
      <p className="card-header"><strong>Subject:</strong> {subject}</p>
      <p className="card-subject"><strong>From:</strong> {from}</p>
      {showCategory && (
        <p className="card-body"><strong>Category:</strong> {category}</p>
      )}

      {expanded && (
        <>
          <div
            className="email-body"
            dangerouslySetInnerHTML={{ __html: body }}
          />
          {gmail_id && (
            <a
              href={`https://mail.google.com/mail/u/0/#inbox/${gmail_id}`}
              target="_blank"
              rel="noopener noreferrer"
              className="email-link"
              onClick={(e) => e.stopPropagation()}
            >
              Open in Gmail
            </a>
          )}
        </>
      )}
    </div>
  );
}

export default EmailCard;

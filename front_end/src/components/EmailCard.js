import React, { useState } from 'react';

function EmailCard({ subject, from, category, body }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className="email-card" onClick={() => setExpanded(!expanded)}>
      <p className="card-header"><strong>Subject:</strong> {subject}</p>
      <p className="card-subject"><strong>From:</strong> {from}</p>
      <p className="card-body"><strong>Category:</strong> {category}</p>

      {expanded && (
        <div
          className="email-body"
          dangerouslySetInnerHTML={{ __html: body }}
        />
      )}
    </div>
  );
}

export default EmailCard;

import React, { useState } from 'react';

function EmailCard({ subject, from, category, body }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className="email-card" onClick={() => setExpanded(!expanded)}>
      {/* Always show this in collapsed view */}
      <p className="card-header"><strong>Subject:</strong> {subject}</p>
      <p className="card-subject"><strong>From:</strong> {from}</p>
      <p className="card-body"><strong>Category:</strong> {category}</p>

      {/* Only show this when expanded */}
      {expanded && (
        <div className="email-body">
          <p>{body}</p>
        </div>
      )}
    </div>
  );
}

export default EmailCard;

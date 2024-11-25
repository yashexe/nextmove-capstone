// Card.js
export function Card(email) {
    // Destructure the email object
    const { from, subject, body } = email;

    // Create a card element
    const card = document.createElement("div");
    card.className = "email-card";

    // Card content
    card.innerHTML = `
      <div class="card-header">
        <strong>From:</strong> ${from}
      </div>
      <div class="card-subject">
        <strong>Subject:</strong> ${subject}
      </div>
      <div class="card-body">
        <p>${body}</p>
      </div>
    `;

    return card;
}

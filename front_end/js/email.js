import { saveData, loadData, STORAGE_KEYS } from './storage.js';
import { Card } from './card.js';

export async function updateEmails() {
  try {
    const response = await fetch('http://127.0.0.1:5000/update-emails');
    const emails = await response.json();
    saveData(STORAGE_KEYS.EMAILS, emails);
    alert('Emails updated successfully!');
  } catch (error) {
    console.error('Error updating emails:', error);
  }
}

export function loadEmails(folderName) {
  const emails = loadData(STORAGE_KEYS.EMAILS);
  const emailList = document.getElementById('email-list');
  emailList.innerHTML = '';

  // For demonstration, only display emails for Gmail.
  if (folderName === 'Gmail') {
    if (emails.length === 0) {
      emailList.innerHTML = '<p>No emails available in Gmail folder.</p>';
      return;
    }
    emails.forEach((email) => {
      const emailCard = Card(email);
      emailList.appendChild(emailCard);
    });
  } else {
    emailList.innerHTML = `<p>No emails available in ${folderName}.</p>`;
  }
}

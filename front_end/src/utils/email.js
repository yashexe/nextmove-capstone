import { saveData, loadData, STORAGE_KEYS } from './storage';

export async function updateEmails() {
  try {
    const response = await fetch('http://127.0.0.1:5000/update-emails');
    const emails = await response.json();
    saveData(STORAGE_KEYS.EMAILS, emails);
  } catch (error) {
    console.error('Error updating emails:', error);
  }
}

export function loadEmails() {
  return loadData(STORAGE_KEYS.EMAILS, {});
}

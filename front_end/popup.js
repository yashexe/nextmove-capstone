import { Card } from './Card.js'; // Import the Card component

// Helper: Save to localStorage
function saveData(key, value) {
  localStorage.setItem(key, JSON.stringify(value));
}

// Helper: Load from localStorage
function loadData(key) {
  return JSON.parse(localStorage.getItem(key)) || [];
}

// Initialize default folders for a user
function initializeDefaultFolders() {
  const folders = loadData('folders');
  const defaultFolders = ['Gmail', 'Outlook', 'Yahoo'];

  // Add default folders if they don't already exist
  defaultFolders.forEach((folder) => {
    if (!folders.includes(folder)) {
      folders.push(folder);
    }
  });

  saveData('folders', folders);
}

// Function to update emails from the backend
function updateEmails() {
  fetch('http://127.0.0.1:5000/update-emails') // Backend URL to update emails
    .then((response) => response.json()) // Parse the JSON response
    .then((emails) => {
      saveData('emails', emails); // Save emails to localStorage
      alert('Emails updated successfully!');
    })
    .catch((error) => console.error('Error updating emails:', error));
}

// Function to load emails from localStorage and display them in the Gmail folder only
function loadEmails(folderName) {
  const emails = loadData('emails'); // Load emails from localStorage
  const emailList = document.getElementById('email-list');
  emailList.innerHTML = ''; // Clear existing emails

  // Ensure emails are displayed only if the folder is "Gmail"
  if (folderName === 'Gmail') {
    if (emails.length === 0) {
      emailList.innerHTML = '<p>No emails available in Gmail folder.</p>';
      return;
    }

    // Display emails in the Gmail folder
    emails.forEach((email) => {
      const emailCard = Card(email); // Create email card
      emailList.appendChild(emailCard); // Append the card to the list
    });
  } else {
    emailList.innerHTML = `<p>No emails available in ${folderName}.</p>`;
  }
}

// Show Registration Screen
function showRegistrationScreen() {
  const content = document.getElementById('content');
  content.innerHTML = `
    <div class="container">
      <h1>Create Account</h1>
      <input type="text" id="name" placeholder="Name" />
      <input type="email" id="email" placeholder="Email" />
      <input type="password" id="password" placeholder="Password" />
      <select id="dob">
        <option value="" disabled selected>Date of Birth</option>
        <option value="1990">1990</option>
        <option value="2000">2000</option>
        <option value="2010">2010</option>
      </select>
      <button id="register-btn">Sign Up</button>
      <p>Already have an account? <button class="secondary" id="login-btn">Log in</button></p>
    </div>
  `;

  document.getElementById('register-btn').addEventListener('click', () => {
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const dob = document.getElementById('dob').value;

    if (name && email && password && dob) {
      saveData('user', { name, email, password, dob });
      initializeDefaultFolders(); // Initialize default folders on registration
      showVerificationScreen();
    } else {
      alert('All fields are required!');
    }
  });

  document.getElementById('login-btn').addEventListener('click', showVerificationScreen);
}

// Show Verification Screen
function showVerificationScreen() {
  const content = document.getElementById('content');
  content.innerHTML = `
    <div class="container">
      <h1>Log In</h1>
      <input type="email" id="email" placeholder="Email" />
      <input type="password" id="password" placeholder="Password" />
      <button id="login-btn">Log In</button>
    </div>
  `;

  document.getElementById('login-btn').addEventListener('click', () => {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const user = loadData('user');

    if (user.email === email && user.password === password) {
      initializeDefaultFolders(); // Ensure default folders exist for every login
      showMainPage();
    } else {
      alert('Invalid credentials!');
    }
  });
}

// Show Main Page
function showMainPage() {
  const content = document.getElementById('content');
  const folders = loadData('folders');
  content.innerHTML = `
    <div class="container">
      <h1>My Folders</h1>
      <button id="create-folder-btn">Create New Folder</button>
      <button id="update-emails-btn">Update Emails</button>
      <div id="folder-list"></div>
      <div id="email-list"></div>
    </div>
  `;

  const folderList = document.getElementById('folder-list');
  folders.forEach((folder) => {
    const folderButton = document.createElement('button');
    folderButton.className = 'secondary folder-btn';
    folderButton.dataset.folder = folder;
    folderButton.textContent = folder;
    folderList.appendChild(folderButton);
  });

  // Event listener to create new folder
  document.getElementById('create-folder-btn').addEventListener('click', showCreateFolderScreen);

  // Event listener for updating emails
  document.getElementById('update-emails-btn').addEventListener('click', updateEmails);

  // Event listeners for folder buttons
  document.querySelectorAll('.folder-btn').forEach((btn) => {
    btn.addEventListener('click', (e) => {
      showFolderScreen(e.target.dataset.folder);
    });
  });
}

// Show Folder Screen
function showFolderScreen(folderName) {
  const content = document.getElementById('content');
  content.innerHTML = `
    <div class="container">
      <h1>${folderName}</h1>
      <p>Emails in ${folderName}</p>
      <div id="email-list"></div>
      <button class="secondary" id="back-btn">Back</button>
    </div>
  `;

  loadEmails(folderName); // Load emails specific to the folder

  document.getElementById('back-btn').addEventListener('click', showMainPage);
}

// Show Create Folder Screen
function showCreateFolderScreen() {
  const content = document.getElementById('content');
  content.innerHTML = `
    <div class="container">
      <h1>Create Folder</h1>
      <input type="text" id="folder-name" placeholder="Folder Name" />
      <button id="create-btn">Create</button>
      <button class="secondary" id="back-btn">Back</button>
    </div>
  `;

  document.getElementById('create-btn').addEventListener('click', () => {
    const folderName = document.getElementById('folder-name').value;
    if (folderName) {
      const folders = loadData('folders');
      folders.push(folderName);
      saveData('folders', folders);
      showMainPage();
    } else {
      alert('Folder name is required!');
    }
  });

  document.getElementById('back-btn').addEventListener('click', showMainPage);
}

// Initialize
document.addEventListener('DOMContentLoaded', showRegistrationScreen);

import { saveData, loadData, STORAGE_KEYS, initializeDefaultFolders } from './storage.js';
import { updateEmails, loadEmails } from './email.js';

// Renders the given content inside the #content element.
export function render(content) {
  const app = document.getElementById('content');
  app.innerHTML = content;
}

// Log out helper: Clear user data and redirect to the login screen.
export function logoutUser() {
  localStorage.removeItem(STORAGE_KEYS.USER);
  showVerificationScreen();
}

export function showRegistrationScreen() {
  render(`
    <div class="container">
      <h1>Create Account</h1>
      <input type="text" id="name" placeholder="Name" />
      <input type="email" id="email" placeholder="Email" />
      <input type="password" id="password" placeholder="Password" />
      <button id="register-btn">Sign Up</button>
      <p>Already have an account?
        <button class="secondary" id="login-btn">Log in</button>
      </p>
    </div>
  `);

  document.getElementById('register-btn').addEventListener('click', () => {
    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value.trim();

    if (name && email && password) {
      saveData(STORAGE_KEYS.USER, { name, email, password});
      initializeDefaultFolders(); // Create default folders for the new user.
      showVerificationScreen();
    } else {
      alert('All fields are required!');
    }
  });

  document.getElementById('login-btn').addEventListener('click', showVerificationScreen);
}

export function showVerificationScreen() {
  render(`
    <div class="container">
      <h1>Log In</h1>
      <input type="email" id="email" placeholder="Email" />
      <input type="password" id="password" placeholder="Password" />
      <button id="login-btn">Log In</button>

      <!-- Add a 'Sign Up' button below -->
      <p>Don't have an account? 
        <button class="secondary" id="register-btn">Sign Up</button>
      </p>
    </div>
  `);

  // Existing login logic
  document.getElementById('login-btn').addEventListener('click', () => {
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value.trim();
    const user = loadData(STORAGE_KEYS.USER, {});

    if (user.email === email && user.password === password) {
      initializeDefaultFolders(); // Ensure folders exist on login
      showMainPage();
    } else {
      alert('Invalid credentials!');
    }
  });

  document.getElementById('register-btn').addEventListener('click', showRegistrationScreen);
}

export function showMainPage() {
  const folders = loadData(STORAGE_KEYS.FOLDERS);
  render(`
    <div class="header">
      <!-- Logout button in the header -->
      <button id="logout-btn">Log Out</button>
    </div>
    <div class="container">
      <h1>My Folders</h1>
      <button id="create-folder-btn">Create New Folder</button>
      <button id="update-emails-btn">Update Emails</button>
      <div id="folder-list"></div>
      <div id="email-list"></div>
    </div>
  `);

  // Bind logout functionality.
  document.getElementById('logout-btn').addEventListener('click', logoutUser);

  // Render folder buttons.
  const folderList = document.getElementById('folder-list');
  folders.forEach((folder) => {
    const folderButton = document.createElement('button');
    folderButton.className = 'secondary folder-btn';
    folderButton.dataset.folder = folder;
    folderButton.textContent = folder;
    folderList.appendChild(folderButton);
  });

  // Bind events.
  document.getElementById('create-folder-btn').addEventListener('click', showCreateFolderScreen);
  document.getElementById('update-emails-btn').addEventListener('click', updateEmails);

  // Use event delegation for folder button clicks.
  folderList.addEventListener('click', (e) => {
    if (e.target.classList.contains('folder-btn')) {
      showFolderScreen(e.target.dataset.folder);
    }
  });
}

export function showFolderScreen(folderName) {
  render(`
    <div class="header">
      <button id="logout-btn">Log Out</button>
    </div>
    <div class="container">
      <h1>${folderName}</h1>
      <p>Emails in ${folderName}</p>
      <div id="email-list"></div>
      <button class="secondary" id="back-btn">Back</button>
    </div>
  `);

  // Bind logout functionality in the folder view.
  document.getElementById('logout-btn').addEventListener('click', logoutUser);

  loadEmails(folderName);

  document.getElementById('back-btn').addEventListener('click', showMainPage);
}

export function showCreateFolderScreen() {
  render(`
    <div class="header">
      <button id="logout-btn">Log Out</button>
    </div>
    <div class="container">
      <h1>Create Folder</h1>
      <input type="text" id="folder-name" placeholder="Folder Name" />
      <button id="create-btn">Create</button>
      <button class="secondary" id="back-btn">Back</button>
    </div>
  `);

  // Bind logout functionality.
  document.getElementById('logout-btn').addEventListener('click', logoutUser);

  document.getElementById('create-btn').addEventListener('click', () => {
    const folderName = document.getElementById('folder-name').value.trim();
    if (folderName) {
      const folders = loadData(STORAGE_KEYS.FOLDERS);
      folders.push(folderName);
      saveData(STORAGE_KEYS.FOLDERS, folders);
      showMainPage();
    } else {
      alert('Folder name is required!');
    }
  });

  document.getElementById('back-btn').addEventListener('click', showMainPage);
}

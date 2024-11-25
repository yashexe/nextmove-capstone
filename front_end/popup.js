// Helper: Save to localStorage
function saveData(key, value) {
  localStorage.setItem(key, JSON.stringify(value));
}

// Helper: Load from localStorage
function loadData(key) {
  return JSON.parse(localStorage.getItem(key)) || [];
}

// Function to update emails from the backend
function updateEmails() {
  // Check if the "Gmail" folder exists
  const folders = loadData('folders');
  if (!folders.includes('Gmail')) {
    alert('The "Gmail" folder does not exist. Please create it first.');
    return;
  }

  fetch('http://127.0.0.1:5000/update-emails') // Backend URL to fetch emails
    .then((response) => response.json()) // Parse the JSON response
    .then((emails) => {
      // Save emails to localStorage under the "Gmail" folder
      saveData('Gmail_emails', emails);
      loadFolderEmails('Gmail'); // Display emails in the "Gmail" folder
    })
    .catch((error) => console.error('Error updating emails:', error));
}

// Function to load emails from a specific folder
function loadFolderEmails(folderName) {
  const emails = loadData(`${folderName}_emails`); // Load emails for the folder
  const content = document.getElementById('content');

  content.innerHTML = `
    <div class="container">
      <h1>${folderName}</h1>
      <div id="email-list">
        ${emails
      .map(
        (email) => `
          <div class="email-item">
            <strong>From:</strong> ${email.from} <br>
            <strong>Subject:</strong> ${email.subject} <br>
            <p>${email.body}</p>
          </div>
        `
      )
      .join('')}
      </div>
      <button class="secondary" id="back-btn">Back</button>
    </div>
  `;

  document.getElementById('back-btn').addEventListener('click', showMainPage);
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
      <div id="folder-list">
        ${folders
      .map(
        (folder) =>
          `<button class="secondary folder-btn" data-folder="${folder}">${folder}</button>`
      )
      .join('')}
      </div>
    </div>
  `;

  // Event listener to create new folder
  document.getElementById('create-folder-btn').addEventListener('click', showCreateFolderScreen);

  // Event listener for updating emails
  document.getElementById('update-emails-btn').addEventListener('click', updateEmails);

  // Event listeners for folder buttons
  document.querySelectorAll('.folder-btn').forEach((btn) => {
    btn.addEventListener('click', (e) => {
      loadFolderEmails(e.target.dataset.folder);
    });
  });
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
showMainPage();

// Elements
const content = document.getElementById('content');

// Function to load the home screen
function showHomeScreen() {
  content.innerHTML = `
    <div class="container">
      <h1>Email Sorter</h1>
      <button id="gmail-btn">Gmail</button>
      <button id="outlook-btn">Outlook</button>
      <button id="yahoo-btn">Yahoo</button>
    </div>
  `;

  // Add event listeners to buttons
  document.getElementById('gmail-btn').addEventListener('click', function() {
    showEmailScreen('Gmail');
  });
  document.getElementById('outlook-btn').addEventListener('click', function() {
    showEmailScreen('Outlook');
  });
  document.getElementById('yahoo-btn').addEventListener('click', function() {
    showEmailScreen('Yahoo');
  });
}

// Function to load a generic email screen
function showEmailScreen(espName) {
  content.innerHTML = `
    <div class="container">
      <h1>${espName} Inbox</h1>
      <p>This is the ${espName} page.</p>
      <button id="back-home-${espName.toLowerCase()}">Back to Home</button>
    </div>
  `;
  
  // Add back button functionality dynamically
  document.getElementById(`back-home-${espName.toLowerCase()}`).addEventListener('click', showHomeScreen);
}

// Initialize by showing the home screen
showHomeScreen();

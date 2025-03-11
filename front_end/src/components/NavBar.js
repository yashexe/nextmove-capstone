import React, { useState } from 'react';

function Navbar({ onLogout }) {
  const [isOpen, setIsOpen] = useState(false);
  const [darkMode, setDarkMode] = useState(false);

  const toggleNavbar = () => setIsOpen(prev => !prev);
  const toggleDarkMode = () => {
    setDarkMode(prev => !prev);
    document.body.classList.toggle('dark-mode');
  };

  const darkModeText = darkMode ? 'Light Mode' : 'Dark Mode';

  return (
    <>
      <button id="navbar-toggle" onClick={toggleNavbar}>
        &#9776;
      </button>
      <div className={`navbar ${isOpen ? 'open' : ''}`}>
        <button className="navbar-btn" onClick={onLogout}>
          Logout
        </button>
        <button className="navbar-btn" onClick={toggleDarkMode}>
          {darkModeText}
        </button>
      </div>
    </>
  );
}

export default Navbar;

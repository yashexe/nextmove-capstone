import React, { useEffect, useState } from 'react';
import { saveBoolean, loadBoolean, STORAGE_KEYS } from '../utils/storage';

function Navbar({ onLogout }) {
  const [isOpen, setIsOpen] = useState(false);
  const [darkMode, setDarkMode] = useState(loadBoolean(STORAGE_KEYS.DARK_MODE));

  const toggleNavbar = () => setIsOpen(prev => !prev);

  const toggleDarkMode = () => {
    const newMode = !darkMode;
    setDarkMode(newMode);
    document.body.classList.toggle('dark-mode', newMode);
    saveBoolean(STORAGE_KEYS.DARK_MODE, newMode);
  };

  useEffect(() => {
    if (darkMode) {
      document.body.classList.add('dark-mode');
    } else {
      document.body.classList.remove('dark-mode');
    }
  }, [darkMode]);

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

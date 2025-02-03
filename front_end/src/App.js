// src/App.js
import React, { useState } from 'react';
import LoginScreen from './components/LoginScreen';
import RegistrationScreen from './components/RegistrationScreen';
import MainPage from './components/MainPage';
import FolderScreen from './components/FolderScreen';
import './styles/styles.css';

function App() {
  // screen can be 'login', 'register', or 'main'
  const [screen, setScreen] = useState('login');
  // When a folder is selected, we store its name here.
  const [currentFolder, setCurrentFolder] = useState(null);

  const handleLoginSuccess = () => setScreen('main');
  const handleRegisterClick = () => setScreen('register');
  const handleRegistrationSuccess = () => setScreen('login');
  const handleLogout = () => {
    setScreen('login');
    setCurrentFolder(null);
  };

  if (screen === 'login') {
    return (
      <LoginScreen
        onLoginSuccess={handleLoginSuccess}
        onRegisterClick={handleRegisterClick}
      />
    );
  } else if (screen === 'register') {
    return (
      <RegistrationScreen
        onRegistrationSuccess={handleRegistrationSuccess}
        onBackToLogin={() => setScreen('login')}
      />
    );
  } else if (screen === 'main' && !currentFolder) {
    return (
      <MainPage
        onLogout={handleLogout}
        onFolderSelect={(folder) => setCurrentFolder(folder)}
      />
    );
  } else if (screen === 'main' && currentFolder) {
    return (
      <FolderScreen
        folder={currentFolder}
        onBack={() => setCurrentFolder(null)}
        onLogout={handleLogout}
      />
    );
  }
  return null;
}

export default App;

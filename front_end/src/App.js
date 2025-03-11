import React, { useState } from 'react';
import LoginScreen from './components/LoginScreen';
import RegistrationScreen from './components/RegistrationScreen';
import MainPage from './components/MainPage';
import FolderScreen from './components/FolderScreen';
import './styles/styles.css';

function App() {
  const [screen, setScreen] = useState('login');
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

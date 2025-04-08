/* global chrome */
import React, { useEffect, useState } from 'react';
import LoginScreen from './components/LoginScreen';
import RegistrationScreen from './components/RegistrationScreen';
import MainPage from './components/MainPage';
import FolderScreen from './components/FolderScreen';
import './styles/styles.css';

function App() {
  const [screen, setScreen] = useState('login');
  const [currentFolder, setCurrentFolder] = useState(null);
  const [activeTabUrl, setActiveTabUrl] = useState('');
  const [checkingTab, setCheckingTab] = useState(true);

  useEffect(() => {
    if (typeof chrome !== 'undefined' && chrome.tabs) {
      chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        setActiveTabUrl(tabs[0]?.url || '');
        setCheckingTab(false);
      });
    } else {
      // If running in dev (no chrome object)
      setCheckingTab(false);
    }
  }, []);

  const isGmail = activeTabUrl.includes("mail.google.com");

  const handleLoginSuccess = () => setScreen('main');
  const handleRegisterClick = () => setScreen('register');
  const handleRegistrationSuccess = () => setScreen('login');
  const handleLogout = () => {
    setScreen('login');
    setCurrentFolder(null);
  };

  if (checkingTab) {
    return <div className="container">Checking current tab...</div>;
  }

  if (!isGmail && activeTabUrl) {
    return (
      <div className="container">
        <h1>NextMove Extension</h1>
        <p>Your smart Gmail email organizer extension.</p>
        <p>Please navigate to <strong>mail.google.com</strong> and open this extension again.</p>
        <button onClick={() => chrome.tabs.create({ url: 'https://mail.google.com' })}>
          Go to Gmail
        </button>
      </div>
    );
  }

  if (!activeTabUrl) {
    // Dev mode fallback
    return (
      <div className="container">
        <h1>NextMove Extension (Development Mode)</h1>
        <p>Chrome API not available in local dev.</p>
        <p>This popup will only show the full app when loaded as an extension.</p>
      </div>
    );
  }

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

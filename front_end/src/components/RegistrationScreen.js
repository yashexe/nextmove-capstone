// src/components/RegistrationScreen.js
import React, { useState } from 'react';
import { saveData, STORAGE_KEYS, initializeDefaultFolders } from '../utils/storage';

function RegistrationScreen({ onRegistrationSuccess, onBackToLogin }) {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleRegister = () => {
    if (name && email && password) {
      saveData(STORAGE_KEYS.USER, { name, email, password });
      initializeDefaultFolders();
      onRegistrationSuccess(); // Redirect to login after registration
    } else {
      alert('All fields are required!');
    }
  };

  return (
    <div className="container">
      <h1>Create Account</h1>
      <input
        type="text"
        placeholder="Name"
        value={name}
        onChange={e => setName(e.target.value)}
      />
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={e => setEmail(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={e => setPassword(e.target.value)}
      />
      <button onClick={handleRegister}>Sign Up</button>
      <p>
        Already have an account?{' '}
        <button className="secondary" onClick={onBackToLogin}>
          Log in
        </button>
      </p>
    </div>
  );
}

export default RegistrationScreen;

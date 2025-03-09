import React, { useState } from 'react';
import { loadData, STORAGE_KEYS } from '../utils/storage';

function LoginScreen({ onLoginSuccess, onRegisterClick }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = () => {
    const user = loadData(STORAGE_KEYS.USER, {});
    if (user.email === email && user.password === password) {
      onLoginSuccess();
    } else {
      alert('Invalid credentials!');
    }
  };

  return (
    <div className="container">
      <h1>Log In</h1>
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
      <button onClick={handleLogin}>Log In</button>
      <p>
        Don't have an account?{' '}
        <button className="secondary" onClick={onRegisterClick}>
          Sign Up
        </button>
      </p>
    </div>
  );
}

export default LoginScreen;

import React, { useState } from 'react';
import { saveData, STORAGE_KEYS, initializeDefaultFolders } from '../utils/storage';

function RegistrationScreen({ onRegistrationSuccess, onBackToLogin }) {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleRegister = async () => {
    if (name && email && password) {
      try {
        const response = await fetch("http://localhost:5000/register", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ email }),
        });
  
        const result = await response.json();
  
        if (!response.ok) {
          alert(result.error);  // shows "Email already registered", or "Email does not match..."
          return;
        }
  
        // If registration is successful
        saveData(STORAGE_KEYS.USER, { name, email, password });
        initializeDefaultFolders();
        alert("Registration successful!");
        onRegistrationSuccess();
  
      } catch (error) {
        console.error("Registration failed:", error);
        alert("An error occurred. Please try again.");
      }
    } else {
      alert("All fields are required!");
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

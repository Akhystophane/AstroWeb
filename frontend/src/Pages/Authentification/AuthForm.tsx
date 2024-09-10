import React, { useState } from 'react';
import { signUp, signIn } from './firebaseAuth';  // Assure-toi que les chemins d'importation sont corrects

const AuthForm: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isSignUp, setIsSignUp] = useState(true);  // Toggle entre inscription et connexion

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (isSignUp) {
      signUp(email, password);
    } else {
      signIn(email, password);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
      />
      <button type="submit">{isSignUp ? 'Sign Up' : 'Sign In'}</button>
      <button type="button" onClick={() => setIsSignUp(!isSignUp)}>
        Switch to {isSignUp ? 'Sign In' : 'Sign Up'}
      </button>
    </form>
  );
};

export default AuthForm;

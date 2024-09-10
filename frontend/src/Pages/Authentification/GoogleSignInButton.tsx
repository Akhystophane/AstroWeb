import React from 'react';
import { signInWithGoogle } from './firebaseAuth';  // Assure-toi que les chemins d'importation sont corrects

const GoogleSignInButton: React.FC = () => {
  return (
    <button onClick={signInWithGoogle}>
      Connexion avec Google
    </button>
  );
};

export default GoogleSignInButton;

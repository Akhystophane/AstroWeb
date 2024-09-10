import React, { useState } from 'react';
import Modal from 'react-modal';
import AuthForm from '../Authentification/AuthForm';
import GoogleSignInButton from '../Authentification/GoogleSignInButton';

Modal.setAppElement('#root'); // Assure-toi que cela est défini dans ton composant racine
interface SignInModalProps {
    isOpen: boolean;
    onClose: () => void; // Définit que onClose est une fonction qui ne retourne rien
  }
  
  const AuthPopup: React.FC<SignInModalProps> = ({ isOpen, onClose }) => {
    console.log(isOpen)
    return (
        <Modal
        isOpen={isOpen}
        onRequestClose={onClose}
        contentLabel="Sign In"
        className="modal-content max-w-md w-full bg-gradient-to-br from-purple-600 to-indigo-700 p-8 rounded-2xl shadow-2xl mx-auto my-12 outline-none transform transition-all duration-300 ease-in-out"
        overlayClassName="modal-overlay fixed inset-0 bg-black bg-opacity-75 backdrop-blur-sm flex justify-center items-center"
        >
        <div className="flex flex-col items-center">
            <h2 className="text-3xl font-bold text-white mb-6">Welcome Back</h2>
            <AuthForm />
            <div className="w-full mb-6">
            <GoogleSignInButton />
            </div>
            <button 
            onClick={onClose} 
            className="mt-4 bg-white text-indigo-700 px-6 py-2 rounded-full hover:bg-indigo-100 transition duration-300 ease-in-out font-semibold text-sm uppercase tracking-wider"
            >
            Close
            </button>
        </div>
        </Modal>
      );
    };
    
  
  export default AuthPopup;
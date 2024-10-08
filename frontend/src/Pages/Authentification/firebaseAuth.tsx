import { 
    getAuth, onAuthStateChanged, createUserWithEmailAndPassword, 
    signInWithEmailAndPassword, UserCredential, AuthError, 
    User, signInWithPopup, GoogleAuthProvider,
} from "firebase/auth";
import {signInAnonymously} from "firebase/auth";
import { initializeApp } from "firebase/app";
import { useEffect, useState } from "react";
const authDomainUrl = process.env.NODE_ENV === 'production'
  ? 'www.astro-nomos.com'
  : 'astronomos-ef1e7.firebaseapp.com';
const firebaseConfig = {
    apiKey: "AIzaSyBBimzONdvbR7yujr7NPK4SQWGGo2EfMuE",
    authDomain: authDomainUrl,
    projectId: "astronomos-ef1e7",
    storageBucket: "astronomos-ef1e7.appspot.com",
    messagingSenderId: "58453053128",
    appId: "1:58453053128:web:977f164540c7d204639ffd",
    measurementId: "G-R75EH3WQRF"
  };
  
  const app = initializeApp(firebaseConfig);
  //const analytics = getAnalytics(app);
  const auth = getAuth(app);
  const googleProvider = new GoogleAuthProvider();
  export { app, auth };
  
// Fonction d'inscription avec callback
export const signUp = (email: string, password: string, onSuccess?: () => void): void => {
    createUserWithEmailAndPassword(auth, email, password)
        .then((_userCredential: UserCredential) => {
            //console.log(userCredential.user);
            if (onSuccess) onSuccess();  // Appeler le callback de succès si fourni
        })
        .catch((_error: AuthError) => {
            //console.error(error.message);
        });
};

// Fonction de connexion avec callback
export const signIn = (email: string, password: string, onSuccess?: () => void): void => {
    signInWithEmailAndPassword(auth, email, password)
        .then((_userCredential: UserCredential) => {
            //console.log(userCredential.user);
            if (onSuccess) onSuccess();  // Appeler le callback de succès si fourni
        })
        .catch((_error: AuthError) => {
            //console.error(error.message);
        });
};
  
  export const useAuthState = (): User | null => {
      const [user, setUser] = useState<User | null>(null);
  
      useEffect(() => {
          const unsubscribe = onAuthStateChanged(auth, setUser);
          return unsubscribe;
      }, []);
  
      return user;
  };
  
  export const signInWithGoogle = (): void => {
      signInWithPopup(auth, googleProvider)
          .then((_result) => {
              //console.log("User signed in: ", result.user);
          }).catch((_error) => {
              //console.error("Error signing in: ", error);
          });
  };

  export const signInAnonymouslyCustom = () => {
    const auth = getAuth(); // Ensure your Firebase app is initialized before this line

    // Returns the promise so that the caller can handle the response
    return signInAnonymously(auth)
        .then(userCredential => {
            // You can handle the successful login here if needed
            console.log("User signed in anonymously with UID:", userCredential.user.uid);
            return userCredential; // Optional: return the userCredential for further processing
        })
        .catch(error => {
            console.error("Error signing in anonymously:", error);
            throw error; // Optional: re-throw the error for the caller to handle
        });
};
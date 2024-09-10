import Card from "../../components/Card";
import StarsBackground from '../../assets/StarsBackground.svg';
import { useLocation } from "react-router-dom";
import SunAnimation from "./components/SunAnimation";
import Bottom from '../../assets/BirthChart/bottom.svg';
import pic1 from '../../assets/BirthChart/pic1.svg';

import { useAuthState } from "../Authentification/firebaseAuth";
import AuthForm from "../Authentification/AuthForm";
import GoogleSignInButton from "../Authentification/GoogleSignInButton";
import { getAuth, User } from "firebase/auth";
import { initializeApp } from "firebase/app";
import { useState } from "react";

const Horoscope = () => {
  const firebaseConfig = {
    apiKey: "AIzaSyBBimzONdvbR7yujr7NPK4SQWGGo2EfMuE",
    authDomain: "astronomos-ef1e7.firebaseapp.com",
    projectId: "astronomos-ef1e7",
    storageBucket: "astronomos-ef1e7.appspot.com",
    messagingSenderId: "58453053128",
    appId: "1:58453053128:web:977f164540c7d204639ffd",
    measurementId: "G-R75EH3WQRF"
  };
  
  const app = initializeApp(firebaseConfig);
  const user = useAuthState();
  const auth = getAuth(app);
  const location = useLocation();
  const transitChartData = location.state;
  console.log(transitChartData);  // The transit data generated from the backend

  const [isPopVisible, setPopVisible] = useState(false);

  const openModal = () => setPopVisible(true);
  const closeModal = () => setPopVisible(false);
  const handleLoginSuccess = () => {
    closeModal();  // Fermer le modal
    console.log('Utilisateur connecté avec succès !');
  };
  

  if (!transitChartData) {
    return (
      <div className="w-full h-full min-h-screen mx-auto" style={{ backgroundImage: `url(${StarsBackground})`, backgroundSize: 'cover', backgroundPosition: 'center' }}>
        <h1 className='h1 mb-6 pb-2 pt-5'>Oh Oh une erreur est survenue...</h1>
        <SunAnimation />
      </div>
    );  // Display an error message if the data is not yet available
  }

  // Convert objects to an array to map over them
  const cards = Object.keys(transitChartData).map(key => transitChartData[key]);

  return (
    <>
      <div className="w-full h-full mx-auto" style={{ backgroundImage: `url(${StarsBackground})`, backgroundSize: 'cover', backgroundPosition: 'center' }}>
        <div className="w-full h-full">
          <div className="text-center">
            <h1 className='h1 mb-6 pb-2 pt-5'>Découvrez votre carte de transit unique</h1>
            <span className="text-black text-6xl">🔮👇</span>
            <SunAnimation />
          </div>
          
          {cards.map((card, index) => (
        <div key={index} className="w-full h-full">
        <h2  className="text-3xl mt-[4rem] font-extrabold text-center mb-8 bg-gradient-to-r from-gray-300 via-gray-500 to-gray-300 bg-clip-text text-transparent animate-pulse">
        {card.title} <span className="text-black">🌠 😍</span>
      </h2>
      <Card
          title={card.subtitle}
          description={card.description}
          imageUrl={pic1}
        />
        </div>

        ))}

    <div>
      {user ? (
        <div>
          <p>Welcome, {user.email}</p>
          <button onClick={() => auth.signOut()}>Sign Out</button>
        </div>
      ) : (
        <div>
          {/* Contenu pour les utilisateurs non connectés */}
        </div>
      )}
      
      {isPopVisible && user && user.isAnonymous && (
        <div className="modal">
          <AuthForm />
          <GoogleSignInButton />
        </div>
      )}
    </div>
        </div>
        <div className="mt-[6rem]">
          <img className="" src={Bottom} alt="Bottom decorative" />
        </div>
      </div>
    </>
  );
};

export default Horoscope;

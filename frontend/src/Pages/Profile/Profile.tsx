import StarsBackground from '../../assets/StarsBackground.svg';
import SunAnimation from "./components/SunAnimation";
import axios from 'axios';
import { useAuthState } from "../Authentification/firebaseAuth";
import { useEffect, useState } from "react";

const Profile = () => {
  const user = useAuthState();

  const [profileData, setProfileData] = useState({
    birth_location: '',
    birth_time: '',
    birth_date: ''
  });


  useEffect(() => {
    if (user) {
      
      // Faire une requête pour récupérer les données de l'utilisateur
      axios.get(`http://localhost:8000/react/${user.uid}`)  // Remplacez `your-api-url.com` par votre URL réelle
        .then(response => {
          setProfileData(response.data); 
          console.log('data: ', response.data) // Mettre à jour les données du profil avec les données récupérées
        })
        .catch(error => {
          console.error("Erreur lors de la récupération des données utilisateur :", error);
        });
    }
  }, [user]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setProfileData(prevState => ({
      ...prevState,
      [name]: value
    }));
  };
  

  const handleSave = async () => {
    if (user) {
    try {
      console.log(user.uid, profileData)
      const response = await axios.put(`http://127.0.0.1:8000/react/${user.uid}`, profileData, {
        headers: {
          'Content-Type': 'application/json',
          // Ajoutez ici d'autres headers si nécessaire
        },
      });
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la mise à jour:', error);
      throw error;
    }}
  };

  if (user && user.isAnonymous) {
    return (
      <div className="w-full h-full min-h-screen mx-auto" style={{ backgroundImage: `url(${StarsBackground})`, backgroundSize: 'cover', backgroundPosition: 'center' }}>
        <h1 className='h1 mb-6 pb-2 pt-5'>Oh Oh une erreur est survenue...</h1>
        <SunAnimation />
      </div>
    );  // Display an error message if the data is not yet available
  }

  return (
    <div>
      <h1>Profile</h1>
      <div>
        <label>
          Birth Location:
          <input
            type="text"
            name="birth_location"
            value={profileData.birth_location ?? ''}  // Utilisez une valeur par défaut vide
            onChange={handleChange}
          />
        </label>
        <label>
          Birth Time:
          <input
            type="time"
            name="birth_time"
            value={profileData.birth_time ?? ''}  // Utilisez une valeur par défaut vide
            onChange={handleChange}
          />
        </label>
        <label>
          Birth Date:
          <input
            type="date"
            name="birth_date"
            value={profileData.birth_date ?? ''}  // Utilisez une valeur par défaut vide
            onChange={handleChange}
          />
        </label>
        <button onClick={handleSave}>Save Changes</button>
      </div>
    </div>
  );
};

export default Profile;
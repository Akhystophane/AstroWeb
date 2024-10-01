import Card from '../../../components/Card'
import BirthCardPic from '../../../assets/BirthCard.svg'
import React, { useEffect, useState } from 'react';
import axios, { AxiosError } from 'axios';
import { useNavigate } from 'react-router-dom';
import { signInAnonymouslyCustom, useAuthState } from '../../Authentification/firebaseAuth';
import { onAuthStateChanged } from 'firebase/auth';
import { auth } from '../../Authentification/firebaseAuth'; 
import SunAnimation from '../../BirthChart/components/SunAnimation';

interface FormData {
  name: string;
  birth_date: string;
  birth_time: string;
  birth_location: string; 
}
const BirthChartSection = () => {

  const user = useAuthState();
  const navigate = useNavigate();
  const [formData, setFormData] = useState<FormData>({
    name: '',
    birth_date: '',
    birth_time: '00:00',
    birth_location: ''
  });

  const [idToken, setIdToken] = useState<string | null>(null);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (currentUser) => {
      if (currentUser) {
        //console.log('Utilisateur connecté:', currentUser);
        const token = await currentUser.getIdToken();
        setIdToken(token);
      } else {
        //console.log('Utilisateur non connecté. Connexion anonyme en cours...');
        signInAnonymouslyCustom()
          .then(async (result) => {
            console.log('Signed in anonymously', result.user);
            if (result.user) {
              const token = await result.user.getIdToken();
              setIdToken(token);
            }
          })
          .catch(_error => {
            console.error('Anonymous sign-in failed', _error);
          });
      }
    });

    return () => unsubscribe();
  }, [auth]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [isBirthTime, setIsBirthTime] = useState(false); // For the "Horoscope du jour" checkbox

  const birthChartUrl = process.env.NODE_ENV === 'production'
    ? 'https://astronomos-fee5d7c001d2.herokuapp.com/charts/birth/'
    : 'http://localhost:8000/charts/birth/';


  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!idToken) {
      console.error('ID Token not available');
      return;
    }
    console.log("Form Data:", formData);
    setLoading(true);
    setErrorMessage(null);
  
    try {
      const response = await axios.post(birthChartUrl, formData, {
        headers: {
          'Authorization': `Bearer ${idToken}`
        }
      });
  
      console.log('Form submitted successfully:', response.data);
      navigate('birth-chart', { state: response.data.birth_chart });
    } catch (error) {
      if (axios.isAxiosError(error)) {
        const axiosError = error as AxiosError;
        if (axiosError.response?.status === 429) {
          //const retryAfter = axiosError.response.headers['retry-after'];
          setErrorMessage(`Tu as atteint la limite de requêtes. Réessaye dans une heure 😀 `);
        } else {
          setErrorMessage('Une erreur est survenue lors de la soumission du formulaire. Veuillez réessayer.');
        }
      } else {
        setErrorMessage('Une erreur inattendue est survenue. Veuillez réessayer.');
      }
      console.error('There was an error submitting the form!', formData, error);
    } finally {
      setLoading(false);
    }
  };

  

  const form = (
    <form onSubmit={handleSubmit}>
      <div className={`mb-4 `}>
        <label htmlFor="name" className="block text-sm font-medium text-gray-700">Prénom</label>
        <input
          type="text"
          id="name"
          name="name"
          value={formData.name}
          onChange={handleChange}
          className="mt-1 p-2 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
          required
        />
      </div>
      
      <div className={`mb-4 `}>
        <label htmlFor="birth_date" className="block text-sm font-medium text-gray-700">Date de naissance</label>
        <input
          type="date"
          id="birth_date"
          name="birth_date"
          value={formData.birth_date}
          onChange={handleChange}
          className="mt-1 p-2 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
          required
        />
      </div>
  
      <div className="mb-4 ">
            <label htmlFor="birth_time" className="block text-sm font-medium text-gray-700">Heure de naissance</label>
            <div className="flex items-center mt-1">
            <input
              type="time"
              id="birth_time"
              name="birth_time"
              value={formData.birth_time}
              onChange={handleChange}
              className="mt-1 p-2 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
              required
              disabled={isBirthTime}
            />
              <label className="flex items-center text-gray-700 ml-5">
              <input
                type="checkbox"
                checked={isBirthTime}
                onChange={() => setIsBirthTime(!isBirthTime)}
                className="mr-2"
              />
              Inconnue
            </label>
            </div>
          </div>
  
      <div className="mb-4">
        <label htmlFor="birth_location" className="block text-sm font-medium text-gray-700">Lieu de naissance</label>
        <input
          type="text"
          id="birth_location"
          name="birth_location"
          value={formData.birth_location}
          onChange={handleChange}
          className="mt-1 p-2 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
          required
        />
      </div>
  
      <button type="submit" disabled={!idToken || loading} className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700">
        {loading ? "Chargement..." : "Soumettre"}
      </button>

    </form>
  );

  useEffect(() => {
    if (loading) {
      document.body.classList.add('overflow-hidden'); // Empêche le scroll sur body
    } else {
      document.body.classList.remove('overflow-hidden'); // Permet le scroll
    }

    return () => {
      // Nettoyage : assurez-vous que le scroll est activé lorsque le composant est démonté
      document.body.classList.remove('overflow-hidden');
    };
  }, [loading]);
  

  return (
    <>
      <div className="relative">
        <div className={`p-5 px-4 mt-5 sm:px-6 lg:px-8 bg-transparent ${loading ? 'pointer-events-none' : ''}`} id='birth_chart'>
          <h2 className="text-3xl font-extrabold text-center mb-8 bg-gradient-to-r from-gray-300 via-gray-500 to-gray-300 bg-clip-text text-transparent animate-pulse">
            Ta carte de naissance personnalisée <span className='text-black'>🌠 😍</span>
          </h2>
          {!errorMessage ? (
            <div className="flex justify-center">
            <div className={`${loading ? 'blur-sm' : ''}`}>
              <Card
                user={user}
                title="Découvre ta Carte de Naissance"
                description="Savais-tu que l'horoscope que tu lis chaque jour ne te raconte qu'une petite partie de l'histoire 👀 ?..  Pour vraiment comprendre ce qui se passe dans ta vie et mieux anticiper les événements à venir, explorer ta carte de transit est essentiel. Elle te montre l'influence actuelle des planètes sur toi, en fonction de ta carte de naissance unique. 🌌"
                buttonText="Créer ma Carte de Naissance"
                buttonLink="#"
                imageUrl={BirthCardPic}
                formContent={form}
              />
            </div>
            {loading && (
              <>
{/*                 <div className="absolute top-[50%]  sm:top-[50%] md:top-[50%] lg:top-[50%] left-0 w-full text-center pointer-events-none z-50">
                  <p className="text-2xl font-bold text-gray-700">Chargement</p>
                </div> */}
                <div className="absolute top-[40%] sm:top-[20%] md:top-[0] lg:top-0 left-0 w-full h-full pointer-events-none z-40">
                  <SunAnimation rotationSpeed={3} />
                </div>
              </>
            )}
          </div >) : (
              <div className="flex items-center justify-center inset-0 z-50">
              <div className="text-red-500 p-2 text-[1.25rem] ">
                {errorMessage}
              </div>
            </div>)

        }
        </div>
      </div>
    </>
  );
}

export default BirthChartSection;

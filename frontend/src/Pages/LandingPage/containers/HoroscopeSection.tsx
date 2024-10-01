import React, { useEffect, useState } from 'react';
import axios, { AxiosError } from 'axios';
import { useNavigate } from 'react-router-dom';
import { useAuthState } from '../../Authentification/firebaseAuth';
import Card from '../../../components/Card'; // Ensure the path to Card is correct.
import HoroscopeCardPic from '../../../assets/HoroscopeCard.jpg';
import { auth } from '../../Authentification/firebaseAuth'; 
import SunAnimation from '../../BirthChart/components/SunAnimation';


interface TransitFormData {
  name?: string;
  birth_date: string;
  birth_time: string;
  birth_location: string;
  transit_start_date: string;
  transit_end_date: string;
}

const HoroscopeSection = () => {
  const user = useAuthState();
  const navigate = useNavigate();
  const [formData, setFormData] = useState<TransitFormData>({
    birth_date: '',
    birth_time: '00:00',
    birth_location: '',
    transit_start_date: '',
    transit_end_date: '',
  });

  const [loading, setLoading] = useState(false);
  //const [isBirthDataLoaded, setIsBirthDataLoaded] = useState(false); // To track if user data is loaded
  const [isDailyHoroscope, setIsDailyHoroscope] = useState(true); // For the "Horoscope du jour" checkbox
  const [isBirthTime, setIsBirthTime] = useState(false); // For the "Horoscope du jour" checkbox

  

  // Calculate today's and tomorrow's date
  useEffect(() => {
    if (isDailyHoroscope) {
      const today = new Date();
      const tomorrow = new Date(today);
      tomorrow.setDate(today.getDate() + 1);
      //console.log("date" + tomorrow.toISOString().split('T')[0])

      setFormData(prevFormData => ({
        ...prevFormData,
        transit_start_date: today.toISOString().split('T')[0], // Format 'YYYY-MM-DD'
        transit_end_date: tomorrow.toISOString().split('T')[0],
      }));
    }
  }, [isDailyHoroscope]);


/*   useEffect(() => {
    if (user && !user.isAnonymous ) {
      const firebaseUid = auth.currentUser?.uid;
      auth.currentUser?.getIdToken().then(idToken => {
        axios.get(`http://localhost:8000/user/data/${firebaseUid}/`, {
          headers: {
            'Authorization': `Bearer ${idToken}`
          }
        })
        .then(response => {
          const userData = response.data[0];

          if (userData) {
            setFormData(prevFormData => ({
              ...prevFormData,
              birth_date: userData.birth_date,
              birth_time: userData.birth_time,
              birth_location: userData.birth_location,
              name: userData.name || '',
            }));
            setIsBirthDataLoaded(true);
          }
        })
        .catch(error => {
          console.error('Error fetching user data:', error);
        });
      });
    }
  }, [user]); */

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const transitChartUrl = process.env.NODE_ENV === 'production'
  ? 'https://astronomos-fee5d7c001d2.herokuapp.com/charts/transit/'
  : 'http://localhost:8000/charts/transit/';
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setErrorMessage(null);


  
    try {
      const idToken = await auth.currentUser?.getIdToken();
      if (!idToken) {
        throw new Error('ID Token not available');
      }
  
      const response = await axios.post(transitChartUrl, formData,
      {
        headers: {
          'Authorization': `Bearer ${idToken}`
        }
      });
  
      //console.log('Form submitted successfully:', response.data);
      navigate('/transit-chart', { state: response.data.transit_chart });
    } catch (error) {
      if (axios.isAxiosError(error)) {
        const axiosError = error as AxiosError;
        if (axiosError.response?.status === 429) {
          //const retryAfter = axiosError.response.headers['retry-after'];
          setErrorMessage(`Tu as atteint la limite de requêtes. Réessaye dans une heure 😀 .`);
        } else {
          setErrorMessage('Une erreur est survenue lors de la soumission du formulaire. Veuillez réessayer.');
        }
      } else if (error instanceof Error) {
        setErrorMessage(error.message);
      } else {
        setErrorMessage('Une erreur inattendue est survenue. Veuillez réessayer.');
      }
      //console.error('There was an error submitting the form!', error);
      //console.log(formData);
    } finally {
      setLoading(false);
    }
  };

  const form = (
    <form onSubmit={handleSubmit}>

        <>
          <div className="mb-4">
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
        </>

            {/* Checkbox for "Horoscope du jour" */}
            <div className="mb-4 text-gray-700">
        <label className="flex items-center ">
          <input
            type="checkbox"
            checked={isDailyHoroscope}
            onChange={() => setIsDailyHoroscope(!isDailyHoroscope)}
            className="mr-2"
          />
          Horoscope personnalisé de demain
        </label>
      </div>
<div className="mb-4">
        <label htmlFor="transit_start_date" className="block text-sm font-medium text-gray-700">Début de la période de transit</label>
        <input
          type="date"
          id="transit_start_date"
          name="transit_start_date"
          value={formData.transit_start_date}
          onChange={handleChange}
          className="mt-1 p-2 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
          required
          disabled={isDailyHoroscope} // Disable input if "Horoscope du jour" is checked
        />
      </div>

      <div className="mb-4">
        <label htmlFor="transit_end_date" className="block text-sm font-medium text-gray-700">Fin de la période de transit</label>
        <input
          type="date"
          id="transit_end_date"
          name="transit_end_date"
          value={formData.transit_end_date}
          onChange={handleChange}
          className="mt-1 p-2 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
          required
          disabled={isDailyHoroscope} // Disable input if "Horoscope du jour" is checked
        />
      </div>


      <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700">
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
    <div className={`p-5 px-4 mt-5 sm:px-6 lg:px-8 bg-transparent ${loading ? 'pointer-events-none' : ''}`} id='transit_chart'>
      
      <h2 className="text-3xl font-extrabold text-center mb-8 bg-gradient-to-r from-gray-300 via-gray-500 to-gray-300 bg-clip-text text-transparent animate-pulse">
        Ton horoscope personnalisé <span className='text-black'>🔮👀</span>
      </h2>

      {!errorMessage ? (<div className={`flex justify-center`}>
        <div className={`${loading ? 'blur-sm' : ''}`}>
        <Card
          user={user}
          title="Découvre ta Carte de transit Personnalisé"
          description="L'horoscope que tu lis ailleurs n'est pas précis 🥲! Il ne prend pas en compte tes informations personnelles comme ta date et ton lieu de naissance... Ici, tu peux générer chaque jour ton horoscope personnalisé, conçu rien que pour toi ❤️. Grâce à ces prévisions adaptées, tu auras les ✨meilleures✨ prédictions sur les plans amoureux, financier, et bien plus encore..."
          buttonText="Voir ma Carte de Transit"
          buttonLink="#"
          imageUrl={HoroscopeCardPic}
          formContent={form}
        />
        </div>
        {loading && (
              <>
              <div className="absolute top-[50%] left-1/2 transform -translate-x-1/2 sm:top-[20%] md:top-0 lg:top-0 w-full lg:w-[60%] h-full pointer-events-none z-40">
                <SunAnimation rotationSpeed={3} />
              </div>

            </>
          )}
      </div>) : 
      (<div className="flex items-center justify-center inset-0 z-50">
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

export default HoroscopeSection;

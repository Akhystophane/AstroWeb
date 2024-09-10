import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { useAuthState } from '../../Authentification/firebaseAuth';
import Card from '../../../components/Card'; // Ensure the path to Card is correct.
import HoroscopeCardPic from '../../../assets/HoroscopeCard.jpg';

interface TransitFormData {
  name?: string;
  birth_date: string;
  birth_time: string;
  birth_location: string;
  transit_start_date: string;
  transit_end_date: string;
  firebase_uid?: string;
}

const HoroscopeSection = () => {
  const user = useAuthState();
  const navigate = useNavigate();
  const [formData, setFormData] = useState<TransitFormData>({
    birth_date: '',
    birth_time: '',
    birth_location: '',
    transit_start_date: '',
    transit_end_date: '',
  });

  const [loading, setLoading] = useState(false);
  const [isBirthDataLoaded, setIsBirthDataLoaded] = useState(false); // To track if user data is loaded

  useEffect(() => {
    if (user && !user.isAnonymous ) {
      axios.get('http://localhost:8000/react') // Fetch all user data
        .then(response => {
          const allUserData = response.data; // Assuming this returns an array of user data
          const currentUserData = allUserData.find((data: any) => data.firebase_uid === user.uid);

          if (currentUserData) {
            setFormData(prevFormData => ({
              ...prevFormData,
              birth_date: currentUserData.birth_date,
              birth_time: currentUserData.birth_time,
              birth_location: currentUserData.birth_location,
              firebase_uid: user.uid,
            }));
            setIsBirthDataLoaded(true); // Mark birth data as loaded
          }
        })
        .catch(error => {
          console.error('Error fetching user data:', error);
        });
    }
  }, [user]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    setLoading(true);
    axios.post('http://localhost:8000/transit-chart/', formData)
      .then(response => {
        console.log('Form submitted successfully:', response.data);
        navigate('transit-chart', { state: response.data.transit_results });  // Navigate to the next page with the generated data
        setLoading(false);
      })
      .catch(error => {
        console.error('There was an error submitting the form!', error);
        console.log(formData)
        setLoading(false);
      });
  };

  const form = (
    <form onSubmit={handleSubmit}>
      {!isBirthDataLoaded && (
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
          <div className="mb-4">
            <label htmlFor="birth_time" className="block text-sm font-medium text-gray-700">Heure de naissance</label>
            <input
              type="time"
              id="birth_time"
              name="birth_time"
              value={formData.birth_time}
              onChange={handleChange}
              className="mt-1 p-2 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
              required
            />
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
      )}
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
        />
      </div>
      <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700">
        {loading ? "Chargement..." : "Soumettre"}
      </button>
    </form>
  );

  return (
    <div className="p-5 px-4 mt-5 sm:px-6 lg:px-8 bg-transparent" id='transit_chart'>
      <h2 className="text-3xl font-extrabold text-center mb-8 bg-gradient-to-r from-gray-300 via-gray-500 to-gray-300 bg-clip-text text-transparent animate-pulse">
        Ta carte de transit personnalisée <span className='text-black'>🔮👀</span>
      </h2>

      <div className="flex justify-center">
        <Card
          user={user}
          title="Découvrez votre Carte de Transit Personnalisée"
          description="Obtenez des informations détaillées sur les influences planétaires pendant une période donnée, basées sur votre signe astrologique."
          buttonText="Voir ma Carte de Transit"
          buttonLink="#"
          imageUrl={HoroscopeCardPic}
          formContent={form}
        />
      </div>
    </div>
  );
}

export default HoroscopeSection;

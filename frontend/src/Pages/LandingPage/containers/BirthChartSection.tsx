import Card from '../../../components/Card'
import BirthCardPic from '../../../assets/BirthCard.svg'
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { initializeApp } from 'firebase/app';
import { signInAnonymouslyCustom, useAuthState } from '../../Authentification/firebaseAuth';
import { getAuth } from 'firebase/auth';
import AuthForm from '../../Authentification/AuthForm';
import GoogleSignInButton from '../../Authentification/GoogleSignInButton';
import AuthPopup from '../../components/authPopup';

interface FormData {
  name: string;
  birth_date: string;
  birth_time: string;
  birth_location: string;
  firebase_uid?: string; 
}
const BirthChartSection = () => {

  const user = useAuthState();
  const navigate = useNavigate();
  const [formData, setFormData] = useState<FormData>({
    name: '',
    birth_date: '',
    birth_time: '',
    birth_location: ''
  });

  useEffect(() => {
    if (!user) {
      signInAnonymouslyCustom().then(result => {
        console.log('Signed in anonymously', result.user);
      }).catch(error => {
        console.error('Anonymous sign-in failed', error);
      });
    } else {
      setFormData(prevFormData => ({
        ...prevFormData,
        firebase_uid: user.uid
      }));
    }
  }, [user]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const [loading, setLoading] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    setLoading(true)
    axios.post('http://localhost:8000/react/', formData)
  .then(response => {
    console.log('Form submitted successfully:', response.data);
    navigate('birth-chart', { state: response.data.birth_chart });  // Passer les données générées à la page suivante
    setLoading(false);
  })
  .catch(error => {
    console.error('There was an error submitting the form!', error);
    setLoading(false);
  });}
  

  const form = (
    <form onSubmit={handleSubmit}>
      

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
      <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700">
        {loading ? "Chargement..." : "Soumettre"}
      </button>
    </form>
  );


  return (
    <div className="p-5 px-4 mt-5 sm:px-6 lg:px-8 bg-transparent" id='birth_chart'>
    <h2 className="text-3xl font-extrabold text-center mb-8 bg-gradient-to-r from-gray-300 via-gray-500 to-gray-300 bg-clip-text text-transparent animate-pulse">
      Ta carte de naissance personnalisée <span className='text-black'>🌠 😍</span>
    </h2>


    <div className="flex justify-center">
    <Card
      user = {user}
      title="Découvrez votre Carte de Naissance"
      description="Votre carte de naissance révèle des informations uniques sur votre personnalité, vos aspirations et bien plus encore. Explorez les étoiles et découvrez ce que l'univers a à dire sur vous."
      buttonText="Explorez votre carte"
      buttonLink="#"
      imageUrl={BirthCardPic}
      formContent={form}

    />
    </div>
    </div>
  );
}

export default BirthChartSection;

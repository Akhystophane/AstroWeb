import React, { useState, ReactNode } from 'react';
import StarsBackground from '../assets/StarsBackground.svg';
import { User } from 'firebase/auth'
import AuthPopup from '../Pages/components/authPopup';
interface CardProps {
  user?:  User | null
  title: string;
  description: string;
  buttonText?: string;
  buttonLink?: string;
  imageUrl: string;
  formContent?: ReactNode; // Formulaire optionnel
}

const Card: React.FC<CardProps> = ({ user, title, description, buttonText, buttonLink, imageUrl, formContent }) => {
  const [isFormVisible, setIsFormVisible] = useState(false);
  const [isPopVisible, setIsPopVisible] = useState(false);

/*   useEffect(() => {
    if (user) {
      setIsFormVisible(true);
    } else {
      setIsFormVisible(false);
    }
  }, [user]);
 */
  const handleButtonClick = () => {
    if (!user) {
      // Afficher le modal de connexion si l'utilisateur n'est pas connecté
      console.log("Login popup");
      console.log(user);
      setIsPopVisible(true);


    } else {
      setIsFormVisible(true)
      // Autre logique si l'utilisateur est déjà connecté
      console.log("L'utilisateur est connecté. On affiche le form");
    }
  };

  const closeModal = () => {
    setIsPopVisible(false);
  };
  const closeFormModal = () => {
    setIsFormVisible(false);
  };
  return (
    <div className="flex items-center justify-center pb-8 px-4 sm:px-6 lg:px-8 bg-gray-100" style={{ backgroundImage: `url(${StarsBackground})`, backgroundSize: 'cover', backgroundPosition: 'center' }}>
      <div className="max-w-md w-full bg-white shadow-lg rounded-lg overflow-hidden sm:max-w-lg md:max-w-xl lg:max-w-3xl xl:max-w-4xl 2xl:max-w-5xl">
        <div className="relative w-full h-56">
          <img
            src={imageUrl}
            alt="Placeholder"
            className="absolute inset-0 w-full h-full object-cover"
          />
        </div>
        <div className="p-6">
          <h2 className="text-xl font-semibold text-gray-800">{title}</h2>
          <p className="text-gray-600 mt-2">{description}</p>
          {buttonLink ? (          
          <div className="mt-4">
            <button
              onClick={handleButtonClick}
              className="px-4 py-2 bg-blue-600 text-white text-sm font-semibold rounded hover:bg-blue-700 transition duration-300 ease-in-out"
            >
              {buttonText}
            </button>
          </div>) : undefined}

        </div>
      </div>

      {/* Modal */}
      
      {!user && (
        <AuthPopup isOpen={isPopVisible} onClose={closeModal} />
      )}

      {isFormVisible && formContent && ( // FormContent ne s'affiche que s'il est fourni
        <div className="fixed inset-0 bg-gray-900 bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-8 rounded-lg shadow-lg max-w-lg w-full">
          <button
            className="ml-auto flex text-gray-700 text-2xl font-bold hover:text-red-600 focus:outline-none"
            onClick={closeFormModal}
          >
            &#x2715;
          </button>
            {formContent}
          </div>
        </div>
      )}
    </div>
  );
};

export default Card;

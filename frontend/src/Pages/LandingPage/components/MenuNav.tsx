import { useState, useEffect } from "react";
import AuthPopup from "../../components/authPopup";
import { auth, useAuthState } from '../../Authentification/firebaseAuth'; 
import { signOut } from "firebase/auth"; // Importer signOut de firebase/auth

const MenuNav = () => {
  const [isPopVisible, setIsPopVisible] = useState(false);
  const user= useAuthState(); // Utiliser useAuthState avec auth

  // Fonction pour ouvrir le modal
  const openModal = () => {
    setIsPopVisible(true);
  };

  // Fonction pour fermer le modal
  const closeModal = () => {
    setIsPopVisible(false);
  };

  // Fonction pour déconnecter l'utilisateur
  const handleSignOut = async () => {
    try {
      await signOut(auth); // Déconnexion de l'utilisateur
    } catch (error) {
      console.error("Erreur lors de la déconnexion:", error);
    }
  };

  // Ne pas afficher le popup si l'utilisateur n'est pas anonyme
  useEffect(() => {
    if (user && !user.isAnonymous) {
      setIsPopVisible(false);
    }
  }, [user]);

  return (
    <div className='w-full h-full   '>
      <nav className=" opacity-100 bg-gradient-to-br from-purple-600 to-indigo-700 px-4 pt-2  pb-2 md:mb-2 shadow-lg">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex-shrink-0">
            <a href="#birth_chart">
            <span className="text-white font-bold text-xl">Astronomos</span>
            </a>
          </div>
          <div className="w-full hidden md:block">
            <div className="ml-10 flex text-center space-x-4">
              <a href="#birth_chart" className="flex-1 text-gray-300 hover:text-white px-3 py-2 rounded-md text-md font-medium">Carte de naissance</a>
              <a href="#transit_chart" className="flex-1 text-gray-300 hover:text-white px-3 py-2 rounded-md text-md font-medium">Horoscope personnalisé</a>
              <a href="#FAQ" className="flex-1 text-gray-300 hover:text-white px-3 py-2 rounded-md text-md font-medium">FAQ</a>
            </div>
          </div>
          <div>
            {/* Afficher le bouton de déconnexion si l'utilisateur n'est pas anonyme */}
            {user && !user.isAnonymous ? (
              <button onClick={handleSignOut} className="flex-1 text-gray-300 hover:text-white px-3 py-2 rounded-md text-md font-medium">
                Déconnexion
              </button>
            ) : (
              // Afficher le bouton de connexion si l'utilisateur est anonyme
              <button onClick={openModal} className="flex-1 text-gray-300 hover:text-white px-3 py-2 rounded-md text-md font-medium">
                Connexion
              </button>
            )}

            {/* Afficher AuthPopup si isPopVisible est vrai */}
            <AuthPopup isOpen={isPopVisible} onClose={closeModal} />
          </div>
        </div>
      </nav>
    </div>
  );
}

export default MenuNav;

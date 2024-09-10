import { useState } from "react";
import AuthPopup from "../../components/authPopup"

const MenuNav = () => {
  const [isPopVisible, setIsPopVisible] = useState(false);

  // Function to open the modal
  const openModal = () => {
    setIsPopVisible(true);
  };

  // Function to close the modal
  const closeModal = () => {
    setIsPopVisible(false);
  };
  return (
    <div className='w-full h-full ' >
    <nav className=" rounded-full mx-4 px-4 pt-5 pb-2 md:mb-20 shadow-lg  ">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <div className="flex-shrink-0 ">
          <span className="text-white font-bold text-xl">Logo</span>
        </div>
        <div className=" w-full hidden md:block ">
          <div className="ml-10 flex text-center space-x-4">
            <a href="#birth_chart" className="flex-1 text-gray-300 hover:text-white px-3 py-2 rounded-md text-md font-medium">Carte de naissance</a>
            <a href="#horoscope" className="flex-1 text-gray-300 hover:text-white px-3 py-2 rounded-md text-md font-medium">Horscope personnalisé</a>
            <a href="#FAQ" className="flex-1 text-gray-300 hover:text-white px-3 py-2 rounded-md text-md font-medium">FAQ</a>
          </div>
        </div>
        <div>
      {/* Button to open the AuthPopup modal */}
      <button onClick={openModal} className="flex-1 text-gray-300 hover:text-white px-3 py-2 rounded-md text-md font-medium">
        Connexion
      </button>

      {/* Render AuthPopup modal conditionally based on isPopVisible state */}
      <AuthPopup isOpen={isPopVisible} onClose={closeModal} />
    </div>
      </div>
    </nav>
    </div>
  )
}

export default MenuNav
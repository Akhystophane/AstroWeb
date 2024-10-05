import Card from "../../components/Card";
import StarsBackground from '../../assets/StarsBackground.svg';
import { useLocation, useNavigate } from "react-router-dom";
import SunAnimation from "./components/SunAnimation";
import Bottom from '../../assets/BirthChart/bottom.svg';
import pic1 from '../../assets/Horoscope/h_pic1.svg';
import pic2 from '../../assets/Horoscope/h_pic2.svg';
import pic3 from '../../assets/Horoscope/h_pic3.svg';
import pic4 from '../../assets/Horoscope/h_pic4.svg';
import { FaArrowLeft } from 'react-icons/fa'; // Icône flèche retour



const Horoscope = () => {
  const navigate = useNavigate();

  // Fonction pour revenir à la page précédente
  const handleGoBack = () => {
    navigate(-1); // Retourne à la page précédente
  };
  const location = useLocation();
  const transitChartData = location.state;
  //console.log(transitChartData);  // The transit data generated from the backend

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
      <button
        onClick={handleGoBack}
        className="absolute top-2 left-[2%] white hover:text-gray-800 focus:outline-none"
      >
        <FaArrowLeft size={24} />
      </button>
        <div className="w-full h-full">
          <div className="text-center">
            <h1 className='h1 mb-6 pb-2 pt-8 px-'>Découvre ton Horscope Personnalisé du jour</h1>
            <span className="text-black text-6xl">🔮👇</span>
            <SunAnimation />
          </div>
          
          {cards.map((card, index) => {
            // Sélectionner l'image en fonction de l'index
            const images = [pic1, pic2, pic3, pic4];
            const selectedImage = images[index % images.length]; // Rotation des images

            return(
              <div key={index} className="w-full h-full">
              <h2  className="text-3xl mt-[4rem] font-extrabold text-center mb-8 bg-gradient-to-r from-gray-300 via-gray-500 to-gray-300 bg-clip-text text-transparent animate-pulse">
              {card.title} <span className="text-black">🌠 😍</span>
            </h2>
            <Card
                title={card.subtitle}
                description={card.description}
                imageUrl={selectedImage}
              />
              </div>
            );
          }


        )}

      <div>

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

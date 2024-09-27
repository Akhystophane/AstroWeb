import Card from "../../components/Card";
import StarsBackground from '../../assets/StarsBackground.svg';
import { useLocation } from "react-router-dom";
import SunAnimation from "./components/SunAnimation";
import Bottom from '../../assets/BirthChart/bottom.svg';
import pic1 from '../../assets/BirthChart/pic1.svg';

const Horoscope = () => {
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
        <div className="w-full h-full">
          <div className="text-center">
            <h1 className='h1 mb-6 pb-2 pt-5'>Découvre ton Horscope Personnalisé du jour</h1>
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

import SolarSystemAnimation from '../components/solarSystemAnimation'
import MenuNav from '../components/MenuNav'
import { useEffect, useRef } from 'react';
import { gsap } from 'gsap';


const HeroSection = () => {
  const titleRef = useRef(null);
  const paragraphRef = useRef(null);

  useEffect(() => {
    // Animation de fade-in du haut vers le bas
    gsap.fromTo(
      titleRef.current,
      {
        opacity: 0,
        y: -50, // Partie haute avant l'animation
      },
      {
        opacity: 1,
        y: 0, // À sa position normale
        duration: 2,
        ease: 'power2.out',
      }
    );

    gsap.fromTo(
      paragraphRef.current,
      {
        opacity: 0,
        y: -50, // Partie haute avant l'animation
      },
      {
        opacity: 1,
        y: 0, // À sa position normale
        duration: 2,
        ease: 'power2.out',
        delay: 0.5, // Légère différence pour un effet plus naturel
      }
    );

    // Animation de clignotement pour le titre
    gsap.to(titleRef.current, {
      opacity: 0.5,
      repeat: -1, // Répète l'animation infiniment
      yoyo: true, // L'animation fait des allers-retours
      duration: 1.2, // Durée d'une phase de clignotement
      ease: 'power1.inOut',
      delay: 1.5, // Clignotement après l'animation initiale
    });
  }, []);
  return (
    <div className='h-full w-full '>
      
        <MenuNav />
        <div className='w-full h-full '>
        
        <h1 ref={titleRef} className='h1 mb-6 pb-2 '>Transforme ta vie grâce à l'Astrologie
          </h1>
          <p ref={paragraphRef} className='body-1 text-center max-w-3xl mx-auto mb-6
          text-n-14 lg:mb-5'>
              Libère ton potentiel grâce à Astronomos.
              Les secrets des astres n'ont jamais été aussi proches.

          </p>
        </div>
        <div className="flex justify-center items-center">
        <a 
          href="#birth_chart"
          className="relative bg-purple-700 text-white py-2 px-4 rounded-lg shadow-lg hover:bg-gray-600 focus:outline-none"
        >
          <span className="absolute inset-0 bg-gradient-to-r from-white/20 to-transparent opacity-0 hover:opacity-100 transition-opacity duration-300 rounded-lg"></span>
          <span className="relative z-0">Découvrir</span>
        </a>
      </div>

       <div className="h-screen w-full  flex items-center justify-center">
        {/* <img src={SolarSystem} alt="Solar System" /> */}
        < SolarSystemAnimation />
        </div>

    </div>
    
  )
}

export default HeroSection
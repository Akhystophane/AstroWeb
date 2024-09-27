import React, { useEffect, useRef } from 'react';
import { gsap } from 'gsap';
import SunHands from '../../../assets/BirthChart/sun-hands.svg'; // Chemin vers votre SVG

// Déclarez l'interface des props
interface SunAnimationProps {
  rotationSpeed?: number; // Prop optionnelle pour la vitesse de rotation
}

const SunAnimation: React.FC<SunAnimationProps> = ({ rotationSpeed = 10 }) => { // Valeur par défaut à 10
  const svgContainerRef = useRef<HTMLDivElement>(null); // Référence à l'élément conteneur du SVG
  const sunRef = useRef<SVGGElement | null>(null); // Référence au groupe <g> du soleil dans le SVG

  useEffect(() => {
    // Vérifier que svgContainerRef.current n'est pas null avant de continuer
    if (!svgContainerRef.current) return;

    // Charger le fichier SVG
    fetch(SunHands)
      .then((response) => response.text())
      .then((svgContent) => {
        if (svgContainerRef.current) { // Double vérification après la promesse
          svgContainerRef.current.innerHTML = svgContent; // Injecter le contenu SVG
          
          // Sélectionner le groupe "sun" par ID
          const svgElement = svgContainerRef.current.querySelector('svg');
          if (svgElement) {
            sunRef.current = svgElement.querySelector('#sun'); // Sélectionner le groupe du soleil par ID

            // Si l'élément soleil est trouvé, démarrer l'animation
            if (sunRef.current) {
              gsap.to(sunRef.current, {
                rotation: 360, // Rotation complète
                transformOrigin: "center center", // Rotation autour du centre
                repeat: -1, // Animation infinie
                ease: "linear", // Rotation constante
                duration: rotationSpeed // Utilisation de la prop rotationSpeed
              });
            } else {
              console.error('Element with ID "sun" not found in the SVG.');
            }
          }
        }
      })
      .catch((error) => console.error('Error loading SVG:', error));
  }, [rotationSpeed]); // Dépendance sur rotationSpeed pour déclencher l'effet quand elle change

  return (
    <div>
      <div ref={svgContainerRef}></div>
    </div>
  );
};

export default SunAnimation;

import { useEffect } from "react";
import ReactGA from "react-ga4";
import { useLocation } from "react-router-dom";

// Fonction d'initialisation de Google Analytics
export const initGA = (): void => {
  ReactGA.initialize("G-R75EH3WQRF"); // Remplacez par votre identifiant de mesure
};

// Fonction de suivi des vues de page
export const logPageView = (path: string): void => {
  ReactGA.send({ hitType: "pageview", page: path });
};

// Fonction de suivi des événements
export const logEvent = (category: string, action: string, label: string): void => {
  ReactGA.event({ category, action, label });
};

// Composant RouteChangeTracker pour suivre les changements de route
const RouteChangeTracker: React.FC = () => {
    const location = useLocation();
  
    useEffect(() => {
      logPageView(location.pathname + location.search);
    }, [location]);
  
    return null;
  };
  
  export default RouteChangeTracker;
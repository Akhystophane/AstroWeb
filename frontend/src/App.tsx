import { useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LandingPage from './Pages/LandingPage/LandingPage';
import BirthChart from './Pages/BirthChart/BirthChart';
import Horoscope from './Pages/Horoscope/Horoscope';
import Profile from './Pages/Profile/Profile';
import { initGA, logPageView } from './analytics';
import RouteChangeTracker from "./analytics";
import ScrollToTop from './components/ScrollToTop';

function App() {
  useEffect(() => {
    initGA();
    logPageView(window.location.pathname + window.location.search);
  }, []);
  return (
    <Router>
      <ScrollToTop/>
      < RouteChangeTracker />
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/birth-chart" element={<BirthChart />} />
        <Route path="/transit-chart" element={<Horoscope />} />
        <Route path="/user-profile" element={<Profile />} />
      </Routes>
    </Router>
  );
}

export default App;


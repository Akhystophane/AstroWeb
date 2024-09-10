import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LandingPage from './Pages/LandingPage/LandingPage';
import BirthChart from './Pages/BirthChart/BirthChart';
import Horoscope from './Pages/Horoscope/Horoscope';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/birth-chart" element={<BirthChart />} />
        <Route path="/transit-chart" element={<Horoscope />} />
      </Routes>
    </Router>
  );
}

export default App;


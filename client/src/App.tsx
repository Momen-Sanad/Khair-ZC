import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, useLocation } from 'react-router-dom';

import './App.css';
import './assets/stylesheets/Navbar.css';

import Home from "./components/Home";
import Auth from "./components/Auth";
import Navbar from "./components/Navbar";
import Campaigns from './components/Campaigns';
import Media from './components/Media';
import Shop from './components/Shop';
import CampaignPage from "./components/CampaignPage";


function App() {
  const [isScrolled, setIsScrolled] = useState<boolean>(false);

  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 50) {
        setIsScrolled(true);
      } else {
        setIsScrolled(false);
      }
    };
    window.addEventListener("scroll", handleScroll);
    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, []);

  return (
    <Router>
      <AppContent isScrolled={isScrolled} />
    </Router>
  );
}

function AppContent({ isScrolled }: { isScrolled: boolean }) {
  const location = useLocation();

  return (
    <>
      {location.pathname !== '/auth' && <Navbar isScrolled={isScrolled}/>}
      <Routes>
        <Route path='/' element={<Home />} />
        <Route path='/auth' element={<Auth />} />
        <Route path='/campaigns' element={<Campaigns/>} />
        <Route path="/campaigns/:id" element={<CampaignPage/>}/>
        <Route path='/media' element={<Media/>} />
        <Route path='/mini-shop' element={<Shop/>} />
      </Routes>
    </>
  );
}

export default App;
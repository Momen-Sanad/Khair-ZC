import { useState,useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import './App.css';
import './assets/stylesheets/Navbar.css';

import Home from "./components/Home";
import Navbar from "./components/Navbar";
import Campaigns from './components/Campaigns';
import Media from './components/Media';
import Shop from './components/Shop';


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
      <Navbar isScrolled={isScrolled}/>
      <Routes>
        <Route path='/' element={<Home />} />
        <Route path='/campaigns' element={<Campaigns/>} />
        <Route path='/media' element={<Media/>} />
        <Route path='/mini-shop' element={<Shop/>} />
      </Routes>
    </Router>
  );
}

export default App;

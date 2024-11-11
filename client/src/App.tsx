import React, { useState,useEffect } from 'react';
import { BrowserRouter as Router, Route,Routes } from 'react-router-dom';
import Navbar from './Navbar';
import logo from './logo.svg';
import './App.css';
import Campaigns from './Campaigns';
import Media from './Media';
import Shop from './Shop';
import Index from './index';


function App() {
  const [isScrolled,setIsScrolled]=useState<boolean>(false);

  useEffect(()=>{
    const handScroll=()=>{
      if(window.scrollY>50)
        setIsScrolled(true)
      else
        setIsScrolled(false)
    };
    window.addEventListener("scroll",handScroll);
    return()=>{
      window.removeEventListener("scroll",handScroll);
    };
  },[]);
  return (
    <Router>
      <Navbar isScrolled={isScrolled}/>
      <Routes>
        <Route path='/' element={<Index/>} />
        <Route path='/campaigns' element={<Campaigns/>} />
        <Route path='/media' element={<Media/>} />
        <Route path='/mini-shop' element={<Shop/>} />
      </Routes>
    </Router>
  );
}

export default App;

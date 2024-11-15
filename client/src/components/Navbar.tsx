import React from 'react';
import { Link } from 'react-router-dom';

import '../assets/stylesheets/Navbar.css';

interface NavbarProps {
  isScrolled: boolean;
}

const Navbar: React.FC<NavbarProps> = ({ isScrolled }) => {
  return (
    <nav className={`navbar ${isScrolled ? "scrolled" : "" }`}>
      <div className='navbar-container'>
        <Link to='/' className='navbar-logo'>
          <img src='../assets/images/KhairZcLogo.png' alt='Logo'/>
        </Link>
        <ul className='navbar-items'>
          <li><Link to='/' className='navbar-item'>Home</Link></li>
          <li><Link to='/campaigns' className='navbar-item'>Campaigns</Link></li>
          <li><Link to='/media' className='navbar-item'>Media</Link></li>
          <li><Link to='/mini-shop' className='navbar-item'>Mini Shop</Link></li>
        </ul> 
      </div>
    </nav>
  );
};

export default Navbar;

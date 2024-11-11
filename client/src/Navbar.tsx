import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

interface NavbarProps {
  isScrolled: boolean;  // Define the type for the isScrolled prop
}

const Navbar: React.FC<NavbarProps> = ({ isScrolled }) => {
  return (
    <nav className={`navbar ${isScrolled ? "scrolled" : "" }`}>
      <div className='navbar-container'>
        <Link to='/' className='navbar-logo'>
          <img src='/KhairZcLogo.png' alt='Logo'/>
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

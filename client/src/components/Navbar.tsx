import React from 'react';
import { Link } from 'react-router-dom';
import { FaUserGraduate } from "react-icons/fa";
import { CgProfile } from "react-icons/cg";
import '../assets/stylesheets/Navbar.css';
import logo from '../assets/images/KhairZcLogo.png';

interface NavbarProps {
  isScrolled: boolean;
}

const Navbar: React.FC<NavbarProps> = ({ isScrolled }) => {
  const loggedIn=true
  return (
    <nav className={`navbar ${isScrolled ? "scrolled" : "" }`}>
      <div className='navbar-container'>
        <Link to='/' className='navbar-logo'>
          <img src={logo} alt='Logo'/>
        </Link>
        <ul className='navbar-items'>
          <li><Link to='/' className='navbar-item'>Home</Link></li>
          <li><Link to='/campaigns' className='navbar-item'>Campaigns</Link></li>
          <li><Link to='/charities' className='navbar-item'>Charities</Link></li>
          <li><Link to='/media' className='navbar-item'>Media</Link></li> 
          { loggedIn ? (
            <>
            <li><Link to='/mini-shop' className='navbar-item'>Mini Shop</Link></li>
            <Link to='/profile' className='auth-button'>
            <CgProfile />
            Profile
            </Link>
            </>
          ) : (
            <>
            <li><Link to='/auth' className='navbar-item'>Mini Shop</Link></li>
            <Link to='/auth' className='auth-button'>
            <FaUserGraduate />
            SIGN UP
            </Link>
            </>
          )}
        </ul> 
      </div>
    </nav>
  );
};

export default Navbar;

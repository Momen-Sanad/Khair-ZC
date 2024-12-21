import React from 'react';
import { Link } from 'react-router-dom';
import { FaUserGraduate } from "react-icons/fa";
import { useState, useEffect } from 'react';
import { CgProfile } from "react-icons/cg";
import '../assets/stylesheets/Navbar.css';
import logo from '../assets/images/KhairZcLogo.png';
import Notification from './Notification';
import { FiBell } from "react-icons/fi";

interface User {
  username: string;
}

interface NavbarProps {
  isScrolled: boolean;
}



const Navbar: React.FC<NavbarProps> = ({ isScrolled }) => {
  const [user, setUser] = useState<User | null>(null); // State for user data
  const [showNotifications, setShowNotifications] = useState<boolean>(false);

  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
  }, []);


  const toggleNotifications = () => {
    setShowNotifications((prev) => !prev);
  };

  return (
    <nav className={`navbar ${isScrolled ? "scrolled" : ""}`}>
      <div className='navbar-container'>
        <Link to='/' className='navbar-logo'>
          <img src={logo} alt='Logo' />
        </Link>
        <ul className='navbar-items'>
          <li><Link to='/' className='navbar-item'>Home</Link></li>
          <li><Link to='/campaigns' className='navbar-item'>Campaigns</Link></li>
          <li><Link to='/charities' className='navbar-item'>Charities</Link></li>
          <li><Link to='/media' className='navbar-item'>Media</Link></li>
          {user ? (
            <>
              <li><Link to='/mini-shop' className='navbar-item'>Mini Shop</Link></li>
              <div className='notification-bell' onClick={toggleNotifications}>
                <FiBell size={24} />
                {showNotifications && (
                  <div className="notification-dropdown">
                    <Notification />
                  </div>
                )}
              </div>
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
                SIGN IN
              </Link>
            </>
          )}
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
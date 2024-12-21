import React from 'react';
import { Link } from 'react-router-dom';
import { FaUserGraduate } from "react-icons/fa";
import { useState, useEffect } from 'react';
import { CgProfile } from "react-icons/cg";
import '../assets/stylesheets/Navbar.css';
import logo from '../assets/images/KhairZcLogo.png';
import Notification from './Notification';
import { FiBell } from "react-icons/fi";

interface user {
  id: string
  firstName: string,
  lastName: string,
  email: string,
  isAdmin: boolean,
  points: number
}

interface NavbarProps {
  isScrolled: boolean;
}



const Navbar: React.FC<NavbarProps> = ({ isScrolled }) => {
  const [user, setUser] = useState<user | null>(null); // State for user data
  const [showNotifications, setShowNotifications] = useState<boolean>(false);
  const fetchUser = 'http://localhost:5000/security/user'

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await fetch(fetchUser, {
          method: 'GET',
          credentials: 'include',
        });
        if (!response.ok) {
          throw new Error('Failed to fetch user data');
        }

        const userData = await response.json();
        setUser(userData);
      } catch (error) {
        console.error('Error:', error);
      }
    };

    fetchUserData();
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
                {user.firstName}
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
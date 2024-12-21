import React, { useState, useEffect } from 'react';
import '../assets/stylesheets/Charities.css';
import { IoPersonOutline } from "react-icons/io5";
import { FaMapLocationDot } from "react-icons/fa6";
import { BiSolidCategory } from "react-icons/bi";
import { Link } from 'react-router-dom';

interface charity {
  id: number,
  name: string,
  address: string,
  description: string,
  category: string,
  image: string
}
interface user {
  id: string
  firstName: string,
  lastName: string,
  email: string,
  isAdmin: boolean,
  points: number
}

const Charities = () => {
  const loggedIn= true
  const [searchInput, setSearchInput] = useState('');
  const [charities, setCharities] = useState<charity[]>([]);
  const [user, setUser] = useState<user>();
  const fetchCharities = 'http://localhost:5000/search/charities'
  const fetchUser = 'http://localhost:5000/auth/user'
  useEffect(() => {
    // Mocking the user data for testing
    const mockedUser = {
      id: '123',
      firstName: 'John',
      lastName: 'Doe',
      email: 'johndoe@example.com',
      isAdmin: true,
      points: 50
    };
    setUser(mockedUser); // Set the mocked user data

    // Fetching charities from the API
    fetch(fetchCharities)
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to fetch charities');
        }
        return response.json();
      })
      .then(data => {
        setCharities(data);
      })
      .catch(error => {
        console.error('Error:', error);
      });
  }, []);
  const handleLogin = async (email: string, password: string) => {
    try {
      const response = await fetch('http://localhost:5000/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, userPass: password }),
      });
      const data = await response.json();
      if (response.ok) {
        // Store token in localStorage
        localStorage.setItem('token', data.token);
        // Redirect to dashboard or another page after successful login
      } else {
        console.error('Login failed:', data.error);
      }
    } catch (error) {
      console.error('Login error:', error);
    }
  };

  const filteredCharities = charities.filter((charity) =>
    charity.name.toLowerCase().includes(searchInput.toLowerCase())
  );
  return (
    <div className='charity-container'>
      <div className="search-bar">
        <input
          type="text"
          placeholder="Search charities..."
          value={searchInput}
          onChange={(e) => setSearchInput(e.target.value)}
        />
      </div>
      {filteredCharities.map((charity) => {

        return (
          <div className='charity-wrapper' key={charity.id}>
            <div className='Charity-card'>
              <Link to={`/charities/${charity.id}`} className="charity-link">
                <div className='Content'>
                  <h1>{charity.name}</h1>
                  <p>
                    {charity.description.slice(0, 100)}.....
                  </p>
                  <ul className='info'>
                    <li>
                      <FaMapLocationDot className='icon' />
                      {charity.address}
                    </li>
                    <li>
                      <BiSolidCategory className='icon' />
                      {charity.category}
                    </li>
                  </ul>
                </div>
                <div className='CharityPhoto'>
                  <img src={charity.image} alt='Charity' />
                </div>
              </Link>
            </div>
          </div>
        );
      })}
      <div className='profile-container'>
        {loggedIn && (
          <>
            {user?.isAdmin ? (
              <>
                <div className='profile-name'>
                  <IoPersonOutline size={30} />
                  <h1>{user.firstName}</h1>
                </div>
                <div className="profile-data">
                  <table>
                    <tbody>
                      <tr>
                        <td>Followed charities:</td>
                        <td>{26}</td>
                      </tr>
                      <tr>
                        <td>Status:</td>
                        <td>Admin</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                <div className="vertical-line"></div>
              </>
            ) : (
              <>
                <div className='profile-name'>
                  <IoPersonOutline size={30} />
                  <h1>{user?.firstName}</h1>
                </div>
                <div className="profile-data">
                  <table>
                    <tbody>
                      <tr>
                        <td>Current points:</td>
                        <td>{user?.points}</td>
                      </tr>
                      <tr>
                        <td>Followed charities:</td>
                        <td>{26}</td>
                      </tr>
                      <tr>
                        <td>Attended Campaigns:</td>
                        <td>2</td>
                      </tr>
                      <tr>
                        <td>Status:</td>
                        <td>User</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                <div className="vertical-line"></div>
              </>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default Charities;

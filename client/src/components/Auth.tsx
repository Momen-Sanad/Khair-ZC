import React, { useState } from 'react';
import { FaUser, FaLock, FaEnvelope } from "react-icons/fa";
import { TbArrowBadgeLeft } from "react-icons/tb";
import '../assets/stylesheets/Auth.css';

const Auth = () =>
{
  const [isSignUp, setIsSignUp] = useState(false);
  const [email, setEmail] = useState('');
  const [fname, setFName] = useState('');
  const [lname, setLName] = useState('');
  const [userPass, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const toggleAuth = () => { setIsSignUp(!isSignUp); };

  const handleSubmit = async(event: React.FormEvent) => {
    event.preventDefault();
    
    if (isSignUp && userPass !== confirmPassword)
    {
      alert("Passwords don't match!");
      return;
    }

    try
    {
      const authType = (isSignUp) ? '/auth/register' : '/auth/login';
      const authParameters = (isSignUp) ? { email, fname, lname, userPass } : { email, userPass }

      const request = await fetch(authType,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(authParameters),
          credentials: 'same-origin'
        }
      );

      const data = await request.json();

      if (request.ok)
      {
        if (isSignUp) { window.location.href = '/auth'; } else { window.location.href = '/'; }
      }
      else
      {
        alert(`Authentication failed: ${data.message}`);
      }
    }
    catch (error)
    {
      console.error('Error during Sign-Up: ', error);
    }
  };

  return (
    <>
      <a href="/" className="back-button">
        <TbArrowBadgeLeft className="icon" />
      </a>
      <div className="auth-box-main">
        <div className="auth-wrapper">
          <div className="auth-form">
            <h2>
              {isSignUp ? 'Sign Up' : 'Welcome back!'}
            </h2>
            <form onSubmit={handleSubmit}>
              <div className="input-data-container">
                <input required type="email" placeholder="Email" value={email} onChange={(event) => setEmail(event.target.value)}/>
                <FaEnvelope className="icon" />
              </div>

              {
                isSignUp &&
                (
                  <>
                    <div className="input-data-container">
                      <input required type="text" placeholder="First name" value={fname} onChange={(event) => setFName(event.target.value)}/>
                      <FaUser className="icon" />
                    </div>
                    <div className="input-data-container">
                      <input required type="text" placeholder="Last name" value={lname} onChange={(event) => setLName(event.target.value)}/>
                      <FaUser className="icon" />
                    </div>
                  </>
                )
              }

              <div className="input-data-container">
                <input required type="password" placeholder="Password" value={userPass} onChange={(event) => setPassword(event.target.value)}/>
                <FaLock className="icon" />
              </div>

              {
                isSignUp &&
                (
                  <>
                    <div className="input-data-container">
                      <input required type="password" placeholder="Confirm Password" value={confirmPassword} onChange={(event) => setConfirmPassword(event.target.value)}/>
                      <FaLock className="icon" />
                    </div>
                  </>
                )
              }
              
              <button type="submit">{isSignUp ? 'Sign Up' : 'Sign In'}</button>
            </form>
          </div>
          <div className="auth-link">
            {isSignUp ? (
              <p>
                Already have an account?{' '}
                <a onClick={(e) => {
                  e.preventDefault();
                  toggleAuth();
                }}>Sign In</a>
              </p>
            ) : (
              <p>
                Don’t have an account?{' '}
                <a onClick={(e) => {
                  e.preventDefault();
                  toggleAuth();
                }}>Sign Up</a>
              </p>
            )}
          </div>
        </div>
        <div className="auth-separator">
          {/*  */}
        </div>
        <div className="auth-with-third-party">
          {/*  */}
        </div>
      </div>
    </>
  );
};

export default Auth;


import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { FaFacebook, FaInstagram, FaLinkedin } from 'react-icons/fa';
import logo from '../assets/images/KhairZcLogo.png';
import '../assets/stylesheets/Home.css';
import khairImage1 from '../assets/images/khairImage1.png';
import khairImage2 from '../assets/images/khairImage2.png';
import khairImage3 from '../assets/images/khairImage3.png';


const Home = () => {
  const [currentSlide, setCurrentSlide] = useState(0);

  const slides = [
    {
      image: khairImage1,
      slogan: "Making a Difference, One Act at a Time",
      subtext: "Join Khair-ZC in our mission to create positive change"
    },
    {
      image: khairImage2,
      slogan: "Together We Can Change Lives",
      subtext: "Building a better community through service"
    },
    {
      image: khairImage3,
      slogan: "Empowering Through Action",
      subtext: "Join our initiatives and make an impact"
    }
  ];

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % slides.length);
    }, 3500);

    return () => clearInterval(timer);
  }, [slides.length]); // Added slides.length as dependency

  return (
    <div className="home-container">
      {/* Hero Section */}
      <div className="hero-section">
        <div className="hero-slider">
          {slides.map((slide, index) => (
            <div
              key={index}
              className={`slide ${index === currentSlide ? 'active' : ''}`}
              style={{ backgroundImage: `url(${slide.image})` }}
            >
              <div className="slide-content">
                <h1>{slide.slogan}</h1>
                <p>{slide.subtext}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* About Section */}
      <section className="about-section">
        <h2>About Khair-ZC</h2>
        <div className="about-content">
          <div className="about-text">
            <p>Khair-ZC is a student-led initiative dedicated to making positive changes in our community. Through various campaigns and events, we aim to create lasting impact and foster a spirit of giving.</p>
          </div>
        </div>
      </section>

      {/* How to Participate Section */}
      <section className="participate-section">
        <h2>How to Get Involved</h2>
        <div className="steps-container">
          <div className="step">
            <div className="step-number">1</div>
            <h3>Sign Up</h3>
            <p>Create your account to join our community</p>
          </div>
          <div className="step">
            <div className="step-number">2</div>
            <h3>Choose Your Cause</h3>
            <p>Browse our campaigns and find what speaks to you</p>
          </div>
          <div className="step">
            <div className="step-number">3</div>
            <h3>Take Action</h3>
            <p>Participate in events and make a difference</p>
          </div>
        </div>
      </section>

      {/* Media Preview Section */}
      <section className="media-section">
        <h2>Our Impact</h2>
        <div className="media-grid">
          {[1, 2, 3, 4].map((item) => (
            <div key={item} className="media-item">
              <img src={`/api/placeholder/300/300`} alt={`Impact ${item}`} />
            </div>
          ))}
        </div>
        <Link to="/media" className="view-more-btn">View More</Link>
      </section>

      {/* Footer */}
      <footer className="footer">
        <div className="footer-content">
          <div className="footer-section">
            <img src={logo} alt="Khair-ZC Logo" className="footer-logo" />
          </div>
          <div className="footer-section">
            <h3>Quick Links</h3>
            <Link to="/campaigns">Campaigns</Link>
            <Link to="/charities">Charities</Link>
            <Link to="/media">Media</Link>
            <Link to="/mini-shop">Mini Shop</Link>
          </div>
          <div className="footer-section">
            <h3>Connect With Us</h3>
            <div className="social-links">
              <a href="https://facebook.com" target="_blank" rel="noopener noreferrer"><FaFacebook /></a>
              <a href="https://instagram.com" target="_blank" rel="noopener noreferrer"><FaInstagram /></a>
              <a href="https://linkedin.com" target="_blank" rel="noopener noreferrer"><FaLinkedin /></a>
            </div>
          </div>
          <div className="footer-section">
            <h3>Join Us</h3>
            <Link to="/auth" className="footer-cta">Sign In / Sign Up</Link>
          </div>
        </div>
        <div className="footer-bottom">
          <p>&copy; {new Date().getFullYear()} Khair-ZC. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};

export default Home;
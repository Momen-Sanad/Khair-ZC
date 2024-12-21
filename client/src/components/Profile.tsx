import React, { useState } from 'react';
import { FaUser, FaCog, FaShieldAlt, FaChartBar, FaSignOutAlt } from "react-icons/fa";
import '../assets/stylesheets/Profile.css';
import logo from '../assets/images/icon.png';

const Profile = () => {
  const [activeTab, setActiveTab] = useState('appearance');

  // Mock user data - replace with your actual data
  const userData = {
    id: "202300491",
    name: "Amr",
    email: "amr@gmail.com",
    description: "This is a description",
    points: 1250,
    followedCharities: 5,
    attendedCampaigns: 12,
    status: "Admin"
  };

  const renderContent = () => {
    switch (activeTab) {
      case 'appearance':
        return (
          <div className="content-section">
            <h2>Profile Details</h2>
            <div className="profile-details">
              <div className="detail-item">
                <p>ID: {userData.id}</p>
                <p>Name: {userData.name}</p>
                <p>Email: {userData.email}</p>
                <p>Description: {userData.description}</p>
              </div>
            </div>
          </div>
        );

      case 'statistics':
        return (
          <div className="content-section">
            <h2>User Statistics</h2>
            <div className="statistics-grid">
              <div className="stat-item">
                <p>Current Points: {userData.points}</p>
                <p>Followed Charities: {userData.followedCharities}</p>
                <p>Attended Campaigns: {userData.attendedCampaigns}</p>
                <p>Status: {userData.status}</p>
              </div>
            </div>
          </div>
        );

      case 'settings':
        return (
          <div className="content-section">
            <h2>Settings</h2>
            <div className="settings-options">
              <button className="edit-button">Edit Profile</button>
              <button className="edit-button">Change Password</button>
            </div>
          </div>
        );

      case 'privacy':
        return (
          <div className="content-section">
            <h2>Privacy Settings</h2>
            <div className="privacy-options">
              <div className="privacy-item">
                <input type="checkbox" id="public-profile" />
                <label htmlFor="public-profile">Make profile public</label>
              </div>
              <div className="privacy-item">
                <input type="checkbox" id="show-stats" />
                <label htmlFor="show-stats">Show statistics to others</label>
              </div>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="prof-page">
      <div className="prof-container">
        {/* Sidebar */}
        <div className="sidebar">
          <div className="sidebar-header">
            <img src={logo} alt="Logo" className="logo" /> <h1>Profile</h1>
          </div>
          <nav className="sidebar-nav">
            <button
              className={`nav-item ${activeTab === 'appearance' ? 'active' : ''}`}
              onClick={() => setActiveTab('appearance')}
            >
              <FaUser className="icon" />
              <span>Appearance</span>
            </button>
            <button
              className={`nav-item ${activeTab === 'statistics' ? 'active' : ''}`}
              onClick={() => setActiveTab('statistics')}
            >
              <FaChartBar className="icon" />
              <span>Statistics</span>
            </button>
            <button
              className={`nav-item ${activeTab === 'privacy' ? 'active' : ''}`}
              onClick={() => setActiveTab('privacy')}
            >
              <FaShieldAlt className="icon" />
              <span>Privacy</span>
            </button>
            <button
              className={`nav-item ${activeTab === 'settings' ? 'active' : ''}`}
              onClick={() => setActiveTab('settings')}
            >
              <FaCog className="icon" />
              <span>Settings</span>
            </button>
          </nav>
          <button className="logout-button">
            <FaSignOutAlt className="icon" />
            <span>Logout</span>
          </button>
        </div>

        {/* Main Content */}
        <div className="main-content">
          {renderContent()}
        </div>
      </div>
    </div>
  );
};

export default Profile;
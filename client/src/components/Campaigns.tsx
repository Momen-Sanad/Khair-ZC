import React, { useState,useEffect } from 'react';
import '../assets/stylesheets/Campaigns.css';
import campaignPhoto from '../assets/images/campaignPhoto1.jpg';
import { IoPersonOutline } from "react-icons/io5";
import { IoTimeOutline } from "react-icons/io5";
import { FaPencil } from "react-icons/fa6";
import { Link } from 'react-router-dom';

interface campaign{
  id: number,
  title: string,
  address: string,
  description: string,
  date: string,
  reward:string,
  charity_id: number,
  capacity: number,
}

const Campaigns = () => {
  const [searchInput, setSearchInput] = useState('');
  const [campaigns, setCampaigns] = useState<campaign[]>([]);
  const fetchLink='http://localhost:5000/search/campaigns'
  useEffect(() => {
    fetch(fetchLink) 
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to fetch campaigns');
        }
        return response.json();
      })
      .then(data => {
        setCampaigns(data);
      })
      .catch(error => {
        console.error('Error:', error);
      });
  }, []);

  const filteredCampaigns = campaigns.filter((campaign) =>
    campaign.title.toLowerCase().includes(searchInput.toLowerCase())
  );
    return (
    <div className='campaign-container'>
      <div className="search-bar">
        <input
          type="text"
          placeholder="Search campaigns..."
          value={searchInput}
          onChange={(e) => setSearchInput(e.target.value)}
        />
      </div>
      {filteredCampaigns.map((campaign) => {
  const date = new Date(campaign.date);
  const day = date.getDate(); 
  const month = date.toLocaleString('default', { month: 'short' });
  const timeAgo = (dateString: string) => {
    const now = new Date();
    const campaignDate = new Date(dateString);
    const diffInSeconds = Math.floor((now.getTime() - campaignDate.getTime()) / 1000);

    if (diffInSeconds < 60) {
      return `${diffInSeconds} second${diffInSeconds === 1 ? '' : 's'} ago`;
    } else if (diffInSeconds < 3600) {
      const minutes = Math.floor(diffInSeconds / 60);
      return `${minutes} minute${minutes === 1 ? '' : 's'} ago`;
    } else if (diffInSeconds < 86400) {
      const hours = Math.floor(diffInSeconds / 3600);
      return `${hours} hour${hours === 1 ? '' : 's'} ago`;
    } else if (diffInSeconds < 2592000) {
      const days = Math.floor(diffInSeconds / 86400);
      return `${days} day${days === 1 ? '' : 's'} ago`;
    } else if (diffInSeconds < 31536000) {
      const months = Math.floor(diffInSeconds / 2592000);
      return `${months} month${months === 1 ? '' : 's'} ago`;
    } else {
      const years = Math.floor(diffInSeconds / 31536000);
      return `${years} year${years === 1 ? '' : 's'} ago`;
    }
  };

  return (
    <div className='campaign-wrapper' key={campaign.id}>
      <div className='Date-box'>
        <h1>{day}</h1>
        <h1>{month}</h1>
      </div>
      <div className='Campaign-card'>
        <Link to={`/campaigns/${campaign.id}`} className="campaign-link">
          <div className='Content'>
            <h1>{campaign.title}</h1>
            <p>
              {campaign.description.slice(0, 100)}.....
            </p>
            <ul className='info'>
              <li>
                <FaPencil className='icon' />
                {campaign.capacity}
              </li>
              <li>
                <IoTimeOutline className='icon' />
                {timeAgo(campaign.date)}
              </li>
            </ul>
          </div>
          <div className='CampaignPhoto'>
            <img src={campaignPhoto} alt='Campaign' />
          </div>
        </Link>
      </div>
    </div>
  );
})}
      <div className='profile-container'>
        <div className='profile-name'>
          <IoPersonOutline size={30} />
          <h1>Name</h1>
        </div>
        <div className="profile-data">
          <table>
            <tr>
              <td>Current points:</td>
              <td>160</td>
            </tr>
            <tr>
              <td>Followed charities:</td>
              <td>26</td>
            </tr>
            <tr>
              <td>Attended Campaigns:</td>
              <td>2</td>
            </tr>
            <tr>
              <td>Status:</td>
              <td>Admin</td>
            </tr>
          </table>
        </div>
      </div>
      <div className="vertical-line"></div>
    </div>
  );
};

export default Campaigns;

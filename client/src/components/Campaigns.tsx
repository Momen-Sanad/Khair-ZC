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
  date: Date,
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
      {filteredCampaigns.map((campaign) => (
        <div className='campaign-wrapper'>
          <div className='Date-box'>
            <h1>{campaign.capacity}</h1>
            <h1>{campaign.capacity}</h1>
          </div>
          <div className='Campaign-card'>
            <Link to={`/campaigns/${campaign.id}`} className="campaign-link">
              <div className='Content'>
                <h1>{campaign.title}</h1>
                <p>
                  {campaign.description.slice(0,100)}.....
                </p>
                <ul className='info'>
                  <li>
                    <FaPencil className='icon' />
                    {campaign.capacity}
                  </li>
                  <li>
                    <IoTimeOutline className='icon' />
                    {campaign.capacity}
                  </li>
                </ul>
              </div>
              <div className='CampaignPhoto'>
                <img src={campaignPhoto} alt='Campaign' />
              </div>
            </Link>
          </div>

        </div>
      ))}
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

import React from 'react';
import '../assets/stylesheets/Campaigns.css';
import campaignPhoto from '../assets/images/campaignPhoto1.jpg';
import { IoPersonOutline } from "react-icons/io5";
import { IoTimeOutline } from "react-icons/io5";
import { FaPencil } from "react-icons/fa6";
import { Link } from 'react-router-dom';

const campaigns = [
  { id: 1, name: "Campaign 1", day: "26", month:"MAY", author: "Author", time: "Posted Time ago" },
  { id: 2, name: "Another Campaign", day: "27", month:"FEB", author: "Another Author", time: "Posted Time ago" },
];


const Campaigns = () => {
  return (
    <div className='campaign-container'>
      {campaigns.map((campaign) => (
      <div className='campaign-wrapper'>
        <div className='Date-box'>
          <h1>{campaign.day}</h1>
          <h1>{campaign.month}</h1>
        </div>
        <div className='Campaign-card'>
        <Link to={`/campaigns/${campaign.id}`} className="campaign-link"/>
        <div className='Content'>
            <h1>{campaign.name}</h1>
            <p>
              Lorem ipsum dolor sit amet consectetur adipisicing elit.
              Quibusdam iusto, facilis velit, cum consequuntur molestias temporibus
              corrupti ad harum saepe minus ea reprehenderit aut eius dolores asperiores
              doloribus alias dolor!
            </p>
            <ul className='info'>
              <li>
                <FaPencil className='icon'/>
                 {campaign.author}
              </li>
              <li>
                <IoTimeOutline className='icon'/>
                {campaign.time}
              </li>
            </ul>
          </div>
          <div className='CampaignPhoto'>
            <img src={campaignPhoto} alt='Campaign' />
          </div>
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

import React from 'react';
import '../assets/stylesheets/Campaigns.css';
import campaignPhoto from '../assets/images/campaignPhoto1.jpg';
import { IoPersonOutline } from "react-icons/io5";

const Campaigns = () => {
  return (
    <div className='campaign-container'>
      <div className='campaign-wrapper'>
        <div className='Date-box'>
          <h1>26</h1>
          <h1>APR</h1>
        </div>
        <div className='Campaign-card'>
          <div className='Content'>
            <h1>Campaign Name</h1>
            <p>
              Lorem ipsum dolor sit amet consectetur adipisicing elit.
              Quibusdam iusto, facilis velit, cum consequuntur molestias temporibus
              corrupti ad harum saepe minus ea reprehenderit aut eius dolores asperiores
              doloribus alias dolor!
            </p>
            <ul className='info'>
              <li>Written by Author</li>
              <li>Posted Time ago</li>
            </ul>
          </div>
          <div className='CampaignPhoto'>
            <img src={campaignPhoto} alt='Campaign' />
          </div>
        </div>
      </div>

      <div className='campaign-wrapper'>
        <div className='Date-box'>
          <h1>27</h1>
          <h1>MAY</h1>
        </div>
        <div className='Campaign-card'>
          <div className='Content'>
            <h1>Another Campaign</h1>
            <p>
              Lorem ipsum dolor sit amet consectetur
              adipisicing elit. Vero eaque vel dicta error
              a facilis porro ipsa itaque suscipit quam.
              Quasi deleniti molestias voluptatem,
              obcaecati aut ipsam non iusto atque.
            </p>
            <ul className='info'>
              <li>Written by Another Author</li>
              <li>Posted Time ago</li>
            </ul>
          </div>
          <div className='CampaignPhoto'>
            <img src={campaignPhoto} alt='Campaign' />
          </div>
        </div>
      </div>

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

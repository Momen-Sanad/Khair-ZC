// CampaignDetails.tsx
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import '../assets/stylesheets/CampaignPage.css';
import campaignPhoto1 from '../assets/images/campaignPhoto1.jpg';

interface Campaign {
    id: number,
    title: string,
    address: string,
    description: string,
    date: string,
    reward:string,
    charity_id: number,
    capacity: number
}

const CampaignPage: React.FC = () => {
    const { id } = useParams<{ id: string }>(); // Get campaign ID from the URL
    const [campaign, setCampaign] = useState<Campaign | null>(null);
    const fetchLink = 'http://localhost:5000/search/campaigns';

    useEffect(() => {
        if (id) {
            fetch(`${fetchLink}/${id}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then((response) => {
                if (!response.ok) {
                    throw new Error('Failed to fetch campaign');
                }
                return response.json();
            })
            .then((data) => {
                setCampaign(data); 
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        }
    }, [id]);

    if (!campaign) {
        return <h1>Loading..</h1>;
    }

    const date = new Date(campaign.date);
    const day = date.getDate();
    const month = date.toLocaleString('default', { month: 'short' });

    return (
        <div className='Campaign-page'>
            <div className='Campaign-container'>
                <div className='Campaign-name'>
                    <h1>{campaign.title}</h1>
                </div>
                <div className='Campaign-Desc'>
                    <p>{campaign.description}</p>
                </div>
                <div className='Campaign-Info'>
                    <p>{campaign.capacity} participants</p>
                    <p>Reward: {campaign.reward} points</p>
                    <p>{day} {month}</p>
                </div>
            </div>
            <div className='Campaign-image'>
                <img src={campaignPhoto1} className='Campaign-image' alt="altPhoto" />
            </div>
        </div>
    );
};

export default CampaignPage;
// CampaignDetails.tsx
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import '../assets/stylesheets/CampaignPage.css';

interface Campaign {
    id: number,
    title: string,
    address: string,
    description: string,
    date: string,
    reward:string,
    charity_id: number,
    capacity: number
    author:string
    image:string
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
    const renderDescription = (description: string) => {
        const urlRegex = /(https?:\/\/[^\s]+)/g;  // Regex to detect URLs
    
        return description.split('\n').map((line, index) => {
            // Split the line into text and links
            const segments = line.split(urlRegex);
            
            return (
                <span key={index} className="text-segment" dir="auto">
                    {segments.map((segment, idx) =>
                        // Check if the segment is a URL and create a link for it
                        urlRegex.test(segment) ? (
                            <a key={idx} href={segment} target="_blank" rel="noopener noreferrer">
                                {segment}
                            </a>
                        ) : (
                            segment
                        )
                    )}
                </span>
            );
        });
    };
    
    return (
        <div className='Campaign-page'>
            <div className='Campaign-container'>
                <div className='Campaign-name'>
                    <h1>{campaign.title}</h1>
                </div>
                <div className='Campaign-Desc'>
                    {renderDescription(campaign.description)}
                </div>
                <div className='Campaign-Info'>
                    <p>{campaign.capacity} participants</p>
                    <p>Reward: {campaign.reward} points</p>
                    <p>{day} {month}</p>
                    <p>{campaign.author}</p>
                </div>
            </div>
            <div className='Campaign-image'>
                <img src={campaign.image} className='Campaign-image' alt="Campaign visual" />
            </div>
        </div>
    );
};

export default CampaignPage;
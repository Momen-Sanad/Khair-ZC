// CampaignDetails.tsx
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import '../assets/stylesheets/CampaignPage.css';
import campaignPhoto1 from '../assets/images/campaignPhoto1.jpg';

interface Campaign {
    id: number;
    name: string;
    description: string;
    day: number;
    month: string;
    author: string;
    time: string;
}

const CampaignPage: React.FC = () => {
    const { id } = useParams<{ id: string }>(); // Get campaign ID from the URL
    const [campaign, setCampaign] = useState<Campaign | null>(null);

    useEffect(() => {
        if (id) {
            const fetchedCampaign: Campaign = {
                id: parseInt(id),
                name: `Campaign ${id}`,
                description: `Lorem ipsum dolor sit amet consectetur,
                 adipisicing elit. Harum, quas alias numquam doloribus laudantium 
                 culpa quia quis sapiente natus eveniet et perspiciatis molestias commodi 
                eaque ipsam rerum reprehenderit corporis eius?
                Lorem ipsum dolor sit amet consectetur,
                 adipisicing elit. Harum, quas alias numquam doloribus laudantium 
                 culpa quia quis sapiente natus eveniet et perspiciatis molestias commodi 
                eaque ipsam rerum reprehenderit corporis eius?
                Lorem ipsum dolor sit amet consectetur,
                 adipisicing elit. Harum, quas alias numquam doloribus laudantium 
                 culpa quia quis sapiente natus eveniet et perspiciatis molestias commodi 
                eaque ipsam rerum reprehenderit corporis eius?`,
                author: `wrote by author ${id}`,
                day: 2,
                month: `Feb`,
                time: `Wrote ${id} days ago`,
            };
            setCampaign(fetchedCampaign);
        }
    }, [id]);

    return (
        <div className='Campaign-page'>
            {campaign ? (
                <>
                    <div className='Campaign-container'>
                        <div className='Campaign-name'>
                            <h1>{campaign.name}</h1>
                        </div>
                        <div className='Campaign-Desc'>
                            <p>{campaign.description}</p>
                        </div>
                        <div className='Campaign-Info'>
                            <p>{campaign.day} {campaign.month}</p>
                            <p>{campaign.author}</p>
                            <p>{campaign.time}</p>
                        </div>
                    </div>
                    <div className='Campaign-image'>
                        <img src={campaignPhoto1} className='Campaign-image'></img>
                    </div>
                </>
            ) : (<h1>Loading..</h1>)}
        </div>
    );
};

export default CampaignPage;

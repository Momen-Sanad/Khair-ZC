// CampaignDetails.tsx
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import '../assets/stylesheets/CharityPage.css';

interface charity {
    id: number,
    name: string,
    address: string,
    description: string,
    category: string,
    image: string
}

const CharityPage: React.FC = () => {
    const { id } = useParams<{ id: string }>(); // Get charity ID from the URL
    const [charity, setCharity] = useState<charity | null>(null);
    const fetchLink = 'http://localhost:5000/search/charities';

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
                    throw new Error('Failed to fetch charity');
                }
                return response.json();
            })
            .then((data) => {
                setCharity(data); 
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        }
    }, [id]);

    if (!charity) {
        return <h1>Loading..</h1>;
    }

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
        <div className='Charity-page'>
            <div className='Charity-container'>
                <div className='Charity-name'>
                    <h1>{charity.name}</h1>
                </div>
                <div className='Charity-Desc'>
                    {renderDescription(charity.description)}
                </div>
                <div className='Charity-Info'>
                    <p>Location: {charity.address}</p>
                    <p>category: {charity.category}</p>
                </div>
            </div>
            <div className='Charity-image'>
                <img src={charity.image} className='Charity-image' alt="Charity visual" />
            </div>
        </div>
    );
};

export default CharityPage;
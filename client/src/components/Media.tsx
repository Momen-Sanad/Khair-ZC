import React from 'react';
import { useState,useEffect } from 'react';
import '../assets/stylesheets/Media.css';

interface image{
  id: number,
  url: string
}

const Media = () => {
  const [images,setImages]=useState<image[]>([]);
  const fetchImages='http://localhost:5000/media/images'
  useEffect(() => {
      fetch(fetchImages) 
        .then(response => {
          if (!response.ok) {
            throw new Error('Failed to fetch Images');
          }
          return response.json();
        })
        .then(data => {
          setImages(data);
        })
        .catch(error => {
          console.error('Error:', error);
        });
    }, []);

  return (
    <div className='Gallery'>
      {images.map((image:image)=>(
        <img
          src={image.url}
          alt={`Gallery item ${image.id}`}
          className='GalleryImage'
        />
      ))}
    </div>

  );
};

export default Media;


import React from 'react';
import { useState,useEffect } from 'react';
import '../assets/stylesheets/Media.css';


const Media = () => {
  const [images,setImages]=useState<string[]>([]);
  useEffect(()=>{
    const numImages=20;
    const imagesPaths=[];
    for(let i=0;i<numImages;i++){
      imagesPaths.push(`/images/KhairGallery/image${i+1}.jpg`);
    }
    setImages(imagesPaths);
  },[])
  return (
    <div className='Gallery'>
      {images.map((src,i)=>(
        <img
          src={src}
          alt={`Image ${i+1}`}
          className='GalleryImage'
        />
      ))}
    </div>

  );
};

export default Media;


import React from 'react';
import '../assets/stylesheets/Shop.css';

const products = [
  { id: 1, name: "Hat", points: 20, description: "A classic, adjustable hat made from soft cotton, perfect for casual outings and sun protection.", imageURL: "https://tinyurl.com/vmetn5yy" },
  { id: 2, name: "T-shirt", points: 30, description: "A soft, breathable cotton t-shirt that offers comfort and style for any occasion.", imageURL: "https://shorturl.at/YJMTL" },
  { id: 3, name: "Mug", points: 15, description: "A durable ceramic mug, perfect for your favorite drinks, microwave and dishwasher safe.", imageURL: "https://shorturl.at/gU9sw" }
]
const Shop = () => {
  return (
    <div className='Products-Container'>
      {products.map((product) => (
        <div className='Product-Card'>
          <div className='Product-image'>
            <img src={product.imageURL} alt={product.name} />
          </div>
          <div className='Product-info'>
            <h2>{product.name}</h2>
            <p>{product.description}</p>
            <h3>{product.points} points</h3>
          </div>
          <button className="btn-donate">
            Redeem
          </button>
        </div>
      ))}
    </div>
  );  
};

export default Shop;


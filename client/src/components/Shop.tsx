import React from 'react';
import '../assets/stylesheets/Shop.css';
import { IoArrowBackCircleOutline } from "react-icons/io5";
import { useNavigate } from 'react-router-dom';

const Points=35;
const products = [
  { id: 1, name: "Hat", points: 20, description: "A classic, adjustable hat made from soft cotton, perfect for casual outings and sun protection.", imageURL: "https://tinyurl.com/vmetn5yy" },
  { id: 2, name: "T-shirt", points: 30, description: "A soft, breathable cotton t-shirt that offers comfort and style for any occasion.", imageURL: "https://shorturl.at/YJMTL" },
  { id: 3, name: "Mug", points: 15, description: "A durable ceramic mug, perfect for your favorite drinks, microwave and dishwasher safe.", imageURL: "https://shorturl.at/gU9sw" }
]

const Shop = () => {
  const navigate = useNavigate();

  const goBack = () => {
    navigate(-1);}

  const handleRedeem=(productName : string,ProductPoints: number)=>{
    const userConfirmed=window.confirm(`Are you sure you want to redeem the ${productName} with ${ProductPoints} points ?`)
    if(userConfirmed){
      alert(`You have successfully redeemed the ${productName}`);
    }};
  return (
    <div className='Products-Container'>
      <div>
        <nav className='ShopBar'>
        <IoArrowBackCircleOutline className='BackArrow' onClick={goBack}/>
          <div className='ShopBar-container'>
            <div className='Available-points'>
                <p>Available Points: {Points}</p>
            </div>
          </div>
        </nav>
      </div>
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
          <button onClick={()=>handleRedeem(product.name,product.points)} className="btn-donate">
            Redeem
          </button>
        </div>
      ))}
    </div>
  );
};

export default Shop;


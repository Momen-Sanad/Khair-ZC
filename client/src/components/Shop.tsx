import React from 'react';
import { useState,useEffect } from 'react';
import '../assets/stylesheets/Shop.css';
import { IoArrowBackCircleOutline } from "react-icons/io5";
import { useNavigate } from 'react-router-dom';

interface product{
  id: number,
  name: string,
  description: string,
  price: number,
  image: string
}

const Points=35;
const Shop = () => {

  const [products, setProducts] = useState<product[]>([]);
  const fetchProducts='http://localhost:5000/shop/products'
  useEffect(() => {
    fetch(fetchProducts)
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to fetch products');
        }
        return response.json();
      })
      .then(data => {
        console.log("Fetched products:", data);
        setProducts(data);
      })
      .catch(error => {
        console.error('Error:', error);
      });
  }, []);
  
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
            <img src={product.image} alt={product.name} />
          </div>
          <div className='Product-info'>
            <h2>{product.name}</h2>
            <p>{product.description}</p>
            <h3>{product.price} points</h3>
          </div>
          <button onClick={()=>handleRedeem(product.name,product.price)} className="btn-donate">
            Redeem
          </button>
        </div>
      ))}
    </div>
  );
};

export default Shop;


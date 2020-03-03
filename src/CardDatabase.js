import React, { useEffect, useState } from 'react';
import Card from './Card'
import './App.css';
const CardDatabase = () => {

    const [cards, setCards] = useState([]);
    const [search, setSearch] = useState("");
    const [query, setQuery] = useState("Fish");
  
    const CARD_QUERY = `https://db.ygoprodeck.com/api/v6/cardinfo.php?race=${query}`;
    const CARD_SET_QUERY = 'https://db.ygoprodeck.com/api/v6/cardsetsinfo.php?setcode=SDY-046'
  
    useEffect(() =>{
      getCards();
    }, [query]);
  
    const getCards = async () => {
      const response = await fetch(CARD_QUERY);
      const data = await response.json();
      // console.log(data)
      setCards(data);
    }
  
    const updateSearch = e => {
      setSearch(e.target.value);
      console.log(search)
    }
  
    const getSearch = e => {
      e.preventDefault();
      setQuery(search);
      setSearch("")
    }

    return(
        <div>
            <h1>Cards</h1>
            <form onSubmit={getSearch} className="search-form">
				<input className="search-bar" type="text" value={search} onChange={updateSearch}/>
        <button classname="search-button" type="submit">
          Search
        </button>
			</form>
      {cards.map(card => (
        <Card
          key={card.name}
          name={card.name}
          type={card.race}
          image={card.card_images[0].image_url_small}
        />
      ))}
          </div>

    )
}




export default CardDatabase
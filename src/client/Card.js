import React from 'react';

const Card = ({name, type, image}) => {
    return(
        <div>
            <h1>{name}</h1>
            <p>{type}</p>
            <img src={image} alt=""/>
        </div>
    );
}

export default Card;
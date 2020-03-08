import React from "react"
import {Link} from "react-router-dom"

// function handleClick(event){
//   return(
//     <div>
//       <Link to="login.html">Login</Link>
//     </div>
//   )

// }

function HomeNavigation(){
  const navStyle = {
    color: 'white'
  }
    return(
        <nav>
        <ul className="nav-links">
          <Link style={navStyle} to="/login"><li>LoginPage</li></Link>
          <Link style={navStyle} to="/carddatabase"><li>Cards</li></Link>
          <Link style={navStyle} to="/"><li>Home</li></Link>
          <Link style={navStyle} to="/createroom"><li>CreateRoom</li></Link>
          
        </ul>
      </nav>
    )
}



export default HomeNavigation

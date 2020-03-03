import React, { useEffect, useState } from 'react';
import Card from './Card'
import './App.css';
import HomeNavigation from "./HomeNavigation"
import CardDatabase from "./CardDatabase"
import LoginPage from "./LoginPage"
import {BrowserRouter as Router,Switch,Route} from "react-router-dom"
const App = () => {


	return (
		<div className="App">
      <Router>
      <HomeNavigation />
      <Switch>
      <Route path="/login" exact component={LoginPage}/>
      <Route path="/carddatabase" component={CardDatabase} />
      <Route path="/" component={Home} />
      </Switch>

      </Router>
		</div>
	);
};

const Home = () =>(
  <div>
    <h1>Home</h1>
  </div>
)


export default App;
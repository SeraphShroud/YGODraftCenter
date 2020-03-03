import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import * as serviceWorker from './serviceWorker';
import {BrowserRouter, Route, Switch} from "react-router-dom"
import LoginPage from "./LoginPage"

ReactDOM.render(<App />, document.getElementById('root'));
// ReactDOM.render(
//     <BrowserRouter>
//      <Switch>
//       <Route exact path="/" component={LoginPage} />
//       {/* <Route path="/page2" component={Page2} /> */}
//     </Switch>
//     </BrowserRouter>,
//     rootElement
//   );

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();

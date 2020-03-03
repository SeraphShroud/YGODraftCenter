import React from 'react';
import { Link } from 'react-router';
import { LoginLink } from 'react-stormpath';



export default class is extends React.Component {
  render() {
    return (
        <div className='MasterPage'>
          { this.props.children }
        </div>
    );
  }
}
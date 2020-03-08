import React from "react"
import {Link } from "react-router-dom";

class LoginPage extends React.Component{
    constructor(){
        super()
        this.state ={isLoginOpen:true, isRegisterOpen:false

        }
    }
    showLoginBox(){
        this.setState({isRegisterOpen:false,isLoginOpen:true})

    }
    showRegisterBox(){
        this.setState({isRegisterOpen:true,isLoginOpen:false})

    }

    render(){
    return(
        <div className="login-container">


            <div className="box-controller">
                <div className={"controller" + (this.state.isLoginOpen ? "selected-controller" : "")} onClick={this.showLoginBox.bind(this)}>
                    Login
                    </div>

            <div className={"controller" + (this.state.isRegisterOpen ? "selected-controller" : "")}onClick={this.showRegisterBox.bind(this)}>
                Register
            </div>
            </div>


            <div className="box-container">
                {this.state.isLoginOpen && <LoginBox />}
                {this.state.isRegisterOpen && <RegisterBox />}
            </div>
    </div>

    )
}
}

class LoginBox extends React.Component{
    constructor(props){
        super(props)
        this.setState ={

        }
    }
    submitLogin(e){

    }
        render() {
            return(
            <div className="inner-contrainer">
                <div className="header">
                    Login
                </div>

                <div className="box">

                    <div className="input-group">

                        <label htmlfor="username"Username></label>
                        <input type="text"name="username" className="login-input" placeholder="Username"/>

                    </div>
                    <div className="input-group">

                        <label htmlfor="password"Password></label>
                        <input type="text"name="password" className="login-input" placeholder="Password"/>

                    </div>
                    <button type="button" className="login-btn" onClick={this.submitLogin.bind(this)}>Login</button>
                </div>

            </div>
            )
          
        }
    
}

class RegisterBox extends React.Component{
    constructor(props){
        super(props)
        this.setState ={

        }
    }
    submitRegister(e){

    }
        render() {
            return(
            <div className="inner-contrainer">
                <div className="header">
                    Register
                </div>

                <div className="box">

                    <div className="input-group">

                        <label htmlfor="username"Username></label>
                        <input type="text"name="username" className="register-input" placeholder="Username"/>

                    </div>
                    <div className="input-group">

                        <label htmlfor="password"Password></label>
                        <input type="text"name="password" className="register-input" placeholder="Password"/>

                    </div>
                    <button type="button" className="login-btn" onClick={this.submitRegister.bind(this)}>Register</button>
                </div>

            </div>
            )
          
        }
    
}


export default LoginPage

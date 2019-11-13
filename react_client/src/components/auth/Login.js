import React, { Component } from 'react';
import { Link, Redirect } from "react-router-dom";

import authServices from '../../services/auth.service';

/***
 *  Login page
 */

class Login extends Component {

    /**
     *  Login constructor
     */

    constructor (props) {
        super(props);
        this.state = {
            email: '',
            password: '',

            redirect: authServices.getUser() && true,
            error: null
        }
    }


    componentDidMount() {
        const token = this.props.match.params.token;
        if (token) {
            authServices.setUser(token);
            this.setState({ redirect: true });
        }
    }


    /**
     *  Handling the change in the form elements and assigning them to states
     *
     *  @param e: input event
     */

    handleChange = (e) => {
        this.setState({[e.target.name]: e.target.value})
    };


    /**
     *  Handling the submit action
     *
     *  @param e: input event
     */

    handleSubmit = (e) => {
        e.preventDefault();

        authServices.login({
            email: this.state.email,
            password: this.state.password
        })
            .then(response => {
                if (response.success) {
                    this.setState({ redirect: true });
                } else {
                    this.setState({ error: response.message });
                }
            })
            .catch(err => console.log(err));
    };


    render() {
        if (this.state.redirect) {
            return <Redirect to={'/'}/>
        }
        return (
            <div>
                <h1>Sign In</h1>
                <form onChange={this.handleChange} onSubmit={this.handleSubmit} method="post">
                    {/* Email */}
                    <label htmlFor="email">Email</label>
                    <input type="email" name="email"/>

                    {/* Password */}
                    <label htmlFor="password">Password</label>
                    <input type="password" name="password"/>

                    {/* Sign Up / Register */}
                    <Link to="/signUp/">Sign Up</Link>

                    {/* Submit */}
                    <button type="submit">Login</button>

                    {/* Error */}
                    {(this.state.error) && <p>{this.state.error}</p>}
                </form>
            </div>
        )
    }
}

// Exporting the component
export default Login;

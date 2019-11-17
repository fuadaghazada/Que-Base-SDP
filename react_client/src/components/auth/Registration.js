import React, { Component } from 'react';
import { Link, Redirect } from 'react-router-dom';

import authServices from '../../services/auth.service';

/***
 *  Registration component
 */


class Registration extends Component {

    /**
     *  Registration constructor
     */

    constructor (props) {
        super(props);
        this.state = {
            firstName: '',
            lastName: '',
            username: '',
            email: '',
            password: '',
            confirmPassword: '',

            redirect: authServices.getUser() && true,
            error: null,
        }
    }


    /**
     *  Handling the change in the form elements and assigning them to states
     *
     *  @param e: input event
     */

    handleChange = (e) => {
        if (e.target.type === 'file') {
            this.setState({[e.target.name]: e.target.files[0]});
        } else {
            this.setState({[e.target.name]: e.target.value})
        }
    };


    /**
     *  Handling the submit action
     *
     *  @param e: input event
     */

    handleSubmit = (e) => {
        e.preventDefault();

        // Adding keys and values to form data
        const data = {
            firstname: this.state.firstName,
            lastname: this.state.lastName,
            username: this.state.username,
            email: this.state.email,
            password: this.state.password,
            confirmPassword: this.state.confirmPassword,
        };

        // Sending POST Request
        authServices.signUp(data)
            .then(response => {
                if (response && response.success) {
                    this.setState({ redirect: true });
                } else {
                    this.setState({ error: response.message });
                }
            })
            .catch(err => {
                console.log(err);
            });
    };


    render() {
        if (this.state.redirect) {
            return <Redirect to={'/'}/>
        }
        return (
            <div>
                <h1>Sign Up</h1>
                <form onChange={this.handleChange} onSubmit={this.handleSubmit} method="post">

                    {/* First Name */}
                    <label htmlFor="firstName">First name</label>
                    <input type="text" name="firstName"/>

                    {/* Last Name */}
                    <label htmlFor="lastName">Last name</label>
                    <input type="text" name="lastName"/>

                    {/* Username */}
                    <label htmlFor="username">Username</label>
                    <input type="text" name="username"/>

                    {/* Email */}
                    <label htmlFor="email">Email</label>
                    <input type="email" name="email"/>

                    {/* Password */}
                    <label htmlFor="password">Password</label>
                    <input type="password" name="password"/>

                    {/* Confirm Password */}
                    <label htmlFor="confirmPassword">Confirm password</label>
                    <input type="password" name="confirmPassword"/>

                    {/* Sign In / Login */}
                    <Link to="/login/">Sign In</Link>

                    {/* Submit */}
                    <button type="submit">Sign Up</button>

                    {/* Error */}
                    {(this.state.error) && <p>{this.state.error}</p>}
                </form>
            </div>
        )
    }
}

// Exporting the component
export default Registration;

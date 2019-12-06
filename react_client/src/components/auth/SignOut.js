import React, { Component } from 'react';
import { Redirect } from "react-router-dom";

import authServices from '../../services/auth.service';

/***
 *  Sign out component
 */

class SignOut extends Component {

    /**
        Constructor
     */

    constructor(props) {
        super(props);

        this.state = {
            redirect: false
        }
    }

    /**
     *  Handling the sign out action
     *
     *  @param e: input event
     */

    handleSubmit = (e) => {
        e.preventDefault();


        authServices.signOut()
            .then(response => {
                this.setState({redirect: response.redirect});
            })
            .catch(err => console.log(err));
    };

    render () {
        if (this.state.redirect) {
            return <Redirect to={'/'}/>
        }

        return (
            <button onClick={this.handleSubmit}>Sign Out</button>
        );
    }
}

// Exporting the component
export default SignOut;

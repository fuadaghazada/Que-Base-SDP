import React, { Component } from 'react';
import { Redirect } from "react-router-dom";

import {Button} from '@material-ui/core';
import ExitToAppIcon from '@material-ui/icons/ExitToApp';

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
            <Button onClick={this.handleSubmit} style={{color: "white"}}><ExitToAppIcon/></Button>
        );
    }
}

// Exporting the component
export default SignOut;

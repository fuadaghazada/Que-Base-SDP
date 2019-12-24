import React, { Component } from 'react';

import authServices from '../../services/auth.service';
import userServices from '../../services/user.service';

import NavBar from "../NavBar";
import UserContainer from "./UserContainer";

/**
 *   User friend wait list
 */

class FriendRequests extends Component {

    constructor(props) {
        super(props);

        this.state = {

            users: null,

            isLoading: false,
            error: null,
            page: 1
        };
    }

    componentDidMount() {

        this.handleRequest(this.state.page)
    }

    handleRequest = (page = 1) => {
        try {
            const user = authServices.getUser();
            const userData = user['user']['sub'];
            const userDataJson = JSON.parse(userData)
            const userId = userDataJson['_id'];

            this.setState({isLoading: true});
            userServices.getWaitList(page, userId)
                .then(response => {

                    if(response['success']) {
                        this.setState({
                            isLoading: false,
                            users: response['result']
                        })
                    }
                })
                .catch(e => {
                    console.log(e);
                })

        } catch (e) {
            console.log(e);
        }
    };

    render() {
        return (
            <div>
                <NavBar/>
                {this.state.users && <UserContainer users={this.state.users}
                                                    page={this.state.page}
                                                    handleRequest={this.handleRequest}
                                                    header={"Friend Requests"}
                                                    state={2}
                />}
            </div>
        )
    }
}

// Exporting the component
export default FriendRequests;

import React, { Component } from 'react';

import userServices from '../../services/user.service';

import NavBar from "../NavBar";
import UserContainer from "./UserContainer";

/**
 *   User friend wait list
 */

class UserSearchResult extends Component {

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

    componentDidUpdate(prevProps, prevState, snapshot) {
        const searchValue = this.props.match.params.username;

        if (prevProps.match.params.username !== searchValue) {
            this.handleRequest(this.state.page);
        }
    }

    handleRequest = (page = 1) => {

        const searchValue = this.props.match.params.username;

        try {
            this.setState({isLoading: true});
            userServices.searchUsers(page, searchValue)
                .then(response => {
                    if(response['success']) {
                        this.setState({
                            isLoading: false,
                            users: response['results']
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

        const searchValue = this.props.match.params.username;

        return (
            <div>
                <NavBar/>
                {this.state.users && <UserContainer users={this.state.users}
                                                    page={this.state.page}
                                                    handleRequest={this.handleRequest}
                                                    header={`Search Results for '${searchValue}'`}
                />}
            </div>
        )
    }
}

// Exporting the component
export default UserSearchResult;

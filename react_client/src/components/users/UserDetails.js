import React, {Component} from 'react';

import authServices from '../../services/auth.service';
import userServices from '../../services/user.service';

import UserContainer from "./UserContainer";
import QuestionContainer from "../questions/QuestionContainer";
import {Tabs, Tab, Container} from '@material-ui/core';
import FaceIcon from '@material-ui/icons/Face';
import FavoriteIcon from '@material-ui/icons/Favorite';
import PeopleIcon from '@material-ui/icons/People';
import UserOverview from "./UserOverview";
import NavBar from "../NavBar";


/*
 *  User details
 */

class UserDetails extends Component {

    constructor(props) {
        super(props);

        this.state = {

            userData: null,
            favoriteQuestions: null,
            friends: null,

            selectedTab: 0,
            showOverview: true,
            showFavQuestions: false,
            showFriends: false,

            isLoading: false,
            error: null,
            page: 1
        }
    }

    componentDidMount() {

        try {
            let userId;
            if (this.props.match.params.id) {
                userId = this.props.match.params.id;

            } else {
                const user = authServices.getUser();
                const userData = user['user']['sub'];
                const userDataJson = JSON.parse(userData)
                userId = userDataJson['_id'];
            }

            this.setState({isLoading: true});
            userServices.getUser(userId)
                .then(response => {

                    if (response['success']) {
                        this.setState({
                            isLoading: false,
                            userData: response.user
                        });
                    }
                })
                .catch(err => {
                    console.log(err);
                })

        } catch (e) {
            console.log(e);
        }
    }

    getQuestions = (page = 1) => {

        if (this.state.userData) {

            const userId = this.state.userData['_id'];

            // Request
            this.setState({isLoading: true});
            userServices.getFavoriteQuestions(page, userId)
                .then(response => {

                    if (response['success']) {
                        this.setState({
                            favoriteQuestions: response.result,
                            isLoading: false
                        })
                    }
                })
                .catch(err => {
                    console.log(err);
                })
        }
    };

    getFriends = (page = 1) => {

        if (this.state.userData) {

            const userId = this.state.userData['_id'];

            // Request
            this.setState({isLoading: true})
            userServices.getFriends(page, userId)
                .then(response => {

                    if (response['success']) {
                        this.setState({
                            friends: response.result,
                            isLoading: false
                        })
                    }
                })
                .catch(err => {
                    console.log(err);
                })
        }
    };

    showDetails = (event, newValue) => {

        this.setState({selectedTab: newValue});

        // Display the overview of the user
        if (newValue === 0) {
            this.setState({showOverview: true, showFavQuestions: false, showFriends: false})
        }
        // Display the favorite questions of the user
        else if (newValue === 1) {
            this.setState({showOverview: false, showFavQuestions: true, showFriends: false})
            this.getQuestions()
        }
        // Display the friends of the user
        else if (newValue === 2) {
            this.setState({showOverview: false, showFavQuestions: false, showFriends: true})
            this.getFriends()
        }
    };

    render(){

        if (this.state.userData) {

            return (
                <div>
                    <NavBar/>
                    <Container maxWidth={"md"}>
                        <Tabs
                            indicatorColor="primary"
                            textColor="primary"
                            aria-label="profile page tabs"
                            onChange = {this.showDetails}
                            value = {this.state.selectedTab}
                        >
                            <Tab icon={<FaceIcon />} label="Overview" />
                            <Tab icon={<FavoriteIcon />} label="Favorite Questions" />
                            <Tab icon={<PeopleIcon />} label="Friends" />
                        </Tabs>

                        {this.state.showOverview && <UserOverview userData={this.state.userData}/> }
                        {this.state.showFavQuestions && this.state.favoriteQuestions && <QuestionContainer questions={this.state.favoriteQuestions} page={this.state.page} handleRequest={this.getQuestions}/>}
                        {this.state.showFriends && this.state.friends && <UserContainer users={this.state.friends} page={this.state.page} handleRequest={this.getFriends}/>}
                    </Container>
                </div>
            )
        }

        return null;
    }
}

// Exporting the component
export default UserDetails;

import React, {Component} from 'react';

import authServices from '../services/auth.service';
import userServices from '../services/user.service';

import UserContainer from "./UserContainer";
import QuestionContainer from "./questions/QuestionContainer";


/***
 *  User details
 */

class UserDetails extends Component {

    constructor(props) {
        super(props);

        this.state = {

            userData: null,
            favoriteQuestions: null,
            friends: null,

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
            this.setState({isLoading: true})
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

    render(){

        if (this.state.userData) {

            const {username, firstname, lastname, email} = this.state.userData;

            return (
                <div>
                    <h1>{firstname} {lastname}</h1>
                    <h2>{username}</h2>
                    <h2>{email}</h2>

                    <button onClick={this.getQuestions}>Get favorite Questions</button>
                    {this.state.favoriteQuestions && <QuestionContainer questions={this.state.favoriteQuestions} page={this.state.page} handleRequest={this.getQuestions}/>}

                    <button onClick={this.getFriends}>Get Friends</button>
                    {this.state.friends && <UserContainer users={this.state.friends} page={this.state.page} handleRequest={this.getFriends}/>}
                </div>

            )
        }

        return null;
    }
}

// Exporting the component
export default UserDetails;

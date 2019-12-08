import React, {Component} from 'react';

import authServices from '../services/auth.service';
import userServices from '../services/user.service';

import UserContainer from "./UserContainer";
import QuestionContainer from "./questions/QuestionContainer";
import Paper from '@material-ui/core/Paper';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';


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
            container: null,

            username: "",
            firstname: "",
            lastname: "",
            email: "",

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

    showDetails = (event, newValue) => {
        console.log(newValue);
        if(newValue === 0)
        {
            const {username, firstname, lastname, email} = this.state.userData;
            this.setState({friends: null, favoriteQuestions: null})
            this.setState({username: username, firstname: firstname, lastname: lastname, email: email})

        }
        if(newValue === 1)
        {
            this.setState({friends: null, username: null, firstname: null, lastname: null, email: null})
            this.getQuestions()
        }
        if(newValue === 2)
        {
            this.setState({favoriteQuestions: null, username: null, firstname: null, lastname: null, email: null})
            this.getFriends()
        }
        
    }

    render(){

        if (this.state.userData) {

            return (
                <div>
                    
                    <Tabs
                        indicatorColor="primary"
                        textColor="primary"
                        aria-label="disabled tabs example"
                        onChange = {this.showDetails}
                      >
                        <Tab label="Overview" />
                        <Tab label="Friends" />
                        <Tab label="Favorite Questions" />
                        {this.state.container}
                      </Tabs>    
                    <h1>{this.state.firstname} {this.state.lastname}</h1>
                    <h2>{this.state.username}</h2>
                    <h2>{this.state.email}</h2>                
                    {this.state.favoriteQuestions && <QuestionContainer questions={this.state.favoriteQuestions} page={this.state.page} handleRequest={this.getQuestions}/>}
                    {this.state.friends && <UserContainer users={this.state.friends} page={this.state.page} handleRequest={this.getFriends}/>}
                    <Paper square>
                      
                    </Paper>
                </div>

            )
        }

        return null;
    }
}

// Exporting the component
export default UserDetails;
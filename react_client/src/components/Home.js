import React, { Component } from 'react';
import NavBar from "./NavBar";

import questionServices from '../services/question.service';
import postServices from '../services/post.service';

import QuestionContainer from "./questions/QuestionContainer";
import PostContainer from "./PostContainer";

/**
    Home Component
*/

class Home extends Component {

    constructor(props) {
        super(props);
        this.state = {

            questionData: null,
            userFeedData: null,

            isLoading: false,
            error: null,
            pageMVQ: 1,
            pageFeed: 1,
            threshold: 0
        }
    }

    componentDidMount() {
        this.handleRequestMVQ(this.state.pageMVQ);
        this.handleRequestFeed(this.state.pageFeed);
    }

    handleRequestMVQ = (page = 1) =>{

        this.setState({isLoading: true});
        questionServices.getMostViewedQuestions(page, this.state.threshold)
            .then(response => {

                if (response['success']) {

                    this.setState({
                        isLoading: false,
                        questionData: response['result']
                    })
                }
            })
            .catch(err => {
                console.log(err);
            })
    };

    handleRequestFeed = (page = 1) =>{

        this.setState({isLoading: true});
        postServices.getPosts(page)
            .then(response => {

                if (response['success']) {

                    this.setState({
                        isLoading: false,
                        userFeedData: response['result']
                    })
                }
            })
            .catch(err => {
                console.log(err);
            })
    };

    render() {
        return (
            <div>
                <NavBar />

                {/* Feed */}
                {this.state.userFeedData && <PostContainer posts={this.state.userFeedData}
                                                           page={this.state.pageFeed}
                                                           handleRequest={this.handleRequestFeed}
                                                           header={"Feed"}
                />}

                {/* Most Viewed Questions */}
                {this.state.questionData && <QuestionContainer questions={this.state.questionData}
                                                               page={this.state.pageMVQ}
                                                               handleRequest={this.handleRequestMVQ}
                                                               header={"Most viewed questions"}
                />}

            </div>
        );
    }

}

// Exporting the component
export default Home;

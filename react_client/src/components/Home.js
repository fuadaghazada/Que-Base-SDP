import React, { Component } from 'react';
import NavBar from "./NavBar";

import questionServices from '../services/question.service';
import QuestionContainer from "./questions/QuestionContainer";

/**
    Home Component
*/

class Home extends Component {

    constructor(props) {
        super(props);
        this.state = {

            questionData: null,

            isLoading: false,
            error: null,
            page: 1,
            threshold: 0
        }
    }

    componentDidMount() {
        this.handleRequest(this.state.page);
    }

    handleRequest = (page = 1) =>{

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

    render() {
        return (
            <div>
                <NavBar />
                {this.state.questionData && <QuestionContainer questions={this.state.questionData}
                                                               page={this.state.page}
                                                               handleRequest={this.handleRequest}
                                                               header={"Most viewed questions"}
                />}
            </div>
        );
    }

}

// Exporting the component
export default Home;

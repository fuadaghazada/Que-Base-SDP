import React, {Component} from 'react';

import QuestionDisplay from './QuestionDisplay';
import NavBar from "../NavBar";

import questionServices from '../../services/question.service';

/***
 *  Question details
 */

class QuestionDetails extends Component {

    constructor(props) {
        super(props);

        this.state = {

            questionData: null,
            isFavorite: false,

            isLoading: false,
            error: null
        }
    }

    componentDidMount() {

        try {
            const questionId = this.props.match.params.id;

            this.setState({isLoading: true});
            questionServices.getQuestion(questionId)
                .then(response => {

                    if (response['success']) {
                        this.setState({
                            isLoading: false,
                            questionData: response['question'],
                            isFavorite: response['favorite']
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

    favoriteQuestion = () => {

        try {
            const questionId = this.props.match.params.id;

            questionServices.favoriteQuestion(questionId)
                .then(response => {
                    if (response['success']) {
                        this.setState({isFavorite: response['result']})
                    }
                })
        } catch (e) {
            console.log(e);
        }
    };

    render(){

        return (
            <div>
                <NavBar/>
                {this.state.questionData && <QuestionDisplay questionData={this.state.questionData} favoriteQuestion={this.favoriteQuestion} isFavorite={this.state.isFavorite}/>}
            </div>
        )
    }
}

// Exporting the component
export default QuestionDetails;

import React, {Component} from 'react';
import questionServices from '../../services/question.service';
import { Container } from '@material-ui/core';
import QuestionDisplay from './QuestionDisplay';


/***
 *  Question details
 */

class QuestionDetails extends Component {

    constructor(props) {
        super(props);

        this.state = {

            questionData: null,

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
                            questionData: response['question']
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

    render(){

        if (this.state.questionData) {

            const {body, title, viewCount, favCount, source, userId} = this.state.questionData;

            return (
                <Container maxWidth = {"md"}>
                    <QuestionDisplay questionData={this.state.questionData}/>
                </Container>
            )
        }

        return null;
    }
}

// Exporting the component
export default QuestionDetails;

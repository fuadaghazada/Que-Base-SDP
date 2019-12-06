import React, {Component} from 'react';
import questionServices from '../../services/question.service';


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
                <div>
                    <h1>{title}</h1>
                    <h2>{viewCount}</h2>
                    <h2>{favCount}</h2>
                    <p>{body}</p>
                    <p>Course: {source.course} University: {source.university} </p>
                </div>
            )
        }

        return null;
    }
}

// Exporting the component
export default QuestionDetails;

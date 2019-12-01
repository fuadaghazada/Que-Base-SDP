import React, { Component } from 'react';
import NavBar from "../NavBar";

import questionServices from "../../services/question.service";
import QuestionContainer from "./QuestionContainer";


/***
 *  Upload question component
 */

class UploadQuestion extends Component {

    /**
     *  Constructor
     */

    constructor(props) {
        super(props);
        this.state = {

            body: "",

            title: "",
            reference: "",
            course: "",
            university: "",

            // Component states
            threshold: null,
            isLoading: false,
            data: null,
            page: 1,
            error: null
        }
    }

    /**
     *  Handling the change in the form elements and assigning them to states
     *
     *  @param e: input event
     */

    handleChange = (e) => {
        this.setState({[e.target.name]: e.target.value})
    };

    /**
     *  Handle request
     */

    handleRequest = (page = 1) => {

        // Data body for request
        const data = {
            body: this.state.body,
            title: this.state.title,
            source: {
                reference: this.state.reference,
                course: this.state.course,
                university: this.state.university
            }
        };

        questionServices.findSimilarQuestions(data, page, this.state.threshold)
            .then(response => {

                this.setState({
                    isLoading: false,
                    data: response['questions'],
                    page: page
                });

            })
            .catch(err => {
                console.log(err);
            })
    };

    /**
     *  Handling the submit action
     *
     *  @param e: input event
     */

    handleSubmit = (e) => {
        e.preventDefault();

        this.handleRequest()
    };

    render() {
        return (
            <div>
                <NavBar />
                <h1>Upload a question</h1>

                <form onChange={this.handleChange} onSubmit={this.handleSubmit}>

                    {/* Body */}
                    <label htmlFor="body">Question Text</label>
                    <textarea name="body"></textarea>

                    {/* Threshold slider */}
                    <label htmlFor="threshold">Threshold</label>
                    <input type="range" min="40" max="100" name="threshold"/>

                    {/* Check for insert */}

                    {/* Submit */}
                    <button type="submit">Upload</button>

                </form>

                {/* Results */}
                {this.state.data && <QuestionContainer questions={this.state.data} page={this.state.page} handleRequest={this.handleRequest}/>}

            </div>
        );
    }

}

// Exporting the component
export default UploadQuestion

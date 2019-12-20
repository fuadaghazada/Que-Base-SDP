import React, { Component } from 'react';
import { Element, scroller } from 'react-scroll';

import NavBar from "../NavBar";
import QuestionContainer from "./QuestionContainer";

import questionServices from "../../services/question.service";
import Filtering from "./Filtering";


/***
 *  Filter questions component
 */

class FilterQuestions extends Component {

    /**
     *  Constructor
     */

    constructor(props) {
        super(props);
        this.state = {
            // Component states
            filterData: null,
            isLoading: false,
            data: null,
            page: 1,
            error: null
        }
    }

    /**
     *  Handle request
     */

    handleRequest = (page = 1, data) => {

        // To keep the filter data
        let filteringData;
        if (data) {
            this.setState({filterData: data});
            filteringData = data;
        } else {
            filteringData = this.state.filterData;
        }

        // Request
        this.setState({isLoading: true});
        questionServices.getQuestions(filteringData, page)
            .then(response => {

                this.setState({
                    isLoading: false,
                    data: response['questions'],
                    page: page
                });
            })
            .catch(err => {
                console.log(err);
            });

        scroller.scrollTo('questions', {
            duration: 1000,
            delay: 100,
            smooth: true,
            offset: 50,
        })
    };

    render() {
        return (
            <div>
                <NavBar />

                <Filtering handleRequest={this.handleRequest} page={this.state.page}/>

                {/* Results */}
                <Element name={"questions"} className={"questions"}>
                    {this.state.data && <QuestionContainer questions={this.state.data} page={this.state.page} handleRequest={this.handleRequest} styles={{marginTop: "100px"}}/>}
                </Element>
            </div>
        );
    }

}

// Exporting the component
export default FilterQuestions

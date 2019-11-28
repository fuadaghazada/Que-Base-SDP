import React, { Component } from 'react';
import NavBar from "../NavBar";

import questionServices from "../../services/question.service";


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

            body: "",

            source: {
                reference: "",
                university: "",
                course: ""
            },

            viewCount: {
                comparisonOperator: "gte",
                value: -1
            },
            favCount: {
                comparisonOperator: "gte",
                value: -1
            },
            entityTag: {
                logicalOp: "or",
                stringsToMatch: ["religion"]
            },
            topic: {
                logicalOp: "or",
                stringsToMatch: []
            },
            category: {
                logicalOp: "or",
                stringsToMatch: []
            },

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
     *  Handling the submit action
     *
     *  @param e: input event
     */

    handleSubmit = (e) => {
        e.preventDefault();

        // Data body for request
        const data = this.state;
        delete data.error;

        // Request
        questionServices.getQuestions(data)
            .then(response => {

                console.log(response);

            })
            .catch(err => {
                console.log(err);
            })
    };

    render() {
        return (
            <div>
                <NavBar />
                <h1>Filter Questions</h1>

                <form onChange={this.handleChange} onSubmit={this.handleSubmit}>

                    {/* Body */}
                    <label htmlFor="body">Question Text</label>
                    <input type="text" name="body"/>

                    <br/>

                    {/* Reference */}
                    <label htmlFor="source.reference">Reference</label>
                    <input type="text" name="source.reference"/>

                    <br/>

                    {/* University */}
                    <label htmlFor="source.university">University</label>
                    <input type="text" name="source.university"/>

                    <br/>

                    {/* Course */}
                    <label htmlFor="source.course">Course</label>
                    <input type="text" name="source.course"/>

                    <br/>

                    {/* View Count */}
                    <label htmlFor="viewCount">View Count</label>
                    <select name="viewCount.comparisonOperator">
                        <option value="gte">GTE</option>
                        <option value="lte">LTE</option>
                    </select>
                    <input type="number" name="viewCount.value"/>

                    <br/>

                    {/* Fav Count */}
                    <label htmlFor="favCount">Favorite Count</label>
                    <select name="favCount.comparisonOperator">
                        <option value="gte">GTE</option>
                        <option value="lte">LTE</option>
                    </select>
                    <input type="number" name="favCount.value"/>

                    <br/>

                    {/* Entity Tags */}
                    <label htmlFor="source.stringsToMatch">Keywords</label>
                    <input type="text" name="source.stringsToMatch"/>

                    <br/>

                    {/* Topics */}
                    <label htmlFor="source.topic">Topics</label>
                    <input type="text" name="source.topic"/>

                    <br/>

                    {/* Categories */}
                    <label htmlFor="source.category">Categories</label>
                    <input type="text" name="source.category"/>

                    <br/>

                    {/* Submit */}
                    <button type="submit">Filter</button>

                </form>

            </div>
        );
    }

}

// Exporting the component
export default FilterQuestions

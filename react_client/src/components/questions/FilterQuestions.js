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
                stringsToMatch: []
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
     *  Handling change for source
     *
     *  @param e: input event
     */

    handleSource = (e) => {

        const name = e.target.name;
        const value = e.target.value;

        this.setState(prevState => ({
            source: {
                ...prevState.source,
                [name]: value
            }
        }));
    };


    /**
     *  Handling change for comparison operator
     *
     *  @param e: input event
     */

    handleComparisonOp = (e) => {

        const name = e.target.name;
        const value = e.target.value;

        this.setState(prevState => ({
            [name]: {
                ...prevState[name],
                comparisonOperator: value
            }
        }));
    };

    /**
     *  Handling change for Value for count
     *
     *  @param e: input event
     */

    handleValue = (e) => {

        const name = e.target.name;
        const value = e.target.value;

        this.setState(prevState => ({
            [name]: {
                ...prevState[name],
                value: value
            }
        }));
    };

    /**
     *  Handling logical operator for array filters
     *
     *  @param e: input event
     */

     handleLogicalOp = (e) => {

         const name = e.target.name;
         const value = e.target.value;

         this.setState(prevState => ({
             [name]: {
                 ...prevState[name],
                 logicalOp: value
             }
         }));
     };

     /**
      *  Handling array elements
      *
      *  @param e: input event
      */

     handleArrayFields = (e) => {

         const name = e.target.name;
         const value = e.target.value;

         const fields = value.split(',').map(el => el.trim()).filter(el => el !== "");

         this.setState(prevState => ({
             [name]: {
                 ...prevState[name],
                 stringsToMatch: fields
             }
         }));
     }

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
            });
    };

    render() {
        return (
            <div>
                <NavBar />
                <h1>Filter Questions</h1>

                <form onSubmit={this.handleSubmit}>

                    {/* Body */}
                    <label htmlFor="body">Question Text</label>
                    <input type="text" name="body" onChange={this.handleChange}/>

                    <br/>

                    {/* Reference */}
                    <label htmlFor="reference">Reference</label>
                    <input type="text" name="reference" onChange={this.handleSource}/>

                    <br/>

                    {/* University */}
                    <label htmlFor="university">University</label>
                    <input type="text" name="university" onChange={this.handleSource}/>

                    <br/>

                    {/* Course */}
                    <label htmlFor="course">Course</label>
                    <input type="text" name="course" onChange={this.handleSource}/>

                    <br/>

                    {/* View Count */}
                    <label htmlFor="viewCount">View Count</label>
                    <select name="viewCount" onChange={this.handleComparisonOp}>
                        <option value="gte">GTE</option>
                        <option value="lte">LTE</option>
                    </select>
                    <input type="number" name="viewCount" onChange={this.handleValue}/>

                    <br/>

                    {/* Fav Count */}
                    <label htmlFor="favCount">Favorite Count</label>
                    <select name="favCount" onChange={this.handleComparisonOp}>
                        <option value="gte">GTE</option>
                        <option value="lte">LTE</option>
                    </select>
                    <input type="number" name="favCount" onChange={this.handleValue}/>

                    <br/>

                    {/* Entity Tags */}
                    <label htmlFor="entityTag">Keywords</label>
                    <select name="entityTag" onChange={this.handleLogicalOp}>
                        <option value="or">Or</option>
                        <option value="and">And</option>
                    </select>
                    <input type="text" name="entityTag" onChange={this.handleArrayFields}/>

                    <br/>

                    {/* Topics */}
                    <label htmlFor="source.topic">Topics</label>
                    <select name="topic" onChange={this.handleLogicalOp}>
                        <option value="or">Or</option>
                        <option value="and">And</option>
                    </select>
                    <input type="text" name="topic" onChange={this.handleArrayFields}/>

                    <br/>

                    {/* Categories */}
                    <label htmlFor="category">Categories</label>
                    <select name="category" onChange={this.handleLogicalOp}>
                        <option value="or">Or</option>
                        <option value="and">And</option>
                    </select>
                    <input type="text" name="category" onChange={this.handleArrayFields}/>

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

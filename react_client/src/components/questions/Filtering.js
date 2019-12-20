import React, {Component} from "react";
import {Button, Container, Grid, MenuItem, Select, TextField, Typography} from "@material-ui/core";


/***
 *  Filtering for questions
 */

class Filtering extends Component {

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
            sort: {
                attr: "_id",
                order: 1
            },
            label: ""
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
        const value = parseInt(e.target.value);

        this.setState(prevState => ({
            [name]: {
                ...prevState[name],
                value: isNaN(value) ? -1 : value
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
    };

    /**
     *  Handling the submit action
     *
     *  @param e: input event
     */

    handleSubmit = (e) => {
        e.preventDefault();

        const data = this.state;
        const { handleRequest, page } = this.props;

        if (handleRequest) {
            handleRequest(page, data);
        }
    };

    render() {
        return (

            <Container maxWidth={"md"}>
                {/* Header */}
                <Typography variant={"h2"}>Filter Questions</Typography>

                {/* Filter Form */}
                <form onSubmit={this.handleSubmit}>

                    <Grid container spacing={5}>

                        {/* Body */}
                        <Grid item md={12}>
                            <TextField label="Question body" placeholder="Text" name="body" onChange={this.handleChange} fullWidth={true}/>
                        </Grid>

                        {/* Reference */}
                        <Grid item md={4}>
                            <TextField label="Reference" placeholder="Reference" name="reference" onChange={this.handleSource} fullWidth={true}/>
                        </Grid>

                        {/* University */}
                        <Grid item md={4}>
                            <TextField label="University" placeholder="University" name="university" onChange={this.handleSource} fullWidth={true}/>
                        </Grid>

                        {/* Course */}
                        <Grid item md={4}>
                            <TextField label="Course" placeholder="Course" name="course" onChange={this.handleSource} fullWidth={true}/>
                        </Grid>

                        {/* View Count */}
                        <Grid item md={6}>
                            <TextField type="number" label="View Count" placeholder="View Count" name="viewCount" onChange={this.handleValue} fullWidth={true}/>
                            <Select
                                value={this.state.viewCount.comparisonOperator}
                                name={"viewCount"}
                                onChange={this.handleComparisonOp}
                            >
                                <MenuItem value="gte">GTE</MenuItem>
                                <MenuItem value="lte">LTE</MenuItem>
                            </Select>
                        </Grid>

                        {/* Fav Count */}
                        <Grid item md={6}>
                            <TextField type="number" label="Favorite Count" placeholder="Favorite Count" name="favCount" onChange={this.handleValue} fullWidth={true}/>
                            <Select
                                value={this.state.favCount.comparisonOperator}
                                name={"favCount"}
                                onChange={this.handleComparisonOp}
                            >
                                <MenuItem value="gte">GTE</MenuItem>
                                <MenuItem value="lte">LTE</MenuItem>
                            </Select>
                        </Grid>

                        {/* Entity Tags */}
                        <Grid item md={4}>
                            <TextField label="Keywords" placeholder="Keywords" name="entityTag" onChange={this.handleArrayFields} fullWidth={true}/>
                            <Select
                                value={this.state.entityTag.logicalOp}
                                name={"entityTag"}
                                onChange={this.handleLogicalOp}
                            >
                                <MenuItem value="or">Or</MenuItem>
                                <MenuItem value="and">And</MenuItem>
                            </Select>
                        </Grid>

                        {/* Topics */}
                        <Grid item md={4}>
                            <TextField label="Topics" placeholder="Topics" name="topic" onChange={this.handleArrayFields} fullWidth={true}/>
                            <Select
                                value={this.state.topic.logicalOp}
                                name={"topic"}
                                onChange={this.handleLogicalOp}
                            >
                                <MenuItem value="or">Or</MenuItem>
                                <MenuItem value="and">And</MenuItem>
                            </Select>
                        </Grid>

                        {/* Categories */}
                        <Grid item md={4}>
                            <TextField label="Categories" placeholder="Categories" name="category" onChange={this.handleArrayFields} fullWidth={true}/>
                            <Select
                                value={this.state.category.logicalOp}
                                name={"category"}
                                onChange={this.handleLogicalOp}
                            >
                                <MenuItem value="or">Or</MenuItem>
                                <MenuItem value="and">And</MenuItem>
                            </Select>
                        </Grid>

                        <Grid item md={12}>
                            <TextField label="Label" placeholder="Label (programming)" name="label" onChange={this.handleChange} fullWidth={true}/>
                        </Grid>

                        {/* Submit */}
                        <Grid item md={12}>
                            <Button variant="contained" type="submit" fullWidth={true} color={"primary"}>Filter</Button>
                        </Grid>

                    </Grid>
                </form>
                {/* End of filter form */}

            </Container>

        );
    }
}

// Exporting the component
export default Filtering;

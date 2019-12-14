import React, { Component } from 'react';
import { Container, TextField, Grid, Typography, Slider, Input, Button, FormControlLabel, Checkbox } from '@material-ui/core';

import questionServices from "../../services/question.service";

import NavBar from "../NavBar";
import QuestionContainer from "./QuestionContainer";
import InsertQuestion from "./InsertQuestion";



/***
 *  Upload question component
 */

class FindQuestion extends Component {

    /**
     *  Constructor
     */

    constructor(props) {
        super(props);
        this.state = {
            body: "",

            threshold: 60,
            save: false,

            // Component states
            isLoading: false,
            data: null,
            page: 1,
            error: null
        };

        this.insertContainer = React.createRef();
    }

    handleCheckbox = name => event => {
        this.setState({[name]: event.target.checked})
    };

    handleSliderChange = (event, threshold) => {
        this.setState({threshold})
    };

    handleInputChange = event => {
        this.setState({threshold: (event.target.value === '' ? '' : Number(event.target.value))});
    };

    handleBlur = () => {
        if (this.state.threshold < 0) {
            this.setState({threshold: 0});
        } else if (this.state.threshold > 100) {
            this.setState({threshold: 100});
        }
    };

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
            body: this.state.body
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

        // Save process..
        if (this.state.save) {
            this.insertContainer.current.handleInsert(this.state.body);
        }


        this.handleRequest()
    };

    render() {
        return (
            <div>
                <NavBar />

                <Container maxWidth={"md"}>

                    {/* Header */}
                    <Typography variant="h2" gutterBottom>Upload a Question</Typography>

                    <form onChange={this.handleChange} onSubmit={this.handleSubmit}>

                        {/* Body */}
                        <TextField
                            id="outlined-multiline-static"
                            label="Question Text"
                            multiline
                            rows="4"
                            placeholder="Paste your question here"
                            variant="outlined"
                            name="body"
                            fullWidth={true}
                        />

                        <Typography variant="overline" display="block" gutterBottom>
                            Pick Similarity Rate:
                        </Typography>

                        <Grid container spacing={2} alignItems="center" maxwidth="md">

                            {/* Threshold slider */}
                            <Grid item md={7}>
                                <Slider
                                    name="threshold"
                                    value={typeof this.state.threshold === 'number' ? this.state.threshold : 0}
                                    onChange={this.handleSliderChange}
                                    aria-labelledby="input-slider"
                                    min={40}
                                />
                            </Grid>
                            {/* Threshold Number Input */}
                            <Grid item md={2}>
                                <Input
                                    value={this.state.threshold}
                                    name={"threshold"}
                                    margin="dense"
                                    onChange={this.handleInputChange}
                                    onBlur={this.handleBlur}
                                    fullWidth={true}
                                    inputProps={{
                                        step: 1,
                                        min: 40,
                                        max: 100,
                                        value: this.state.threshold,
                                        type: 'number',
                                        'aria-labelledby': 'input-slider',
                                    }}
                                />
                            </Grid>
                            {/* Check for insert */}
                            <Grid item md={3}>
                                <FormControlLabel
                                    control={
                                        <Checkbox
                                            checked={this.state.save}
                                            onChange={this.handleCheckbox('save')}
                                            color="primary"
                                        />
                                    }
                                    label="Save question?"
                                />
                            </Grid>
                        </Grid>

                        {/* Insert container */}
                        {this.state.save && <InsertQuestion bodyExists={true} ref={this.insertContainer}/>}

                        {/* Submit */}
                        <Button type="submit" variant="contained" color="primary" fullWidth={true}>Find</Button>

                    </form>

                    {/* Results */}
                    {this.state.data && <QuestionContainer questions={this.state.data} page={this.state.page} handleRequest={this.handleRequest}/>}
                </Container>

            </div>
        );
    }

}

// Exporting the component
export default FindQuestion

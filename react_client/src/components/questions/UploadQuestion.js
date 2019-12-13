import React, { Component } from 'react';
import NavBar from "../NavBar";
import questionServices from "../../services/question.service";
import QuestionContainer from "./QuestionContainer";
import { makeStyles } from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import Slider from '@material-ui/core/Slider';
import Input from '@material-ui/core/Input';
import Button from '@material-ui/core/Button';

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
            newValue: 0,
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
            error: null,
            classes: null
        }
    }
    componentDidMount() {
   
        this.setState({classes: makeStyles({   // DOESN'T WORK FOR SOME REASON...
            root: {
              width: 250,
            },
            input: {
              width: 42,
            },
          })})

    }

    handleSliderChange = (event, newValue) => {
    this.setState({newValue: newValue})
    };

    handleInputChange = event => {
        this.setState({newValue: (event.target.value === '' ? '' : Number(event.target.value))});
    };

    handleBlur = () => {
        if (this.state.newValue < 0) {
          this.setState({newValue: 0});
        } else if (this.state.newValue > 100) {
          this.setState({newValue: 100});

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
            body: this.state.body,
            title: this.state.title,
            source: {
                reference: this.state.reference,
                course: this.state.course,
                university: this.state.university
            },
            filter: {
                "body": "",
                "source": {
                    "reference": "",
                    "university": "",
                    "course": ""
                },
                "viewCount": {
                    "comparisonOperator": "gte",
                    "value": -1
                },
                "favCount": {
                    "comparisonOperator": "gte",
                    "value": -1
                },
                "entityTag": {
                    "logicalOp": "or",
                    "stringsToMatch": []
                },
                "topic": {
                    "logicalOp": "and",
                    "stringsToMatch": []
                },
                "category": {
                    "logicalOp": "and",
                    "stringsToMatch": []
                },
                "sort": {
                    "attr": "_id",
                    "order": 1
                }
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
                <Typography variant="h4" gutterBottom>
                    Upload a Question:
                </Typography>
                
                <form onChange={this.handleChange} onSubmit={this.handleSubmit}>

                    {/* Body */}
                    <TextField
                        id="outlined-multiline-static"
                        label="Question Text"
                        multiline
                        rows="4"
                        placeholder="Enter your question here"
                        variant="outlined"
                        name="body"
                    />
                    <Typography variant="overline" display="block" gutterBottom>
                        Pick Similarity Rate:
                    </Typography>
                    <Grid container spacing={2} alignItems="center" maxWidth="sm">
                    
                        {/* Threshold slider */}
                        <Grid item sm={3}>
                            <Slider
                                name="threshold"
                                value={typeof this.state.newValue === 'number' ? this.state.newValue : 0}
                                onChange={this.handleSliderChange}
                                aria-labelledby="input-slider"
                            />
                        </Grid>
                        <Grid item>
                            <Input
                                    value={this.state.newValue}
                                    margin="dense"
                                    onChange={this.handleInputChange}
                                    onBlur={this.handleBlur}
                                    inputProps={{
                                    step: 1,
                                    min: 0,
                                    max: 100,
                                    type: 'number',
                                    'aria-labelledby': 'input-slider',
                                        }}
                            />
                        </Grid>
                    </Grid>

                    {/* Check for insert */}

                    {/* Submit */}
                    <Button type="submit" variant="contained" color="primary">
                        Upload
                    </Button>

                </form>

                {/* Results */}
                {this.state.data && <QuestionContainer questions={this.state.data} page={this.state.page} handleRequest={this.handleRequest}/>}

            </div>
        );
    }

}

// Exporting the component
export default UploadQuestion

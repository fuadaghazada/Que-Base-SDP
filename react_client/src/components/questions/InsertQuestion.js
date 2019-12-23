import React, {Component} from "react";
import {Grid, TextField} from "@material-ui/core";

import questionServices from "../../services/question.service";

/***
 *  Insert a question
 */

class InsertQuestion extends Component {

    /**
     *  Constructor
     */

    constructor(props) {
        super(props);
        this.state = {
            body: null,
            title: null,

            source: {
                reference: "",
                university: "",
                course: ""
            },
        }
    }

    /**
     *  Handling the change in the form elements and assigning them to states
     *
     *  @param e: input event
     */

    handleChange = (e) => {

        if (e.target.value !== '') {
            this.setState({[e.target.name]: e.target.value})
        } else {
            if (e.target.name === "level") {
                delete this.state[e.target.name];
                this.setState(this.state);
            } else {
                this.setState({[e.target.name]: undefined})
            }
        }
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
     *  Handling change for labels
     *
     *  @param e: input event
     */

    handleArrayFields = (e) => {
        const name = e.target.name;
        const value = e.target.value;

        if (name === "labels" && value === "") {
            delete this.state[e.target.name];
            this.setState(this.state);

        } else {
            const fields = value.split(',').map(el => el.trim()).filter(el => el !== "");

            this.setState(prevState => ({
                [name]: {
                    ...prevState[name],
                    stringsToMatch: fields
                }
            }));
        }
    };

    /**
     *  Handling the submit action
     *
     *  @param questionBody: input event
     */

    handleInsert = (questionBody) => {

        // Data to be inserted
        const data = this.state;
        data['body'] = questionBody;

        questionServices.postInsertQuestion(data)
            .then(response => {
                if (response)
                    console.log(response['message']);
            })
            .catch(err => {
                console.log(err);
            })
    };

    render() {

        let { type } = this.props;
        type = (type) ? type : "soc";

        return (

            <Grid container spacing={5}>

                {/* Body */}
                {!this.props['bodyExists'] &&
                <Grid item md={12}>
                    <TextField label="Question body" placeholder="Text" name="body" onChange={this.handleChange} fullWidth={true}/>
                </Grid>
                }

                <Grid item md={12}>
                    <TextField label="Title" placeholder="Text" name="title" onChange={this.handleChange} fullWidth={true} required={true}/>
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

                {/* Labels */}
                {type !== "soc" &&
                <Grid item md={6}>
                    <TextField label="Labels" placeholder="Labels" name="labels" onChange={this.handleArrayFields} fullWidth={true} required={true}/>
                </Grid>
                }

                {/* Level */}
                {type !== "soc" &&
                <Grid item md={6}>
                    <TextField label="Level" placeholder="Level" name="level" onChange={this.handleChange} fullWidth={true}/>
                </Grid>

                }
            </Grid>

        );
    }
}

// Exporting the component
export default InsertQuestion;

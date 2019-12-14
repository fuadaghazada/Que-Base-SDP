import React, { Component } from 'react';
import { Redirect } from 'react-router-dom';

import authServices from '../../services/auth.service';

import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';
import Link from '@material-ui/core/Link';
import Grid from '@material-ui/core/Grid';
import LockOutlinedIcon from '@material-ui/icons/LockOutlined';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';

/***
 *  Registration component
 */


class Registration extends Component {

    /**
     *  Registration constructor
     */

    constructor (props) {
        super(props);
        this.state = {
            firstName: '',
            lastName: '',
            username: '',
            email: '',
            password: '',
            confirmPassword: '',

            redirect: authServices.getUser() && true,
            error: null,
            useStyles: makeStyles(theme => ({
                paper: {
                  marginTop: theme.spacing(8),
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                },
                avatar: {
                  margin: theme.spacing(1),
                  backgroundColor: theme.palette.secondary.main,
                },
                form: {
                  width: '100%', // Fix IE 11 issue.
                  marginTop: theme.spacing(3),
                },
                submit: {
                  margin: theme.spacing(3, 0, 2),
                },
              }))
        }
    }


    /**
     *  Handling the change in the form elements and assigning them to states
     *
     *  @param e: input event
     */

    handleChange = (e) => {
        if (e.target.type === 'file') {
            this.setState({[e.target.name]: e.target.files[0]});
        } else {
            this.setState({[e.target.name]: e.target.value})
        }
    };


    /**
     *  Handling the submit action
     *
     *  @param e: input event
     */

    handleSubmit = (e) => {
        e.preventDefault();

        // Adding keys and values to form data
        const data = {
            firstname: this.state.firstName,
            lastname: this.state.lastName,
            username: this.state.username,
            email: this.state.email,
            password: this.state.password,
            confirmPassword: this.state.confirmPassword,
        };

        // Sending POST Request
        authServices.signUp(data)
            .then(response => {
                if (response && response.success) {
                    this.setState({ redirect: true });
                } else {
                    this.setState({ error: response.message });
                }
            })
            .catch(err => {
                console.log(err);
            });
    };


    render() {
        if (this.state.redirect) {
            return <Redirect to={'/'}/>
        }
        return (
            <Container component="main" maxWidth="xs">
                <CssBaseline />
                <form onChange={this.handleChange} onSubmit={this.handleSubmit} method="post">
                    <div className={this.state.useStyles.paper}>
                        <Avatar className={this.state.useStyles.avatar}>
                        <LockOutlinedIcon />
                        </Avatar>
                        <Typography component="h1" variant="h5">
                        Sign up
                        </Typography>
                        <form className={this.state.useStyles.form} noValidate>
                        <Grid container spacing={2}>
                            <Grid item xs={12} sm={6}>
                            <TextField
                                autoComplete="fname"
                                name="firstName"
                                variant="outlined"
                                required
                                fullWidth
                                id="firstName"
                                label="First Name"
                                autoFocus
                            />
                            </Grid>
                            <Grid item xs={12} sm={6}>
                            <TextField
                                variant="outlined"
                                required
                                fullWidth
                                id="lastName"
                                label="Last Name"
                                name="lastName"
                                autoComplete="lname"
                            />
                            </Grid>
                            <Grid item xs={12}>
                            <TextField
                                variant="outlined"
                                required
                                fullWidth
                                id="email"
                                label="Email Address"
                                name="email"
                                autoComplete="email"
                            />
                            </Grid>
                            <Grid item xs={12}>
                            <TextField
                                variant="outlined"
                                required
                                fullWidth
                                id="username"
                                label="User Name"
                                name="username"
                                autoComplete="username"
                            />
                            </Grid>
                            <Grid item xs={12}>
                            <TextField
                                variant="outlined"
                                required
                                fullWidth
                                name="password"
                                label="Password"
                                type="password"
                                id="password"
                                autoComplete="current-password"
                            />
                            </Grid>
                            <Grid item xs={12}>
                            <TextField
                                variant="outlined"
                                required
                                fullWidth
                                name="confirmPassword"
                                label="Confirm Password"
                                type="password"
                                id="confirmPassword"
                                autoComplete="current-password"
                            />
                            </Grid>
                        </Grid>
                        <Button
                            type="submit"
                            fullWidth
                            variant="contained"
                            color="primary"
                            className={this.state.useStyles.submit}
                        >
                            Sign Up
                        </Button>
                        <Grid container justify="flex-end">
                            <Grid item>
                            <Link href="/login/" variant="body2">
                                Already have an account? Sign in
                            </Link>
                            </Grid>
                        </Grid>
                        </form>
                    </div>
                    {/* Error */}
                    {(this.state.error) && alert(this.state.error)}
                </form>

            </Container>

        )
    }
}

// Exporting the component
export default Registration;

import React from 'react';
import { Typography, Paper, Grid, Fab, Box } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import FavoriteIcon from '@material-ui/icons/Favorite';

const useStyles = makeStyles(theme => ({
      questionBody: {
        padding: theme.spacing(3, 3)
      },
      button: {
        margin: theme.spacing(1)
      },
      stat: {
        fontStyle: 'italic'
      },
      sourceField: {
        fontStyle: 'bold'
      }
    }));

const QuestionDisplay = (props) => {

    const classes = useStyles();
    const { title, body, viewCount, favCount, source } = props.questionData;

    return (
        <div>
            <Typography variant={"h4"}>{title}</Typography>

            <Paper className={classes.questionBody}>
                <Typography variant={"body1"}>{body}</Typography>
            </Paper>

            <Grid
              container
              direction="row"
              justify="space-between"
            >
                <Box>
                    <Typography className={classes.stat} variant={"subtitle1"}>View count: {viewCount}</Typography>
                    <Typography className={classes.stat} variant={"subtitle1"}>Favorite count: {favCount}</Typography>
                </Box>
                <Box>
                    <Typography variant={"subtitle1"}>Course: {source.course}</Typography>
                    <Typography variant={"subtitle1"}>University: {source.university}</Typography>
                    <Typography variant={"subtitle1"}>Reference: {source.reference}</Typography>
                </Box>
                <Fab className={classes.button} color="secondary" aria-label="favorite">
                    <FavoriteIcon />
                </Fab>
            </Grid>

        </div>
    )
};

// Exporting the component
export default QuestionDisplay;

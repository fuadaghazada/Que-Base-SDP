import React from 'react';
import { Container, Typography, Paper, Grid, Fab, Box } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import FavoriteIcon from '@material-ui/icons/Favorite';
import FavoriteBorderIcon from '@material-ui/icons/FavoriteBorder';
import VideoContainer from "../VideoContainer";

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
    const { title, body, viewCount, favCount, source, labels, youtubeVideos } = props.questionData;
    const { isFavorite, favoriteQuestion } = props;

    let course = "---";
    let university = "---";
    let reference = "---";

    try {
        course = source.course;
        university = source.university;
        reference = source.reference;
    } catch (err) {console.log("No property")}

    return (
        <Container maxWidth={"md"}>
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
                    {labels && <Typography component={"p"}> Labels: {labels} %</Typography>}
                </Box>
                <Box>
                    <Typography variant={"subtitle1"}>Course: {course}</Typography>
                    <Typography variant={"subtitle1"}>University: {university}</Typography>
                    <Typography variant={"subtitle1"}>Reference: {reference}</Typography>
                </Box>
                <Fab className={classes.button} color="secondary" aria-label="favorite" onClick={favoriteQuestion}>
                    {!isFavorite ? <FavoriteIcon /> : <FavoriteBorderIcon />}
                </Fab>
            </Grid>

            {/*  Video  */}
            <VideoContainer videoData={youtubeVideos}/>

        </Container>
    )
};

// Exporting the component
export default QuestionDisplay;

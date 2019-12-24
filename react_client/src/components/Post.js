import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import {
    Typography,
    Card,
    CardActionArea,
    CardContent,
    Link,
    Grid
} from '@material-ui/core';

import color from '../utils/color';
import Avatar from "@material-ui/core/Avatar";

const dateFormat = require('dateformat');

/**
    User Preview (functional component)
*/

const Post = (props) => {

    const {message, questionId, timestamp, userId, questionTitle} = props['data'];
    const date = dateFormat(new Date(timestamp), "mmm d HH:MM")
    const username = message.split(" ")[0];
    const remainingMessage = message.replace(username, " ");

    const useStyles = makeStyles({
        card: {
            width: '100%',
            padding: "20px",
            marginBottom: "5px"
        },
        color: {
            color: '#fff',
            backgroundColor: color.generateColor(message)[500],
          },
        font: {
            fontSize: 22,
            textDecoration: null
        }
    });
    const classes = useStyles();

    return (
        <Card className = {classes.card}>
            <CardActionArea>
                <CardContent>
                    <Grid container direction="row" alignItems='center'>
                        <Grid container item md={2} >
                            <Avatar className={classes.color}>{username[0].toUpperCase()}</Avatar>
                        </Grid>
                        <Grid container item md={10} spacing={2} >
                            <Typography className={classes.font}><Link href={`/userDetails/${userId}`}>{username}</Link>{remainingMessage}</Typography>
                        </Grid>
                    </Grid>
                </CardContent>
                <CardContent>
                    <Grid container direction="row">
                        <Grid container item md={8} >
                            <Typography component={"h2"}>{questionTitle}</Typography>
                        </Grid>
                        <Grid container item md={2}>
                            {/*{labels && <Typography component={"p"}><strong>Labels:</strong> {labels.toString()}</Typography>}*/}
                        </Grid>
                        <Grid container item md={2} justify={"flex-end"}>
                            <Typography component={"p"}>{date}</Typography>
                        </Grid>
                        <Link href={`/questionDetails/${questionId}`}>View Question</Link>
                    </Grid>
                </CardContent>
            </CardActionArea>
        </Card>


    );
};

// Exporting the component
export default Post;

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
import Avatar from '@material-ui/core/Avatar';

import color from '../utils/color';


/**
    User Preview (functional component)
*/

const Post = (props) => {

    // console.log(props['data'])
    const {username, _id, title, viewCount, labels} = props['data'];
    const useStyles = makeStyles({
        card: {
            width: '100%',
        },
        color: {
            color: '#fff',
            backgroundColor: color.generateColor(username)[500],
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
                        <Grid container item md={1} >
                            <Avatar className={classes.color}>{username[0].toUpperCase()}</Avatar>
                        </Grid>
                        <Grid container item md={11} spacing={2} >
                            <Typography className={classes.font}><Link href={`/userDetails/${_id}`}>{username + " "}</Link>{" favorited a question"}</Typography>
                        </Grid>
                    </Grid>
                </CardContent>
                <CardContent>
                    <Grid container direction="row">
                        <Grid container item md={8} >
                            <Typography component={"h2"}>{title}</Typography>
                        </Grid>
                        <Grid container item md={2}>
                            {labels && <Typography component={"p"}><strong>Labels:</strong> {labels.toString()}</Typography>}
                        </Grid>
                        <Grid container item md={2} justify={"flex-end"}>
                            <Typography component={"p"}>Views: {viewCount}</Typography>
                        </Grid>
                        <Link href={`/questionDetails/${_id}`}>View Question</Link>
                    </Grid>
                </CardContent>
            </CardActionArea>
        </Card>


    );
};

// Exporting the component
export default Post;

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

import color from '../../utils/color';

/**
    User Preview (functional component)
*/

const UserPreview = (props) => {

    // console.log(props['data'])
    const {username, _id} = props['data'];
    const useStyles = makeStyles({
        card: {
            width: '100%',
            marginBottom: "5px"
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
                        <Grid container item md={2} >
                            <Avatar className={classes.color}>{username[0].toUpperCase()}</Avatar>
                        </Grid>
                        <Grid container item md={10} >
                            <Link href={`/userDetails/${_id}`}><Typography className={classes.font}>{username}</Typography></Link>
                        </Grid>
                    </Grid>
                </CardContent>
            </CardActionArea>
        </Card>


    );
};

// Exporting the component
export default UserPreview;
